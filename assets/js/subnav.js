// Section navigation on inner pages: always open beside the content on wide screens,
// a closed "In this section" disclosure above the content on smaller ones.
export default function (boxes) {
  const wide = matchMedia('(min-width: 1100px)');
  const set = () => boxes.forEach((box) => { box.open = wide.matches; });
  set();
  wide.addEventListener('change', set);
  boxes.forEach((box) => box.addEventListener('toggle', () => { if (wide.matches && !box.open) box.open = true; }));

  // A link with a query (Closed Tenders: /tenders/?tender_status=closed) is the current page when the address matches it
  if (!location.search) return;
  boxes.forEach((box) => {
    const match = [...box.querySelectorAll('a[href*="?"]')].find((a) => {
      const url = new URL(a.href);
      return url.pathname === location.pathname && url.search === location.search;
    });
    if (!match) return;
    box.querySelector('a[aria-current="page"]')?.removeAttribute('aria-current');
    match.setAttribute('aria-current', 'page');
  });
}
