// Hero slider: auto-advances every 7s with pause/play, previous/next and slide buttons.
// Holds while hovered, off-screen or in a hidden tab; stops when keyboard focus enters it
// (until Play is pressed) and never auto-plays under prefers-reduced-motion.
import { reduceMotion } from './util.js';

const INTERVAL = 7000;

export default (roots) => roots.forEach(init);

function init(root) {
  const slides = [...root.querySelectorAll('.ca-slide')];
  const images = [...root.querySelectorAll('.ca-hero__img')];
  const dots = [...root.querySelectorAll('[data-carousel-dot]')];
  const live = root.querySelector('[data-carousel-slides]');
  const toggle = root.querySelector('[data-carousel-pause]');
  const toggleLabel = toggle.querySelector('.ca-vh');
  const holds = new Set();
  let index = 0;
  let playing = !reduceMotion();
  let timer = 0;
  let startedAt = 0;
  let remaining = INTERVAL;

  root.style.setProperty('--interval', `${INTERVAL}ms`);

  const schedule = () => {
    clearTimeout(timer);
    if (!playing || holds.size) return;
    startedAt = Date.now();
    timer = setTimeout(() => show(index + 1), remaining);
  };

  const show = (n) => {
    index = (n + slides.length) % slides.length;
    slides.forEach((el, i) => el.classList.toggle('is-active', i === index));
    images.forEach((el, i) => el.classList.toggle('is-active', i === index));
    dots.forEach((el, i) => el.setAttribute('aria-current', i === index ? 'true' : 'false'));
    remaining = INTERVAL;
    schedule();
  };

  const setPlaying = (on) => {
    playing = on;
    remaining = INTERVAL;
    root.classList.toggle('is-paused', !on);
    toggleLabel.textContent = on ? 'Pause slides' : 'Play slides';
    live.setAttribute('aria-live', on ? 'off' : 'polite'); // announce slide changes only when the user drives them
    schedule();
  };

  // temporary holds (hover, off-screen, hidden tab) keep the remaining time
  const hold = (reason, on) => {
    const wasHeld = holds.size > 0;
    if (on) holds.add(reason); else holds.delete(reason);
    if (!wasHeld && holds.size && playing) { clearTimeout(timer); remaining -= Date.now() - startedAt; }
    root.classList.toggle('is-held', holds.size > 0);
    if (wasHeld && !holds.size) schedule();
  };

  toggle.addEventListener('click', () => setPlaying(!playing));
  root.querySelector('[data-carousel-prev]').addEventListener('click', () => show(index - 1));
  root.querySelector('[data-carousel-next]').addEventListener('click', () => show(index + 1));
  dots.forEach((dot, i) => dot.addEventListener('click', () => show(i)));

  root.addEventListener('mouseenter', () => hold('hover', true));
  root.addEventListener('mouseleave', () => hold('hover', false));
  root.addEventListener('focusin', (e) => { if (playing && e.target !== toggle) setPlaying(false); });
  document.addEventListener('visibilitychange', () => hold('hidden', document.hidden));
  new IntersectionObserver(([e]) => hold('offscreen', !e.isIntersecting)).observe(root);

  // swipe on touch screens (buttons remain the primary controls)
  let x0 = null;
  root.addEventListener('pointerdown', (e) => { if (e.pointerType === 'touch') x0 = e.clientX; });
  root.addEventListener('pointerup', (e) => {
    if (x0 === null) return;
    const dx = e.clientX - x0;
    x0 = null;
    if (Math.abs(dx) > 48) show(index + (dx < 0 ? 1 : -1));
  });

  setPlaying(playing);
}
