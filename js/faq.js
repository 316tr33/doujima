document.addEventListener("DOMContentLoaded", () => {
  // FAQ要素の取得
  const faqItems = document.querySelectorAll(".faq-item");
  const searchInput = document.querySelector(".faq-search");
  const categoryButtons = document.querySelectorAll(".category-btn");
  const noResultsMessage = document.querySelector(".no-results");
  const scrollTopBtn = document.querySelector(".scroll-top");

  // カテゴリ別に質問を分類
  const categories = {
    all: "すべて",
    basic: "基本情報",
    preparation: "準備・装備",
    pilgrimage: "巡礼方法",
    manners: "作法・マナー",
    misc: "その他",
  };

  // アコーディオン機能
  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");

    // 回答コンテンツをラップ（サニタイズ付き）
    if (answer && !answer.querySelector(".faq-answer-content")) {
      const content = answer.innerHTML;
      // DOMPurifyの代替として、基本的なサニタイズを実装
      const sanitizedContent = content
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
        .replace(/on\w+\s*=\s*"[^"]*"/gi, '')
        .replace(/on\w+\s*=\s*'[^']*'/gi, '')
        .replace(/javascript:/gi, '');
      
      // textContentとinnerHTMLの使い分けで安全性向上
      const wrapper = document.createElement('div');
      wrapper.className = 'faq-answer-content';
      wrapper.innerHTML = sanitizedContent;
      answer.innerHTML = '';
      answer.appendChild(wrapper);
    }

    question.addEventListener("click", () => {
      const isActive = item.classList.contains("active");

      // 他のアクティブな項目を閉じる
      const currentlyActive = document.querySelector(".faq-item.active");
      if (currentlyActive && currentlyActive !== item) {
        currentlyActive.classList.remove("active");
      }

      // 現在の項目をトグル
      item.classList.toggle("active");

      // スムーズスクロール
      if (!isActive) {
        setTimeout(() => {
          const rect = item.getBoundingClientRect();
          const scrollTop =
            window.pageYOffset || document.documentElement.scrollTop;
          const targetY = rect.top + scrollTop - 100;

          window.scrollTo({
            top: targetY,
            behavior: "smooth",
          });
        }, 100);
      }
    });
  });

  // 検索機能
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const searchTerm = e.target.value.toLowerCase();
      let hasResults = false;

      faqItems.forEach((item) => {
        const question = item
          .querySelector(".faq-question span")
          .textContent.toLowerCase();
        const answer = item
          .querySelector(".faq-answer p")
          .textContent.toLowerCase();

        if (question.includes(searchTerm) || answer.includes(searchTerm)) {
          item.style.display = "block";
          hasResults = true;

          // 検索語をハイライト
          if (searchTerm.length > 2) {
            highlightSearchTerm(item, searchTerm);
          } else {
            removeHighlight(item);
          }
        } else {
          item.style.display = "none";
          item.classList.remove("active");
        }
      });

      // 検索結果なしメッセージの表示
      if (noResultsMessage) {
        noResultsMessage.style.display = hasResults ? "none" : "block";
      }
    });
  }

  // カテゴリフィルター機能
  if (categoryButtons.length > 0) {
    categoryButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        // アクティブボタンの更新
        categoryButtons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");

        const category = btn.dataset.category;
        filterByCategory(category);
      });
    });
  }

  // カテゴリでフィルタリング
  function filterByCategory(category) {
    let hasResults = false;

    faqItems.forEach((item) => {
      if (category === "all" || item.dataset.category === category) {
        item.style.display = "block";
        hasResults = true;
      } else {
        item.style.display = "none";
        item.classList.remove("active");
      }
    });

    if (noResultsMessage) {
      noResultsMessage.style.display = hasResults ? "none" : "block";
    }
  }

  // 検索語のハイライト
  function highlightSearchTerm(item, term) {
    const question = item.querySelector(".faq-question span");
    const answer = item.querySelector(".faq-answer p");

    // 元のテキストを保存
    if (!question.dataset.original) {
      question.dataset.original = question.textContent;
    }
    if (!answer.dataset.original) {
      answer.dataset.original = answer.textContent;
    }

    // ハイライト適用（XSS対策済み）
    // 検索語をエスケープしてから正規表現化
    const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedTerm})`, "gi");
    
    // textContentでテキストを取得し、安全にハイライト
    const highlightText = (text) => {
      const div = document.createElement('div');
      const parts = text.split(regex);
      
      parts.forEach((part, index) => {
        if (index % 2 === 1 && regex.test(part)) {
          const mark = document.createElement('mark');
          mark.style.cssText = 'background: #d4af37; color: #1a1a1a; padding: 2px;';
          mark.textContent = part;
          div.appendChild(mark);
        } else {
          div.appendChild(document.createTextNode(part));
        }
      });
      
      return div.innerHTML;
    };
    
    question.innerHTML = highlightText(question.dataset.original);
    answer.innerHTML = highlightText(answer.dataset.original);
  }

  // ハイライトを削除
  function removeHighlight(item) {
    const question = item.querySelector(".faq-question span");
    const answer = item.querySelector(".faq-answer p");

    if (question.dataset.original) {
      question.textContent = question.dataset.original;
    }
    if (answer.dataset.original) {
      answer.textContent = answer.dataset.original;
    }
  }

  // スクロールトップボタン
  if (scrollTopBtn) {
    // スクロール時の表示/非表示
    window.addEventListener("scroll", () => {
      if (window.pageYOffset > 300) {
        scrollTopBtn.classList.add("visible");
      } else {
        scrollTopBtn.classList.remove("visible");
      }
    });

    // クリックで上部へスクロール
    scrollTopBtn.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }

  // URLハッシュから特定の質問を開く
  function openQuestionFromHash() {
    const hash = window.location.hash;
    if (hash) {
      const targetId = hash.substring(1);
      const targetItem = document.getElementById(targetId);
      if (targetItem && targetItem.classList.contains("faq-item")) {
        // 他のアクティブな項目を閉じる
        document.querySelectorAll(".faq-item.active").forEach((item) => {
          item.classList.remove("active");
        });

        // ターゲット項目を開く
        targetItem.classList.add("active");

        // スクロール
        setTimeout(() => {
          targetItem.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
        }, 100);
      }
    }
  }

  // ページ読み込み時とハッシュ変更時に実行
  openQuestionFromHash();
  window.addEventListener("hashchange", openQuestionFromHash);

  // キーボードナビゲーション
  document.addEventListener("keydown", (e) => {
    const activeItem = document.querySelector(".faq-item.active");

    if (e.key === "Escape" && activeItem) {
      activeItem.classList.remove("active");
    }

    // 矢印キーでナビゲーション
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      const visibleItems = Array.from(faqItems).filter(
        (item) => item.style.display !== "none"
      );
      const currentIndex = visibleItems.indexOf(activeItem);

      let nextIndex;
      if (e.key === "ArrowDown") {
        nextIndex =
          currentIndex < visibleItems.length - 1 ? currentIndex + 1 : 0;
      } else {
        nextIndex =
          currentIndex > 0 ? currentIndex - 1 : visibleItems.length - 1;
      }

      if (visibleItems[nextIndex]) {
        if (activeItem) activeItem.classList.remove("active");
        visibleItems[nextIndex].classList.add("active");
        visibleItems[nextIndex].scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }
    }
  });

  // 統計情報の更新
  function updateStats() {
    const totalQuestions = faqItems.length;
    const totalCategories = Object.keys(categories).length - 1; // 'all'を除く

    const statElements = document.querySelectorAll(".stat-number");
    if (statElements.length >= 2) {
      statElements[0].textContent = totalQuestions;
      statElements[1].textContent = totalCategories;
    }
  }

  updateStats();
});
