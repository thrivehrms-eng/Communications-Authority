// Shared helpers for the homepage modules
export const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),[tabindex]:not([tabindex="-1"])';
export const focusables = (root) => [...root.querySelectorAll(FOCUSABLE)].filter((el) => el.getClientRects().length);

// Keep Tab inside the given containers (in order). Returns a release function.
export function trapFocus(containers) {
  const onKey = (e) => {
    if (e.key !== 'Tab') return;
    const els = containers.flatMap((c) => (c.matches(FOCUSABLE) ? [c] : focusables(c)));
    if (!els.length) return;
    e.preventDefault();
    const i = els.indexOf(document.activeElement);
    els[(i + (e.shiftKey ? -1 : 1) + els.length) % els.length].focus();
  };
  document.addEventListener('keydown', onKey);
  return () => document.removeEventListener('keydown', onKey);
}

// Overlays announce themselves so the others can close
export const announceOpen = (name) => document.dispatchEvent(new CustomEvent('ca:open', { detail: name }));
export const onOtherOpen = (name, fn) => document.addEventListener('ca:open', (e) => e.detail !== name && fn());
