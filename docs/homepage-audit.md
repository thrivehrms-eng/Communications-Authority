# Communications Authority of Kenya — Homepage Audit & Build Brief

**Site audited:** https://ca.programmer.co.ke/ (staging build of the CA website)
**Audit date:** 22 October 2026
**Scope:** Homepage only. Inner pages, CMS integration and visual concepts will follow in later briefs.
**Build target:** Static homepage in semantic HTML, modern CSS and vanilla JavaScript (no frameworks, no jQuery).

How to use this document: Part A records what exists today and what is wrong with it. Part B is the instruction set for Claude Code. Paste Part B (plus the appendices) into Claude Code, or save this file in the project root as `docs/homepage-brief.md` and tell Claude Code to follow it.


> **Background only.** This audit records the state of the current site (October 2026). Its Part B was an earlier build proposal and is **superseded** by [`homepage-build-instructions.md`](homepage-build-instructions.md). Follow that file when building.

---

# PART A — HOMEPAGE AUDIT

## A1. Snapshot

| Item | Finding |
|---|---|
| Platform | WordPress 7.1, custom theme `communications-authority-kenya`, Elementor 4.2.4, TranslatePress (English / Swahili) |
| Page length | 4,422 px on desktop (1440 wide); **8,932 px on mobile** (390 wide), about 10.5 screens |
| Requests / weight | 47 requests, ~0.9 MB transferred on first load |
| Server response (TTFB) | ~1.4 s (lab measurement), so page caching is probably off |
| Largest Contentful Paint | ~2.5 s (lab); the LCP element is the hero slide's CSS background image |
| Layout shift (CLS) | 0.007 (good) |
| Fonts | Inter (body) and Maitree 700 (headings) are declared, **but both font files return 403 Forbidden**, so the site renders in fallback fonts (Georgia/Times-style headings) |

## A2. Current section inventory (top to bottom)

1. **Skip link**: "Skip to main content".
2. **Utility bar** (blue): Innovations · Complaints · Contact Us · Careers · Swahili (flag icon).
3. **Main header**: logo; primary nav: Home · About CA · Licensing & Industry · Consumer Protection · Procurement · Info Hub (each opens a tabbed mega menu); search icon button.
4. **Hero carousel**: 2 auto-rotating slides (7 s each), with previous/next arrows and dots.
   - Slide 1: "Building sustainable digital society through responsive regulation" / "Regulating Kenya's communications sector in the public interest." / CTA "Get In Touch" → Contact Us.
   - Slide 2: "Connecting every county through Universal Access" / "Extending communications services to underserved areas." / CTA "Learn more" → About the Authority.
5. **About The Authority** (dark navy band): one 70-word paragraph on CA's mandate under KICA (CAP 411A); "Who We Are" button; photo of CA Centre that swaps to a second photo on hover.
6. **Quick Links**: an intro paragraph, then 6 image cards: Licensing Procedures, Guidelines, Market Structure, Cybersecurity, Type Approval, Our Portals.
7. **Need Help?**: intro "Choose a service below. Your submission goes directly to the Authority and is treated in confidence."; a decorative fibre-optic image strip; 4 action cards: File a Complaint, Make Enquiries, Report Corruption, Consumer Feedback.
8. **News Update**: 4 latest posts (image, "CA NEWS" label, date, title) plus "View More".
9. **YouTube Feed**: 4 video cards using a click-to-load YouTube facade, plus "View More" → youtube.com/@CAoKenya.
10. **Footer**: white logo; contact block (address, 3 phone numbers, email); "Stay Connected" social icons; four link columns (Popular Services, Resources, The Authority, Affiliations); legal bar (Terms & Conditions, Privacy Policy, copyright); "Back to top" button.

## A3. What already works (keep it in the redesign)

- Skip link, landmark roles, `aria-label`s on each nav, tab/tabpanel roles in the mega menu, and screen-reader text on icon buttons.
- `prefers-reduced-motion` support; the carousel pauses on hover and focus.
- YouTube "facade" pattern: a thumbnail first, then a `youtube-nocookie.com` iframe only after a click. Good for privacy and speed.
- WebP images with `width`/`height`, `loading="lazy"` and `srcset`; descriptive alt text on news images.
- A coherent colour token set (see Appendix C); the brand blues are strong.
- A sensible footer information architecture, and a useful "Need Help?" concept.
- English/Swahili `hreflang` alternates are present.

## A4. Issues, by priority

### Critical (broken or embarrassing on a live government site)

| # | Issue | Evidence |
|---|---|---|
| C1 | **Brand fonts never load.** Both `.woff2` files return 403, so headings render in a Times-like fallback and the brand typography is lost. | `assets/fonts/inter-latin-wght-normal.woff2` and `maitree-latin-700-normal.woff2` → 403 |
| C2 | **Broken image in the language switcher.** The Kenyan flag SVG returns 403 and shows a broken-image icon next to "Swahili" (desktop and mobile). | `assets/images/flags/ke.svg` → 403 |
| C3 | **"Who We Are" button points to a developer's local machine.** | `href="http://localhost/Projects/CA-website/about-the-authority/"` |
| C4 | **Social links are placeholders.** | All five go to `https://example.com/LinkedIn`, `/X`, `/Facebook`, … |
| C5 | **Terms & Conditions and Privacy Policy link back to the homepage.** | Both `href="https://ca.programmer.co.ke/"` |
| C6 | **Two `<h1>` elements** (one per carousel slide), so the page has no single main heading. | 2 × `h1.cak-hero__title` |

### High

| # | Issue | Why it matters |
|---|---|---|
| H1 | **The auto-rotating hero carousel has no pause control.** | Fails WCAG 2.2.2 (Pause, Stop, Hide) for content that moves automatically for more than 5 s. Most visitors never see slide 2, and its CTA ("Learn more" → About) doesn't match its message (Universal Access). |
| H2 | **The hero image is a CSS `background-image`.** | The browser can't discover or preload the LCP image, it gets no responsive `srcset`, and it has no alt text. |
| H3 | **The page isn't built around tasks.** | Citizens and licensees come to do things (file a complaint, check a phone's IMEI, apply for a licence, check the licensee register, find tenders, verify a CA officer). Those tasks are scattered across Quick Links, Need Help, the utility bar and the footer, and there is nothing task-related above the fold. Search is only a small icon. |
| H4 | **Missing SEO and sharing metadata.** | No meta description, no Open Graph/Twitter tags, no structured data (`GovernmentOrganization`, `WebSite` + `SearchAction`). The `<title>` is just the organisation name. |
| H5 | **Heavy, unnecessary JavaScript and CSS.** | jQuery (285 KB, unminified), jQuery Migrate, jQuery UI Core, Elementor frontend JS (97 KB) and Elementor CSS (64 KB) all load, though the homepage is rendered by the custom theme. The theme CSS is 141 KB unminified. |
| H6 | **Navigation quality problems.** | Top-level items use `href="#"`, so there are no landing pages. The mega menu has 70+ links with duplicates: Broadcasting, Telecommunication and Postal & Courier all go to `/market-structure/`; Universal Access and the Universal Service Advisory Council each appear twice; Contact Us appears in 3 places. Six mega-menu tabs hold only one link each (Careers, Access to Information, IMEI Checker, Regulatory Sandbox, Telecommunications Services, Verification). |

### Medium

| # | Issue |
|---|---|
| M1 | **Inconsistent containers.** Left edges differ by section (hero text ~108 px in, About ~24 px, Quick Links ~40 px), so the page looks unaligned. |
| M2 | **Large empty vertical gaps** between sections, and an uneven 2 + 4 card grid in Quick Links. |
| M3 | **The "Need Help?" image is a thin decorative strip** that adds no meaning. The 4 action cards repeat links found elsewhere. |
| M4 | **An external-link icon appears on internal links** (Quick Links, Need Help cards), which misleads users. |
| M5 | **Truncated card text** (ellipses on Guidelines, Type Approval, Our Portals) hides information. The Quick Links intro is boilerplate that repeats the About text. |
| M6 | **News cards are all labelled "CA NEWS"**, which tells users nothing. Headlines are small blue serif text. There is no featured story. |
| M7 | **"YouTube Feed" names the platform, not the content.** The videos are hard-coded and partly dated (2018–2023 achievements, ICT Week 2023). |
| M8 | **Mobile header and menu.** The burger sits mid-header rather than at the right edge. The open drawer doesn't cover the viewport, so page content shows beneath it. On mobile, Quick Links becomes 6 full-width image cards. |
| M9 | **No regulator "pulse" content.** There are no public notices, open consultations (with closing dates), tenders or key sector statistics on the homepage, though these are core to a regulator's audience. |
| M10 | **Mega-menu link text is #737779 at 14 px** (about 4.5:1, right at the AA limit). The "About" images have empty alt text although they show CA Centre. |

### Low

| # | Issue |
|---|---|
| L1 | Version leaks: `<meta name="generator">` exposes WordPress 7.1 and Elementor 4.2.4; `xmlrpc.php` is advertised (security hygiene). |
| L2 | The copyright year is hard-coded, and the email address relies on Cloudflare's JavaScript obfuscation. |
| L3 | Grammar: "Building sustainable digital society" should read "Building **a** sustainable digital society". |

---

# PART B — BUILD INSTRUCTIONS FOR CLAUDE CODE (HOMEPAGE ONLY)

> **Copy everything from here to the end of the document into Claude Code.**

## B1. Role, goal and constraints

You are a senior front-end engineer building the **redesigned homepage of the Communications Authority of Kenya (CA)**, Kenya's ICT sector regulator.

**Goal:** a fast, accessible, task-first homepage that helps citizens, licensees, industry and partners complete their most common tasks in one or two clicks, while presenting CA as a credible, modern regulator.

**Hard constraints**
- Plain **HTML5, CSS and vanilla JavaScript (ES2020+ modules)**. No frameworks, no jQuery, no CSS frameworks, no build step required. The page must work when `index.html` is opened from a simple static server.
- **No third-party runtime dependencies**, except the YouTube iframe, which loads only after a user clicks.
- **WCAG 2.2 AA** compliance is mandatory.
- **British English** throughout ("licence", "organisation", "programme"), matching CA's usage.
- **Do not invent facts.** Statistics, notices, tender titles, deadlines and URLs not given in this brief must be clearly marked placeholders (see B9).
- Write markup in self-contained components (header, hero, cards, footer) so it can later be ported into WordPress theme template parts without restructuring.
- The scope is **the homepage only**. Further pages and design concepts will come in later briefs; do not build them.

**Working method:** build in the phases listed in B10. After each phase, stop and give a short summary of what was built and anything you need from me.

## B2. File structure

```
/
├── index.html
├── assets/
│   ├── css/
│   │   ├── tokens.css        # design tokens (custom properties) only
│   │   ├── base.css          # reset, typography, global elements, utilities
│   │   ├── layout.css        # container, grid, section spacing
│   │   ├── components.css    # buttons, cards, tabs, badges, forms, nav, footer
│   │   └── home.css          # homepage-specific section styles
│   ├── js/
│   │   ├── main.js           # entry: imports and initialises modules
│   │   ├── nav.js            # mega menu + mobile drawer
│   │   ├── search.js         # search panel
│   │   ├── tabs.js           # accessible tabs (notices panel)
│   │   ├── video.js          # YouTube facade
│   │   └── ui.js             # sticky header, back-to-top, alert dismiss, footer year
│   ├── fonts/                # self-hosted WOFF2 (see B3)
│   ├── img/                  # optimised images (AVIF/WebP + JPEG fallback)
│   └── icons/sprite.svg      # inline SVG symbol sprite (Lucide-style 24px, 1.75 stroke)
├── docs/
│   └── content-todo.md       # every placeholder that needs real content (generated by you)
└── README.md                 # how to run locally, structure, conventions
```

CSS loads in the order listed with `<link rel="stylesheet">`. JS loads as `<script type="module" src="assets/js/main.js">`. Naming convention: BEM with a `ca-` prefix (e.g. `ca-card`, `ca-card__title`, `ca-card--task`).

## B3. Design system

### Colour tokens (keep the existing brand palette; contrast rules are mandatory)

```css
:root {
  /* Brand */
  --ca-blue-50:  #F2F7FF;
  --ca-blue-500: #1D51A3;   /* primary: links, buttons, header bar */
  --ca-blue-600: #0B4191;   /* hover */
  --ca-blue-700: #00327C;
  --ca-blue-900: #04214F;   /* dark bands, footer base */
  --ca-orange-500: #EC5B13; /* accent: decorative only, NEVER for text on white (3.5:1) */
  --ca-orange-600: #BD4400; /* accent text / focus ring on light backgrounds (5.2:1) */
  --ca-cyan-500: #38C3FF;   /* highlights on dark backgrounds only */
  --ca-cyan-600: #008CBC;
  /* Neutrals */
  --ca-neutral-0:   #FFFFFF;
  --ca-neutral-50:  #FAFAFA;
  --ca-neutral-200: #E4E5E6;
  --ca-neutral-500: #6B6F72; /* darkened from #7D8184 for AA on white */
  --ca-neutral-700: #3D4043;
  --ca-neutral-900: #131415;
  /* Status */
  --ca-success: #1E8A5C; --ca-danger: #C81E27; --ca-warning: #B07800; --ca-info: #2563EB;
  /* Semantic */
  --ca-bg: var(--ca-neutral-50);
  --ca-surface: var(--ca-neutral-0);
  --ca-text: var(--ca-neutral-900);
  --ca-text-muted: var(--ca-neutral-700);
  --ca-border: var(--ca-neutral-200);
  --ca-link: var(--ca-blue-500);
  --ca-focus: var(--ca-orange-600);
}
```

Every text/background pair must reach **4.5:1** (body text) or **3:1** (text ≥ 24 px, or ≥ 18.66 px bold, and UI components). Check every pair you use.

### Typography

- **Inter** (variable, 400–700) for body and UI; **Maitree 700** for display headings (h1–h2 and section titles only). Keep the existing brand pairing.
- Self-host both as WOFF2 in `assets/fonts/` (Latin subset, from Google Fonts or Fontsource), with `font-display: swap`. Preload only Inter and Maitree 700. **Verify the files actually load (HTTP 200).** The current site's fonts return 403.
- Fallback stacks: `Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif` and `Maitree, Georgia, serif`. Use `size-adjust` / `ascent-override` on fallback `@font-face` rules to minimise layout shift.
- Fluid type scale (use `clamp()`):

| Token | Use | Mobile → Desktop |
|---|---|---|
| `--fs-display` | Hero h1 | 2.0rem → 3.5rem, line-height 1.1 |
| `--fs-h2` | Section titles | 1.625rem → 2.25rem, line-height 1.2 |
| `--fs-h3` | Card titles | 1.125rem → 1.25rem, line-height 1.3 |
| `--fs-body-lg` | Lead paragraphs | 1.0625rem → 1.25rem, line-height 1.6 |
| `--fs-body` | Body | 1rem (never smaller), line-height 1.6 |
| `--fs-small` | Meta, labels | 0.875rem, line-height 1.4 |

Maximum line length for body copy is 70ch.

### Spacing, layout, shape and motion

- Spacing scale (4 px base): `--sp-1: 4px` … `--sp-2: 8px`, `--sp-3: 12px`, `--sp-4: 16px`, `--sp-6: 24px`, `--sp-8: 32px`, `--sp-12: 48px`, `--sp-16: 64px`, `--sp-24: 96px`.
- Section vertical padding: `clamp(48px, 8vw, 96px)`. Avoid the big dead gaps the current site has.
- **One container for every section:** `max-width: 1280px; margin-inline: auto; padding-inline: clamp(16px, 4vw, 32px)`. Every section's content must share the same left edge (this fixes audit M1).
- Breakpoints (mobile-first, `min-width`): 640, 768, 1024, 1280.
- Radii: `--radius-sm: 6px` (inputs, badges), `--radius-md: 12px` (cards), `--radius-pill: 999px`.
- Shadows: `--shadow-sm: 0 1px 2px rgb(4 33 79 / .06)`, `--shadow-md: 0 8px 24px rgb(4 33 79 / .10)`; cards lift with `--shadow-md` on hover/focus.
- Motion: 150–250 ms, `cubic-bezier(.2,.8,.2,1)`. Under `prefers-reduced-motion: reduce`, remove all transforms and transitions except opacity.
- Focus style: `outline: 3px solid var(--ca-focus); outline-offset: 3px;` on every interactive element, using `:focus-visible`. Never remove outlines.

### Core components to build

Buttons (primary, secondary/outline, ghost, on-dark variants; min height 44 px), text link with arrow, task tile, content card (image + meta + title), news card (featured and compact), video card (facade), badge (category, "Closes in X days", "New"), tabs, list item with date, icon, alert banner, and section header (title + optional "View all" link).

**External links** get a visible external-link icon plus screen-reader text "(opens external site)", and that applies to external links only. Internal links never get this icon (audit M4).

## B4. Page structure: build in this order

### 0. Global

- `<html lang="en">`, a skip link to `#main`, then landmarks `<header>`, `<nav>`, `<main id="main">` and `<footer>`.
- **Exactly one `<h1>`** on the page (the hero). A logical h2 → h3 hierarchy follows.

### 1. Notice banner (optional, dismissible)

- A slim bar above the header for one urgent item, e.g. "Public consultation open: [title], closes [date]. [Read and respond →]".
- Has a close button that remembers dismissal in `localStorage` (wrap the access in try/catch). The bar is hidden entirely when there's no active notice (controlled by a `hidden` attribute).
- Use placeholder content (see B9).

### 2. Header

**Utility bar** (desktop ≥ 1024 px; on mobile its links move inside the drawer):
- Left: "Official website of the Communications Authority of Kenya" (small, muted, on dark blue).
- Right: Complaints · Careers · Tenders · Contact Us · a language switch.
- Make the language switch a **text** toggle, `EN | Kiswahili`. Mark the current language with `aria-current="true"`, and give the Kiswahili link `hreflang="sw"` and `lang="sw"`, pointing to `/sw/`. **Do not use a flag image** (audit C2).

**Main bar:**
- Logo (SVG, links to home, alt "Communications Authority of Kenya – Home").
- Primary nav: **About CA · Licensing & Industry · Consumer Protection · Procurement · Info Hub**. "Home" is dropped, since the logo does that job.
- Search button (icon + visible "Search" label on desktop).
- On mobile: logo left, then search and menu buttons **right-aligned**.

**Mega menu (desktop):**
- Each top-level item is a `<button aria-expanded aria-controls>` that opens a full-width panel. Opening is **click-based**; hover opens after a 150 ms delay but never closes on accidental mouse-out under 300 ms.
- Panel layout: a left column with a short description and an "Overview →" link to the section landing page, then 2–3 columns of grouped links.
- Use the cleaned link map in **Appendix A** (duplicates removed; single-link groups merged).
- Keyboard: Esc closes and returns focus to the trigger; Tab moves through links naturally; clicking outside closes.
- Only one panel open at a time.

**Mobile drawer (< 1024 px):**
- A full-height off-canvas panel that **covers the viewport** (fixes audit M8).
- Each top-level item is an accordion (`<button aria-expanded>`), and the utility links and language toggle sit at the bottom.
- Locks body scroll and traps focus while open. Esc closes it and returns focus to the menu button.

**Sticky header:** sticks on scroll, condenses to the main bar only (the utility bar scrolls away) and gains `--shadow-sm`. Do not hide it on scroll down.

### 3. Hero (static — no carousel)

- Two columns on desktop (text 6/12, image 6/12); stacked on mobile with the image below the text, or omitted under 640 px if it pushes the tasks too far down.
- **Eyebrow:** "Regulating Kenya's communications sector".
- **H1:** "Building a sustainable digital society through responsive regulation".
- **Lead:** "We license and regulate telecommunications, broadcasting, postal and courier services, manage Kenya's spectrum and numbering resources, and protect the people who use them."
- **Search** is the primary action. Build a large search form (`role="search"`, a visible label "What can we help you find?", placeholder "e.g. licence fees, IMEI check, tenders"). It submits `GET` to `/` with `name="s"` (WordPress-compatible).
- **Popular searches** (chips/links, Appendix B): Apply for a licence · IMEI checker · Licensee register · Tenders · Type approval.
- **Secondary CTAs:** "File a complaint" (primary button) and "About the Authority" (outline button).
- **Image:** a real `<img>` (not a CSS background) with `srcset`/`sizes`, `fetchpriority="high"`, no lazy loading, `width`/`height` set, and meaningful alt text (e.g. "Satellite earth station dish at dusk"). Use the existing hero image (Appendix D) until new photography arrives.
- The Universal Access message from the old slide 2 moves to section 6 rather than a carousel slide.

### 4. Top tasks: "What would you like to do?"

- 8 task tiles in a grid: 4 columns on desktop, 2 on tablet, 2 compact columns on mobile. Each tile has an icon, a title, a one-line description and a full-tile link (one `<a>` wrapping or using the stretched-link pattern; never nested links).

| Task | Description | Link |
|---|---|---|
| File a complaint | Unresolved issue with a telco, broadcaster or courier | `/consumer-complaint/` |
| Check a phone's IMEI | Verify a device before you buy | `/imei-checker/` |
| Apply for a licence | Procedures, forms and fees | `/licensing-procedures/` |
| Search licensee register | Confirm a provider is licensed | `/licensee-register/` |
| Type-approved equipment | Check a device is approved for use in Kenya | `/type-approval/` |
| Tenders & procurement | Open tenders and awarded contracts | `/tenders/` |
| Report a cyber incident | National KE-CIRT/CC (external) | `https://ke-cirt.go.ke/report-an-incident/` |
| Verify a CA officer | Confirm staff identity before engaging | `/staff-verification-portal/` |

- This section **replaces** both the old "Quick Links" and "Need Help?" sections (audit H3, M3).
- The remaining old quick links (Guidelines, Market Structure, Our Portals) move into section 5.

### 5. Find services by audience

- Three cards, side by side on desktop and stacked on mobile. Each has a heading, one sentence and 4–5 links.

  - **For the public:** File a complaint · Consumer education & outreach · Child online protection · Quality of service · IMEI checker.
  - **For industry & licensees:** Licensing overview · Statutes & regulations · Guidelines · Market structure · Our online portals.
  - **For partners & suppliers:** Tenders · Supplier registration portal · Awarded contracts · Public consultations · Careers.

### 6. About CA + mandate + key figures (dark navy band, `--ca-blue-900`)

- Left: an h2 "About the Authority" and a rewritten short intro (2 sentences max): "The Communications Authority of Kenya is the regulator of Kenya's ICT sector, established under the Kenya Information and Communications Act (CAP 411A). We license operators, manage spectrum and numbering resources, promote universal access and protect consumers." Link: "Who we are →" `/about-the-authority/` (**the correct URL**, audit C3).
- Right: the CA Centre photo with real alt text ("CA Centre headquarters on Waiyaki Way, Nairobi"). No hover image swap.
- Below: a **mandate strip** of 6 icon items: Telecommunications · Broadcasting · Postal & courier · Spectrum & numbering · Cybersecurity (KE-CIRT/CC) · Consumer protection.
- **Key figures row** (4 stats, large Maitree numerals) with labels such as "Mobile subscriptions", "Internet subscriptions", "Counties reached by Universal Service Fund projects" and "Licensed operators", plus a source line, "Source: CA Sector Statistics Report, [quarter/year]". **All numbers must be placeholders** (`data-placeholder`); do not invent data.
- Include a "Universal Access" highlight line linking to `/universal-access/` (the content from old hero slide 2).

### 7. Notices & opportunities (tabs)

- h2 "Notices & opportunities". An accessible tabs component with three tabs: **Public notices · Open consultations · Tenders**.
- Each panel holds 3–4 list items: a date (`<time datetime>`), a title link, and a badge where relevant ("Closes 14 Nov 2026" / "Closing soon" when ≤ 7 days, calculated in JS from a `data-closes` attribute).
- Each panel ends with a "View all" link (`/public-notices/`, `/open-consultations/`, `/tenders/`).
- Tabs follow the WAI-ARIA tabs pattern: arrow keys move between tabs, Home/End jump, and selection is automatic.
- Without JS, all three panels render stacked with their headings visible.
- All items are placeholders (B9).

### 8. News & media

- h2 "Latest news" plus a "View all news →" link (`/news/`).
- Layout: 1 **featured** story (large image, category, date, title, 2-line excerpt) and 3 **compact** stories (thumbnail, category, date, title). On mobile, the featured story comes first and the compact ones follow as a list.
- Categories must be meaningful (Press release, News, Speech, Event), not a generic "CA NEWS".
- Use the 4 real stories in Appendix B (titles, dates, images, alt text, URLs).
- Titles use Inter 600 (not small blue serif) for legibility.

### 9. Watch: videos

- h2 "Watch" (not "YouTube Feed"), with "Visit our YouTube channel →" (external) → `https://www.youtube.com/@CAoKenya`.
- 1 large featured video plus 3 smaller ones, using the 4 IDs in Appendix B.
- **Facade pattern:** show the thumbnail (local image, or `https://i.ytimg.com/vi/{ID}/hqdefault.jpg`) with a play button. The button reads "Play video: {title}". On click, replace it with an iframe from `https://www.youtube-nocookie.com/embed/{ID}?autoplay=1&rel=0` with a `title` attribute; focus moves to the iframe.
- Without JS, the facade is a plain link to the YouTube watch URL.

### 10. Stay safe online (campaign band, optional)

- A full-width band with an image, h2 "Protecting children online", one sentence, and CTAs "Child online protection" (`/child-online-protection/`) and "Consumer education" (`/consumer-education-and-outreach/`).
- Build it as a reusable "campaign" component so content can rotate later.

### 11. Footer

- **Top row:** white logo with the tagline "Opening your world"; a contact block (CA Centre, Waiyaki Way, Westlands · P.O. Box 14448 – 00800 Nairobi; phones as `tel:` links: +254 20 4242000, +254 703 042 000, +254 730 172 000; email `info@ca.go.ke` as a plain `mailto:` link); and "Stay connected" social icon links with accessible names.
- **Link columns:** Popular services · Resources · The Authority · Affiliations (content in Appendix B). On mobile, the columns become accordions (`<details>`/`<summary>`).
- **Legal bar:** Terms & Conditions · Privacy Policy · Accessibility statement · Sitemap, each to its own URL (placeholders where pages don't exist yet; audit C5). The copyright line reads "© [year] Communications Authority of Kenya. All rights reserved.", with the year set by JS and a static fallback.
- **Social URLs:** only YouTube is confirmed. Every other social link is a placeholder flagged in `content-todo.md` (audit C4); do not ship `example.com`.
- A "Back to top" button appears after scrolling 2 viewport heights.

## B5. JavaScript requirements

- One ES module per concern (B2), initialised from `main.js` only when its elements exist on the page.
- **Progressive enhancement.** Without JS, the nav links still work: each top-level item also has a real overview URL, and the mobile menu falls back to a `<details>`-based list or the footer links. Tabs show all panels, and videos link to YouTube.
- No layout shift from JS initialisation.
- Event delegation where sensible, `{ passive: true }` scroll listeners, and `IntersectionObserver` instead of scroll maths for the sticky header and back-to-top.
- No `console` errors. Wrap all `localStorage` access in try/catch.
- Total hand-written JS: **≤ 15 KB minified**.

## B6. Accessibility (WCAG 2.2 AA) checklist

- One h1 and a logical heading order; landmarks are labelled.
- All interactive targets are **≥ 44 × 44 px** (WCAG 2.5.8 needs at least 24 px; we use 44).
- Visible `:focus-visible` styles everywhere; focus is never obscured by the sticky header (`scroll-padding-top` equals the header height).
- Menus, drawer, search and tabs are fully keyboard-operable; Esc closes overlays and focus returns to the trigger.
- **No auto-playing or auto-advancing content.**
- Images: meaningful alt text, or `alt=""` with `aria-hidden` on decorative SVGs.
- Icon-only buttons have accessible names. External links announce "(opens external site)" only if they open in a new tab. Prefer the same tab and simply mark them as external.
- Colour is never the only signal (e.g. "Closing soon" has text, not just colour).
- Text resizes to 200% without loss, and the layout reflows at 320 px wide with no horizontal scroll.
- Respect `prefers-reduced-motion`. Add a `forced-colors` mode check (borders remain visible).
- Swahili content (link labels) is marked with `lang="sw"`.

## B7. Performance budget

| Metric | Budget |
|---|---|
| LCP (4G mid-range mobile) | < 2.0 s |
| CLS | < 0.05 |
| INP | < 200 ms |
| CSS (total, minified) | ≤ 45 KB |
| JS (total, minified) | ≤ 15 KB |
| Initial page weight (excluding lazy images) | ≤ 500 KB |
| Fonts | ≤ 2 preloaded files, WOFF2, subset |

- Hero image: `<img>` with `srcset` (640/960/1280/1600 widths), AVIF or WebP, `fetchpriority="high"`, and a matching `<link rel="preload" as="image" imagesrcset>`.
- All below-the-fold images use `loading="lazy" decoding="async"` with explicit `width`/`height` or `aspect-ratio`.
- No icon fonts; use an SVG sprite.
- No jQuery, Elementor or other unused assets (audit H5).

## B8. SEO & metadata (in `<head>`)

- `<title>`: "Communications Authority of Kenya | ICT Sector Regulator".
- `<meta name="description">`: "The Communications Authority of Kenya regulates telecommunications, broadcasting, postal and courier services. File a complaint, check an IMEI, apply for a licence or find tenders."
- A canonical link, plus `hreflang` alternates for `en` and `sw` and an `x-default`.
- Open Graph and Twitter Card tags (`og:title`, `og:description`, `og:image` at 1200×630 as a placeholder, `og:type=website`, `og:locale=en_KE`, `og:locale:alternate=sw_KE`).
- JSON-LD: `GovernmentOrganization` (name, alternateName "CA", url, logo, address, telephone, email, sameAs [social URLs once confirmed]) and `WebSite` with a `SearchAction` (`/?s={search_term_string}`).
- Favicon set (32, 192, 180 apple-touch, SVG) and `theme-color` `#1D51A3`.
- No `generator` meta tag (audit L1).

## B9. Content and placeholder rules

- Use the real copy, links and media from **Appendix B** wherever they exist.
- Anything not supplied (statistics, notices, consultation and tender items, social URLs, new photography, the Accessibility statement URL) is a **visible placeholder**:
  - Text in square brackets, e.g. `[Tender title — to be supplied]`.
  - The element carries `data-placeholder="true"`.
  - Placeholders are styled with a subtle dashed outline **only when `<html>` has the class `show-placeholders`**. Add a `?placeholders` URL toggle for review.
- Generate `docs/content-todo.md` listing every placeholder: section, what's needed, and a suggested source (e.g. "Sector Statistics Report Q2 2026/27").
- Do not use lorem ipsum. Write realistic but clearly bracketed placeholder text.
- Use relative internal links (e.g. `/consumer-complaint/`), so the page works on any domain.

## B10. Build phases (stop and report after each)

1. **Scaffold & tokens:** file structure, `tokens.css`, `base.css`, `layout.css`, self-hosted fonts (verify they load), the SVG sprite, README.
2. **Header & navigation:** utility bar, main bar, mega menu, mobile drawer, search panel, sticky behaviour, language toggle.
3. **Hero & top tasks:** sections 3–4.
4. **Content sections:** sections 5–10.
5. **Footer & global UI:** section 11, back-to-top, notice banner.
6. **Head metadata & SEO:** section B8.
7. **QA pass:**
   - Run Lighthouse (mobile) and report scores, and an axe-core scan with zero violations.
   - Keyboard-only walkthrough; screen widths 320 / 390 / 768 / 1024 / 1440.
   - Disable JS and confirm the page is still usable.
   - Check every contrast pair; produce `docs/content-todo.md`.
   - Fix everything found, then report what was fixed.

## B11. Definition of done

- [ ] Matches the section order and content in B4; exactly one h1.
- [ ] No carousel and no auto-advancing content.
- [ ] Fonts and all images load with HTTP 200; no broken images and no console errors.
- [ ] No `localhost`, `example.com` or `href="#"` links (placeholders use real paths or are flagged).
- [ ] Lighthouse mobile scores: Performance ≥ 95, Accessibility 100, Best Practices ≥ 95, SEO 100.
- [ ] axe-core: 0 violations. Keyboard-only use works for all features.
- [ ] Reflows at 320 px with no horizontal scroll; usable at 200% zoom.
- [ ] Performance budgets in B7 are met.
- [ ] Works without JavaScript (degraded but usable).
- [ ] `README.md` and `docs/content-todo.md` are complete.

---

# APPENDICES

## Appendix A — Cleaned navigation map (duplicates removed)

**About CA** (overview: `/about-the-authority/`)
- The Authority: About the Authority `/about-the-authority/` · Board of Directors `/board-of-directors/` · Management Team `/management-team/` · Organisation Structure `/organisation-structure/` · Finance and Accounts `/finance-and-accounts/` · Universal Service Advisory Council `/universal-service-advisory-council/`
- Policies & commitments: Vision, Mission & Core Values `/vision-mission/` · Strategic Plan `/strategic-plan/` · Service Charter `/service-charter/` · Whistleblowing Policy `/whistle-blowing-policy/` · Quality & Information Security Policy `/quality-and-information-security-policy-statement/`
- Work with us: Careers `/careers/` · Access to Information `/access-to-information/` · Contact Us `/contact-us/`

**Licensing & Industry** (overview: `/licensing-overview/`)
- Licensing: Licensing Overview `/licensing-overview/` · Licensing Procedures `/licensing-procedures/` · Licensee Register `/licensee-register/` · Type Approval `/type-approval/` · Telecommunications Services `/telecommunications-services/`
- Law & policy: Statutes & Regulations `/statutes-and-regulations/` · Sector Policy `/sector-policy/` · Sector Legislation `/sector-legislation/` · Sector Regulations `/sector-regulations/` · Guidelines `/guidelines/` · Industry Codes of Practice `/industry-codes-of-practice/` · Rulings `/rulings/` · Determinations `/determinations/` · National Broadband Strategy `/national-broadband-strategy/`
- Market & compliance: Market Structure `/market-structure/` · Compliance and Enforcement `/compliance-and-enforcement/` · Monitoring and Inspections `/monitoring-and-inspections/` · Regulatory Sandbox `/regulatory-sandbox/`
- Universal access: Overview `/universal-access/` · Universal Service Fund `/universal-service-fund/` · Purpose of the Fund `/purpose-of-the-fund/` · Universal Access Projects `/universal-access-projects/` · ICT Services Coverage Geo-Portal `/ict-services-coverage-geo-portal/` · ICT Access Gap Study `/ict-access-gap-study/` · Data Dictionaries `/data-dictionaries/`
- National projects & innovation: National Public Key Infrastructure `/national-public-key-infrastructure/` · National Addressing System `/national-addressing-system-kenya/` · E-Commerce Development `/e-commerce-development/` · Innovations `/innovations/` · Cybersecurity `/cybersecurity/`

> Note: the old "Market Structure" sub-links (Broadcasting / Telecommunication / Postal and Courier) all pointed to the same page, so they are collapsed into one link. The 13 individual Universal Access project pages are reached from `/universal-access-projects/` and are not listed in the mega menu.

**Consumer Protection** (overview: `/our-role-in-your-protection/`)
- Complaints & feedback: File a Complaint `/consumer-complaint/` · Public Complaints `/public-complaints/` · Feedback & Complaints `/feedback-and-complaints/` · Customer Feedback Questionnaire `/customer-feedback-questionnaire/` · Customer Satisfaction Survey `/customer-satisfaction-survey/`
- Stay protected: Our Role in Your Protection `/our-role-in-your-protection/` · Consumer Education & Outreach `/consumer-education-and-outreach/` · Child Online Protection `/child-online-protection/` · Quality of Service `/quality-of-service/` · IMEI Checker `/imei-checker/`

**Procurement** (overview: `/procurement/`)
- Tenders `/tenders/` · Closed Tenders `/tenders/?tender_status=closed` · Awarded Contracts `/awarded-contracts/` · Certificate of Award `/certificate-of-award/` · Supplier Registration Portal `/supplier-registration/`

**Info Hub** (overview: `/information-centre/`)
- News & media: News `/news/` · Press Statements `/press-statements/` · Speeches `/speeches/` · Upcoming Events `/upcoming-events/` · Campaigns `/campaigns/`
- Publications & data: Publications `/publications/` · Annual Reports `/annual-reports/` · Reports and Studies `/reports-and-studies/` · Statistics `/statistics/` · Documents `/documents/`
- Public participation: Open Consultations `/open-consultations/` · Closed Consultations `/closed-consultations/` · Published Findings `/published-findings/` · KICA Regulations RIA `/kica-regulations-ria/` · Public Notices `/public-notices/`
- More: Our Portals `/portals/` · Staff Verification Portal `/staff-verification-portal/` · Corporate Social Responsibility `/corporate-social-responsibility/` · International Obligations `/international-obligations/`

## Appendix B — Existing content to reuse

**News (latest 4)**

| Date | Title | URL slug | Image alt |
|---|---|---|---|
| 9 Sep 2026 | CA and UoN Undertake Preliminary Review of Findings of the National Survey on Child Online Protection and Safety in Kenya | `/ca-and-uon-undertake-preliminary-review-findings-national-survey-child-online-protection-and-safety/` | CA and University of Nairobi officials at a session reviewing preliminary findings of the National Survey on Child Online Protection |
| 19 Aug 2026 | 120,000 Kenyans to Gain Digital Skills to Drive Meaningful Digital Inclusion | `/120000-kenyans-gain-digital-skills-drive-meaningful-digital-inclusion/` | Stakeholders at the Universal Service Fund workshop on the Digital Skilling Project for 120,000 Kenyans |
| 13 Aug 2026 | CA clarifies new cyber cafe licence rules and says no browsing history will be required | `/ca-clarifies-new-cyber-cafe-license-rules-and-says-no-browsing-history-will-be-required/` | Rows of computers in a public cyber cafe |
| 10 Aug 2026 | CA Celebrates Creativity and Digital Safety at the Kenya Music Festivals | `/ca-celebrates-creativity-and-digital-safety-kenya-music-festivals/` | Kenya Music Festival branding graphic |

**Videos (YouTube IDs)**

| Title | ID |
|---|---|
| ICT WEEK: Digital Inclusion | `O32Wd94dv84` |
| CA and Meta Online safety campaign | `B3n4m3SMawU` |
| Local Area Network (LAN) Project, Connecting 42 Law Courts | `8Rz5RukpyIU` |
| CA Achievements 2018–2023 | `xpTuVnIBae8` |

**Contact:** CA Centre, Waiyaki Way, Westlands · P.O. Box 14448 – 00800 Nairobi · +254 20 4242000 · +254 703 042 000 · +254 730 172 000 · info@ca.go.ke

**Footer — Popular services:** Apply for a licence `/licensing-procedures/` · File a complaint `/consumer-complaint/` · Licensee register `/licensee-register/` · Report a cyber incident `https://ke-cirt.go.ke/report-an-incident/` (external) · Type-approved equipment `/wp-content/uploads/licensing/licensee-register/list-of-type-approved-equipment-august-2026-1bbe52eb.pdf` (PDF; label the link with its file type) · Forms and fees `/telecommunications-services/` · Numbering Management System `https://nms.ca.go.ke/` (external)

**Footer — Resources:** Acts and regulations `/statutes-and-regulations/` · Guidelines `/guidelines/` · Public consultations `/open-consultations/` · Statistics `/statistics/` · Reports and studies `/reports-and-studies/` · Public notices `/public-notices/`

**Footer — The Authority:** About CA `/about-the-authority/` · Careers `/careers/` · Contact us `/contact-us/` · Tenders `/tenders/` · Info Hub `/information-centre/` · Sitemap `/wp-sitemap.xml`

**Footer — Affiliations (all external):** Ministry of Information, Communications and the Digital Economy `https://ict.go.ke/` · International Telecommunication Union `https://itu.int/` · Universal Postal Union `https://www.upu.int/` · African Telecommunications Union `https://atuuat.africa/` · Pan African Postal Union `https://www.upap-papu.africa/` · Commonwealth Telecommunications Organisation `https://www.cto.int/` · East African Communications Organisation `https://eaco.int/` · African Advanced Level Telecommunications Institute `https://www.afralti.org/`

**Social:** YouTube `https://www.youtube.com/@CAoKenya` (confirmed). LinkedIn, X, Facebook and Instagram are **placeholders**; the client must supply the URLs.

## Appendix C — Original colour tokens (from the current theme)

Primary 50 `#F2F7FF` · 500 `#1D51A3` · 600 `#0B4191` · 700 `#00327C` · 900 `#04214F`; Secondary 500 `#EC5B13` · 600 `#BD4400`; Accent 500 `#38C3FF` · 600 `#008CBC`; Neutral 50 `#FAFAFA` · 200 `#E4E5E6` · 500 `#7D8184` · 700 `#3D4043` · 900 `#131415`; Success `#22A06B` · Danger `#DC262F` · Warning `#E5A000` · Info `#2563EB`.
Fonts: Inter (variable), Maitree 700, JetBrains Mono (code only). Existing breakpoints: 640 / 768 / 1024 / 1280.

## Appendix D — Existing image assets (download from the staging site into `assets/img/`)

Base URL: `https://ca.programmer.co.ke/wp-content/`

- Logo: `themes/communications-authority-kenya/assets/images/ca-logo.svg`, plus the white version `ca-logo-white.svg` (same folder)
- Hero: `uploads/2026/09/ca-hero-1-optimized-1600x634.webp` (satellite dish) and `uploads/ca-hero-2-source-scaled-optimized-1600x634.webp`
- About: `uploads/2026/09/ca-about-1-optimized-625x420.webp` (CA Centre) and `uploads/ca-about-2-scaled-optimized-625x420.webp`
- Favicons: `uploads/ca-favicon-32x32.png`, `ca-favicon-192x192.png`, `ca-favicon-180x180.png`, `ca-favicon-270x270.png`
- News and video thumbnails: as referenced on the current homepage

If an asset can't be downloaded, use a neutral, correctly sized placeholder (with the same aspect ratio) and list it in `docs/content-todo.md`. **Higher-resolution hero photography (min. 2400 px wide) is needed from the client.**
