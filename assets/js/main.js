// Entry point: initialise each module only if its root element exists
const modules = {
  header: '[data-header]',
  carousel: '[data-carousel]',
  'overlay-menu': '[data-overlay]',
  search: '[data-search-panel]',
  fab: '[data-fab]',
  accordion: '[data-disclosure]',
  ticker: '[data-ticker]',
  filter: '[data-filter]',
  videos: '[data-videos]',
  subnav: '[data-subnav]',
  profiles: '[data-profiles]',
  forms: '[data-form]',
  imei: '[data-imei]',
  truncate: '[data-max-chars]',
  reveal: '[data-reveal], [data-reveal-stagger]',
  'hero-fx': '[data-fx]',
  consent: '[data-consent]',
  motion: 'body',
};

for (const [name, selector] of Object.entries(modules)) {
  const roots = [...document.querySelectorAll(selector)];
  if (roots.length) import(`./${name}.js`).then((m) => m.default(roots)).catch((err) => console.error(`[ca] ${name}`, err));
}

// A page opened from one of our links starts at the top. Browsers do this in a normal tab; this also covers
// previews that show the site in a frame as tall as the page, where the outer page would keep its scroll.
const arrival = performance.getEntriesByType('navigation')[0];
const fromOurPage = document.referrer && new URL(document.referrer).origin === location.origin;
if (window.self !== window.top && arrival?.type === 'navigate' && fromOurPage && !location.hash) {
  const root = document.documentElement;
  root.style.scrollPaddingTop = '0px'; // the header offset would otherwise push the page too far up
  root.scrollIntoView({ block: 'start', behavior: 'instant' });
  root.style.scrollPaddingTop = '';
}

document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
