// Mirvan — interactivity
(function () {
  'use strict';

  // -------- Theme toggle --------
  const STORAGE_KEY = 'mirvan-theme';
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');

  function setTheme(theme, persist) {
    root.setAttribute('data-theme', theme);
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) {}
    }
  }

  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') || 'light';
      setTheme(current === 'dark' ? 'light' : 'dark', true);
    });
  }

  // Honor live OS changes if user hasn't manually picked
  if (window.matchMedia) {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e) => {
      let stored = null;
      try { stored = localStorage.getItem(STORAGE_KEY); } catch (err) {}
      if (!stored) {
        setTheme(e.matches ? 'dark' : 'light', false);
      }
    };
    if (mq.addEventListener) mq.addEventListener('change', handler);
    else if (mq.addListener) mq.addListener(handler);
  }

  // -------- Reveal on scroll --------
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const reveals = document.querySelectorAll('.reveal');

  if (reduced || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('is-visible'));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    reveals.forEach((el) => io.observe(el));
  }

  // -------- Footer year --------
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
