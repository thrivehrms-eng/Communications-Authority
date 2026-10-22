# Content to-do — homepage

Every item below is a visible placeholder in `index.html` (text in square brackets and/or `data-placeholder="true"`).
Open the page with `?placeholders` in the URL to outline them all with a dashed border.

## Images and logos

| Section | What's needed | Format / size | Suggested source |
|---|---|---|---|
| 7.2 Logo ticker | Logos for the **Ministry of Information, Communications and the Digital Economy** and **PAPU** (still text tiles). ITU, UPU, ATU, CTO, EACO and AFRALTI now use their official logos, taken from each organisation's own website (`assets/img/logos/`) | SVG preferred, else transparent PNG/WebP ≥ 96px tall | ict.go.ke failed TLS verification from the build environment; PAPU: see URLs below. Confirm logo-use permission with each body |
| 7.3 About | Director-General portrait (currently the CA Centre photo is used, as the brief allows) plus name for the caption "[Name], Director-General" | 4:5 portrait, ≥ 900×1125, AVIF/WebP | CA Corporate Communications |
| 7.6 Highlight | Universal Service Fund logo for the badge chip (`[USF logo]`) | SVG, square-safe | USF / CA Corporate Communications |
| 7.6 Highlight | Optional dedicated USF image (the "120,000 Kenyans" news image is reused for now) | 4:5, ≥ 960×1200 | USF programme photography |
| 7.8 Projects | All six tiles have photos. E-Justice, Education Broadband and Voice Infrastructure use CA's own ca.go.ke portfolio photos. **Computerisation of Health Centres, ICT for Persons with Disabilities and Community Telecentres use illustrative CC0 photos from nappy.co** (credits below), not photos of the projects; replace them with CA project photography when available | 4:3, ≥ 1200×900, AVIF/WebP; keep the lower third calm | USF programme photography |
| 8 Footer | Certification marks (`[ISO certification mark — to be supplied]`, `[Certification mark — to be supplied]`) as white monochrome lockups | SVG, white | CA Quality / ISMS office |
| Higher-resolution photos | The Broadband project photo is only 382px tall at source; the hero photo is 1600px wide | Broadband ≥ 1200×900; hero ≥ 2880px wide | CA Corporate Communications |
| Head (SEO) | Open Graph / Twitter image (`assets/img/og-placeholder.png` is a navy placeholder) | 1200×630 PNG/JPG | CA Corporate Communications |

## Text

| Section | What's needed | Notes |
|---|---|---|
| 6.3 Menu overlay | Office hours (`[Office hours — to be confirmed]`) | Short line, e.g. days + times |
| 6.3 Menu overlay "Latest" | Public notices: 8 × `[Notice title]` + `[date]` | Each links to `/public-notices/` until individual URLs exist |
| 6.3 Menu overlay "Latest" and 7.9 News | One-sentence summary for the featured story and for each overlay item (`[One-sentence summary — to be supplied]`) | **≤ 140 characters** (longer text is shortened at a word boundary). News **titles ≤ 80 characters** on cards and in the overlay, **≤ 100** for the featured story |
| 7.4 Commitments | Confirm the five one-line descriptions against the Service Charter | Currently marked `data-placeholder` |
| 7.6 Highlight | Second paragraph: `[One-paragraph USF highlight — e.g. latest digital skilling programme — to be supplied]` | 1 paragraph, ≤ 60 words |
| 7.1 Hero slider | Four slides (Welcome · Licensing online · Complaints · Universal access): titles, one-line texts and buttons are proposed copy. Titles follow a two-line rhythm: a short statement + a highlighted phrase (≤ 24 characters each) | Confirm wording; confirm `https://lms.ca.go.ke/` (taken from the current ca.go.ke banner) |
| 7.1 Hero slider images | Slides use CA's dish photo, the ca.go.ke "network globe" banner image, the staging tower-at-sunset image and the USF base station photo | Purpose-shot photography at ≥ 2880×1140 would sharpen slides 2–3 (sources are 1200–1600px wide) |
| 7.1 Hero | Popular tasks (6) and the search label are proposed; they mirror the search FAQ | Confirm the six against contact-centre or site-search data |

## Links / URLs to confirm

| Where | Current value | Needed |
|---|---|---|
| Header language toggle + `hreflang` | `/sw/` | Real Kiswahili homepage URL |
| Logo ticker: PAPU | **No link.** The brief's `https://www.upap-papu.africa/` now redirects to an unrelated shop (`xl-shops.com`), which suggests the domain has lapsed | PAPU's current official URL |
| Menu overlay + footer social buttons | LinkedIn, X, Facebook, Instagram (rendered disabled, no `href`) | Official profile URLs (YouTube is confirmed) |
| Footer legal row + consent text | `/terms-and-conditions/`, `/privacy-policy/`, `/accessibility/` | Confirm slugs |
| Footer "The Authority" | `/sitemap/` | Confirm slug |
| Head: canonical, `og:url`, JSON-LD | `https://ca.programmer.co.ke/` (staging) | Switch to the production domain at launch |

## Asset download log

All requested CA assets downloaded with HTTP 200 and were optimised into `assets/img/`:

- `ca-logo.svg`, `ca-logo-white.svg` (unchanged)
- `ca-hero-1-optimized-1600x634.webp` → `hero-wide-800/1600.{avif,webp}` (full-width hero)
- ca.go.ke portfolio photos `E-Justice.jpg`, `_AK_7654.JPG` (USF base station, West Pokot), `Broadband.png` → `project-*.{avif,webp}` (4:3)
- Official logos from itu.int, upu.int, atuuat.africa, cto.int, eaco.int, afralti.org → `assets/img/logos/` (SVGs checked for scripts and external references; rasters trimmed to 96px tall WebP)
- `ca-about-1-optimized-625x420.webp` → `ca-centre-625.{avif,webp}`
- The four homepage news images → `news-*-320/640.{avif,webp}`
- Favicons (32, 180, 192) from the current site
- Fonts: identical files from Fontsource (`@fontsource-variable/inter` 5.3.0, `@fontsource/maitree` 5.3.0, Latin subset); both return HTTP 200 locally

## Image credits (CC0, credit not required)

- `project-health-*`: "Doctor office examination" by @c0fbf559 on nappy.co
- `project-pwd-*`: "Person with a hand splint holding a phone" by @MetaLab on nappy.co
- `project-telecentres-*`: "Friends working on a computer" by @antoinedigital on nappy.co
