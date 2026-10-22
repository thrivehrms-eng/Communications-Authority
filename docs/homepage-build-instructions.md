# Build Instructions — Communications Authority of Kenya Homepage (Concept: Media Harbour)

> **For Claude Code.** Rebuild the homepage of https://ca.programmer.co.ke/ (Communications Authority of Kenya, "CA") in HTML, CSS and vanilla JavaScript. Match the layout, components and interactions of the concept site https://www.media-harbour.com/en/ from the navigation, through the body, to the footer. **The concept supplies the layout and behaviour only. Brand, colours and fonts come strictly from the current CA site.**
> Scope: **homepage only**. Further pages will follow in later briefs.
> Visual references: `docs/reference/concept/` (concept screenshots: layout and behaviour only, not colours or fonts) and `docs/reference/current-site/` (the current CA site: brand source). Background audit: `docs/homepage-audit.md`.

---

## 1. Goal & constraints

- **Goal:** a modern, calm, highly structured homepage in the concept's visual language that gets CA's audiences (citizens, licensees, industry, suppliers, media) to their task quickly.
- **Stack:** semantic HTML5, modern CSS (custom properties, grid, `clamp()`, `:has()` where it degrades safely) and vanilla ES modules. **No frameworks, no jQuery, no GSAP, no CSS frameworks, no build step.**
- **Do not copy the concept's code, images, logos or text.** Re-create its *patterns* only.
- **Brand lock:** use only the CA logo, the CA colour tokens in §3 and the CA fonts (Inter + Maitree). Do not introduce any colour or typeface from the concept site. If a concept element needs a colour, map it to the nearest CA token in §3. Never add a new hex value.
- **Accessibility:** WCAG 2.2 AA is mandatory.
- **Language:** British English ("licence", "organisation", "programme").
- **Facts:** never invent facts, figures, names, dates or URLs. Anything not given in this brief is a marked placeholder (see §12).
- **Structure:** build each section as a self-contained component so it can later be ported to WordPress template parts.
- **Working method:** work in the phases in §14. Stop after each phase with a short summary and a list of anything you need from me.

## 2. File structure

```
/
├── index.html
├── assets/
│   ├── css/  tokens.css · base.css · layout.css · components.css · sections.css · overlays.css
│   ├── js/   main.js · header.js · overlay-menu.js · search.js · accordion.js · ticker.js
│   │         filter.js · reveal.js · hero-fx.js · cursor.js · consent.js · dot-nav.js
│   ├── fonts/  inter-latin-wght-normal.woff2 · maitree-latin-700-normal.woff2
│   ├── img/    (optimised AVIF/WebP + fallbacks; placeholders where assets are missing)
│   └── icons/  sprite.svg (24px line icons, 1.75 stroke, round caps)
├── docs/content-todo.md   (generated: every placeholder still needing real content)
└── README.md
```

Use BEM naming with a `ca-` prefix (`ca-panel`, `ca-card__title`, `ca-btn--primary`). `main.js` initialises each module only if its root element exists.

## 3. Design tokens (`tokens.css`)

All colour values below are taken **verbatim from the current CA theme** (`--wp--preset--color--*` on ca.programmer.co.ke). The concept's colours are not used.

```css
:root {
  /* ── CA palette (verbatim from the current theme; do not add colours) ── */
  --ca-primary-50:  #F2F7FF;
  --ca-primary-500: #1D51A3;
  --ca-primary-600: #0B4191;
  --ca-primary-700: #00327C;
  --ca-primary-900: #04214F;
  --ca-secondary-500: #EC5B13;
  --ca-secondary-600: #BD4400;
  --ca-accent-500:  #38C3FF;
  --ca-accent-600:  #008CBC;
  --ca-neutral-50:  #FAFAFA;
  --ca-neutral-200: #E4E5E6;
  --ca-neutral-500: #7D8184;
  --ca-neutral-700: #3D4043;
  --ca-neutral-900: #131415;
  --ca-success-500: #22A06B;
  --ca-danger-500:  #DC262F;
  --ca-warning-500: #E5A000;
  --ca-info-500:    #2563EB;
  --ca-surface-background: #FAFAFA;
  --ca-surface-card: #FFFFFF;
  --ca-text-strong:  #131415;
  --ca-text-medium:  #737779;
  --ca-border-default: #E4E5E6;

  /* ── Semantic roles (concept layout → CA colours) ── */
  --canvas:         var(--ca-neutral-200);    /* page background the panels float on */
  --surface:        var(--ca-surface-card);   /* white panels and cards */
  --surface-tint:   var(--ca-primary-50);     /* light-blue panels and tinted cards */
  --border:         var(--ca-border-default); /* card borders and dividers on light surfaces */
  --primary:        var(--ca-primary-500);    /* buttons, primary panels, links */
  --primary-hover:  var(--ca-primary-600);
  --dark:           var(--ca-primary-900);    /* dark panels, footer */
  --dark-2:         var(--ca-primary-700);    /* gradient partner for dark panels */
  --accent:         var(--ca-accent-500);     /* highlight words and meta on dark/primary panels ONLY */
  --signature:      var(--ca-secondary-500);  /* CA orange: decorative details only (see below) */
  --text:           var(--ca-text-strong);
  --text-muted:     var(--ca-neutral-700);    /* secondary copy on white AND on --surface-tint */
  --text-meta:      var(--ca-text-medium);    /* dates/meta on WHITE only, ≥ 14px */
  --text-on-dark:   #FFFFFF;
  --text-on-dark-muted: rgb(255 255 255 / .80);

  /* Shape (concept layout) */
  --radius-panel: 28px;   /* section panels, footer */
  --radius-card:  20px;   /* cards, dropdowns, header bar */
  --radius-media: 16px;   /* images inside cards/panels */
  --radius-pill:  100px;  /* buttons, chips, eyebrow badges */

  /* Space */
  --gutter:       clamp(10px, 1.2vw, 22px);  /* canvas gap around and between panels */
  --panel-pad-y:  clamp(56px, 7vw, 96px);
  --content-max:  1200px;
  --content-pad:  clamp(20px, 5vw, 72px);

  /* Elevation (tinted with CA navy) */
  --shadow-header: 0 6px 24px rgb(4 33 79 / .08);
  --shadow-card:   0 10px 30px rgb(4 33 79 / .12);

  /* Motion */
  --ease-out: cubic-bezier(0, 0, .36, 1);
  --ease-std: cubic-bezier(.4, 0, .2, 1);
  --dur-1: 160ms; --dur-2: 280ms; --dur-3: 600ms;

  /* Focus */
  --focus: 3px solid var(--ca-secondary-600);   /* on light surfaces */
  --focus-on-dark: 3px solid var(--ca-accent-500);
}
```

**Colour usage rules**
- **CA orange (`--signature`)** is the brand's signature detail, used exactly as on the current site. Use it for:
  - the 3px top border on dropdowns and the menu overlay (the current mega menu has this orange line)
  - the dot inside eyebrow badges
  - the active page-dot
  - small icon accents

  Never use `#EC5B13` for text on white (3.5:1). Where orange text is unavoidable, use `--ca-secondary-600`.
- **CA cyan (`--accent`)** is only for highlight words, eyebrows and meta on `--dark` or `--primary` panels. On `--primary` panels, use it for large text only (≥ 24px; contrast 3.9:1).
- `--text-meta` (#737779) is allowed only on white at ≥ 14px. On `--surface-tint`, use `--text-muted`.
- Status colours (`--ca-success-500`, etc.) are for badges and icons, always paired with text.

### Typography (CA's current fonts)

Keep the current CA pairing exactly: **Inter** (variable) for body and UI, and **Maitree 700** for headings. Fallback stacks are copied from the current theme:

```css
--font-body:    "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
--font-heading: "Maitree", Georgia, "Times New Roman", serif;
```

**Font files:** self-host two WOFF2 files, Latin subset, with `font-display: swap`, and preload both:
- `inter-latin-wght-normal.woff2`
- `maitree-latin-700-normal.woff2`

These are the same files the CA theme references. On the staging server they currently return **403**, so obtain identical files from Fontsource (`@fontsource-variable/inter` and `@fontsource/maitree`, weight 700, Latin subset) and **verify both load with HTTP 200**.

| Role | Font | Size (mobile → desktop) | Weight | Line height | Tracking |
|---|---|---|---|---|---|
| Hero H1 | Maitree | `clamp(2.4rem, 5.5vw, 4.25rem)` | 700 | 1.12 | -0.01em |
| Section H2 | Maitree | `clamp(1.9rem, 3.4vw, 2.75rem)` | 700 | 1.16 | -0.005em |
| Featured / news titles | Maitree | `clamp(1.15rem, 1.8vw, 1.6rem)` | 700 | 1.25 | 0 |
| Card / accordion titles (H3) | Inter | `clamp(1.1rem, 1.5vw, 1.25rem)` | 600 | 1.3 | -0.01em |
| Nav links | Inter | `1.0625rem` | 500 | 1.4 | — |
| Lead | Inter | `clamp(1.05rem, 1.4vw, 1.2rem)` | 400 | 1.65 | — |
| Body | Inter | `1rem`–`1.0625rem` | 400 | 1.65 | — |
| Eyebrow | Inter | `0.875rem`, UPPERCASE | 600 | 1.6 | 0.14em |
| Meta (dates, tags) | Inter | `0.8125rem` | 500 | 1.4 | — |
| Button | Inter | `1.0625rem` (small: `0.9375rem`) | 600 | 1.2 | — |

Do not load JetBrains Mono (the current theme declares it, but the homepage doesn't use it).

- **Two-tone headlines** come from the concept, set in Maitree. Each H1/H2 has one *highlighted phrase*, wrapped in `<span class="ca-hl">`. On white or tint panels it is coloured `--primary`. On `--dark`, `--primary` and `--fx` panels it is `--accent` (CA cyan). Use solid colour only, with no gradient text.
- Body copy has a maximum width of 62ch.

## 4. Global layout pattern

- `body` background is `--canvas`. **Every section is a rounded "panel"** (`.ca-panel`, radius `--radius-panel`) floating on the canvas, inset by `--gutter` on left/right and separated by `--gutter` vertically. Panels span the viewport minus the gutters.
- Inside each panel, content sits in `.ca-container` (`max-width: var(--content-max)`, centred, `padding-inline: var(--content-pad)`). Every section shares the same content edges.
- Panel colour variants:
  - `--white`: `--surface`.
  - `--tint`: `--surface-tint`.
  - `--primary`: `--primary`, white text.
  - `--dark`: a `linear-gradient(200deg, var(--dark-2), var(--dark))` background with white text.
  - `--fx`: dark plus an animated particle/line background (see §9).
- Section header pattern (`.ca-section-head`): eyebrow → H2 with highlighted phrase → optional intro (max 60ch). It is left-aligned by default; use the centred variant for the Projects and News sections.
- **Eyebrow badge variant** (used in the hero and on `--fx` panels): a pill with a 1px light border, a small glowing CA-orange (`--signature`) dot before the text, uppercase, and a translucent background.

## 5. Core components (`components.css`)

1. **Buttons (pill):**
   - Variants: `--primary` (primary bg, white text), `--white` (white bg, primary text; for dark panels), `--outline-light` (transparent, 1.5px white border), `--outline` (transparent, 1.5px primary border).
   - Height 52–56px (small: 44px) with horizontal padding of about 28px.
   - Optional trailing arrow icon that shifts 3px right on hover/focus.
   - The hover state darkens the background (`--primary-hover`) or inverts outline buttons.
2. **Text link with arrow** ("More about …", "Read more", "All news"): weight 600, `--primary` (white on dark), with an arrow nudge on hover.
3. **Service card** (on the white panel): background `--primary`, radius `--radius-card`, padding 24–28px.
   - Contents: a white H3, a muted-white paragraph, and a link at the bottom (pinned with flex column + `margin-top: auto`).
   - The whole card is clickable via the stretched-link pattern (the `a` in the H3 gets `::after { inset: 0 }`).
   - Hover: background `--primary-hover`, lifts by 2px.
4. **Accordion row** (on the primary panel):
   - Layout: a check icon in a translucent circle, then the title, then a chevron at the end, with a 1px translucent divider below.
   - Uses `<h3><button aria-expanded aria-controls>` with a `role="region"` panel. Animate the height with the `grid-template-rows: 0fr → 1fr` technique.
   - Only one row is open at a time (optional).
5. **Project tile:** a large image card (radius `--radius-card`, aspect ratio about 4:3 on desktop) with a dark gradient scrim from the bottom.
   - Tags: small translucent pills, top-left.
   - A centred white logo or icon, and a white title at the bottom centre.
   - Hover: the image scales to 1.04.
   - The full tile is a single link.
6. **News card:** white card, 1px border `--border`, radius `--radius-card`.
    - Contents: image (16:9, radius on top only), meta line (CATEGORY in primary caps, then "date · X min read" in `--text-meta`), H3 title in Maitree 700, 3-line clamped excerpt, "Read more →".
   - **Featured news card variant:** a horizontal dark card (`--dark` gradient) with the image left and text right, meta in `--accent`.
7. **Filter chips:** pill buttons with a 1px primary border and primary text. The active chip has a primary background and white text. They sit in a `role="group"` with an `aria-label`, and each chip has `aria-pressed`.
8. **Social circle button:** a 44px circle, translucent on dark (white icon) or bordered on light (primary icon).
9. **Logo tile** (ticker item): a greyscale logo, coloured on hover/focus, with a visually hidden name.

## 6. Header & navigation

### 6.1 Header bar (desktop ≥ 1100px)

- The header is a **floating rounded white bar**: `position: sticky; top: var(--gutter)`, inset by the gutter, radius `--radius-card`, height about 76px, `--shadow-header`, with a slight `backdrop-filter` blur once scrolled.
- Left to right: **CA logo** (SVG, links to home) · **primary nav** (centre-right) · **CTA pill** "File a complaint" (`--primary`, small) → `/consumer-complaint/` · **language toggle** `EN | SW` (text, current language in primary, divider `|`, `hreflang`/`lang` set) · **search icon button** · **burger icon** (two lines of unequal length, which morph into ✕ when open).
- Primary nav items (Inter 17px, weight 500, `--primary` as on the current site, chevron for dropdowns, 2px primary underline on hover/active):
  **About CA ▾ · Licensing & Industry ▾ · Consumer Protection ▾ · Procurement ▾ · Info Hub ▾**

### 6.2 Dropdowns (concept style)

- A white card (radius `--radius-card`, `--shadow-card`, **3px CA-orange top border**) that appears 12px below the trigger with a fade + 6px slide.
- Each row is a link (16px, padding 14px 22px) with a 1px divider in `--border` and a `--surface-tint` background on hover.
- Small sections (Procurement, Consumer Protection) use a **single-column card**.
- Large sections (About CA, Licensing & Industry, Info Hub) use a **wide card** (max 880px) with 2–3 columns, each with a small uppercase group heading. It keeps the same visual language.
- The first row of every dropdown is "Overview →" to the section landing page.
- Behaviour:
  - Triggers are `<button aria-expanded aria-controls>` next to (or instead of) the link.
  - Opening uses click/Enter/Space, and hover with a 120ms intent delay. Closing uses mouse-leave after 250ms, Esc (focus returns to the trigger), or a click outside.
  - Only one dropdown is open at a time.
- Link map: see Appendix A.

### 6.3 Menu overlay (burger), desktop

- A large white rounded panel (radius `--radius-panel`) that drops in below the header bar and fills the viewport height minus the gutters. The page behind it is not scrollable. Animate with fade + 12px slide, and move focus into the panel.
- Two columns separated by a 1px vertical divider:
  - **Left: "Latest"** (H2) with an "All news →" link at the top right.
    - A 3×2 grid of **tinted cards** (`--surface-tint`, radius `--radius-card`), each showing a date (primary, small), title (18px), and a 2-line clamped excerpt.
    - Mix the latest news and public notices (Appendix B; notices are placeholders).
    - Previous/next arrow buttons page through further items.
  - **Right: "Contact"** (H2).
    - Contact centre block: icon + phone, icon + email, icon + hours `[Office hours — to be confirmed]`.
    - Primary pill CTA "File a complaint →".
    - A divider, then the postal address, then social circle buttons.
    - A row of quick links: Careers · Tenders · Innovations · Contact us (these replace the old utility bar).
- Close it with the burger (✕), Esc, or a click on the canvas. Focus is trapped while it's open.

### 6.4 Mobile header & menu (< 1100px)

- Header bar: logo · `EN | SW` · search icon · burger. Hide the CTA and nav links.
- The burger opens the same overlay panel, but its content is: the **primary nav as an accordion list** (24px items, dividers, chevron toggles that reveal sub-links), followed by the Contact block. Remove "Latest" on mobile.

### 6.5 Search panel

- The search icon swaps the nav area of the header bar for a large borderless input ("Search the CA website…") and drops a white rounded results panel below it.
- The panel has a close button (✕ circle, top-right) and a **"Frequently asked"** label above a two-column numbered list (number in a tinted circle, row dividers). Each row is a link to the answering page:
  1. How do I file a complaint against my service provider? → `/consumer-complaint/`
  2. How can I check if a phone is genuine (IMEI)? → `/imei-checker/`
  3. How do I apply for a licence? → `/licensing-procedures/`
  4. Is this company licensed by CA? → `/licensee-register/`
  5. Is my device type-approved? → `/type-approval/`
  6. Where can I find current tenders? → `/tenders/`
  7. How do I register as a supplier? → `/supplier-registration/`
  8. How do I report a cyber incident? → `https://ke-cirt.go.ke/report-an-incident/` (external)
  9. How can I verify a CA officer? → `/staff-verification-portal/`
  10. How do I take part in a public consultation? → `/open-consultations/`
- Submitting the input goes to `/?s=…` (WordPress-compatible `GET`, field name `s`).
- **No AI features.** Plain search plus the FAQ list. Typing filters the FAQ list live (simple keyword match).
- Esc closes the panel, and focus returns to the search button.

### 6.6 Floating help button (FAB)

- A 56px circular button fixed at the bottom-right (offset by the gutter + 16px). It is light-tinted with a primary chat/help icon and the accessible name "Quick help".
- It opens a small rounded card above itself containing:
  - the title "How can we help?"
  - three icon links: Call (`tel:`), Email (`mailto:`), Contact page
  - a primary pill "File a complaint"
- Esc or a click outside closes it. Hide the button while the menu overlay or search panel is open.

### 6.7 Page dot navigation (desktop ≥ 1280px)

- A vertical stack of small dots fixed at the right edge, vertically centred, one per homepage section.
- It uses `<nav aria-label="Page sections">` with links to section anchors, each with a visually hidden label and a tooltip on hover/focus.
- The active dot (tracked with IntersectionObserver) is elongated and coloured primary.

### 6.8 Cookie consent

- A rounded white card fixed at the bottom-left (on mobile: full width minus the gutters), shown on the first visit.
- Title "Your cookie settings" and one sentence linking to the Privacy Policy (reference Kenya's Data Protection Act, 2019, without quoting it).
- Buttons: "Settings" (text button that expands toggles for Necessary [locked on] / Analytics / Embedded media), then "Only necessary", "Accept all" and "Save selection" (outline pills).
- Store the choice in `localStorage` (try/catch). "Cookie settings" in the footer reopens the card.
- No analytics script is included in this build; only expose `window.caConsent.get('analytics')` for later use.

## 7. Homepage sections (in order)

Give each section an `id` for the dot nav. Each subsection below names the concept element first, then gives the CA implementation.

### 7.1 Hero — concept: dark-blue FX panel with badge, giant two-tone headline, two pill buttons

- **Panel:** `--fx` variant (dark gradient plus animated lines/particles, see §9). Min-height `min(78vh, 760px)`. Content left-aligned in the left 60%.
- **Eyebrow badge:** "Communications Authority of Kenya".
- **H1** (the only H1 on the page), two lines: "Connecting Kenya." / "<span class="ca-hl">Protecting</span> every user." *(Proposed copy; easy to edit. Keep it two short lines.)*
- **Lead (white, 80%):** "We license and regulate telecommunications, broadcasting, postal and courier services, manage Kenya's spectrum and numbering resources, and protect the people who use them — building a sustainable digital society through responsive regulation."
- **Buttons:** "Our services" (`--white`, anchors to §7.5) and "File a complaint" (`--outline-light`) → `/consumer-complaint/`.
- **Optional right-side visual:** on wide screens, CA's satellite-dish photo fades into the right 40% via a mask gradient (`assets/img/hero-dish.webp`). Without it, the line animation fills the panel.
- **Mobile:** text stacks, buttons go full-width and stacked, and the animation is simplified (fewer particles).

### 7.2 Logo ticker — concept: white strip with an infinitely scrolling client-logo marquee and a pause button

- **Panel:** white, compact (padding-block 28px).
- **Content:** CA's affiliations and partners, as a greyscale logo marquee with links (external): Ministry of Information, Communications and the Digital Economy · ITU · UPU · African Telecommunications Union · Pan African Postal Union · Commonwealth Telecommunications Organisation · EACO · AFRALTI. **Logos are placeholders** (neutral wordmark tiles) until assets are supplied.
- **Behaviour:**
  - CSS `@keyframes` translate with the list duplicated once; the duplicate gets `aria-hidden="true"` and `tabindex="-1"` on its links.
  - Pauses on hover and focus-within, and has a visible **pause/play button** at the end (`aria-pressed`).
  - Under `prefers-reduced-motion`, it shows as a static, horizontally scrollable row.
- Add a visually hidden heading: "Our affiliations".

### 7.3 About — concept: "Who we are" tinted panel, text left, portrait right with caption

- **Panel:** `--tint`. A two-column grid (text 1fr, image 0.85fr) that stacks on mobile with the image below.
- **Eyebrow:** "Who we are".
- **H2:** "Kenya's ICT regulator, <span class="ca-hl">in the public interest.</span>"
- **Text:**
  - P1: "The Communications Authority of Kenya (CA) is the regulatory agency for the ICT sector in Kenya, established by the Kenya Information and Communications Act, CAP 411A (KICA). We oversee telecommunications, radio communications, broadcasting, electronic transactions, the country's numbering and frequency spectrum resources, and postal and courier services."
  - P2: "CA is also mandated to protect the consumers of these services." Include inline links to `/consumer-education-and-outreach/` and `/universal-access/`.
- **Button:** "Get to know the Authority →" (`--primary`) → `/about-the-authority/`.
- **Image:** a portrait card (radius `--radius-media`, aspect 4:5). Use the Director-General's portrait (**placeholder**) with the caption "[Name], Director-General" in muted 14px text below. If no portrait is supplied, use the CA Centre photo with the caption "CA Centre, Waiyaki Way, Nairobi".

### 7.4 Commitments — concept: primary-blue panel, H2 left, accordion list with check icons right

- **Panel:** `--primary`. Two columns: the H2 vertically centred on the left (5/12), accordion on the right (7/12). Stacks on mobile.
- **H2 (white):** "What you can expect <span class="ca-hl">from us.</span>" (On primary panels the highlight is `--accent`, which is allowed because H2 is large text.)
- **Accordion rows** (titles and one-line descriptions; mark the descriptions `data-placeholder` until checked against the Service Charter):
  1. **Fair and transparent regulation:** clear rules, published decisions and open public consultation.
  2. **Consumer protection:** an independent channel to resolve complaints you couldn't settle with your provider.
  3. **Universal access:** extending communications services to underserved areas through the Universal Service Fund.
  4. **Secure digital spaces:** the National KE-CIRT/CC works to mitigate cyber threats.
  5. **Service you can rely on:** service standards set out in our Service Charter → link `/service-charter/`.

### 7.5 Services grid — concept: white panel, "What we do for you.", 6 blue cards, "All services" button

- **Panel:** white. Section head: eyebrow "Our services", H2 "What we do <span class="ca-hl">for you.</span>", intro "The Authority provides regulatory, licensing, consumer protection and industry support services across Kenya's communications and digital ecosystem."
- **Grid:** 3 × 2 on desktop, 2 columns on tablet, 1 on mobile. Six **service cards**:

| Title | Text | Link label → URL |
|---|---|---|
| Licensing | The Authority has a number of procedures that apply to the various licences it issues. | More about licensing → `/licensing-procedures/` |
| Type approval | Phones, routers and other equipment must be type-approved before sale or use in Kenya. | More about type approval → `/type-approval/` |
| Consumer protection | File complaints, check devices and learn how CA protects users of communications services. | More about consumer protection → `/our-role-in-your-protection/` |
| Cybersecurity | The National KE-CIRT/CC was established to mitigate cyber threats. | More about cybersecurity → `/cybersecurity/` |
| Guidelines & regulation | The Authority issues guidelines for the ICT sector on the implementation of specific regulatory matters. | More about guidelines → `/guidelines/` |
| Online portals | The Authority runs online portals for licensing, spectrum and other regulatory services. | More about our portals → `/portals/` |

- **Below the grid:** a centred "All services at a glance →" (`--primary`) → `/licensing-overview/`.
- **Mobile:** show the first 3 cards, then a "Show more services ▾" outline pill that reveals the rest (`aria-expanded`). The last visible card fades out with a gradient mask until the list is expanded.

### 7.6 Highlight teaser — concept: dark panel, image card left with badge overlay, text right

- **Panel:** `--dark`. Two columns (image 5/12, text 6/12, with a gap), vertically centred. Stacks on mobile with the image first.
- **Image card:** radius `--radius-media`, aspect 4:5, a subtle dot-grid texture overlay. A badge chip sits bottom-left: translucent white card with the "Universal Service Fund" label (**placeholder** USF logo).
- **Eyebrow (accent colour):** "Universal access".
- **H2 (white):** "Connecting every county. <span class="ca-hl">No one left behind.</span>"
- **Paragraphs (white 80%):** "Through the Universal Service Fund, the Authority extends communications services to underserved areas — from voice infrastructure and education broadband to community telecentres and ICT access for persons with disabilities." Add a second paragraph as a placeholder: `[One-paragraph USF highlight — e.g. latest digital skilling programme — to be supplied]`.
- **Button:** "Explore universal access →" (`--white`) → `/universal-access/`.

### 7.7 Two-column feature on FX background — concept: pill eyebrow, headline, intro, sub-blocks left, block + button right

- **Panel:** `--fx` (same animation system as the hero, lower particle density).
- **Eyebrow badge:** "Stay safe online".
- **H2 (white):** "Know before you buy. <span class="ca-hl">Report what's wrong.</span>"
- **Intro:** "Simple checks and clear routes to help — whether you're buying a phone, protecting a child online or responding to a cyber incident."
- **Left column:** two sub-blocks, each with an H3 (white, 18px, weight 600) and a paragraph.
  - "Check a phone before you buy": "Use the IMEI checker to confirm a device is genuine and type-approved." Link → `/imei-checker/`.
  - "Protecting children online": "Guidance for parents, guardians and schools on keeping children safe online." Link → `/child-online-protection/`.
- **Right column:** one sub-block plus a button.
  - "Report a cyber incident": "The National KE-CIRT/CC coordinates the response to cyber threats in Kenya."
  - Button: "Report an incident →" (`--primary`), external → `https://ke-cirt.go.ke/report-an-incident/`.

### 7.8 Projects with filter — concept: centred head, filter chips, 2-column image tiles, "Show all" button

- **Panel:** white. Centred head: eyebrow "Projects", H2 "<span class="ca-hl">Universal access</span> in action."
- **Filter chips:** All · Education · Health · Justice · Infrastructure · Inclusion.
- **Grid:** 2 columns of **project tiles** (1 column on mobile). Show these 6 (images are placeholders until supplied; each tile links to its page):

| Title | Tags | URL |
|---|---|---|
| E-Justice | Justice · Infrastructure | `/e-justice/` |
| Education Broadband Connectivity | Education · Infrastructure | `/education-broadband-connectivity/` |
| Computerisation of Health Centres | Health | `/computerization-of-health-centres/` |
| ICT for Persons with Disabilities | Inclusion | `/ict-for-persons-with-disabilities/` |
| Voice Infrastructure Project | Infrastructure | `/voice-infrastructure-project/` |
| Community Telecentres | Inclusion · Education | `/community-telecentres/` |

- **Filter behaviour:**
  - Filters hide or show tiles with a fade, and an `aria-live="polite"` status announces "Showing X projects".
  - An empty state reads "No projects in this category."
  - Without JS, all tiles show and the chips are hidden.
- **Button:** "Show all projects →" (`--primary`) → `/universal-access-projects/`.
- **Cursor follower (desktop, fine pointer only):** over a tile, a 76px primary circle labelled "VIEW" follows the cursor (§9). It is decorative (`aria-hidden`).

### 7.9 News — concept: centred head, one featured dark card, then 3 cards and an "All articles" button

- **Panel:** white. Centred head: eyebrow "News", H2 "What's happening <span class="ca-hl">at the Authority.</span>"
- **Featured card** (full width, `--dark`): the latest story. Then a 3-column row of news cards (1 column on mobile). Use the 4 real stories in Appendix B. The category label is "News" for all four unless told otherwise; read time is a placeholder.
- **Button:** "All news →" (`--primary`) → `/news/`. Cursor follower label: "READ".
- **Optional:** add a small "Watch" link row under the button → `https://www.youtube.com/@CAoKenya` (external).

### 7.10 Closing CTA — concept: primary panel, centred H2, paragraph, underlined secondary link, two buttons

- **Panel:** `--primary`, centred text, max-width 720px.
- **H2:** "Need help from <span class="ca-hl">the Authority?</span>"
- **Paragraph:** "If your service provider hasn't resolved your issue, tell us about it. A short description is enough to get started — we'll guide you through the next steps. Your submission goes directly to the Authority and is treated in confidence."
- **Underlined link:** "Or make a general enquiry." → `/contact-us/`.
- **Buttons:** "File a complaint →" (`--white`) and "Report corruption →" (`--outline-light`) → `/public-complaints/`.

## 8. Footer — concept: dark rounded panel, brand block with badges, link columns with expandable sub-lists, contact column with social circles, bottom legal row

- **Panel:** `--dark`, radius `--radius-panel`, inset by the gutter, with a `--gutter` bottom margin.
- **Grid (desktop):** brand (1.3fr) · Services (1fr) · The Authority (1fr) · Contact (1fr).
  - **Brand:** white CA logo; address "CA Centre, Waiyaki Way, Westlands" / "P.O. Box 14448 – 00800 Nairobi"; a badge row of **placeholder** certification badges (e.g. `[ISO certification mark — to be supplied]`) shown as white monochrome lockups.
  - **Services** (column heading links to `/licensing-overview/`): Apply for a licence · File a complaint · Licensee register · Type-approved equipment · Report a cyber incident (external) · Numbering Management System (external, `https://nms.ca.go.ke/`).
    - "Apply for a licence" has an **expand chevron** revealing sub-links: Licensing procedures · Statutes & regulations · Guidelines.
    - "File a complaint" expands to: Consumer complaint · Public complaints · Customer feedback.
    - Each expander is a `<button aria-expanded>` next to the link.
  - **The Authority:** About CA · Careers · Tenders · Public consultations · Statistics · Info Hub · Sitemap.
  - **Contact:** phone numbers as `tel:` links (+254 20 4242000 · +254 703 042 000 · +254 730 172 000); `info@ca.go.ke` as an underlined `mailto:` link; social circle buttons (YouTube confirmed: `https://www.youtube.com/@CAoKenya`; LinkedIn, X, Facebook and Instagram are **placeholders**, never `example.com`).
- **Divider** (1px, white 12%), then the bottom row:
  - Left: "© <year> Communications Authority of Kenya" (year set by JS, with a static fallback).
  - Right: legal links separated by thin pipes: Terms & Conditions · Privacy Policy · Accessibility · Cookie settings (a button that reopens consent).
- **Affiliations** live in the logo ticker (§7.2), not in the footer.
- **Mobile:** columns stack. Column lists stay open (don't collapse), but the sub-list expanders still work. The bottom row stacks.

## 9. Motion & interactions

All animations must be disabled or reduced to simple opacity changes under `prefers-reduced-motion: reduce`.

1. **Scroll reveal:** panels and cards fade up 24px over `--dur-3` with `--ease-out`, triggered by IntersectionObserver (threshold 0.15) and staggered 60ms within grids. Content must be visible without JS: the hidden state applies only when `<html class="js">`.
2. **Hero / FX background (`hero-fx.js`):** a `<canvas>` behind the content (`aria-hidden`) drawing about 12 soft flowing horizontal light curves in `--ca-primary-500` and `--ca-accent-500` (varying opacity), plus about 40 small drifting `--ca-accent-500` dots, at 30fps max. Read the colours from the CSS custom properties; don't hard-code them.
   - Pause when the canvas is off-screen (IntersectionObserver) or the tab is hidden.
   - Static gradient fallback, and **a pause button** in the panel corner (WCAG 2.2.2).
   - Respect `devicePixelRatio`, capped at 2.
   - Keep the script under 4 KB.
3. **Header:** becomes slightly more opaque, with a shadow, after 24px of scroll. It stays visible (no hide-on-scroll).
4. **Cursor follower (`cursor.js`):** only with `(hover: hover) and (pointer: fine)` and no reduced motion. A primary circle with a white uppercase label (VIEW/READ) scales in over hovered tiles and cards, follows the pointer with lerp smoothing, and is never the only way to see the link.
5. **Dropdowns, overlay, search, FAB:** opacity + 6–12px translate over `--dur-2`. Focus is managed as described in §6.
6. **Smooth anchor scrolling** with native `scroll-behavior: smooth`, with `scroll-padding-top` equal to the header height + gutter. **Do not** emulate the concept's scroll-smoothing library.

## 10. Accessibility requirements

- Skip link "Skip to main content" → `#main`; landmarks are `header`, `nav` (each labelled), `main` and `footer`. Exactly **one H1**, and the heading order never skips levels.
- All interactive targets are ≥ 44×44px, with visible `:focus-visible` everywhere (`--focus` on light, `--focus-on-dark` on dark).
- Every overlay/dialog (menu, search, FAB card, consent) is keyboard-operable: focus moves in, Tab is trapped where modal, Esc closes, and focus returns to the opener.
- Contrast: check every text/background pair, including text over images. Project tiles need the scrim, giving at least 4.5:1 for the bottom title.
- The ticker, FX canvas and any other motion are pausable, and there is no auto-advancing content.
- Images: meaningful `alt`; decorative ones get `alt=""`. Logos use the organisation's name as alt.
- External links show an external icon plus visually hidden "(external site)". Internal links never show it.
- `lang="en"` on `<html>`; the "SW" toggle has `lang="sw" hreflang="sw"`.
- The page works at 320px wide with no horizontal scroll, and at 200% zoom.

## 11. Performance & SEO

- **Budgets:** total CSS ≤ 50 KB and JS ≤ 25 KB (both minified-equivalent), with two font files (Inter variable + Maitree 700). LCP < 2.0s on 4G mobile, CLS < 0.05, INP < 200ms.
- **Images:** AVIF/WebP via `<picture>`, `srcset`/`sizes`, explicit `width`/`height`, and `loading="lazy" decoding="async"` below the fold. The hero has no LCP image dependency (text-led), or, if the dish photo is used, `fetchpriority="high"` and a preload.
- **Head:**
  - `<title>`: "Communications Authority of Kenya | ICT Sector Regulator".
  - Meta description: "The Communications Authority of Kenya regulates telecommunications, broadcasting, postal and courier services. File a complaint, check an IMEI, apply for a licence or find tenders."
  - Also include: canonical; `hreflang` for en, sw and x-default; Open Graph and Twitter tags (placeholder 1200×630 image); `theme-color` `#1D51A3`; and favicons.
- **JSON-LD:** `GovernmentOrganization` (name, url, logo, address, telephone, email, sameAs [YouTube only for now]) and `WebSite` with `SearchAction` (`/?s={search_term_string}`).
- No generator meta and no third-party scripts.

## 12. Content & placeholder rules

- Use the copy, links and data in this brief and in Appendices A–B verbatim where given.
- Anything not provided (portraits, project images, partner logos, badges, notices, office hours, read times, the USF highlight, social URLs) must be a **visible placeholder**:
  - Text in square brackets.
  - The element carries `data-placeholder="true"`.
  - A dashed outline appears only when the URL contains `?placeholders` (JS adds `html.show-placeholders`).
  - Image placeholders are neutral tinted blocks at the correct aspect ratio, with the label centred.
- Generate `docs/content-todo.md` listing each placeholder: section, what's needed, format/size, and the suggested source.
- Internal links are root-relative (e.g. `/tenders/`).
- Download these existing CA assets into `assets/img/`. If one fails, use a placeholder and log it in `content-todo.md`:
  - `https://ca.programmer.co.ke/wp-content/themes/communications-authority-kenya/assets/images/ca-logo.svg` and `ca-logo-white.svg`
  - `https://ca.programmer.co.ke/wp-content/uploads/2026/09/ca-hero-1-optimized-1600x634.webp` (satellite dish)
  - `https://ca.programmer.co.ke/wp-content/uploads/2026/09/ca-about-1-optimized-625x420.webp` (CA Centre)
  - The four news images referenced on the current homepage

## 13. Responsive behaviour summary

| Breakpoint | Key changes |
|---|---|
| ≥ 1280 | Dot nav visible; wide dropdowns; overlay in two columns |
| 1100–1279 | Full header nav; dot nav hidden |
| 768–1099 | Header collapses to burger; services in 2 columns; projects in 2 columns; footer 2×2 |
| < 768 | Single column throughout; buttons full width in hero/CTA; "Show more services"; news cards stacked; consent full width; gutter 10px |

## 14. Build phases (stop and report after each)

1. **Foundation:** file structure, tokens, base/typography, panel and container system, buttons and links, icon sprite, self-hosted Inter + Maitree 700 (verify both load with HTTP 200), README.
2. **Header system:** header bar, dropdowns, language toggle, burger overlay (desktop + mobile), search panel with FAQ, FAB, cookie consent, dot nav.
3. **Hero, ticker, about, commitments:** §7.1–7.4, plus `hero-fx.js` and the ticker.
4. **Services, highlight, feature, projects, news, CTA:** §7.5–7.10, plus the filter and cursor follower.
5. **Footer:** §8.
6. **Motion and polish:** reveal, reduced-motion pass, hover states, spacing audit against the concept rhythm.
7. **QA:**
   - Lighthouse mobile results and axe-core scan (0 violations).
   - Keyboard-only walkthrough.
   - Widths 320 / 390 / 768 / 1024 / 1280 / 1440.
   - JS disabled; `prefers-reduced-motion` on.
   - Contrast check.
   - Generate `docs/content-todo.md`.
   - Fix everything found and report.

## 15. Definition of done

- [ ] Every concept element is present in CA form: floating header bar with CTA/language/search/burger · dropdowns · menu overlay (Latest + Contact) · FAQ search panel · help FAB · dot nav · cookie consent · FX hero · logo ticker · tinted about panel · primary accordion panel · services card grid · dark highlight teaser · FX two-column feature · filterable project tiles · featured + card news · primary CTA panel · dark footer with expanders and legal row.
- [ ] Exactly one H1; no `href="#"`, `localhost` or `example.com` links; no console errors; all assets return 200.
- [ ] All motion is pausable or disabled under reduced motion.
- [ ] Lighthouse mobile scores: Performance ≥ 90, Accessibility 100, Best Practices ≥ 95, SEO 100. axe-core reports 0 violations.
- [ ] Budgets in §11 are met; the page works without JS (degraded but complete).
- [ ] `README.md` and `docs/content-todo.md` are complete.

---

## Appendix A — Dropdown link map

**About CA** — Overview `/about-the-authority/`
- *The Authority:* Board of Directors `/board-of-directors/` · Management Team `/management-team/` · Organisation Structure `/organisation-structure/` · Finance and Accounts `/finance-and-accounts/` · Universal Service Advisory Council `/universal-service-advisory-council/`
- *Policies & commitments:* Vision, Mission & Core Values `/vision-mission/` · Strategic Plan `/strategic-plan/` · Service Charter `/service-charter/` · Whistleblowing Policy `/whistle-blowing-policy/` · Quality & Information Security Policy `/quality-and-information-security-policy-statement/`
- *Work with us:* Careers `/careers/` · Access to Information `/access-to-information/` · Contact Us `/contact-us/`

**Licensing & Industry** — Overview `/licensing-overview/`
- *Licensing:* Licensing Procedures `/licensing-procedures/` · Licensee Register `/licensee-register/` · Type Approval `/type-approval/` · Telecommunications Services `/telecommunications-services/`
- *Law & policy:* Statutes & Regulations `/statutes-and-regulations/` · Sector Policy `/sector-policy/` · Sector Legislation `/sector-legislation/` · Sector Regulations `/sector-regulations/` · Guidelines `/guidelines/` · Industry Codes of Practice `/industry-codes-of-practice/` · Rulings `/rulings/` · Determinations `/determinations/` · National Broadband Strategy `/national-broadband-strategy/`
- *Market & compliance:* Market Structure `/market-structure/` · Compliance and Enforcement `/compliance-and-enforcement/` · Monitoring and Inspections `/monitoring-and-inspections/` · Regulatory Sandbox `/regulatory-sandbox/`
- *Universal access:* Universal Access `/universal-access/` · Universal Service Fund `/universal-service-fund/` · Universal Access Projects `/universal-access-projects/` · ICT Services Coverage Geo-Portal `/ict-services-coverage-geo-portal/` · ICT Access Gap Study `/ict-access-gap-study/`
- *National projects & innovation:* National Public Key Infrastructure `/national-public-key-infrastructure/` · National Addressing System `/national-addressing-system-kenya/` · E-Commerce Development `/e-commerce-development/` · Innovations `/innovations/` · Cybersecurity `/cybersecurity/`

**Consumer Protection** — Overview `/our-role-in-your-protection/`
File a Complaint `/consumer-complaint/` · Public Complaints `/public-complaints/` · IMEI Checker `/imei-checker/` · Consumer Education & Outreach `/consumer-education-and-outreach/` · Child Online Protection `/child-online-protection/` · Quality of Service `/quality-of-service/` · Customer Feedback Questionnaire `/customer-feedback-questionnaire/`

**Procurement** — Overview `/procurement/`
Tenders `/tenders/` · Closed Tenders `/tenders/?tender_status=closed` · Awarded Contracts `/awarded-contracts/` · Certificate of Award `/certificate-of-award/` · Supplier Registration Portal `/supplier-registration/`

**Info Hub** — Overview `/information-centre/`
- *News & media:* News `/news/` · Press Statements `/press-statements/` · Speeches `/speeches/` · Upcoming Events `/upcoming-events/` · Campaigns `/campaigns/`
- *Publications & data:* Publications `/publications/` · Annual Reports `/annual-reports/` · Reports and Studies `/reports-and-studies/` · Statistics `/statistics/` · Documents `/documents/`
- *Public participation:* Open Consultations `/open-consultations/` · Closed Consultations `/closed-consultations/` · Published Findings `/published-findings/` · Public Notices `/public-notices/`
- *Portals:* Our Portals `/portals/` · Staff Verification Portal `/staff-verification-portal/`

## Appendix B — Real content

**News (newest first)**

| Date | Title | URL | Image alt |
|---|---|---|---|
| 9 September 2026 | CA and UoN Undertake Preliminary Review of Findings of the National Survey on Child Online Protection and Safety in Kenya | `/ca-and-uon-undertake-preliminary-review-findings-national-survey-child-online-protection-and-safety/` | CA and University of Nairobi officials at a session reviewing preliminary findings of the National Survey on Child Online Protection |
| 19 August 2026 | 120,000 Kenyans to Gain Digital Skills to Drive Meaningful Digital Inclusion | `/120000-kenyans-gain-digital-skills-drive-meaningful-digital-inclusion/` | Stakeholders at the Universal Service Fund workshop on the Digital Skilling Project for 120,000 Kenyans |
| 13 August 2026 | CA clarifies new cyber cafe licence rules and says no browsing history will be required | `/ca-clarifies-new-cyber-cafe-license-rules-and-says-no-browsing-history-will-be-required/` | Rows of computers in a public cyber cafe |
| 10 August 2026 | CA Celebrates Creativity and Digital Safety at the Kenya Music Festivals | `/ca-celebrates-creativity-and-digital-safety-kenya-music-festivals/` | Kenya Music Festival branding graphic |

Excerpts for the news cards and the overlay "Latest" cards are placeholders: `[One-sentence summary — to be supplied]`.
Public notices in the overlay are placeholders: `[Notice title]`, `[date]` → `/public-notices/`.

**Contact:** CA Centre, Waiyaki Way, Westlands · P.O. Box 14448 – 00800 Nairobi · +254 20 4242000 · +254 703 042 000 · +254 730 172 000 · info@ca.go.ke

**Affiliation links (ticker, all external):** `https://ict.go.ke/` · `https://itu.int/` · `https://www.upu.int/` · `https://atuuat.africa/` · `https://www.upap-papu.africa/` · `https://www.cto.int/` · `https://eaco.int/` · `https://www.afralti.org/`
