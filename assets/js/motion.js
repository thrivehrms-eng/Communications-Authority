// Ambient motion: header scroll progress, hero parallax, pointer spotlights,
// rotating search hints and a one-time "hello" from the help button.
import { reduceMotion } from './util.js';

export default function () {
  const still = reduceMotion();
  const header = document.querySelector('[data-header]');
  const heroBg = document.querySelector('.ca-hero__bg');
  let queued = false;

  const onScroll = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      const max = document.documentElement.scrollHeight - innerHeight;
      header?.style.setProperty('--progress', max > 0 ? (scrollY / max).toFixed(4) : '0');
      if (heroBg && !still && scrollY < innerHeight) heroBg.style.transform = `translate3d(0, ${Math.min(80, scrollY * 0.18).toFixed(1)}px, 0)`;
    });
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (still) return;

  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.querySelectorAll('[data-spotlight]').forEach((el) => el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', `${e.clientX - r.left}px`);
      el.style.setProperty('--my', `${e.clientY - r.top}px`);
    }, { passive: true }));
  }

  document.querySelectorAll('[data-placeholder-cycle]').forEach((input) => {
    const hints = input.dataset.placeholderCycle.split('|');
    let i = 0;
    setInterval(() => {
      if (document.hidden || input.value || document.activeElement === input) return;
      input.classList.add('is-swapping');
      setTimeout(() => {
        i = (i + 1) % hints.length;
        input.placeholder = hints[i];
        input.classList.remove('is-swapping');
      }, 200);
    }, 3200);
  });

  const fab = document.querySelector('[data-fab]');
  if (fab) setTimeout(() => fab.classList.add('is-hello'), 2500);
}
