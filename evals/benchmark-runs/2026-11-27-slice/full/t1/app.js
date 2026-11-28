// Progressive enhancement: smooth-scroll for in-page anchor links only.
(function () {
  'use strict';
  if (typeof document === 'undefined' || !document.querySelectorAll) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var links = document.querySelectorAll('a[href^="#"]');
  if (!links || !links.length) return;

  Array.prototype.forEach.call(links, function (link) {
    link.addEventListener('click', function (e) {
      var href = link.getAttribute('href');
      if (!href || href.length < 2) return;
      var target = null;
      try {
        target = document.getElementById(decodeURIComponent(href.slice(1)));
      } catch (err) {
        return;
      }
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      if (history && history.pushState) history.pushState(null, '', href);
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    });
  });
})();
