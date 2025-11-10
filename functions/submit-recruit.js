/**
 * 堂島フロント企画 - 採用応募フォーム送信処理
 * Cloudflare Pages Functions + Resend API
 *
 * 機能:
 * - Turnstile検証
 * - ハニーポット検証
 * - レート制限(IPベース、5分間に3回まで)
 * - データバリデーション
 * - Resend経由でメール送信
 */

export async function onRequest(context) {
  const { request, env } = context;

  // CORS設定(同一オリジンのみ許可)
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
    // リクエストボディの取得(FormData形式)
    const formData = await request.formData();
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';

    // FormDataをオブジェクトに変換
    const data = {};
    for (const [key, value] of formData.entries()) {
      // positionフィールドは複数選択可能なので配列として処理
      if (key === 'position') {
        if (!data.position) {
          data.position = [];
        }
        data.position.push(value);
      } else {
        data[key] = value;
      }
    }

    console.log('[採用応募フォーム] 送信リクエスト受信:', {
      ip: clientIP,
      name: data.name,
      timestamp: new Date().toISOString(),
    });

    // ハニーポット検証(スパムボット対策)
    if (data.website && data.website.trim() !== '') {
      console.log('[採用応募フォーム] スパム検出(ハニーポット):', clientIP);
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
      console.log('[採用応募フォーム] Turnstile検証失敗:', clientIP);
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
      console.log('[採用応募フォーム] レート制限超過:', {
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
    const validation = validateRecruitForm(data);
    if (!validation.valid) {
      console.log('[採用応募フォーム] バリデーションエラー:', validation.error);
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

    // メール送信(Resend API)
    const emailResult = await sendRecruitEmailViaResend(data, env, clientIP);

    if (!emailResult.success) {
      console.error('[採用応募フォーム] メール送信失敗:', emailResult.error);
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

    console.log('[採用応募フォーム] 送信成功:', {
      ip: clientIP,
      email: data.email,
      name: data.name,
    });

    return new Response(
      JSON.stringify({
        success: true,
        message: 'ご応募ありがとうございます。担当者より折り返しご連絡いたします。',
      }),
      {
        status: 200,
        headers: corsHeaders,
      }
    );
  } catch (error) {
    console.error('[採用応募フォーム] 予期しないエラー:', error);
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
    return result.success === true;
  } catch (error) {
    console.error('[Turnstile検証] エラー:', error);
    return false;
  }
}

/**
 * レート制限チェック(Workers KV使用)
 */
async function checkRateLimit(context, clientIP) {
  const { env } = context;
  const rateLimitKey = `ratelimit:recruit:${clientIP}`;
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

    // カウント増加(TTL: 300秒)
    await env.RATE_LIMIT.put(rateLimitKey, (count + 1).toString(), {
      expirationTtl: windowSeconds,
    });

    return { allowed: true, count: count + 1 };
  } catch (error) {
    console.error('[レート制限] KVエラー:', error);
    // KVエラー時は処理を継続(セキュリティよりも可用性優先)
    return { allowed: true, count: 0 };
  }
}

/**
 * 採用応募フォームのバリデーション
 */
function validateRecruitForm(data) {
  // 必須フィールドチェック
  const requiredFields = {
    name: 'お名前',
    kana: 'フリガナ',
    email: 'メールアドレス',
    phone: '電話番号',
    position: '応募職種',
    privacy: 'プライバシーポリシー同意',
  };

  for (const [field, label] of Object.entries(requiredFields)) {
    if (field === 'position') {
      // positionは配列なので特別処理
      if (!data.position || data.position.length === 0) {
        return {
          valid: false,
          error: `${label}を選択してください。`,
        };
      }
    } else if (!data[field] || (typeof data[field] === 'string' && data[field].trim() === '')) {
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

  // フリガナ(カタカナのみ)チェック
  const kanaRegex = /^[ァ-ヶー\s]+$/;
  if (!kanaRegex.test(data.kana)) {
    return {
      valid: false,
      error: 'フリガナは全角カタカナで入力してください。',
    };
  }

  // 電話番号形式チェック
  const phoneRegex = /^[0-9\-\+\(\)\s]{10,20}$/;
  if (!phoneRegex.test(data.phone)) {
    return {
      valid: false,
      error: '有効な電話番号を入力してください。',
    };
  }

  // 年齢チェック(任意フィールド)
  if (data.age) {
    const age = parseInt(data.age, 10);
    if (isNaN(age) || age < 15 || age > 100) {
      return {
        valid: false,
        error: '年齢は15〜100の範囲で入力してください。',
      };
    }
  }

  return { valid: true };
}

/**
 * Resend API 経由でメール送信
 */
async function sendRecruitEmailViaResend(data, env, clientIP) {
  const timestamp = new Date().toLocaleString('ja-JP', {
    timeZone: 'Asia/Tokyo',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  // 環境変数チェック
  if (!env.RESEND_API_KEY) {
    console.error('[Resend] RESEND_API_KEY が設定されていません');
    return {
      success: false,
      error: 'メール送信システムが正しく設定されていません。',
    };
  }

  const fromEmail = env.FROM_EMAIL || 'noreply@doujimafront.com';
  const recipientEmail = env.RECIPIENT_EMAIL || 'info@doujimafront.com';

  // 応募職種の整形(配列を文字列に変換)
  const positionText = Array.isArray(data.position)
    ? data.position.join('、')
    : data.position;

  // メール件名
  const subject = `【採用応募】${data.name} - ${positionText}`;

  // メール本文(HTML形式)
  const htmlBody = `
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Noto Sans JP', sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background-color: #b8860b; color: white; padding: 20px; text-align: center; }
    .content { background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; }
    .field { margin-bottom: 15px; }
    .label { font-weight: bold; color: #b8860b; }
    .value { margin-top: 5px; padding: 10px; background-color: white; border-left: 3px solid #b8860b; }
    .footer { margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>堂島フロント企画 採用応募フォーム</h2>
    </div>
    <div class="content">
      <p>新しい採用応募がありました。</p>

      <div class="field">
        <div class="label">お名前</div>
        <div class="value">${data.name}</div>
      </div>

      <div class="field">
        <div class="label">フリガナ</div>
        <div class="value">${data.kana}</div>
      </div>

      <div class="field">
        <div class="label">メールアドレス</div>
        <div class="value">${data.email}</div>
      </div>

      <div class="field">
        <div class="label">電話番号</div>
        <div class="value">${data.phone}</div>
      </div>

      <div class="field">
        <div class="label">応募職種</div>
        <div class="value">${positionText}</div>
      </div>

      <div class="field">
        <div class="label">年齢</div>
        <div class="value">${data.age || '未入力'}</div>
      </div>

      <div class="field">
        <div class="label">住所</div>
        <div class="value">${data.address || '未入力'}</div>
      </div>

      <div class="field">
        <div class="label">職務経験</div>
        <div class="value">${data.experience || '未入力'}</div>
      </div>

      <div class="field">
        <div class="label">志望動機</div>
        <div class="value">${data.motivation || '未入力'}</div>
      </div>

      <div class="field">
        <div class="label">その他・メッセージ</div>
        <div class="value">${data.message || '未入力'}</div>
      </div>

      <div class="footer">
        送信日時: ${timestamp}<br>
        送信元IP: ${clientIP}<br>
        このメールは堂島フロント企画の自動送信システムより送信されています。
      </div>
    </div>
  </div>
</body>
</html>
  `;

  try {
    console.log('[Resend] メール送信開始:', {
      from: fromEmail,
      to: recipientEmail,
      subject: subject,
    });

    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: `堂島フロント企画 採用応募フォーム <${fromEmail}>`,
        to: [recipientEmail],
        subject: subject,
        html: htmlBody,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('[Resend] APIエラー:', {
        status: response.status,
        error: errorText,
      });
      return {
        success: false,
        error: `Resend API エラー: ${response.status} - ${errorText}`,
      };
    }

    const result = await response.json();
    console.log('[Resend] メール送信成功:', result);

    return { success: true, data: result };
  } catch (error) {
    console.error('[Resend] メール送信エラー:', error);
    return {
      success: false,
      error: `メール送信エラー: ${error.message}`,
    };
  }
}
