// Floating "Quick help" button and its card
import { announceOpen, onOtherOpen } from './util.js';

export default function ([fab]) {
  const btn = fab.querySelector('[data-fab-toggle]');
  const card = document.getElementById(btn.getAttribute('aria-controls'));

  const set = (open, returnFocus) => {
    if (open === !card.hidden) return;
    if (open) announceOpen('fab');
    card.hidden = !open;
    btn.setAttribute('aria-expanded', open);
    if (open) card.querySelector('a').focus();
    else if (returnFocus) btn.focus();
  };

  // On phones and short landscape screens the button would sit on top of the hero controls, the search and
  // popular tasks, which offer the same routes; it waits until they have scrolled away (CSS decides where)
  const defer = document.querySelectorAll('[data-fab-defer]');
  if (defer.length && 'IntersectionObserver' in window) {
    const inView = new Set();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? inView.add(e.target) : inView.delete(e.target)));
      fab.classList.toggle('is-deferred', inView.size > 0);
    });
    defer.forEach((el) => io.observe(el));
  }

  btn.addEventListener('click', () => set(card.hidden));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !card.hidden) set(false, true); });
  document.addEventListener('click', (e) => { if (!fab.contains(e.target)) set(false); });
  onOtherOpen('fab', () => set(false));
}
