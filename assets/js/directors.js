// Supplier registration has room for ten directors. Without JavaScript all ten fieldsets show; with it,
// directors 2 to 10 start hidden (unless they already hold answers) and are added, or removed, one at a time.
export default function (roots) {
  roots.forEach((root) => {
    const sets = [...root.querySelectorAll('[data-director]')];
    const add = root.querySelector('[data-director-add]');
    const status = root.querySelector('[data-director-status]');
    const controls = (fs) => [...fs.querySelectorAll('input, select')];
    const filled = (fs) => controls(fs).some((c) => (c.type === 'file' ? c.files.length : c.value.trim()));
    const name = (fs) => fs.querySelector('legend').firstChild.textContent.trim();

    const update = () => { add.hidden = !sets.some((fs) => fs.hidden); };

    sets.slice(1).forEach((fs) => {
      if (!filled(fs)) fs.hidden = true;
      const remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'ca-btn ca-btn--outline ca-btn--sm ca-director__remove';
      remove.textContent = `Remove ${name(fs).toLowerCase()}`;
      remove.addEventListener('click', () => {
        controls(fs).forEach((c) => { c.value = ''; });
        fs.hidden = true;
        update();
        status.textContent = `${name(fs)} removed.`;
        add.focus();
      });
      fs.append(remove);
    });

    add.addEventListener('click', () => {
      const next = sets.find((fs) => fs.hidden);
      if (!next) return;
      next.hidden = false;
      update();
      status.textContent = `${name(next)} added.${sets.some((fs) => fs.hidden) ? '' : ` You can list up to ${sets.length} directors.`}`;
      controls(next)[0].focus();
    });

    update();
  });
}
