/* reading-progress.js — scroll progress bar, ~380 bytes minified
   rAF + dirty-flag pattern: scroll event only sets a flag,
   rAF loop does the single style.width write. No layout thrashing. */
(function () {
  'use strict';
  var bar = document.getElementById('reading-progress');
  if (!bar) return;

  /* Find the article element to measure scroll depth against */
  var article = document.querySelector('main article, article[class], main');
  if (!article) return;

  var artTop = 0, artH = 0, ticking = false;

  function measure() {
    var rect = article.getBoundingClientRect();
    artTop = rect.top + window.pageYOffset;
    artH   = article.offsetHeight;
  }

  function update() {
    ticking = false;
    var scrolled = window.pageYOffset - artTop;
    var pct = artH > 0 ? Math.min(Math.max(scrolled / artH, 0), 1) : 0;
    bar.style.width = (pct * 100).toFixed(2) + '%';
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }

  /* Debounced resize — re-measure article bounds */
  var resizeTimer;
  function onResize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(measure, 150);
  }

  measure();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize, { passive: true });
}());
