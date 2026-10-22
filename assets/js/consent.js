// Cookie consent card. Exposes window.caConsent.get(category) for scripts added later.
const KEY = 'ca-consent';
const read = () => { try { return JSON.parse(localStorage.getItem(KEY)); } catch { return null; } };
const write = (v) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* storage unavailable */ } };

export default function ([box]) {
  let state = read();
  window.caConsent = { get: (category) => category === 'necessary' || !!state?.[category] };

  const settingsBtn = box.querySelector('[data-consent-settings]');
  const settings = document.getElementById(settingsBtn.getAttribute('aria-controls'));
  const analytics = box.querySelector('#consent-analytics');
  const media = box.querySelector('#consent-media');
  let opener = null;

  const show = (focus) => {
    analytics.checked = !!state?.analytics;
    media.checked = !!state?.media;
    box.hidden = false;
    if (focus) { box.tabIndex = -1; box.focus(); }
  };
  const hide = () => {
    box.hidden = true;
    opener?.focus();
    opener = null;
  };
  const save = (choice) => {
    state = { necessary: true, ...choice, date: new Date().toISOString() };
    write(state);
    document.dispatchEvent(new CustomEvent('ca:consent', { detail: state }));
    hide();
  };

  box.addEventListener('click', (e) => {
    const action = e.target.closest('[data-consent-action]')?.dataset.consentAction;
    if (action === 'all') save({ analytics: true, media: true });
    else if (action === 'necessary') save({ analytics: false, media: false });
    else if (action === 'save') save({ analytics: analytics.checked, media: media.checked });
  });
  settingsBtn.addEventListener('click', () => {
    const open = settingsBtn.getAttribute('aria-expanded') !== 'true';
    settingsBtn.setAttribute('aria-expanded', open);
    settings.hidden = !open;
  });
  box.addEventListener('keydown', (e) => { if (e.key === 'Escape') hide(); });
  document.querySelectorAll('[data-consent-open]').forEach((btn) => btn.addEventListener('click', () => { opener = btn; show(true); }));

  if (!state) show(false);
}
