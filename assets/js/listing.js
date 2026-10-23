// Search and filters for long lists (tenders, awarded contracts, publications, documents, news).
// Every item is in the HTML, so without JavaScript the whole list shows and the tools stay hidden.
// With it, the list filters as you type or choose, shows a page at a time, and keeps the choices in the URL
// so a filtered view can be shared or linked to (the menu's "Closed Tenders" link uses ?tender_status=closed).

export default function (roots) {
  roots.forEach((root) => {
    const form = root.querySelector('form');
    const q = form.querySelector('[data-listing-q]');
    const filters = [...form.querySelectorAll('[data-listing-filter]')];
    const items = [...root.querySelector('[data-listing-items]').children];
    const status = root.querySelector('[data-listing-status]');
    const empty = root.querySelector('[data-listing-empty]');
    const more = root.querySelector('[data-listing-more]');
    const size = Number(root.dataset.pageSize) || 12;
    const [one, many] = root.dataset.noun.split('|');
    const noun = (n) => (n === 1 ? one : many);
    let matches = items;
    let limit = size;
    let timer;

    // Start from the URL, ignoring values the list does not offer
    const params = new URLSearchParams(location.search);
    if (params.has(q.name)) q.value = params.get(q.name);
    filters.forEach((sel) => {
      const v = params.get(sel.name);
      if (v && [...sel.options].some((o) => o.value === v)) sel.value = v;
    });

    function render() {
      matches.forEach((el, i) => { el.hidden = i >= limit; });
      const shown = Math.min(limit, matches.length);
      const left = matches.length - shown;
      more.parentElement.hidden = left === 0;
      more.textContent = `Show ${Math.min(size, left)} more ${noun(Math.min(size, left))}`;
      empty.hidden = matches.length > 0;
      const total = `${items.length} ${noun(items.length)}`;
      let text;
      if (!matches.length) text = `No ${many} match your search.`;
      else if (matches.length === items.length) text = left ? `Showing ${shown} of ${total}` : total;
      else text = `${matches.length} of ${total} match${left ? `, showing the first ${shown}` : ''}`;
      if (status.textContent !== text) status.textContent = text;
    }

    function apply() {
      const words = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      const chosen = filters.filter((sel) => sel.value).map((sel) => [sel.dataset.listingFilter, sel.value]);
      matches = items.filter((el) => words.every((w) => el.dataset.text.includes(w))
        && chosen.every(([key, v]) => el.dataset[key] === v));
      items.forEach((el) => { el.hidden = true; });
      limit = size;
      render();

      const url = new URL(location.href);
      [q, ...filters].forEach((f) => { if (f.value.trim()) url.searchParams.set(f.name, f.value.trim()); else url.searchParams.delete(f.name); });
      history.replaceState(history.state, '', url);
    }

    q.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(apply, 250); });
    filters.forEach((sel) => sel.addEventListener('change', apply));
    form.addEventListener('submit', (e) => { e.preventDefault(); clearTimeout(timer); apply(); });

    more.addEventListener('click', () => {
      const first = matches[limit];
      limit += size;
      render();
      // Move to the first new item (its title, or its title link) so keyboard and screen reader users carry on from there
      const heading = first.querySelector('h2, h3');
      const target = heading?.querySelector('a[href]') || heading || first;
      if (!target.matches('a[href]')) target.tabIndex = -1;
      target.focus();
    });

    root.querySelector('[data-listing-reset]').addEventListener('click', () => {
      q.value = '';
      filters.forEach((sel) => { sel.value = ''; });
      apply();
      q.focus();
    });

    apply();
  });
}
