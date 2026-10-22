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

  // On phones the button would sit on top of the hero's popular tasks, which offer the same routes
  const tasks = document.querySelector('.ca-hero-tasks');
  if (tasks && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => fab.classList.toggle('is-deferred', e.isIntersecting)).observe(tasks);
  }

  btn.addEventListener('click', () => set(card.hidden));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !card.hidden) set(false, true); });
  document.addEventListener('click', (e) => { if (!fab.contains(e.target)) set(false); });
  onOtherOpen('fab', () => set(false));
}
