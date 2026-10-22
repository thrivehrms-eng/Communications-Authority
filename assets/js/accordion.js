// Disclosures: buttons with aria-expanded that show/hide the element named by aria-controls (footer expanders)
export default function (buttons) {
  buttons.forEach((btn) => {
    const target = document.getElementById(btn.getAttribute('aria-controls'));
    target.hidden = btn.getAttribute('aria-expanded') !== 'true';
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      target.hidden = !open;
    });
  });
}
