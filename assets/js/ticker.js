// Logo ticker: duplicate the list once for a seamless CSS marquee, with a pause/play button
import { reduceMotion } from './util.js';

export default function (roots) {
  if (reduceMotion()) return; // stays a static, horizontally scrollable row
  roots.forEach((ticker) => {
    const track = ticker.querySelector('[data-ticker-track]');
    const copy = track.firstElementChild.cloneNode(true);
    copy.setAttribute('aria-hidden', 'true');
    copy.querySelectorAll('a').forEach((a) => { a.tabIndex = -1; });
    track.append(copy);
    ticker.classList.add('is-ready');

    const btn = ticker.querySelector('[data-ticker-pause]');
    btn.addEventListener('click', () => {
      const paused = btn.getAttribute('aria-pressed') !== 'true';
      btn.setAttribute('aria-pressed', paused);
      ticker.classList.toggle('is-paused', paused);
    });
  });
}
