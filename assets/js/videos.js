// Video row: each video plays here in a dialog rather than sending people off to YouTube.
// Nothing loads from YouTube until a video is opened, and then only from youtube-nocookie.com.
// Without "Embedded media" consent the dialog first says that playing loads YouTube, with a one-off
// Play button and an option to remember the choice. Without JS the links simply open YouTube.
export default function ([section]) {
  const dialog = section.querySelector('[data-video-dialog]');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const title = dialog.querySelector('[data-video-title]');
  const frame = dialog.querySelector('[data-video-frame]');
  const consent = dialog.querySelector('[data-video-consent]');
  const remember = dialog.querySelector('[data-video-remember]');
  const watchOnYouTube = dialog.querySelector('[data-video-yt]');
  let opener = null;

  const play = (id) => {
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0&playsinline=1`;
    iframe.title = `Video: ${title.textContent}`;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin'; // YouTube refuses embeds that send no referrer
    frame.replaceChildren(iframe);
    consent.hidden = true;
  };

  const open = (link) => {
    opener = link;
    title.textContent = link.title || link.textContent.trim(); // truncate.js keeps the full title in `title`
    watchOnYouTube.href = link.href;
    dialog.dataset.video = link.dataset.video;
    if (window.caConsent?.get('media')) {
      play(link.dataset.video);
    } else {
      const still = link.closest('.ca-video')?.querySelector('picture')?.cloneNode(true);
      if (still) still.querySelector('img').loading = 'eager';
      frame.replaceChildren(...(still ? [still] : []));
      remember.checked = false;
      consent.hidden = false;
    }
    dialog.showModal();
  };

  section.querySelectorAll('[data-video]').forEach((link) => {
    link.setAttribute('aria-haspopup', 'dialog');
    link.addEventListener('click', (e) => {
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; // new-tab clicks still go to YouTube
      e.preventDefault();
      open(link);
    });
  });

  dialog.querySelector('[data-video-play]').addEventListener('click', () => {
    if (remember.checked) window.caConsent?.set('media', true);
    play(dialog.dataset.video);
    // the button has gone: keep focus on Close rather than inside the player, where YouTube would swallow Esc
    dialog.querySelector('[data-video-close]').focus();
  });
  dialog.querySelector('[data-video-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); }); // backdrop
  dialog.addEventListener('close', () => {
    frame.replaceChildren(); // removing the player stops playback
    consent.hidden = true;
    opener?.focus();
  });
}
