// People listings: a name opens that person's profile in a dialog, loaded from their profile page,
// so several profiles can be read without leaving the list. The links still work on their own.
export default function (lists) {
  if (typeof HTMLDialogElement !== 'function') return;
  const sprite = document.querySelector('use')?.getAttribute('href').split('#')[0] || '/assets/icons/sprite.svg';
  const dialog = document.createElement('dialog');
  dialog.className = 'ca-profile-dialog';
  dialog.setAttribute('aria-labelledby', 'profile-dialog-title');
  dialog.innerHTML = `<div class="ca-profile-dialog__bar"><h2 class="ca-profile-dialog__title" id="profile-dialog-title"></h2>
    <button class="ca-iconbtn" type="button" data-close><svg class="ca-icon" aria-hidden="true"><use href="${sprite}#close"/></svg><span class="ca-vh">Close profile</span></button></div>
    <div class="ca-profile-dialog__body"></div>`;
  document.body.append(dialog);
  const title = dialog.querySelector('h2');
  const body = dialog.querySelector('.ca-profile-dialog__body');
  const cache = new Map();
  let opener = null;

  const load = (url) => {
    if (!cache.has(url)) {
      cache.set(url, fetch(url)
        .then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then((text) => new DOMParser().parseFromString(text, 'text/html').querySelector('[data-profile-content]')));
    }
    return cache.get(url);
  };

  lists.forEach((list) => {
    // start loading as soon as someone points at or tabs to a name
    const warm = (e) => { const a = e.target.closest?.('a[data-profile]'); if (a) load(a.href).catch(() => cache.delete(a.href)); };
    list.addEventListener('pointerover', warm);
    list.addEventListener('focusin', warm);
    list.addEventListener('click', async (e) => {
      const link = e.target.closest('a[data-profile]');
      if (!link || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      try {
        const content = await load(link.href);
        if (!content) throw new Error('no profile');
        opener = link;
        title.textContent = link.textContent.trim();
        body.replaceChildren(document.importNode(content, true));
        dialog.showModal();
        dialog.scrollTop = 0;
      } catch {
        cache.delete(link.href);
        location.href = link.href; // fall back to the profile page
      }
    });
  });

  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => opener?.focus());
}
