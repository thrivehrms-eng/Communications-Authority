# UX review — homepage v2

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
