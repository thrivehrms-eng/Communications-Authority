// Header: scrolled state + the mega menu.
// One white surface resizes between sections; a section's content slides in from the side it was
// approached from; a pill tracks the section under the pointer. Click/Enter/Space toggle a section,
// ArrowDown opens it and moves into it, Left/Right move between sections, Esc and click outside close.
export default function ([header]) {
  const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 24);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const nav = header.querySelector('[data-nav]');
  if (!nav) return;
  const bar = header.querySelector('.ca-header__bar');
  const items = [...nav.querySelectorAll('.ca-nav__item')];
  const hover = matchMedia('(hover: hover)');
  const trigger = (item) => item.querySelector('.ca-nav__trigger');
  const view = (item) => item.querySelector('.ca-dropdown');
  let current = null;
  let openTimer;
  let closeTimer;
  let hoverOpenedAt = 0;

  // apply a change with transitions switched off, then switch them back on
  const instantly = (cls, change) => { nav.classList.add(cls); change(); void nav.offsetWidth; nav.classList.remove(cls); };

  const movePill = (item) => {
    if (!item) { nav.classList.remove('has-pill'); return; }
    const b = bar.getBoundingClientRect();
    const r = trigger(item).getBoundingClientRect();
    const place = () => {
      nav.style.setProperty('--pill-x', `${r.left - b.left - 4}px`);
      nav.style.setProperty('--pill-w', `${r.width + 8}px`);
    };
    // glide between sections; appear in place when it was hidden
    if (nav.classList.contains('has-pill')) place(); else instantly('pill-jump', place);
    nav.classList.add('has-pill');
  };

  const open = (item) => {
    const prev = current;
    if (prev === item) return;
    const dir = prev ? Math.sign(items.indexOf(item) - items.indexOf(prev)) : 0;
    if (prev) {
      view(prev).style.setProperty('--dir', -dir);
      view(prev).classList.remove('is-open');
      trigger(prev).setAttribute('aria-expanded', 'false');
    }
    // park the incoming content on the side it arrives from, then measure it
    const v = view(item);
    v.classList.add('is-entering');
    v.style.setProperty('--dir', dir);
    const height = `${v.offsetHeight}px`;
    v.classList.remove('is-entering');
    // switching morphs the surface; a first open appears at full size
    if (prev) nav.style.setProperty('--mega-h', height);
    else instantly('is-placing', () => nav.style.setProperty('--mega-h', height));
    v.classList.add('is-open');
    nav.classList.add('is-open');
    trigger(item).setAttribute('aria-expanded', 'true');
    current = item;
    movePill(item);
  };

  const close = (returnFocus = false) => {
    clearTimeout(openTimer);
    if (!current) return;
    const item = current;
    current = null;
    view(item).style.setProperty('--dir', 0);
    view(item).classList.remove('is-open');
    nav.classList.remove('is-open');
    trigger(item).setAttribute('aria-expanded', 'false');
    if (returnFocus) trigger(item).focus();
    if (!nav.matches(':hover')) movePill(null);
  };

  items.forEach((item, i) => {
    const btn = trigger(item);
    btn.addEventListener('click', () => {
      if (current !== item) open(item);
      // a click straight after a hover-open should not close it again
      else if (Date.now() - hoverOpenedAt > 500) close();
    });
    btn.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        open(item);
        view(item).querySelector('a').focus();
      } else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        trigger(items[(i + (e.key === 'ArrowRight' ? 1 : -1) + items.length) % items.length]).focus();
      }
    });
    btn.addEventListener('focus', () => { if (btn.matches(':focus-visible')) movePill(item); });

    // hover intent: a short pause before opening, a shorter one when switching sections
    item.addEventListener('mouseenter', () => {
      if (!hover.matches) return;
      clearTimeout(openTimer);
      movePill(item);
      if (current === item) return;
      openTimer = setTimeout(() => { open(item); hoverOpenedAt = Date.now(); }, current ? 80 : 140);
    });
    item.addEventListener('mouseleave', () => clearTimeout(openTimer));
    item.addEventListener('focusout', (e) => {
      if (current !== item || item.contains(e.relatedTarget)) return;
      if (!e.relatedTarget && item.matches(':hover')) return; // a click on the menu's background
      close();
    });
  });

  // leaving the nav closes after a grace period, long enough to cross the gap down to the menu
  nav.addEventListener('mouseenter', () => clearTimeout(closeTimer));
  nav.addEventListener('mouseleave', () => {
    if (!hover.matches) return;
    clearTimeout(openTimer);
    clearTimeout(closeTimer);
    movePill(current);
    closeTimer = setTimeout(() => close(), 280);
  });
  nav.addEventListener('focusout', (e) => {
    if (!nav.contains(e.relatedTarget) && !nav.matches(':hover')) movePill(current);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && current) close(current.contains(document.activeElement));
  });
  document.addEventListener('click', (e) => { if (current && !nav.contains(e.target)) close(); });
  addEventListener('resize', () => {
    if (!current) return;
    nav.style.setProperty('--mega-h', `${view(current).offsetHeight}px`);
    movePill(current);
  });
  matchMedia('(max-width: 1099px)').addEventListener('change', () => { close(); movePill(null); });
}
