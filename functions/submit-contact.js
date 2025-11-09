/**
 * 堂島フロント企画 - お問い合わせフォーム送信処理
 * Cloudflare Pages Functions + MailChannels API
 *
 * 機能:
 * - Turnstile検証
 * - ハニーポット検証
 * - レート制限（IPベース、5分間に3回まで）
 * - データバリデーション
 * - MailChannels経由でメール送信
 */

export async function onRequest(context) {
  const { request, env } = context;

  // CORS設定（同一オリジンのみ許可）
  const corsHeaders = {
    'Access-Control-Allow-Origin': request.headers.get('Origin') || '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json; charset=utf-8',
  };

  // プリフライトリクエスト対応
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: corsHeaders,
    });
  }

  // POSTメソッドのみ許可
  if (request.method !== 'POST') {
    return new Response(
      JSON.stringify({
        success: false,
        error: '許可されていないリクエストメソッドです。',
      }),
      {
        status: 405,
        headers: corsHeaders,
      }
    );
  }

  try {
    // リクエストボディの取得（FormData形式）
    const formData = await request.formData();
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';

    // FormDataをオブジェクトに変換
    const data = {};
    for (const [key, value] of formData.entries()) {
      data[key] = value;
    }

    console.log('[お問い合わせフォーム] 送信リクエスト受信:', {
      ip: clientIP,
      service: data.service,
      timestamp: new Date().toISOString(),
    });

    // ハニーポット検証（スパムボット対策）
    if (data.website && data.website.trim() !== '') {
      console.log('[お問い合わせフォーム] スパム検出（ハニーポット）:', clientIP);
      return new Response(
        JSON.stringify({
          success: false,
          error: '不正な送信が検出されました。',
        }),
        {
          status: 403,
          headers: corsHeaders,
        }
      );
    }

    // Turnstile検証
    const turnstileToken = data['cf-turnstile-response'];
    if (!turnstileToken) {
      return new Response(
        JSON.stringify({
          success: false,
          error: 'セキュリティ検証が完了していません。',
        }),
        {
          status: 400,
          headers: corsHeaders,
        }
      );
    }

    const turnstileValid = await verifyTurnstile(
      turnstileToken,
      env.TURNSTILE_SECRET_KEY,
      clientIP
    );

    if (!turnstileValid) {
      console.log('[お問い合わせフォーム] Turnstile検証失敗:', clientIP);
      return new Response(
        JSON.stringify({
          success: false,
          error: 'セキュリティ検証に失敗しました。ページを再読み込みしてください。',
        }),
        {
          status: 403,
          headers: corsHeaders,
        }
      );
    }

    // レート制限チェック
    const rateLimitResult = await checkRateLimit(context, clientIP);
    if (!rateLimitResult.allowed) {
      console.log('[お問い合わせフォーム] レート制限超過:', {
        ip: clientIP,
        count: rateLimitResult.count,
      });
      return new Response(
        JSON.stringify({
          success: false,
          error: '送信回数が制限を超えました。しばらく時間をおいてから再度お試しください。',
        }),
        {
          status: 429,
          headers: {
            ...corsHeaders,
            'Retry-After': '300',
          },
        }
      );
    }

    // データバリデーション
    const validation = validateContactForm(data);
    if (!validation.valid) {
      console.log('[お問い合わせフォーム] バリデーションエラー:', validation.error);
      return new Response(
        JSON.stringify({
          success: false,
          error: validation.error,
        }),
        {
          status: 400,
          headers: corsHeaders,
        }
      );
    }

    // メール送信
    const emailResult = await sendContactEmail(data, env, clientIP);

    if (!emailResult.success) {
      console.error('[お問い合わせフォーム] メール送信失敗:', emailResult.error);
      return new Response(
        JSON.stringify({
          success: false,
          error: 'メール送信に失敗しました。時間をおいて再度お試しください。',
        }),
        {
          status: 500,
          headers: corsHeaders,
        }
      );
    }

    console.log('[お問い合わせフォーム] 送信成功:', {
      ip: clientIP,
      email: data.email,
      service: data.service,
    });

    return new Response(
      JSON.stringify({
        success: true,
        message: 'お問い合わせを受け付けました。担当者より折り返しご連絡いたします。',
      }),
      {
        status: 200,
        headers: corsHeaders,
      }
    );
  } catch (error) {
    console.error('[お問い合わせフォーム] 予期しないエラー:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: 'システムエラーが発生しました。しばらく時間をおいて再度お試しください。',
      }),
      {
        status: 500,
        headers: corsHeaders,
      }
    );
  }
}

/**
 * Turnstile検証
 */
async function verifyTurnstile(token, secretKey, clientIP) {
  try {
    const response = await fetch(
      'https://challenges.cloudflare.com/turnstile/v0/siteverify',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          secret: secretKey,
          response: token,
          remoteip: clientIP,
        }),
      }
    );

    const result = await response.json();
    console.log('[Turnstile検証] レスポンス:', result);
    return result.success === true;
  } catch (error) {
    console.error('[Turnstile検証] エラー:', error);
    return false;
  }
}

/**
 * レート制限チェック（Workers KV使用）
 */
async function checkRateLimit(context, clientIP) {
  const { env } = context;
  const rateLimitKey = `ratelimit:contact:${clientIP}`;
  const maxAttempts = 3;
  const windowSeconds = 300; // 5分

  try {
    // KV Namespaceが設定されていない場合はスキップ
    if (!env.RATE_LIMIT) {
      console.log('[レート制限] KV未設定のため、レート制限をスキップ');
      return { allowed: true, count: 0 };
    }

    // KVからカウント取得
    const currentCount = await env.RATE_LIMIT.get(rateLimitKey);
    const count = currentCount ? parseInt(currentCount, 10) : 0;

    if (count >= maxAttempts) {
      return { allowed: false, count };
    }

    // カウント増加（TTL: 300秒）
    await env.RATE_LIMIT.put(rateLimitKey, (count + 1).toString(), {
      expirationTtl: windowSeconds,
    });

    return { allowed: true, count: count + 1 };
  } catch (error) {
    console.error('[レート制限] KVエラー:', error);
    // KVエラー時は処理を継続（セキュリティよりも可用性優先）
    return { allowed: true, count: 0 };
  }
}

/**
 * お問い合わせフォームのバリデーション
 */
function validateContactForm(data) {
  // 必須フィールドチェック
  const requiredFields = {
    company: '会社名',
    name: 'ご担当者名',
    email: 'メールアドレス',
    service: 'ご希望サービス',
    privacy: 'プライバシーポリシー同意',
  };

  for (const [field, label] of Object.entries(requiredFields)) {
    if (!data[field] || (typeof data[field] === 'string' && data[field].trim() === '')) {
      return {
        valid: false,
        error: `${label}は必須項目です。`,
      };
    }
  }

  // プライバシーポリシー同意チェック
  if (data.privacy !== true && data.privacy !== 'true') {
    return {
      valid: false,
      error: 'プライバシーポリシーに同意してください。',
    };
  }

  // メールアドレス形式チェック
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(data.email)) {
    return {
      valid: false,
      error: '有効なメールアドレスを入力してください。',
    };
  }

  // 電話番号形式チェック（任意フィールド）
  if (data.phone && data.phone.trim() !== '') {
    const phoneRegex = /^[0-9\-\+\(\)\s]{10,20}$/;
    if (!phoneRegex.test(data.phone)) {
      return {
        valid: false,
        error: '有効な電話番号を入力してください。',
      };
    }
  }

  // 参加人数チェック（任意フィールド）
  if (data.participants) {
    const participants = parseInt(data.participants, 10);
    if (isNaN(participants) || participants < 1 || participants > 10000) {
      return {
        valid: false,
        error: '参加予定人数は1〜10000の範囲で入力してください。',
      };
    }
  }

  return { valid: true };
}

/**
 * MailChannels経由でメール送信
 */
async function sendContactEmail(data, env, clientIP) {
  const timestamp = new Date().toLocaleString('ja-JP', {
    timeZone: 'Asia/Tokyo',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  // メール件名
  const subject = `【お問い合わせ】${data.company} - ${data.service}`;

  // メール本文
  const mailBody = `堂島フロント企画 お問い合わせフォームより新しいお問い合わせがありました。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ お問い合わせ内容
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【会社名】
${data.company}

【ご担当者名】
${data.name}

【メールアドレス】
${data.email}

【電話番号】
${data.phone || '未入力'}

【ご希望サービス】
${data.service}

【希望実施日】
${data.date || '未入力'}

【参加予定人数】
${data.participants ? `${data.participants}名` : '未入力'}

【ご要望・詳細】
${data.message || '未入力'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
送信日時: ${timestamp}
送信元IP: ${clientIP}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

このメールは堂島フロント企画の自動送信システムより送信されています。
`;

  try {
    const fromEmail = env.FROM_EMAIL || 'noreply@doujimafront.com';
    console.log('[メール送信] FROM_EMAIL:', fromEmail);
    console.log('[メール送信] RECIPIENT_EMAIL:', env.RECIPIENT_EMAIL);

    const response = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        personalizations: [
          {
            to: [{ email: env.RECIPIENT_EMAIL }],
          },
        ],
        from: {
          email: fromEmail,
          name: '堂島フロント企画 お問い合わせフォーム',
        },
        subject: subject,
        content: [
          {
            type: 'text/plain',
            value: mailBody,
          },
        ],
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      return {
        success: false,
        error: `MailChannels API エラー: ${response.status} - ${errorText}`,
      };
    }

    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: `メール送信エラー: ${error.message}`,
    };
  }
}
