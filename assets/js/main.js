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
  truncate: '[data-max-chars]',
  reveal: '[data-reveal], [data-reveal-stagger]',
  'hero-fx': '[data-fx]',
  consent: '[data-consent]',
  'dot-nav': '[data-dots]',
  motion: 'body',
};

for (const [name, selector] of Object.entries(modules)) {
  const roots = [...document.querySelectorAll(selector)];
  if (roots.length) import(`./${name}.js`).then((m) => m.default(roots)).catch((err) => console.error(`[ca] ${name}`, err));
}

document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
