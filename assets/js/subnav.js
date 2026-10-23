// Section navigation on inner pages: always open beside the content on wide screens,
// a closed "In this section" disclosure above the content on smaller ones.
export default function (boxes) {
  const wide = matchMedia('(min-width: 1100px)');
  const set = () => boxes.forEach((box) => { box.open = wide.matches; });
  set();
  wide.addEventListener('change', set);
  boxes.forEach((box) => box.addEventListener('toggle', () => { if (wide.matches && !box.open) box.open = true; }));
}
