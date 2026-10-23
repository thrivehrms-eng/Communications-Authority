# UX review — homepage v2 to v9

A review of the first homepage build using the **UI/UX Pro Max** skill (v2.15.0, local design/UX database), followed by the changes made.
Rule IDs in backticks are the skill's own guideline names; items marked *(judgement)* had no database match after one retry and are general practice.

## What the skill recommended

| Query | Verified match | Used? |
|---|---|---|
| Design system for "government regulator public service citizen" | Style **Accessible & Ethical**: high contrast (7:1 target), 16px+ text, 3–4px focus rings, 44×44 targets, reduced motion; avoid ornate design and motion effects | **Yes**, as the quality bar |
| Product type "government portal / civic services" | Landing pattern **Service Directory + Search** | **Yes**: search-led hero + popular tasks |
| Landing "service directory search" | Hero (search focused) → categories with visual icons → featured content → trust → contact CTA | **Yes**: drives the new section order |
| Colour palette | Navy `#0F172A` / blue `#0369A1` | **No**: the brand lock requires CA's own palette. CA's navy/blue already meets the intent (white on primary 7.6:1, primary on white 7.6:1) |
| Typography | Atkinson Hyperlegible | **No**: the brand lock requires Inter + Maitree 700 |
| Pattern "Minimal single column, single CTA" | — | **No**: a regulator homepage serves several audiences; the directory pattern fits better |
| `--motion` GSAP presets | — | **No**: the brief forbids GSAP |

## Findings and changes

| # | Finding in v1 | Rule | Change in v2 |
|---|---|---|---|
| 1 | Hero offered no way to act except two buttons; most visitors arrive with a task | product → Service Directory + Search; `search-accessible`; `primary-action` | Search-led hero with a **visible label**, `required`, `enterkeyhint="search"`, plus a "Popular tasks" grid of six icon links (File a complaint, Check a phone (IMEI), Licensee register, Apply for a licence, Current tenders, Verify a CA officer) |
| 2 | On phones the first service card was ~3,000px down | `content-priority` | New order: Hero → Services → Stay safe online → News → Universal access → Projects → Who we are → Commitments → Affiliations → Get help. On phones the hero drops the redundant badge so search + four tasks fit in the first screen |
| 3 | Cursor follower hid the system pointer and trailed it with lag | `cursor-pointer`, `no-precision-required`; style: avoid motion effects | Removed (`cursor.js` deleted) |
| 4 | Several moving things per view (two animated canvases, marquee, reveals) | `excessive-motion` (1–2 per view) | Only the hero canvas animates; "Stay safe online" renders one still frame; marquee slowed from 45s to 70s; reveal stagger 60 → 40ms (`stagger-sequence`) |
| 5 | Commitments hid one sentence each behind an accordion | *(judgement)*: disclosure costs more than it saves for one-line content | Always-visible list with check icons |
| 6 | "Show more services" hid half the services on phones | `content-priority`, `truncation-strategy` | Compact icon cards on phones; all six visible; toggle removed |
| 7 | Cookie card (fixed, bottom-left) covered the hero search and focused controls, and overlapped the help button on phones | `focus-not-obscured`, `fixed-element-offset`; *(judgement)* for consent layout | In-flow banner above the header that never overlays content; two equal choices ("Only necessary", "Accept all"); "Customise" reveals categories and "Save selection" |
| 8 | Help button covered a task tile in the phone hero | `focus-not-obscured` | Hidden on phones while the hero tasks (which offer the same routes) are on screen |
| 9 | Dates/meta in `#737779` at 13px (4.5:1) | style target 7:1; `readable-font-size` | Meta at 14px in `--text-muted` (10.4:1) |
| 10 | Muted white at 80% on primary blue (5.5:1) | style target 7:1; `color-accessible-pairs` | Body copy on primary surfaces is full white (7.6:1); muted white on navy raised to 86% (≥ 9:1) |
| 11 | Active filter chip shown by colour alone | `color-not-only` | Check icon on the pressed chip |
| 12 | No press feedback; closes as slow as opens | `scale-feedback`, `exit-faster-than-enter`, `tap-delay` | `:active` scale on buttons, cards, chips and tasks; dropdowns close in 160ms (open 280ms); `touch-action: manipulation` |
| 13 | Hero sized with `vh`; ad-hoc z-index values | `viewport-units`, `z-index-management` | `svh` with `vh` fallback; layer tokens `--z-dots/fab/overlay/header/skip` |
| 14 | Fixed help button could cover focused elements near the bottom | `focus-not-obscured` | `scroll-padding-bottom: 96px` |
| 15 | Six tall project placeholders (3 rows at 4:3) dominated the page | `whitespace-balance`, `content-priority` | 3 columns from 1100px; 16:10 tiles on phones |
| 16 | Decorative backdrop blur on badges and tags | `blur-purpose` | Removed (header keeps blur for legibility over content) |
| 17 | External-link icon wrapped onto its own line in the footer | `long-token-wrapping` | Last word + icon kept together |

## Departures from the original brief (v1 → v2)

These change what `CA-Homepage-Build-Instructions.md` specified and should be confirmed:

- **§7 order** changed (see #2). The logo ticker moved from second to ninth.
- **§7.1 hero buttons** "Our services" / "File a complaint" replaced by the search form and popular tasks ("File a complaint" is the first task and stays in the header).
- **§7.4** accordion → always-visible list.
- **§7.5** mobile "Show more services" removed.
- **§6.8** cookie consent is an in-flow banner, not a fixed bottom-left card.
- **§7.7** feature panel's FX background is static.
- **§7.8/§9.4** cursor follower removed.

## Verification (v2)

- axe-core 4.10: 0 violations at 1440, 390 and 320 (reduced motion), and with the dropdown, menu and mobile menu open.
- No horizontal scroll and no content clipped by panels at 320 / 390 / 768 / 1024 / 1100 / 1280 / 1440; header fits from 1100 to 1920.
- Keyboard: Esc returns focus to the opener for dropdowns, search, menu, help and consent; menu traps Tab.
- Budgets (esbuild minified): CSS 45.6 KB, JS 12.4 KB; `hero-fx.js` 3.0 KB.
- Lighthouse not run in this environment.

## v3 — client feedback

| Feedback | Change |
|---|---|
| News titles too big; cards carry unnecessary info; add a character limit | Card titles 18px (featured 20–24px, was up to 32px). Cards show image, date and title only; category label, "[X] min read", excerpt and "Read more" removed (the whole card is the link). The featured card keeps a one-sentence summary. Limits via `data-max-chars`: titles 80 (featured 100), summary 140, cut at a word boundary with an ellipsis; the full title stays in the accessible name and as a tooltip (`truncation-strategy`). CSS line-clamp is the no-JS fallback |
| Hero overcrowded; make the image shorter than the viewport and put search and popular tasks below | Hero is now the full-width satellite-dish photo at 62% of the viewport height (max 600px) with only the headline and a one-line lead over a navy scrim. Badge, FX canvas and pause button removed from the hero. Search and the six popular tasks moved into a new "What do you need to do?" panel directly below |
| Find appropriate logos and images for affiliations and projects | Official logos for ITU, UPU, ATU, CTO, EACO and AFRALTI from each organisation's website, greyscale at rest and in colour on hover or focus, with the organisation's name as alt text. CA's own ca.go.ke portfolio photos for E-Justice, Education Broadband and Voice Infrastructure (the USF base station in West Pokot). The Ministry, PAPU and three project photos are still needed (see `content-todo.md`) |

Other v3 adjustments:
- The "Stay safe online" panel is the page's single animated area again (pausable), since the hero no longer animates (`excessive-motion` stays at one per page).
- On phones the help button stays hidden while the search and tasks panel is on screen, so it can't cover the Search button.
- **PAPU's link was removed**: `upap-papu.africa` now redirects to an unrelated shop site.

## v4 — client feedback

| Feedback | Change |
|---|---|
| Hero text unbalanced and unwelcoming | One persistent welcome line ("Welcome to the Communications Authority of Kenya", the page's H1, with the orange signature dot), then per slide: a two-line title (statement + highlighted phrase on its own line), a one-sentence text (≤ 44ch) and a single white button, all on one left edge with a fixed rhythm (16–22px gaps) |
| Hero should be an auto-playing slider | Four slides with CA imagery: Welcome (dish), Licensing online (lms.ca.go.ke, from CA's live banner), Complaints (tower at sunset), Universal access (USF base station). 7s auto-play with a progress bar on the active slide button; pause/play, previous/next, slide buttons and touch swipe. Per the skill's `auto-rotation-controls` rule: holds on hover, off-screen and hidden tabs, stops when keyboard focus enters (until Play), never auto-plays under reduced motion; inactive slides are hidden from tab order and screen readers; `aria-live` is off while playing, polite once paused. Crossfade only, with no slide-in motion. The "Stay safe online" panel is a still frame again, so the slider is the page's one moving element |
| "What do you need to do?" too big | Compact tint strip (about 170px tall on desktop, was about 400): heading + search on the left, six popular tasks as a two-column list of icon links on the right |
| News could be better | Skill match for news is "Minimalism & Swiss Style + Flat Design", led by a featured story. News is now a lead story (16:9 photo, date, title, one-line summary) beside a list of three rows (thumbnail, date, title) that share the lead's height; "All news" sits beside the heading. No card borders or shadows; hover underlines the title and gently zooms the image |

Also fixed: after dismissing the cookie banner on a first visit, focus now continues from the skip link (shown only to keyboard users) instead of being dropped on the page body.

## v5 — client feedback

| Feedback | Change |
|---|---|
| "Know before you buy" and "What you can expect from us" too big | Both use a tighter panel (`.ca-panel--tight`, 40–64px padding) and a smaller section heading. **Stay safe online**: heading + one-line intro side by side, then three clickable action cards (orange icon badge, title, one sentence, arrow) in a row; about 404px tall on desktop (was about 700). **Commitments**: the heading takes the first cell of a 3 × 2 grid and the five commitments fill the rest as icon cards; about 409px on desktop (was about 735). On phones: 584px and 751px (the stay-safe intro is hidden there because the three cards say the same thing) |
| Add icons and colour | Each card and commitment has its own icon in an orange badge (phone, child, alert; scale, shield-user, mast, shield-lock, badge-check); cards have a subtle glass surface that gets an orange border on hover |
| Orange under-used | Orange now marks **actions** and **signature details** (rules in README, "Using CA orange"): every "File a complaint" button and the help button are orange (white text 5.3:1); a short orange bar leads every eyebrow; orange icon badges on service cards; orange task, contact and FAQ icons; orange news dates; orange slider progress bar; orange top edge on the footer; orange hover underlines on text links; orange text selection. Contrast was checked for every pairing before use; orange never sits directly on the primary blue |

Also: the "Our commitments" eyebrow is white on the blue panel (cyan is only 3.8:1 there at 14px). Icon badges are one shared component (`.ca-icon-badge`). Decorative backdrop blurs were removed (`blur-purpose`), and the footer CSS was consolidated, keeping CSS within the 50 KB budget (49.99 KB minified).

## v6 — client feedback

| Feedback | Change |
|---|---|
| No dotted styling on the USF image | Dot-grid overlay removed |
| Footer social icons on one row | Contact column has a 256px minimum and the five 44px buttons sit on one row with 6px gaps (fits down to 320px) |
| Orange is overkill; use it sparingly, mostly on light backdrops | No orange on navy or blue panels: icon badges are glass chips with cyan icons; eyebrow bars are cyan/white on dark; slider progress is white; the footer's orange edge is gone; complaint buttons on dark backdrops (hero slide 3, closing panel) are white. Orange remains on white/light-blue surfaces only (rules in README) |
| Make the page come alive with micro-interactions and animations | See README → Motion. Skill guidance applied: transform/opacity only (`transform-performance`), hover only on hover-capable pointers, press feedback (`scale-feedback`), staggered entrances (`stagger-sequence`), final states set by classes rather than animation events (`cancellable-state-transitions`), and `prefers-reduced-motion` respected throughout |
| Every project needs an image | Three CC0 illustrative photos added from nappy.co (Wikimedia, Openverse, Unsplash, Pexels and Pixabay were blocked or rate-limited from the build environment) |
| Ignore budget limits | CSS is now 56.9 KB minified (was capped at 50 KB) |

Fix found while testing: the curtain reveal first clipped the observed element itself, which makes the browser treat it as off-screen so it never revealed. The clip now sits on the inner `<picture>`.

## v7 — client feedback

| Feedback | Change |
|---|---|
| Ticker: the AFRALTI and Ministry tiles touch | The list's end padding (which makes the seam between the two looping copies match the 16px gap) was being reset by the base `ul[role="list"]` rule. The selector is now specific enough to win; the seam measures 16px, the same as every other gap |
| News needs a "Read more" element | Each story (featured and the three rows) ends with an orange "Read more →" cue, on the white panel only. The arrow nudges forward on hover or keyboard focus. The cue is decorative: the title stays the story's single link and its click area still covers the whole card |
| Borrow Cloudflare's dropdown practices: smooth, easy to tell sections and titles apart, not overwhelming | The five dropdowns are now one **mega menu** (below) |

What was taken from Cloudflare's menu (studied from its page markup) and how it was adapted:

- **One container for every section.** A single white surface opens under the header and resizes smoothly between sections instead of five separate boxes popping in and out. Each section's content is clipped to the surface while it resizes, so nothing spills out mid-move, and slides in from the side the pointer came from, so moving left or right through the menu feels spatial.
- **A highlight that follows the pointer.** A soft light-blue pill glides behind the section button under the pointer (and under keyboard focus), so it is always clear which section a panel belongs to.
- **Clear hierarchy inside each panel.** A tinted intro column names the section, says in one line what it is for and links to its overview. Links sit in small titled groups ("Licensing", "Universal access", "Market & compliance"…). Each link has an icon, a name and a one-line description, so people can scan by shape or by words. Long tails (Law & policy, National projects, Portals) drop into a quieter band of plain inline links under a divider, rather than adding more columns.
- **Forgiving pointer behaviour.** Opening waits 140ms so a pointer passing over the bar doesn't flash panels (80ms when already open, so switching feels instant), and the menu stays open for 280ms after the pointer leaves the header so it can travel diagonally down into a panel.
- **Same links, same order.** All 73 links from the previous menu (Appendix A) are unchanged. Group names, the section summaries and the link descriptions are proposed copy (see content-todo).

Skill guidance applied (ui-ux-pro-max): `nav-hierarchy` (section → group → link with one-line descriptions), `progressive-disclosure` (long tails as quiet inline links), `continuity` and `shared-element-transition` (one surface that resizes, direction-aware slides), `cancellable-state-transitions` (fast switching retargets the resize instead of queueing), `hover-vs-tap` (every section also opens on click, tap and keyboard; hover only adds a short-delay shortcut), `exit-faster-than-enter` (sections fade out in 160ms, in over 240ms), `keyboard-nav` (disclosure pattern with arrow keys and Esc), and `reduced-motion` (all of it becomes instant).

Mobile is unchanged in behaviour: the burger menu's accordion is still built from the same markup, showing names only (no icons, summaries or descriptions) to keep it short.

## v8 — client feedback

| Feedback | Change |
|---|---|
| The hero is too tall on mobile and takes up most of the screen; make it responsive with the sections below in view | The hero is now sized to the screen (README → Hero sizing). On phones it is as tall as its content plus a strip of photo, capped at half the screen, with smaller type, a 46px button and tighter spacing. "What do you need to do?" and its search box now show without scrolling on every common phone |

Where the hero ends, as a share of the screen (header included):

| Screen | Before | After |
|---|---|---|
| 320×568 | 107% | 83% |
| 360×640 | 95% | 69% |
| 375×667 | 93% | 66% |
| 390×664 (iPhone 14 with Safari's toolbars) | — | 67% |
| 390×844 | 86% | 60% |
| 412×915 | 80% | 56% |
| 844×390 (phone on its side) | 146% | 95% (whole hero visible under the header) |
| 768×1024 | 71% | 71% |
| 1366×768 | 87% | 76% |
| 1440×900 | 80% | 76% |

Details:

- **Readable over every photo.** On phones the text now covers most of the hero, so a top-to-bottom fade would leave the welcome line on a light part of the photo (measured 4.0:1 on the clouds slide). The scrim now follows the text block itself and feathers out over 56px above it; the strip above stays clear photo. Measured against the brightest pixel behind each line: welcome line, title and text are ≥ 10.9:1 on all four slides on phones, ≥ 6.8:1 on landscape phones and ≥ 5.0:1 on tablets. On 768–1099px screens the side scrim now holds its depth further right, since the text runs further across.
- **Phones on their side.** Content-height hero; the slide controls sit beside the slides on a solid navy backing (inactive bars brighter) so they read over any photo; the previous/next arrows are dropped there, as the slide buttons and swipe remain.
- **Help button.** On phones and short landscape screens it now also waits while the hero is on screen, as it already did for the search strip, so it never sits on the slider controls.
- **Laptop-height screens** (≤ 820px tall, e.g. 1366×768) get less padding around the slides.

Skill guidance applied (ui-ux-pro-max): `mobile-first` and `viewport-units` (`svh` so mobile browser toolbars don't push content off screen), `content-priority` (the task strip, the page's main job, is now in the first view), `color-accessible-pairs` (contrast re-measured against the photos, not assumed), and `touch-target-size` (all controls stay 44px).

## v9 — client feedback

| Feedback | Change |
|---|---|
| "Who we are" should come after our services | Moved: Services → Who we are → Stay safe online → News. The page dots follow the new order |
| Add a section of YouTube videos below the news instead of sending visitors to YouTube, one row high | New **Videos** panel after News: one row of the channel's four newest videos (date, title, duration on each still). They play in a player dialog on the page; the "Watch our videos on YouTube" link under News is gone, and a smaller channel link sits in the panel's heading for people who want more. On screens under 1000px the row scrolls sideways with the next video peeking in, so it stays one row instead of stacking |

How the player works:

- **Fast and private by default.** The stills are served from the site; nothing loads from YouTube until a video is opened, and the player comes from `youtube-nocookie.com`.
- **Respects the cookie settings.** The cookie banner already offers an "Embedded media" choice. Without it, the dialog first says that playing loads YouTube, with a one-off **Play video** and an **Always play YouTube videos on this site** option (which switches on only that setting). With it, the video starts straight away.
- **Keyboard and screen readers.** Native modal `<dialog>`: focus moves in, Tab stays in, Esc or Close shuts it, the video stops and focus returns to the card. After Play, focus stays on Close, because inside YouTube's frame Esc is swallowed. Without JavaScript the cards are ordinary links to YouTube.

Heights: the panel is 492px at 1440px (heading plus one row of 16:9 stills), 408px at 1024px and 482px on a 390px phone.

Skill guidance applied (ui-ux-pro-max): `content-priority` (secondary content folded: the videos sit below News and take one row on every screen), `horizontal-scroll` (the page itself never scrolls sideways, checked at 320–1440px; only the video row does, inside its panel), `modal-motion` (the player rises in from below over a dimmed, blurred backdrop), `focus-management` (focus moves in, is held, and returns to the opener), and `lazy-loading` (`videos.js` is imported only when the section exists, and the player itself only when someone presses play).
