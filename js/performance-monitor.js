// パフォーマンス監視とメモリ最適化ツール

class PerformanceMonitor {
  constructor() {
    this.observers = new Map();
    this.timers = new Set();
    this.eventListeners = new WeakMap();
    this.startTime = performance.now();
  }

  // IntersectionObserver の統合管理
  createObserver(options, callback, elements) {
    const observerKey = JSON.stringify(options);
    
    if (!this.observers.has(observerKey)) {
      const observer = new IntersectionObserver(callback, options);
      this.observers.set(observerKey, observer);
    }
    
    const observer = this.observers.get(observerKey);
    elements.forEach(el => observer.observe(el));
    
    return observer;
  }

  // タイマー管理（メモリリーク防止）
  createTimeout(callback, delay) {
    const timer = setTimeout(() => {
      callback();
      this.timers.delete(timer);
    }, delay);
    
    this.timers.add(timer);
    return timer;
  }

  createInterval(callback, interval) {
    const timer = setInterval(callback, interval);
    this.timers.add(timer);
    return timer;
  }

  // 全タイマークリア
  clearAllTimers() {
    this.timers.forEach(timer => clearTimeout(timer));
    this.timers.clear();
  }

  // Observer クリーンアップ
  cleanupObservers() {
    this.observers.forEach(observer => observer.disconnect());
    this.observers.clear();
  }

  // メモリ使用量チェック
  checkMemoryUsage() {
    if (performance.memory) {
      const memory = performance.memory;
      console.log('Memory Usage:', {
        used: `${(memory.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB`,
        total: `${(memory.totalJSHeapSize / 1024 / 1024).toFixed(2)}MB`,
        limit: `${(memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2)}MB`
      });
    }
  }

  // FPS測定
  measureFPS(duration = 3000) {
    let frames = 0;
    let lastTime = performance.now();
    
    const measure = (currentTime) => {
      frames++;
      if (currentTime - lastTime >= duration) {
        const fps = (frames * 1000) / (currentTime - lastTime);
        console.log(`Average FPS: ${fps.toFixed(1)}`);
        return;
      }
      requestAnimationFrame(measure);
    };
    
    requestAnimationFrame(measure);
  }

  // パフォーマンス統計
  getPerformanceStats() {
    const navigation = performance.getEntriesByType('navigation')[0];
    const paintEntries = performance.getEntriesByType('paint');
    
    return {
      domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
      loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
      firstPaint: paintEntries.find(entry => entry.name === 'first-paint')?.startTime || 0,
      firstContentfulPaint: paintEntries.find(entry => entry.name === 'first-contentful-paint')?.startTime || 0,
      sessionDuration: performance.now() - this.startTime
    };
  }

  // 全体クリーンアップ
  cleanup() {
    this.clearAllTimers();
    this.cleanupObservers();
    console.log('Performance monitor cleanup completed');
  }
}

// グローバル監視インスタンス
window.performanceMonitor = new PerformanceMonitor();

// ページ離脱時のクリーンアップ
window.addEventListener('beforeunload', () => {
  window.performanceMonitor.cleanup();
  if (window.slideshowCleanup) {
    window.slideshowCleanup();
  }
});

// 開発モード時のデバッグ情報
if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
  console.log('Performance monitoring enabled');
  
  // 5秒後にメモリ使用量チェック
  setTimeout(() => {
    window.performanceMonitor.checkMemoryUsage();
    console.log('Performance Stats:', window.performanceMonitor.getPerformanceStats());
  }, 5000);
  
  // FPS測定開始
  window.performanceMonitor.measureFPS();
}