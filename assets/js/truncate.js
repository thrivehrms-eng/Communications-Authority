// Character limits for titles/excerpts (data-max-chars). Cuts at a word boundary and adds an ellipsis;
// the full text stays available to screen readers and as a tooltip. Without JS, CSS line-clamp applies.
export default function (els) {
  els.forEach((el) => {
    const max = Number(el.dataset.maxChars);
    const full = el.textContent.replace(/\s+/g, ' ').trim();
    if (!max || full.length <= max) return;
    // keep the last word only if the limit falls exactly on its end
    const head = /\s/.test(full[max]) ? full.slice(0, max) : full.slice(0, max).replace(/\s+\S*$/, '');
    const cut = head.replace(/[\s,.;:—–-]+$/, '');
    const shown = document.createElement('span');
    shown.setAttribute('aria-hidden', 'true');
    shown.textContent = `${cut}…`;
    const spoken = document.createElement('span');
    spoken.className = 'ca-vh';
    spoken.textContent = full;
    el.replaceChildren(shown, spoken);
    el.title = full;
  });
}
