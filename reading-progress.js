/* reading-progress.js — scroll progress bar
   v2: article-only gating + correct 100% math
   ─────────────────────────────────────────────────────────────────
   GATING: only activates when the page contains .review-body
   (single-tool reviews) or .ct-article (comparison / deep-dive
   pages). All other pages (home, hubs, about, contact) have neither
   class, so the script exits immediately and the bar stays at 0%.

   MATH FIX: progress = scrolled / (articleHeight - viewportHeight)
   This means the bar reaches 100% exactly when the bottom of the
   article content aligns with the bottom of the viewport — i.e.,
   when the reader has seen the last line.

   rAF + dirty-flag pattern: scroll event only sets a flag;
   rAF loop does the single style.width write. No layout thrashing.
   ───────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  /* 1. Find the progress bar element */
  var bar = document.getElementById('reading-progress');
  if (!bar) return;

  /* 2. Gate: only run on article pages.
        .review-body  → single-tool review pages
        .ct-article   → comparison pages and long-form deep-dives
        Any page without one of these classes gets no active bar. */
  var article = document.querySelector('.review-body, .ct-article');
  if (!article) {
    /* Leave bar at width:0 — invisible, no event listeners attached */
    return;
  }

  var artTop = 0, artH = 0, ticking = false;

  function measure() {
    var rect = article.getBoundingClientRect();
    artTop = rect.top + window.pageYOffset;
    artH   = article.offsetHeight;
  }

  function update() {
    ticking = false;
    var scrolled  = window.pageYOffset - artTop;
    /* Readable distance = article height minus one viewport height.
       At this point the bottom of the article is at the bottom of
       the viewport — the reader has reached the end. */
    var readable  = artH - window.innerHeight;
    var pct = readable > 0
      ? Math.min(Math.max(scrolled / readable, 0), 1)
      : 0;
    bar.style.width = (pct * 100).toFixed(2) + '%';
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }

  /* Debounced resize — re-measure article bounds on window resize */
  var resizeTimer;
  function onResize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(measure, 150);
  }

  measure();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize, { passive: true });
}());
