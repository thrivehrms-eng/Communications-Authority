// Scroll reveal: fade up 24px; elements already on screen at load stay at rest
export default function (els) {
  if (!('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver((entries) => entries.forEach(({ isIntersecting, target }) => {
    if (!isIntersecting) return;
    io.unobserve(target);
    target.classList.remove('reveal-pending');
    // drop the transition (and stagger delays) once done so hover states respond immediately
    setTimeout(() => target.classList.remove('reveal-run'), 600 + target.children.length * 60);
  }), { threshold: 0.15 });

  els.forEach((el) => {
    if (el.getBoundingClientRect().top < innerHeight * 0.9) return;
    if (el.hasAttribute('data-reveal-stagger')) {
      [...el.children].forEach((child, i) => child.style.setProperty('--reveal-delay', `${i * 60}ms`));
    }
    el.classList.add('reveal-pending', 'reveal-run');
    io.observe(el);
  });
}
