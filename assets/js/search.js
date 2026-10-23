// Search: swaps the nav for an input, shows the FAQ panel and filters it live
import { announceOpen, onOtherOpen } from './util.js';

export default function ([panel]) {
  const header = panel.closest('[data-header]');
  const toggle = header.querySelector('[data-search-toggle]');
  const form = header.querySelector('[data-search-form]');
  const input = form.querySelector('input[name="s"]');
  const items = [...panel.querySelectorAll('.ca-faq > li')];
  const empty = panel.querySelector('[data-search-empty]');
  const status = panel.querySelector('[data-search-status]');

  const filter = () => {
    const words = input.value.toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    items.forEach((li) => {
      const match = words.every((w) => li.textContent.toLowerCase().includes(w));
      li.hidden = !match;
      shown += match;
    });
    empty.hidden = shown > 0;
    status.textContent = words.length ? `${shown} matching question${shown === 1 ? '' : 's'}` : '';
  };

  const set = (open, returnFocus = true) => {
    if (open === !panel.hidden) return;
    if (open) announceOpen('search');
    panel.hidden = !open;
    header.classList.toggle('is-search', open);
    document.documentElement.classList.toggle('is-search', open);
    toggle.setAttribute('aria-expanded', open);
    if (open) {
      input.focus();
    } else {
      input.value = '';
      filter();
      if (returnFocus) toggle.focus();
    }
  };

  toggle.addEventListener('click', () => set(panel.hidden));
  panel.querySelector('[data-search-close]').addEventListener('click', () => set(false));
  input.addEventListener('input', filter);
  form.addEventListener('submit', (e) => { if (!input.value.trim()) e.preventDefault(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !panel.hidden) set(false); });
  document.addEventListener('click', (e) => { if (!panel.hidden && !header.contains(e.target)) set(false, false); });
  onOtherOpen('search', () => set(false, false));
}
