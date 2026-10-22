// Burger menu overlay: Latest (desktop) + mobile nav accordion + Contact
import { trapFocus, focusables, announceOpen, onOtherOpen } from './util.js';

export default function ([overlay]) {
  const toggle = document.querySelector('[data-menu-toggle]');
  const label = toggle.querySelector('[data-menu-label]');
  const panel = overlay.querySelector('[data-overlay-panel]');
  const root = document.documentElement;
  let release;

  buildMobileNav(overlay.querySelector('[data-mobile-nav]'));
  initLatest(overlay.querySelector('[data-latest]'));

  const set = (open, returnFocus = true) => {
    if (open === !overlay.hidden) return;
    if (open) announceOpen('menu');
    overlay.hidden = !open;
    toggle.setAttribute('aria-expanded', open);
    label.textContent = open ? 'Close menu' : 'Open menu';
    root.classList.toggle('is-locked', open);
    root.classList.toggle('is-overlay', open);
    if (open) {
      release = trapFocus([toggle, panel]);
      focusables(panel)[0]?.focus();
    } else {
      release?.();
      if (returnFocus) toggle.focus();
    }
  };

  toggle.addEventListener('click', () => set(overlay.hidden));
  overlay.addEventListener('click', (e) => { if (e.target === overlay) set(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !overlay.hidden) set(false); });
  onOtherOpen('menu', () => set(false, false));
}

// Mobile: rebuild the primary nav as an accordion from the desktop dropdown markup
function buildMobileNav(nav) {
  if (!nav) return;
  const list = document.createElement('ul');
  list.className = 'ca-mnav';
  list.setAttribute('role', 'list');
  document.querySelectorAll('.ca-nav__item').forEach((item, i) => {
    const inner = item.querySelector('.ca-dropdown__inner').cloneNode(true);
    inner.querySelectorAll('[id]').forEach((el) => { el.id = `m-${el.id}`; });
    inner.querySelectorAll('[aria-labelledby]').forEach((el) => el.setAttribute('aria-labelledby', `m-${el.getAttribute('aria-labelledby')}`));
    const btn = item.querySelector('.ca-nav__trigger').cloneNode(true);
    btn.className = 'ca-mnav__btn';
    btn.setAttribute('aria-controls', `mnav-${i}`);
    btn.setAttribute('aria-expanded', 'false');
    const sub = document.createElement('div');
    sub.className = 'ca-mnav__panel';
    sub.id = `mnav-${i}`;
    sub.hidden = true;
    sub.append(inner);
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      sub.hidden = !open;
    });
    const li = document.createElement('li');
    li.append(btn, sub);
    list.append(li);
  });
  nav.append(list);
}

// "Latest": 3×2 cards, previous/next paging
function initLatest(section) {
  if (!section) return;
  const items = [...section.querySelectorAll('[data-latest-list] > li')];
  const prev = section.querySelector('[data-latest-prev]');
  const next = section.querySelector('[data-latest-next]');
  const count = section.querySelector('[data-latest-count]');
  const per = 6;
  const pages = Math.ceil(items.length / per);
  let page = 0;
  const render = () => {
    items.forEach((li, i) => { li.hidden = Math.floor(i / per) !== page; });
    count.textContent = `${page + 1} / ${pages}`;
    prev.disabled = page === 0;
    next.disabled = page === pages - 1;
  };
  prev.addEventListener('click', () => { page = Math.max(0, page - 1); render(); });
  next.addEventListener('click', () => { page = Math.min(pages - 1, page + 1); render(); });
  render();
}
