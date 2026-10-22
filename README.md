# Communications Authority of Kenya — Homepage (concept: Media Harbour)

A static rebuild of the CA homepage in semantic HTML, modern CSS and vanilla ES modules: no frameworks, no build step.
The layout and interactions follow the Media Harbour concept, while brand colours, logo and fonts (Inter + Maitree 700) come strictly from the current CA theme.

Version 2 applied a UX review (see `docs/ux-review.md`): a task-first section order, less motion, higher text contrast and an in-page cookie banner. Version 3 (client feedback) moved search and popular tasks into their own panel, slimmed the news with character limits, and added real partner logos and CA project photos. Version 4 turns the hero into an auto-playing slider with a consistent two-line headline rhythm, compacts the find panel into a single strip, and rebuilds News as a lead story plus a list.

## Run locally

Any static server works (ES modules need `http://`, not `file://`):

```sh
npx http-server -c-1 .     # then open http://localhost:8080/
```

Add `?placeholders` to the URL to outline every placeholder that still needs real content (see `docs/content-todo.md`).

## Structure

```
index.html                  the homepage (one H1, sections from §7 of the brief, footer)
assets/css/
  tokens.css                CA palette (verbatim) → semantic roles, type, space, motion; @font-face
  base.css                  reset, typography, focus, utilities, reduced motion
  layout.css                floating panels, container, section heads, eyebrows
  components.css            buttons, links, service card, accordion, project tile, news card, chips, social, logo tile
  sections.css              header bar + mega menu, each homepage section, footer
  overlays.css              menu overlay, search panel, help FAB, cookie banner, dot nav, reveal
  motion.css                entrances, reveal variants and hover micro-interactions
assets/js/
  main.js                   entry: imports a module only if its root element exists
  util.js                   focus trap, reduced-motion check, "one overlay at a time" events
  carousel.js               hero slider: 7s auto-play, pause/play, previous/next, slide buttons, swipe; holds on hover/off-screen, stops on focus and reduced motion
  header.js                 scrolled state, mega menu (morphing surface, sliding pill, hover intent, Enter/Space/ArrowDown/Left/Right, Esc, click outside)
  overlay-menu.js           burger overlay (Latest pager + Contact; mobile nav accordion built from the mega menu)
  search.js                 search mode, live FAQ filter, GET /?s=
  fab.js                    "Quick help" floating button (deferred on phones while the hero tasks are visible)
  accordion.js              disclosures (footer expanders)
  ticker.js                 logo marquee (duplicated list, pause/play)
  filter.js                 project filter chips + live status
  truncate.js               character limits (data-max-chars): word-boundary cut + ellipsis, full text kept for screen readers
  reveal.js                 scroll reveal (only below-the-fold content starts hidden)
  motion.js                 header scroll progress, hero parallax, pointer spotlights, rotating search hints, help-button hello
  hero-fx.js                canvas light curves + dots (≤30fps, pausable, < 4 KB); data-fx-static draws one still frame
  consent.js                cookie banner; exposes window.caConsent.get('analytics')
  dot-nav.js                page section dots (≥1280px)
assets/fonts/               Inter variable + Maitree 700 (Latin, WOFF2)
assets/img/                 CA logos, favicons, AVIF/WebP images
assets/img/logos/           affiliation logos (official files from each organisation)
assets/icons/sprite.svg     24px line icons, 1.75 stroke, round caps
docs/content-todo.md        every placeholder still needing real content
docs/ux-review.md           v2 UX review: findings, rules applied, departures from the brief
```

Naming is BEM with a `ca-` prefix. Each section is self-contained markup (`<section class="ca-panel …">`) so it can be lifted into a WordPress template part.

## Porting to WordPress

- Asset paths are relative (`assets/...`). In a theme, prefix them with `get_template_directory_uri()`.
- Internal links are root-relative (`/tenders/`) and the search form is `GET /?s=`, so both work as-is.
- The main menu is rendered once. Each section is a `.ca-nav__item` holding an intro (title, one-line summary, overview link), groups of links (icon, name and a one-line description) and, where a section has a long tail, a quick-links band of plain links. The mobile menu is cloned from the same markup at runtime and drops the summaries, icons and descriptions.
- In WordPress, a custom `Walker_Nav_Menu` can output this markup: use the menu item's built-in **Description** field for the one-liner and a CSS class (e.g. `icon-licence`) or a custom field for the sprite icon name; top-level items carry the section intro, and second-level items marked as groups become headings.
- Character limits: news titles 80 (featured 100), summaries 140. In WordPress, enforce them server-side (e.g. `wp_html_excerpt()` / a word-boundary `mb_substr()`) and keep the full title in a visually hidden span, as `truncate.js` does.

## Behaviour without JavaScript

All content is visible: footer sub-lists expanded, every project tile shown (filter chips hidden), ticker as a scrollable row, and desktop menu sections open on hover or keyboard focus (each with its own white background). The hero search works (plain `GET /?s=`). Burger, header search, FAB, cookie banner and the pause buttons are hidden.

## Using CA orange

Orange is used sparingly and **only on light backdrops** (white, light blue). On navy and blue panels the accent is cyan or white. Two tokens, chosen by contrast (see `tokens.css`):

| Token | Value | Use for |
|---|---|---|
| `--action` | `--ca-secondary-600` `#BD4400` | "File a complaint" buttons on white surfaces (header, menu, help card: white text 5.3:1), the help button's icon, news dates, the news "Read more" cues and FAQ numbers (text 5.3:1 on white), small icons in Popular tasks and the contact list, text selection |
| `--signature` | `--ca-secondary-500` `#EC5B13` | Decorative details on light surfaces only: the bar before eyebrows on light panels, the header's scroll-progress line, the top edge of the mega menu and the menu overlay, the active page dot, logo-tile hover borders, link hover underlines, and the small welcome dot in the hero (CA's signature mark) |

Never: orange text on white in `#EC5B13` (3.5:1); orange on the primary blue (2.2:1); orange elements on navy panels (use cyan `--accent` or white).

## Motion

All motion lives in `assets/css/motion.css` and `assets/js/motion.js` (plus the slider in `carousel.js`). It uses transform, opacity and clip-path only; hover effects apply only on pointer devices; `prefers-reduced-motion` reduces everything to instant state changes and turns off the JavaScript effects.

| Where | What |
|---|---|
| Hero | Welcome line, title, highlighted second line, text and button rise in sequence on load and on every slide change; the photo slowly settles from a 1.08 zoom (paused with the slider); gentle scroll parallax |
| Header | Thin orange line shows how far down the page you are |
| Sections | Softer, longer scroll reveals; About text slides in from the left and USF text from the right; photos open like a curtain; eyebrow bars draw in; icon badges pop in after their cards |
| Cards and tiles | A soft light follows the pointer over service cards, stay-safe cards and project tiles; icon badges tilt and grow; project photos zoom while titles lift |
| Buttons and links | Lift on hover, a light sweep across filled buttons, press-down on click; news titles underline from left to right and the "Read more" arrow nudges forward |
| Main menu | One white surface opens under the header and resizes smoothly between sections; each section's content slides in from the side you came from and is clipped to the surface while it resizes; a soft pill glides behind the section under the pointer (or keyboard focus); groups fade up in sequence; link icons fill blue and tilt on hover |
| Other menus | Menu overlay, search and help items stagger in |
| Search | The placeholder cycles through example searches (IMEI, type approval, licence fees…) until you focus it |
| Filter | Project tiles return one after another |
| Help button | Pulses twice, once, 2.5s after load |

## Accessibility notes

- Skip link, labelled landmarks, exactly one H1, no skipped heading levels.
- Every overlay (menu, search, FAB) moves focus in, closes on Esc and returns focus to its opener; the menu traps Tab. The cookie banner sits in the page flow, so it never covers content or focus.
- Only the hero slider and the ticker move; both have a visible pause control, stop on hover/focus and do not auto-play under `prefers-reduced-motion`. The slider's live region is silent while it auto-plays and polite once the user takes control.
- Text contrast targets 7:1 where the CA palette allows (body on white 10.4:1, white on primary 7.6:1, muted white on navy ≥ 9:1).
- Main menu: each section is a disclosure button (`aria-expanded`/`aria-controls`) followed by its links in DOM order, so Tab moves straight from a section into its links and on to the next section (which closes the previous one). ArrowDown opens a section and moves into it, Left/Right move between sections, Esc closes and returns focus to the section button. Hover opens after a 140ms pause (80ms when switching sections) and closes 280ms after the pointer leaves, so the gap down to the menu can be crossed. Closing sections stop taking pointer events at once, so a fading section never steals a click.
- News "Read more" cues are decorative (`aria-hidden`): each story is one link (its title) whose click area covers the whole card, so screen readers hear the title once rather than a list of identical "Read more" links.
- External links carry an icon plus visually hidden "(external site)".
- Under 380px wide the language links shrink to 36px wide so the header fits at 320px (still above the WCAG 2.2 AA 24px minimum).

## QA status (this build)

- axe-core 4.10: 0 violations at 1440, 390 and 320px (reduced motion), and with a mega-menu section, the menu overlay and the mobile menu open.
- Mega menu checked at 1100, 1440 and 1920px for hover, switching, travelling from a section button down into its links, keyboard (ArrowDown/Left/Right, Tab through and out, Esc) and click outside; without JavaScript sections open on hover and keyboard focus.
- No console errors; no horizontal scroll or clipped content at 320 / 390 / 768 / 1024 / 1100 / 1280 / 1440; works with JS disabled and with reduced motion.
- Size (esbuild minified): CSS 60.3 KB, JS 17.5 KB. The original 50 KB CSS budget was lifted by the client in v6 in favour of richer motion.
- Lighthouse was not run in this environment.
