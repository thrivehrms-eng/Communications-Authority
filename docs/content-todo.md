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
| 7.9b Videos | The heading "See our work in action." is proposed. The four videos are the newest distinct ones on the CA Kenya channel (checked 23 October 2026): the Judiciary LAN Project documentary (2 Feb 2026), the CA and Meta online safety campaign (24 Oct 2025), the Quality of Service exercise in Turkana County (11 Oct 2025) and Kenya's re-election to the UPU Postal Operations Council (17 Sep 2025). Titles are YouTube's own, with hashtags removed and typographic apostrophes/dashes | Confirm the choice, or switch to the automatic feed (README → Porting) |
| 7.1 Hero | Popular tasks (6) and the search label are proposed; they mirror the search FAQ | Confirm the six against contact-centre or site-search data |
| 6.2 Main menu | Each section's one-line summary, the group names (e.g. "Policies & commitments", "Market & compliance", "Public participation") and the one-line description under every link are **proposed functional copy**; the links and their order are unchanged from the brief | Confirm wording with Corporate Communications; keep descriptions to about 30 characters so most stay on one line at 1440px |

## About CA and Consumer Protection pages

Content, images and documents come from the WordPress site (ca.programmer.co.ke). Items to resolve there or confirm:

| Page | Issue | Needed |
|---|---|---|
| All pages with documents | In the WordPress page content, every document link points to `http://localhost/Projects/CA-website/wp-content/uploads/…` (a development address). The same files exist on ca.programmer.co.ke, which is what the new pages use (all 30 checked, HTTP 200) | Replace the localhost links in the WordPress content before launch |
| About the Authority vs Vision, Mission & Core Values | The WordPress About page gives the vision as "A globally competitive ICT sector that transforms lives", the mission as "To facilitate transformation of lives through progressive regulation of the ICT sector" and the values as Integrity, Professionalism, Innovation, Teamwork, Customer focus. The Vision page (citing ca.go.ke/vision-mission) gives "Digital access for all", "Enabling a sustainable digital society through responsive regulation" and Integrity, Innovation, Excellence, Agility, Inclusion | The new pages use the Vision page's wording on both pages, as it matches the 2023–2027 Strategic Plan ("#DigitalAccess4All"). Confirm, and update the WordPress About page |
| Our Role in Your Protection | "Constitution of Kenya, 2010 (sections 46 and 47)": the Constitution numbers these as Articles | Confirm wording ("Articles 46 and 47") |
| Page summaries | Where the WordPress page has no introduction, the line under the title is proposed: About the Authority, Board of Directors, Management Team, Universal Service Advisory Council, Organisation Structure, Vision, Mission & Core Values, Access to Information, Contact Us, IMEI Checker, Our Role in Your Protection. Elsewhere it is the page's own first sentence | Confirm the proposed lines |
| Board, Management, USAC | 12 people have no biography in WordPress, so their cards do not link to a profile: Waweru Kimani, Eng. Dennis Chepkwony, Eng. Leo Boruett, CHRP (K) Reginah Kemboi, Mohamed Haji, Martin Mirero, Peter Mwangi, FCPA Rosalind Murithi, Dr. Vincent Ngundi, Dr. Priscilla Njako, CPA Joseph Kimanga, CPA Matilda Wakere | Biographies, or confirm they stay as cards only |
| Finance and Accounts | Bank transfer, M-PESA/PayBill, payment reference, receipts and verification time are marked "to be confirmed" in WordPress and shown as such | Details from Finance and Accounts |
| Careers | Both adverts in WordPress have closed (18 September and 5 October 2026); they are listed as Closed. Status is worked out when the pages are built | Remove or archive closed adverts as appropriate |
| Contact Us | The head office card adds "Waiyaki Way, Westlands" (from the homepage footer) to the WordPress address "CA Centre, P.O. Box 14448-00800, Nairobi" | Confirm |
| Strategic Plan, Service Charter | Each page now plays a video from CA's YouTube channel: "CA’s 5th Strategic Plan 2023–2027 Highlights" and "CA Service Charter Video 2023" (the latter linked from the WordPress page) | Confirm |
| Forms | Consumer complaint, public complaints, customer feedback and contact forms keep the WordPress field names but are not connected in this static build: a completed form shows a notice that nothing was sent | Connect in the theme (README → Porting) |
| Strategic Plan | WordPress text "spells out CA’s its purpose" corrected to "CA’s purpose" | — |

## Procurement and Info Hub pages

Content, images and documents come from the WordPress site (pages, posts and the tender, contract, publication and document archives). Items to resolve there or confirm:

| Page | Issue | Needed |
|---|---|---|
| Tenders | All 220 tenders (financial years 2022/23 to 2025/26) have closed; the latest closed on 20 May 2026. The page and the Procurement overview say there are no open tenders at the moment, worked out from the closing dates when the pages are built | Rebuild when tenders open, or render the note in WordPress |
| Procurement | The WordPress page links the two procurement plans on www.ca.go.ke. The new pages use the copies already uploaded to ca.programmer.co.ke (the "Procurement Plans" documents) | Confirm the uploaded copies are current |
| Procurement | The four "How procurement works here" steps are proposed copy, written from the WordPress text on supplier registration, tenders and awards | Confirm with Supply Chain Management |
| Awarded Contracts | Of 336 contracts, 180 have no published value, 30 no award date and 72 no reference number; the table shows a dash (read out as "Not published") | Fill the gaps in WordPress where the reports allow |
| Info Hub | The overview's second paragraph and the three "Most requested" documents (latest annual report, latest sector statistics report, the 2024–2025 QoS report) are proposed | Confirm the picks with Corporate Communications |
| Open Consultations | The WordPress page lists nine consultation titles without their papers; it says papers are published individually as they open | Consultation papers, comment templates and closing dates for each |
| Closed Consultations, Published Findings | Titles only (13 and 10), no documents | The findings documents, where published |
| Public Notices | One notice (dot KE domain names for critical information infrastructure), without a date | The notice date; further notices as issued |
| Upcoming Events | WordPress has no events scheduled; the page says so and shows the latest news | — |
| News | 111 posts (June 2022 to September 2026) at their WordPress URLs. Three have no featured image and show a placeholder tile. 15 posts link to reports on www.ca.go.ke, which may move at launch | Featured images for the three; check the ca.go.ke links at launch |
| News | One post set its opening sentence as a heading; it is shown as a lead paragraph. The revenue-share table in "Kenyan Mobile Sector Records Growth in Revenue and Investments" had no caption; it now reads "Share of revenue by operator, year ended June 2023 (%)" | Make the same changes in WordPress |
| Speeches, Press Statements | Three document titles corrected for display: "Difrector" → "Director", "Cockail" → "Cocktail", and the file name "Press-Statement-on-Forensic-Audit-on-SIM-Card-Registration1" → "Press Statement on Forensic Audit on SIM Card Registration" | Correct the titles in WordPress |
| Publications | Two publications have no year and are filed under "Undated" | Years, if known |
| Our Portals | Licensee Register links to `/licensee-register/`, in the Licensing section (not built yet; the preview opens it on the WordPress site) | — |
| Forms | Supplier registration and staff verification keep the WordPress field names but are not connected in this static build: a completed form shows a notice that nothing was sent | Connect in the theme (README → Porting) |
| Page summaries | Proposed where WordPress has no introduction: Tenders, Awarded Contracts, News, Publications, Documents, Our Portals, Info Hub and Procurement overviews | Confirm |

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
- Video stills for the four videos from CA Kenya's own YouTube channel (`i.ytimg.com/vi/<id>/maxresdefault.jpg`, or `sddefault.jpg` where no HD still exists, cropped to 16:9) → `video-*-320/640.{avif,webp}`. Channel identity checked against its page title ("CA Kenya") and description; dates from each video page
- Fonts: identical files from Fontsource (`@fontsource-variable/inter` 5.3.0, `@fontsource/maitree` 5.3.0, Latin subset); both return HTTP 200 locally

## Image credits (CC0, credit not required)

- `project-health-*`: "Doctor office examination" by @c0fbf559 on nappy.co
- `project-pwd-*`: "Person with a hand splint holding a phone" by @MetaLab on nappy.co
- `project-telecentres-*`: "Friends working on a computer" by @antoinedigital on nappy.co
