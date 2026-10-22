// Cursor follower (decorative): a labelled circle that trails the pointer over tiles and cards
import { reduceMotion } from './util.js';

export default function (targets) {
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches || reduceMotion()) return;
  const el = document.querySelector('[data-cursor-follower]');
  const label = el.firstElementChild;
  let x = 0, y = 0, cx = 0, cy = 0, raf = 0;
  document.documentElement.classList.add('has-cursor');

  const loop = () => {
    cx += (x - cx) * 0.2; cy += (y - cy) * 0.2;
    el.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
    raf = Math.abs(x - cx) + Math.abs(y - cy) > 0.5 ? requestAnimationFrame(loop) : 0;
  };
  addEventListener('pointermove', (e) => { x = e.clientX; y = e.clientY; if (!raf) raf = requestAnimationFrame(loop); }, { passive: true });

  targets.forEach((t) => {
    t.addEventListener('pointerenter', (e) => {
      label.textContent = t.dataset.cursor;
      if (!el.classList.contains('is-active')) { cx = x = e.clientX; cy = y = e.clientY; loop(); }
      el.classList.add('is-active');
    });
    t.addEventListener('pointerleave', () => el.classList.remove('is-active'));
  });
}
