// Project filter chips (hidden without JS, so all tiles show)
import { reduceMotion } from './util.js';

export default function (roots) {
  roots.forEach((root) => {
    const chips = root.querySelector('[data-filter-chips]');
    const items = [...root.querySelectorAll('[data-tags]')];
    const status = root.querySelector('[data-filter-status]');
    const empty = root.querySelector('[data-filter-empty]');
    chips.hidden = false;

    chips.addEventListener('click', (e) => {
      const chip = e.target.closest('[data-filter-value]');
      if (!chip) return;
      chips.querySelectorAll('[data-filter-value]').forEach((c) => c.setAttribute('aria-pressed', c === chip));
      const value = chip.dataset.filterValue;
      const shown = items.filter((li) => value === 'all' || li.dataset.tags.split(' ').includes(value));

      items.forEach((li) => li.classList.add('is-fading'));
      setTimeout(() => {
        items.forEach((li) => li.classList.toggle('is-hidden', !shown.includes(li)));
        shown.forEach((li, i) => li.style.setProperty('--filter-delay', `${i * 60}ms`));
        requestAnimationFrame(() => requestAnimationFrame(() => shown.forEach((li) => li.classList.remove('is-fading'))));
        setTimeout(() => items.forEach((li) => li.style.removeProperty('--filter-delay')), 700);
        empty.hidden = shown.length > 0;
        status.textContent = shown.length ? `Showing ${shown.length} project${shown.length === 1 ? '' : 's'}` : 'No projects in this category.';
      }, reduceMotion() ? 0 : 200);
    });
  });
}
