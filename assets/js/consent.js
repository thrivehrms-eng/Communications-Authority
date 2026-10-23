// Cookie consent card. Exposes window.caConsent.get(category) and .set(category, on) for other scripts.
const KEY = 'ca-consent';
const read = () => { try { return JSON.parse(localStorage.getItem(KEY)); } catch { return null; } };
const write = (v) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* storage unavailable */ } };

export default function ([box]) {
  let state = read();
  const store = (choice) => {
    state = { necessary: true, ...choice, date: new Date().toISOString() };
    write(state);
    document.dispatchEvent(new CustomEvent('ca:consent', { detail: state }));
  };
  window.caConsent = {
    get: (category) => category === 'necessary' || !!state?.[category],
    // e.g. "Always play YouTube videos" in the video player; keeps the other choices as they are
    set: (category, on) => store({ analytics: !!state?.analytics, media: !!state?.media, [category]: !!on }),
  };

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
    // return focus to whatever opened the banner; on a first visit, continue from the skip link
    (opener || document.querySelector('.ca-skip'))?.focus();
    opener = null;
  };
  const save = (choice) => { store(choice); hide(); };

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
