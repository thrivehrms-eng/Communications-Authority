// Page dot navigation: marks the section in the middle of the viewport
export default function ([nav]) {
  const links = new Map();
  nav.querySelectorAll('a[href^="#"]').forEach((a) => {
    const section = document.getElementById(a.hash.slice(1));
    if (section) links.set(section, a);
  });
  const io = new IntersectionObserver((entries) => entries.forEach(({ isIntersecting, target }) => {
    if (!isIntersecting) return;
    links.forEach((a) => a.removeAttribute('aria-current'));
    links.get(target).setAttribute('aria-current', 'location');
  }), { rootMargin: '-45% 0px -50% 0px' });
  links.forEach((_, section) => io.observe(section));
}
