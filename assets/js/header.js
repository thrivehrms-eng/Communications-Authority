// Header: scrolled state + dropdowns (click/Enter/Space, hover intent, Esc, click outside)
export default function ([header]) {
  const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 24);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const hover = matchMedia('(hover: hover)');
  let current = null;
  let timer;
  let hoverOpenedAt = 0;

  const set = (item, open, returnFocus) => {
    const btn = item.querySelector('.ca-nav__trigger');
    btn.setAttribute('aria-expanded', open);
    item.querySelector('.ca-dropdown').classList.toggle('is-open', open);
    if (open) {
      if (current && current !== item) set(current, false);
      current = item;
    } else if (current === item) {
      current = null;
      if (returnFocus) btn.focus();
    }
  };

  header.querySelectorAll('.ca-nav__item').forEach((item) => {
    const btn = item.querySelector('.ca-nav__trigger');
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      // a click right after hover-open should not immediately close it
      if (open && Date.now() - hoverOpenedAt < 500) return;
      set(item, !open);
    });
    item.addEventListener('mouseenter', () => {
      if (!hover.matches) return;
      clearTimeout(timer);
      timer = setTimeout(() => {
        if (current !== item) { set(item, true); hoverOpenedAt = Date.now(); }
      }, current ? 0 : 120);
    });
    item.addEventListener('mouseleave', () => {
      if (!hover.matches) return;
      clearTimeout(timer);
      timer = setTimeout(() => current === item && set(item, false), 250);
    });
    item.addEventListener('focusout', (e) => { if (!item.contains(e.relatedTarget)) set(item, false); });
  });

  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && current) set(current, false, true); });
  document.addEventListener('click', (e) => { if (current && !current.contains(e.target)) set(current, false); });
}
