// Accordion (commitments), generic disclosures (footer expanders) and the mobile "Show more services"
export default function () {
  document.querySelectorAll('[data-accordion]').forEach((acc) => {
    const buttons = [...acc.querySelectorAll('.ca-acc__btn')];
    const single = acc.hasAttribute('data-single');
    const set = (btn, open) => {
      btn.setAttribute('aria-expanded', open);
      document.getElementById(btn.getAttribute('aria-controls')).classList.toggle('is-open', open);
    };
    buttons.forEach((btn) => btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      if (open && single) buttons.forEach((other) => other !== btn && set(other, false));
      set(btn, open);
    }));
  });

  document.querySelectorAll('[data-disclosure]').forEach((btn) => {
    const target = document.getElementById(btn.getAttribute('aria-controls'));
    target.hidden = btn.getAttribute('aria-expanded') !== 'true';
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      target.hidden = !open;
    });
  });

  const grid = document.querySelector('[data-services]');
  const more = document.querySelector('[data-services-toggle]');
  if (grid && more) {
    grid.classList.add('is-collapsed');
    more.hidden = false;
    more.addEventListener('click', () => {
      const open = more.getAttribute('aria-expanded') !== 'true';
      more.setAttribute('aria-expanded', open);
      grid.classList.toggle('is-collapsed', !open);
      more.firstChild.textContent = open ? 'Show fewer services' : 'Show more services';
      if (open) grid.querySelector('.ca-services__extra a')?.focus();
    });
  }
}
