// FX background: soft flowing light curves + drifting dots on a canvas (≤30fps, pausable).
// Panels with data-fx-static get a single still frame (one animated area per page is enough).
import { reduceMotion } from './util.js';

export default (panels) => panels.forEach(init);

function init(panel) {
  const c = panel.querySelector('[data-fx-canvas]');
  const btn = panel.querySelector('[data-fx-pause]');
  const ctx = c.getContext('2d');
  const css = getComputedStyle(document.documentElement);
  const cols = ['--ca-primary-500', '--ca-accent-500'].map((v) => css.getPropertyValue(v).trim());
  const k = (+panel.dataset.fxDensity || 1) * (matchMedia('(max-width: 767px)').matches ? 0.5 : 1);
  const still = reduceMotion() || panel.hasAttribute('data-fx-static');
  const r = (a, b) => a + Math.random() * (b - a);
  const lines = Array.from({ length: Math.max(4, Math.round(12 * k)) }, (_, i) => ({
    y: r(0.15, 0.95), amp: r(0.03, 0.12), f: r(0.5, 1.4), sp: r(0.08, 0.22), ph: r(0, 6.28),
    col: cols[i % 2], a: r(0.12, 0.38), lw: r(0.6, 1.6),
  }));
  const dots = Array.from({ length: Math.round(40 * k) }, () => ({
    x: Math.random(), y: Math.random(), vx: r(-0.012, 0.012), vy: r(-0.008, 0.008), s: r(0.8, 2), a: r(0.3, 0.8),
  }));
  let w, h, raf, last = 0, t = r(0, 50), visible = true, paused = false;

  const size = () => {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    w = c.clientWidth; h = c.clientHeight;
    c.width = w * dpr; c.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  const draw = () => {
    ctx.clearRect(0, 0, w, h);
    for (const l of lines) {
      ctx.beginPath();
      ctx.strokeStyle = l.col; ctx.globalAlpha = l.a; ctx.lineWidth = l.lw;
      for (let x = 0; x <= w + 16; x += 16) {
        const p = x / w;
        const y = (l.y + Math.sin(p * l.f * 6.28 + l.ph + t * l.sp) * l.amp + Math.sin(p * 3 + t * l.sp * 0.7) * l.amp * 0.4) * h;
        x ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
      }
      ctx.stroke();
    }
    ctx.fillStyle = cols[1];
    for (const d of dots) {
      ctx.globalAlpha = d.a;
      ctx.beginPath(); ctx.arc(d.x * w, d.y * h, d.s, 0, 6.28); ctx.fill();
    }
    ctx.globalAlpha = 1;
  };
  const step = (now) => {
    raf = requestAnimationFrame(step);
    if (now - last < 33) return;
    const dt = Math.min((now - last) / 1000, 0.1);
    last = now; t += dt;
    for (const d of dots) { d.x = (d.x + d.vx * dt + 1) % 1; d.y = (d.y + d.vy * dt + 1) % 1; }
    draw();
  };
  const run = () => {
    cancelAnimationFrame(raf);
    if (!still && !paused && visible && !document.hidden) { last = performance.now(); raf = requestAnimationFrame(step); }
  };

  size(); draw();
  new ResizeObserver(() => { size(); draw(); }).observe(c);
  if (still) { if (btn) btn.hidden = true; return; }
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; run(); }).observe(panel);
  document.addEventListener('visibilitychange', run);
  btn.addEventListener('click', () => { paused = !paused; btn.setAttribute('aria-pressed', paused); run(); });
}
