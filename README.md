# Communications Authority of Kenya — Homepage (concept: Media Harbour)

A static rebuild of the CA homepage in semantic HTML, modern CSS and vanilla ES modules: no frameworks, no build step.
The layout and interactions follow the Media Harbour concept, while brand colours, logo and fonts (Inter + Maitree 700) come strictly from the current CA theme.

Version 2 applies a UX review (see `docs/ux-review.md`): a search-led hero with popular tasks, a task-first section order, less motion, higher text contrast and an in-page cookie banner.

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
  sections.css              header bar + dropdowns, each homepage section, footer
  overlays.css              menu overlay, search panel, help FAB, cookie banner, dot nav, reveal
assets/js/
  main.js                   entry: imports a module only if its root element exists
  util.js                   focus trap, reduced-motion check, "one overlay at a time" events
  header.js                 scrolled state, dropdowns (click/Enter/Space, 120ms hover intent, Esc, click outside)
  overlay-menu.js           burger overlay (Latest pager + Contact; mobile nav accordion built from the dropdowns)
  search.js                 search mode, live FAQ filter, GET /?s=
  fab.js                    "Quick help" floating button (deferred on phones while the hero tasks are visible)
  accordion.js              disclosures (footer expanders)
  ticker.js                 logo marquee (duplicated list, pause/play)
  filter.js                 project filter chips + live status
  reveal.js                 scroll reveal (only below-the-fold content starts hidden)
  hero-fx.js                canvas light curves + dots (≤30fps, pausable, < 4 KB); data-fx-static draws one still frame
  consent.js                cookie banner; exposes window.caConsent.get('analytics')
  dot-nav.js                page section dots (≥1280px)
assets/fonts/               Inter variable + Maitree 700 (Latin, WOFF2)
assets/img/                 CA logos, favicons, AVIF/WebP images
assets/icons/sprite.svg     24px line icons, 1.75 stroke, round caps
docs/content-todo.md        every placeholder still needing real content
docs/ux-review.md           v2 UX review: findings, rules applied, departures from the brief
```

Naming is BEM with a `ca-` prefix. Each section is self-contained markup (`<section class="ca-panel …">`) so it can be lifted into a WordPress template part.

## Porting to WordPress

- Asset paths are relative (`assets/...`). In a theme, prefix them with `get_template_directory_uri()`.
- Internal links are root-relative (`/tenders/`) and the search form is `GET /?s=`, so both work as-is.
- The menu dropdowns are plain nested lists; the mobile menu is generated from them at runtime, so only one menu needs to be rendered.

## Behaviour without JavaScript

All content is visible: footer sub-lists expanded, every project tile shown (filter chips hidden), ticker as a scrollable row, and desktop dropdowns open on hover or keyboard focus. The hero search works (plain `GET /?s=`). Burger, header search, FAB, cookie banner and the pause buttons are hidden.

## Accessibility notes

- Skip link, labelled landmarks, exactly one H1, no skipped heading levels.
- Every overlay (menu, search, FAB) moves focus in, closes on Esc and returns focus to its opener; the menu traps Tab. The cookie banner sits in the page flow, so it never covers content or focus.
- Only the hero canvas and the ticker move; both have a visible pause control and stop under `prefers-reduced-motion`.
- Text contrast targets 7:1 where the CA palette allows (body on white 10.4:1, white on primary 7.6:1, muted white on navy ≥ 9:1).
- External links carry an icon plus visually hidden "(external site)".
- Under 380px wide the language links shrink to 36px wide so the header fits at 320px (still above the WCAG 2.2 AA 24px minimum).

## QA status (this build)

- axe-core 4.10: 0 violations at 1440, 390 and 320px (reduced motion), and with the dropdown, menu and mobile menu open.
- No console errors; no horizontal scroll or clipped content at 320 / 390 / 768 / 1024 / 1100 / 1280 / 1440; works with JS disabled and with reduced motion.
- Budgets (esbuild minified): CSS 45.6 KB, JS 12.4 KB; `hero-fx.js` 3.0 KB.
- Lighthouse was not run in this environment.
