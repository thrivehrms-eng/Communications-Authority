# Content to-do — homepage

Every item below is a visible placeholder in `index.html` (text in square brackets and/or `data-placeholder="true"`).
Open the page with `?placeholders` in the URL to outline them all with a dashed border.

## Images and logos

| Section | What's needed | Format / size | Suggested source |
|---|---|---|---|
| 7.2 Logo ticker | Logos for: Ministry of Information, Communications and the Digital Economy; ITU; UPU; ATU; PAPU; CTO; EACO; AFRALTI (currently text wordmark tiles) | SVG preferred (monochrome-friendly), else PNG ≥ 400px wide, transparent background | Each organisation's media/brand page; CA Corporate Communications |
| 7.3 About | Director-General portrait (currently the CA Centre photo is used, as the brief allows) plus name for the caption "[Name], Director-General" | 4:5 portrait, ≥ 900×1125, AVIF/WebP | CA Corporate Communications |
| 7.6 Highlight | Universal Service Fund logo for the badge chip (`[USF logo]`) | SVG, square-safe | USF / CA Corporate Communications |
| 7.6 Highlight | Optional dedicated USF image (the "120,000 Kenyans" news image is reused for now) | 4:5, ≥ 960×1200 | USF programme photography |
| 7.8 Projects | One image per project tile (6): E-Justice, Education Broadband Connectivity, Computerisation of Health Centres, ICT for Persons with Disabilities, Voice Infrastructure Project, Community Telecentres | 4:3, ≥ 1200×900, AVIF/WebP; keep the lower third calm (title sits there over a scrim) | USF project pages on ca.go.ke |
| 8 Footer | Certification marks (`[ISO certification mark — to be supplied]`, `[Certification mark — to be supplied]`) as white monochrome lockups | SVG, white | CA Quality / ISMS office |
| Head (SEO) | Open Graph / Twitter image (`assets/img/og-placeholder.png` is a navy placeholder) | 1200×630 PNG/JPG | CA Corporate Communications |

## Text

| Section | What's needed | Notes |
|---|---|---|
| 6.3 Menu overlay | Office hours (`[Office hours — to be confirmed]`) | Short line, e.g. days + times |
| 6.3 Menu overlay "Latest" | Public notices: 8 × `[Notice title]` + `[date]` | Each links to `/public-notices/` until individual URLs exist |
| 6.3 Menu overlay "Latest" and 7.9 News | One-sentence summary for each of the 4 news stories (`[One-sentence summary — to be supplied]`) | ≤ 160 characters; overlay clamps to 2 lines, cards to 3 |
| 7.9 News | Read time for each story (`[X] min read`) | Whole minutes |
| 7.4 Commitments | Confirm the five one-line descriptions against the Service Charter | Currently marked `data-placeholder` |
| 7.6 Highlight | Second paragraph: `[One-paragraph USF highlight — e.g. latest digital skilling programme — to be supplied]` | 1 paragraph, ≤ 60 words |
| 7.1 Hero | H1 is proposed copy ("Connecting Kenya. / Protecting every user.") | Confirm or replace; keep two short lines |

## Links / URLs to confirm

| Where | Current value | Needed |
|---|---|---|
| Header language toggle + `hreflang` | `/sw/` | Real Kiswahili homepage URL |
| Menu overlay + footer social buttons | LinkedIn, X, Facebook, Instagram (rendered disabled, no `href`) | Official profile URLs (YouTube is confirmed) |
| Footer legal row + consent text | `/terms-and-conditions/`, `/privacy-policy/`, `/accessibility/` | Confirm slugs |
| Footer "The Authority" | `/sitemap/` | Confirm slug |
| Head: canonical, `og:url`, JSON-LD | `https://ca.programmer.co.ke/` (staging) | Switch to the production domain at launch |

## Asset download log

All requested CA assets downloaded with HTTP 200 and were optimised into `assets/img/`:

- `ca-logo.svg`, `ca-logo-white.svg` (unchanged)
- `ca-hero-1-optimized-1600x634.webp` → `hero-dish-370/740.{avif,webp}` (cropped to the dish)
- `ca-about-1-optimized-625x420.webp` → `ca-centre-625.{avif,webp}`
- The four homepage news images → `news-*-320/640.{avif,webp}`
- Favicons (32, 180, 192) from the current site
- Fonts: identical files from Fontsource (`@fontsource-variable/inter` 5.3.0, `@fontsource/maitree` 5.3.0, Latin subset); both return HTTP 200 locally
