#!/usr/bin/env python3
"""Build the inner pages of the site as static HTML.

Each page is a fragment in src/pages/<slug>.html with a small front-matter comment. The header, menus,
footer and help button are taken from index.html, so the homepage stays the single source for them.
Repeated structures (document lists, people, jobs, section links) come from src/data/*.json and the
main menu, through shortcodes such as <!--docs:strategic-plans-->.

    python3 tools/build.py                  writes /<slug>/index.html, /people/<slug>/, /careers/<slug>/
    python3 tools/build.py --preview DIR    also writes a flat copy with relative links (for previews)

Standard library only. Images and documents link to the files already uploaded to the WordPress site.
"""
import html
import json
import re
from collections import Counter
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://ca.programmer.co.ke'  # canonical base and asset host (the WordPress site); switch at launch
ORG = 'Communications Authority of Kenya'
SECTIONS = {'about': 'dd-about', 'licensing': 'dd-licensing', 'consumer': 'dd-consumer', 'procurement': 'dd-procurement', 'info': 'dd-info'}
MENU_IDS = ['dd-about', 'dd-licensing', 'dd-consumer', 'dd-procurement', 'dd-info']
DATA = {name: json.loads((ROOT / f'src/data/{name}.json').read_text())
        for name in ('documents', 'people', 'jobs', 'tenders', 'contracts', 'publications', 'library', 'news', 'schools')}
GROUP_PAGES = {
    'board-of-directors': 'Board of Directors',
    'management-team': 'Management Team',
    'universal-service-advisory-council': 'Universal Service Advisory Council',
}

esc = html.escape


def icon(name, cls='ca-icon'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="/assets/icons/sprite.svg#{name}"/></svg>'


def long_date(iso):
    d = date.fromisoformat(iso)
    return f'{d.day} {d:%B %Y}'


def file_size(n):
    return f'{n / 1048576:.1f} MB' if n >= 1048576 else f'{max(1, round(n / 1024))} KB'


# ── Shared chrome from the homepage ──
INDEX = (ROOT / 'index.html').read_text()


def rooted(s):
    """Homepage asset paths are relative (assets/…); inner pages live in folders, so make them root-relative."""
    return re.sub(r'(?<=["\s,])assets/', '/assets/', s)


BODY_START = rooted(INDEX[INDEX.index('<body>') + len('<body>'):INDEX.index('<main')])
BODY_END = rooted(INDEX[INDEX.index('</main>') + len('</main>'):INDEX.index('</body>')])


def menu(menu_id):
    """Section title, overview link and groups of links (with icon and description) from the main menu."""
    block = INDEX[INDEX.index(f'id="{menu_id}"'):]
    block = block[:min(i for i in (block.find('<li class="ca-nav__item">'), block.find('</nav>')) if i > 0)]
    title = re.search(r'<p class="ca-mega__title">(.*?)</p>', block).group(1)
    summary = re.search(r'<p class="ca-mega__summary">(.*?)</p>', block).group(1)
    overview = re.search(r'<a class="ca-dropdown__overview" href="([^"]+)"', block).group(1)
    groups = []
    for g in re.finditer(r'<p class="ca-dropdown__heading"[^>]*>(.*?)</p>\s*<ul[^>]*>(.*?)</ul>', block, re.S):
        links = re.findall(r'<a class="ca-mega__link" href="([^"]+)">.*?#([\w-]+)".*?<span class="ca-mega__label">(.*?)</span><span class="ca-mega__desc">(.*?)</span>', g.group(2), re.S)
        if links:
            groups.append({'title': g.group(1), 'links': [{'href': h, 'icon': i, 'label': l, 'desc': d} for h, i, l, d in links]})
        else:  # a quick-links band: plain links
            quick = re.findall(r'<a href="([^"]+)">(.*?)</a>', g.group(2))
            groups.append({'title': g.group(1), 'quick': True, 'links': [{'href': h, 'icon': 'arrow-right', 'label': l, 'desc': ''} for h, l in quick]})
    return {'title': title, 'summary': summary, 'overview': overview, 'groups': groups}


MENUS = {s: menu(i) for s, i in SECTIONS.items()}
ALL_LINKS = {l['href']: l for i in MENU_IDS for g in menu(i)['groups'] for l in g['links']}


def mark_current(chrome, path, section):
    """aria-current on links to this page (header, menus, footer); highlight the section in the main nav."""
    chrome = re.sub(rf'(<a\b[^>]*\shref="{re.escape(path)}")', r'\1 aria-current="page"', chrome)
    if section:
        chrome = chrome.replace(f'<li class="ca-nav__item">\n          <button class="ca-nav__trigger" type="button" aria-expanded="false" aria-controls="{SECTIONS[section]}">',
                                f'<li class="ca-nav__item is-current">\n          <button class="ca-nav__trigger" type="button" aria-expanded="false" aria-controls="{SECTIONS[section]}">')
    return chrome


# ── Components rendered from data ──
def file_icon(kind):
    """A page with a folded corner and a coloured file-type tag (decorative: the type is also in the text)."""
    return (f'<span class="ca-file ca-file--{kind.lower()}" aria-hidden="true"><svg viewBox="0 0 40 48" focusable="false">'
            '<path class="ca-file__page" d="M8 1.5h18.6l11.9 11.9V43.5a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3v-39a3 3 0 0 1 3-3z"/>'
            '<path class="ca-file__fold" d="M26.6 1.5v9a2.9 2.9 0 0 0 2.9 2.9h9"/>'
            '<path class="ca-file__lines" d="M11.5 20h14M11.5 25.5h19"/></svg>'
            f'<span class="ca-file__tag">{kind}</span></span>')


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def doc_item(d, extra='', attrs=''):
    """One document link: file icon, title, then type and size (plus any extra meta, e.g. category or year)."""
    lang = f' lang="{d["lang"]}"' if d.get('lang') else ''
    meta = ' · '.join(filter(None, [extra, f'{d["type"]}, {file_size(d["bytes"])}']))
    return (f'<li{attrs}><a class="ca-doc" href="{esc(d["url"])}">{file_icon(d["type"])}'
            f'<span class="ca-doc__text"><span class="ca-doc__title"{lang}>{esc(d["title"])}</span>'
            f'<span class="ca-doc__meta">{esc(meta)}</span></span>{icon("download", "ca-icon ca-doc__icon")}</a></li>')


def docs(list_id, opts='', items=None):
    items = DATA['documents'][list_id] if items is None else items
    cols = ' ca-docs--2' if 'cols=2' in opts else ''
    return f'<ul class="ca-docs{cols}" role="list">\n' + '\n'.join(doc_item(d, d.get('year', '') if 'years' in opts else '') for d in items) + '\n</ul>'


def library(category, opts=''):
    """Documents of one type from the WordPress document library (e.g. speeches, press statements); `search` adds a search box."""
    items = [d for d in DATA['library'] if slug(d['category']) == category]
    if not items:
        raise SystemExit(f'library: no documents of type {category}')
    if 'search' not in opts:
        return docs(None, opts, items)
    lis = [doc_item(d, d['year'] if 'years' in opts else '', f' data-text="{text_of(d["title"], d["year"])}"') for d in items]
    tools = search_field(f'{category}-q', 'q', f'Search {items[0]["category"].lower()}', 'Title or year')
    return listing('document|documents', lis, tools, 12, '<ul class="ca-docs" role="list" data-listing-items>')


def covers(list_id):
    """Reports shown by their covers (annual reports)."""
    lis = [(f'<li class="ca-cover"><a href="{esc(d["url"])}"><span class="ca-cover__img"><img src="{esc(d["cover"])}" alt="" width="{d["cover_w"]}" height="{d["cover_h"]}" loading="lazy" decoding="async"></span>'
            f'<span class="ca-cover__title">{esc(d["title"])}</span><span class="ca-cover__meta">{d["type"]}, {file_size(d["bytes"])}</span></a></li>')
           for d in DATA['documents'][list_id]]
    return '<ul class="ca-covers" role="list" data-reveal-stagger>\n' + '\n'.join(lis) + '\n</ul>'


# ── Long lists: search and filters (listing.js), every item in the HTML so they work without JavaScript ──
def listing(noun, items_html, tools, page_size, list_open, list_close='</ul>'):
    """list_open is the element holding the items (marked data-listing-items); noun is 'singular|plural'."""
    many = noun.split('|')[1]
    return f'''<div class="ca-listing" data-listing data-page-size="{page_size}" data-noun="{noun}">
<form class="ca-listing__tools" role="search" aria-label="Find {many}" data-js-only>
{tools}
</form>
<p class="ca-listing__status" role="status" data-listing-status>{len(items_html)} {many}</p>
{list_open}
{chr(10).join(items_html)}
{list_close}
<div class="ca-listing__empty" data-listing-empty hidden><p>No {many} match your search.</p><button class="ca-btn ca-btn--outline ca-btn--sm" type="button" data-listing-reset>Clear search and filters</button></div>
<div class="ca-listing__more" data-js-only><button class="ca-btn ca-btn--outline" type="button" data-listing-more>Show more</button></div>
</div>'''


def search_field(id_, name, label, placeholder):
    return (f'<div class="ca-field ca-listing__search"><label for="{id_}">{label}</label>'
            f'<input class="ca-input" type="search" id="{id_}" name="{name}" placeholder="{placeholder}" autocomplete="off" data-listing-q></div>')


def select_field(id_, name, label, key, options, all_label):
    opts = ''.join(f'<option value="{v}">{esc(t)}</option>' for v, t in options)
    return (f'<div class="ca-field"><label for="{id_}">{label}</label><select class="ca-input" id="{id_}" name="{name}" data-listing-filter="{key}">'
            f'<option value="">{all_label}</option>{opts}</select></div>')


def text_of(*parts):
    return esc(' '.join(p for p in parts if p).lower(), quote=True)


def tender_open(t):
    return bool(t['closing']) and date.fromisoformat(t['closing']) >= date.today()


def tenders():
    items = []
    for t in DATA['tenders']:
        state = 'open' if tender_open(t) else 'closed'
        files = ''.join(
            f'<li><a class="ca-filelink" href="{esc(f["url"])}"><span class="ca-filelink__tag ca-filelink__tag--{f["type"].lower()}">{f["type"]}</span>'
            f'<span>{esc(f["label"])}<span class="ca-vh">: {esc(t["title"])}</span><span class="ca-filelink__size">{file_size(f["bytes"])}</span></span></a></li>' for f in t['files'])
        dates = ''.join(f'<div><dt>{k}</dt><dd><time datetime="{v}">{long_date(v)}</time></dd></div>' for k, v in (('Opened', t['opening']), ('Closing date', t['closing'])) if v)
        items.append(
            f'<li class="ca-tender" data-status="{state}" data-fy="{t["fy"].replace("/", "-")}" data-text="{text_of(t["title"], t["number"])}">'
            f'<h2 class="ca-tender__title">{esc(t["title"])}</h2>'
            f'<dl class="ca-tender__facts"><div><dt>Tender number</dt><dd>{esc(t["number"])}</dd></div>'
            f'<div><dt>Status</dt><dd><span class="ca-badge ca-badge--{state}">{state.title()}</span></dd></div>{dates}</dl>'
            + (f'<ul class="ca-filelinks" role="list">{files}</ul>' if files else '') + '</li>')
    years = sorted({t['fy'] for t in DATA['tenders'] if t['fy']}, reverse=True)
    tools = (search_field('tender-q', 'tender_q', 'Search tenders', 'Title or tender number')
             + select_field('tender-status', 'tender_status', 'Status', 'status', [('open', 'Open'), ('closed', 'Closed')], 'All tenders')
             + select_field('tender-fy', 'tender_fy', 'Financial year', 'fy', [(y.replace('/', '-'), y) for y in years], 'All years'))
    return listing('tender|tenders', items, tools, 10, '<ul class="ca-tenders" role="list" data-listing-items>')


def open_tenders_notice(elsewhere=False):
    n = sum(tender_open(t) for t in DATA['tenders'])
    if n:
        return f'<p class="ca-lead">There {"is" if n == 1 else "are"} {n} open tender{"" if n == 1 else "s"}.</p>'
    return (f'<div class="ca-callout">{icon("info")}<p class="ca-callout__title">There are no open tenders at the moment</p>'
            f'<p>Past tenders and their documents are listed {"on the Tenders page" if elsewhere else "below"}. To be considered for future opportunities, '
            f'<a href="/supplier-registration/">register as a supplier</a>.</p></div>')


def money(v):
    return '<span class="ca-vh">Not published</span><span aria-hidden="true">—</span>' if v in ('', '—') else esc(v)


def awarded_date(s):
    try:
        return long_date(datetime.strptime(s, '%d %b, %Y').date().isoformat())
    except ValueError:
        return s


def contracts():
    rows = []
    for c in DATA['contracts']['contracts']:
        when = awarded_date(c['awarded']) if c['awarded'] else ''
        ref = c['ref'].strip('—')
        rows.append(f'<tr data-text="{text_of(ref, c["description"], c["supplier"])}"><td data-label="Reference">{money(c["ref"])}</td>'
                    f'<th scope="row" data-label="Description">{esc(c["description"])}</th><td data-label="Supplier">{esc(c["supplier"])}</td>'
                    f'<td class="ca-num" data-label="Value (KES)">{money(c["value"])}</td><td data-label="Awarded">{money(when)}</td></tr>')
    tools = search_field('contract-q', 'contract_q', 'Search awarded contracts', 'Description, supplier or reference')
    table = ('<div class="ca-tablewrap" role="region" aria-labelledby="contracts-caption" tabindex="0"><table class="ca-table ca-table--stack">'
             '<caption id="contracts-caption">Contracts awarded by the Authority</caption><thead><tr><th scope="col">Reference</th><th scope="col">Description</th>'
             '<th scope="col">Supplier</th><th scope="col" class="ca-num">Value (KES)</th><th scope="col">Awarded</th></tr></thead><tbody data-listing-items>')
    return listing('contract|contracts', rows, tools, 25, table, '</tbody></table></div>')


def publications():
    items = [doc_item(p, p['year'], f' data-pubyear="{p["year"] or "undated"}" data-text="{text_of(p["title"], p["year"])}"') for p in DATA['publications']]
    years = sorted({p['year'] for p in DATA['publications'] if p['year']}, reverse=True)
    tools = (search_field('pub-q', 'q', 'Search publications', 'Title, e.g. annual report')
             + select_field('pub-year', 'year', 'Year', 'pubyear', [(y, y) for y in years] + [('undated', 'Undated')], 'All years'))
    return listing('publication|publications', items, tools, 15, '<ul class="ca-docs" role="list" data-listing-items>')


def library_listing():
    counts = Counter(d['category'] for d in DATA['library'])
    items = [doc_item(d, ' · '.join(filter(None, [d['category'], d['year']])), f' data-category="{slug(d["category"])}" data-text="{text_of(d["title"], d["category"], d["year"])}"')
             for d in DATA['library']]
    tools = (search_field('doc-q', 'q', 'Search documents', 'Title or subject')
             + select_field('doc-type', 'type', 'Document type', 'category', [(slug(k), f'{k} ({v})') for k, v in sorted(counts.items())], 'All types'))
    return listing('document|documents', items, tools, 15, '<ul class="ca-docs" role="list" data-listing-items>')


def schools():
    """Schools connected under the Education Broadband Connectivity Project, with search and a county filter."""
    rows = [f'<tr data-county="{slug(r["county"])}" data-text="{text_of(r["school"], r["subcounty"], r["county"])}"><th scope="row" data-label="School">{esc(r["school"])}</th>'
            f'<td data-label="Sub-county">{esc(r["subcounty"])}</td><td data-label="County">{esc(r["county"])}</td></tr>' for r in DATA['schools']]
    counties = sorted({r['county'] for r in DATA['schools']})
    tools = (search_field('school-q', 'q', 'Search schools', 'School or sub-county')
             + select_field('school-county', 'county', 'County', 'county', [(slug(c), c) for c in counties], 'All 47 counties'))
    table = ('<div class="ca-tablewrap" role="region" aria-labelledby="schools-caption" tabindex="0"><table class="ca-table ca-table--stack">'
             '<caption id="schools-caption">Schools connected under the Education Broadband Connectivity Project</caption>'
             '<thead><tr><th scope="col">School</th><th scope="col">Sub-county</th><th scope="col">County</th></tr></thead><tbody data-listing-items>')
    return listing('school|schools', rows, tools, 25, table, '</tbody></table></div>')


def toc(page):
    """"On this page" links to the page's second-level headings that carry an id."""
    heads = re.findall(r'<h2 id="([\w-]+)"[^>]*>(.*?)</h2>', page['body'])
    links = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    return f'<nav class="ca-toc" aria-label="On this page"><p class="ca-toc__title">On this page</p><ul role="list">{links}</ul></nav>'


def news_card(n, tag='h2', sizes='(min-width: 1100px) 360px, (min-width: 700px) 45vw, 92vw'):
    """A story card (the homepage news component), with the image above the date and title."""
    if n['image']:
        i = n['image']
        media = (f'<img src="{esc(i["card"])}" srcset="{esc(i["srcset"])}" sizes="{sizes}" alt="{esc(i["alt"])}" '
                 f'width="{i["card_w"]}" height="{i["card_h"]}" loading="lazy" decoding="async">')
    else:
        media = f'<span class="ca-story__noimg">{icon("newspaper")}</span>'
    return (f'<article class="ca-story ca-story--card"><div class="ca-story__media">{media}</div><div class="ca-story__body">'
            f'<p class="ca-story__date"><time datetime="{n["date"]}">{long_date(n["date"])}</time></p>'
            f'<{tag} class="ca-story__title"><a href="/{n["slug"]}/">{esc(n["title"])}</a></{tag}>'
            f'<span class="ca-story__more" aria-hidden="true">Read more{icon("arrow-right")}</span></div></article>')


def excerpt(text, limit=220):
    return text if len(text) <= limit else text[:limit].rsplit(' ', 1)[0].rstrip(',;:') + '…'


def news():
    lead = next((n for n in DATA['news'] if n['sticky']), DATA['news'][0])
    i = lead['image']
    lead_html = (f'<article class="ca-story ca-story--feature"><div class="ca-story__media"><img src="{esc(i["src"])}" srcset="{esc(i["srcset"])}" '
                 f'sizes="(min-width: 1100px) 520px, 92vw" alt="{esc(i["alt"])}" width="{i["width"]}" height="{i["height"]}" decoding="async"></div>'
                 f'<div class="ca-story__body"><p class="ca-eyebrow">Featured</p><p class="ca-story__date"><time datetime="{lead["date"]}">{long_date(lead["date"])}</time></p>'
                 f'<h2 class="ca-story__title"><a href="/{lead["slug"]}/">{esc(lead["title"])}</a></h2>'
                 f'<p class="ca-story__summary">{esc(excerpt(lead["excerpt"]))}</p>'
                 f'<span class="ca-story__more" aria-hidden="true">Read more{icon("arrow-right")}</span></div></article>')
    items = [f'<li data-pubyear="{n["date"][:4]}" data-text="{text_of(n["title"], n["excerpt"])}">{news_card(n, "h3")}</li>' for n in DATA['news'] if n is not lead]
    years = sorted({n['date'][:4] for n in DATA['news']}, reverse=True)
    tools = (search_field('news-q', 'q', 'Search news', 'Search the news')
             + select_field('news-year', 'year', 'Year', 'pubyear', [(y, y) for y in years], 'All years'))
    return (lead_html + '\n<h2 id="all-news">All news</h2>\n'
            + listing('story|stories', items, tools, 12, '<ul class="ca-storygrid" role="list" data-listing-items>'))


def latest_news(count):
    return '<ul class="ca-storygrid ca-storygrid--3" role="list">' + ''.join(f'<li>{news_card(n, "h3")}</li>' for n in DATA['news'][:int(count)]) + '</ul>'



def people(group):
    members = sorted((p for p in DATA['people'] for g in p['groups'] if g['group'] == group),
                     key=lambda p: next(g['order'] for g in p['groups'] if g['group'] == group))
    cards = []
    for p in members:
        role = next(g['role'] for g in p['groups'] if g['group'] == group)
        img = (f'<img src="{esc(p["photo"])}" srcset="{esc(p["srcset"])}" sizes="(min-width: 1100px) 220px, (min-width: 600px) 30vw, 45vw" '
               f'alt="" width="400" height="480" loading="lazy" decoding="async">')
        name = esc(p['name'])
        if has_bio(p):
            name = f'<a href="/people/{p["slug"]}/" data-profile>{name}</a>'
        cards.append(f'<li class="ca-person{" has-profile" if has_bio(p) else ""}"><div class="ca-person__photo">{img}</div>'
                     f'<h2 class="ca-person__name">{name}</h2><p class="ca-person__role">{esc(role)}</p></li>')
    return (f'<ul class="ca-people" role="list" data-profiles data-reveal-stagger>\n' + '\n'.join(cards) + '\n</ul>\n'
            f'<p class="ca-people__note">Select a name to read their profile.</p>')


def has_bio(p):
    return len(re.sub(r'<[^>]+>', '', p['bio'])) > 40


def linkcard(l, tag='h3'):
    return (f'<li class="ca-linkcard"><span class="ca-linkcard__icon">{icon(l["icon"])}</span>'
            f'<{tag} class="ca-linkcard__title"><a href="{l["href"]}">{l["label"]}</a></{tag}>'
            f'<p class="ca-linkcard__desc">{l["desc"]}</p>{icon("arrow-right", "ca-icon ca-linkcard__arrow")}</li>')


def subpages(section, current):
    """The section's pages as link cards, grouped as in the main menu."""
    out = []
    for g in MENUS[section]['groups']:
        if g.get('quick'):
            pills = ''.join(f'<li><a class="ca-pill" href="{l["href"]}">{l["label"]}{icon("arrow-right", "ca-icon ca-icon--sm")}</a></li>' for l in g['links'])
            out.append(f'<div class="ca-linkgroup"><h3 class="ca-linkgroup__title">{g["title"]}</h3>\n<ul class="ca-pills" role="list">{pills}</ul></div>')
            continue
        cards = [linkcard(l, 'h4') for l in g['links'] if l['href'] != current]
        if cards:
            out.append(f'<div class="ca-linkgroup"><h3 class="ca-linkgroup__title">{g["title"]}</h3>\n'
                       f'<ul class="ca-linkcards" role="list" data-reveal-stagger>\n' + '\n'.join(cards) + '\n</ul></div>')
    return '<div class="ca-linkgroups">\n' + '\n'.join(out) + '\n</div>'


def related(paths):
    """Link cards for a few related pages, using the menu's labels, icons and descriptions."""
    missing = [p for p in paths.split(',') if p not in ALL_LINKS]
    if missing:
        raise SystemExit(f'related: not in the main menu: {missing}')
    cards = [linkcard(ALL_LINKS[p]) for p in paths.split(',')]
    return '<ul class="ca-linkcards ca-linkcards--related" role="list">\n' + '\n'.join(cards) + '\n</ul>'


DIRECTOR_FIELDS = [  # (key, label, type, error message for director 1)
    ('name', 'Name', 'text', 'Enter the director’s name'),
    ('pin', 'KRA PIN', 'text', 'Enter the director’s KRA PIN'),
    ('gender', 'Gender', 'select', 'Select the director’s gender'),
    ('nationality', 'Nationality', 'text', 'Enter the director’s nationality'),
    ('phone', 'Phone number', 'tel', 'Enter the director’s phone number'),
    ('email', 'Email address', 'email', 'Enter the director’s email address'),
    ('share', 'Share (%)', 'number', 'Enter the director’s share as a percentage'),
]
UPLOAD_HINT = 'Accepted: PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG, PNG. Maximum 10 MB.'
UPLOAD_TYPES = '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png'


def directors(count):
    """Director fieldsets for supplier registration (field names as in the WordPress form); directors.js adds them one at a time."""
    out = []
    for n in range(1, int(count) + 1):
        req = n == 1  # only the first director is required
        star = ' <span class="ca-req" aria-hidden="true">*</span>' if req else ''
        attrs = ' required' if req else ''
        fields = []
        for key, label, kind, error in DIRECTOR_FIELDS:
            fid, name = f'sr-d{n}-{key}', f'cak_data[director_{n}_{key}]'
            err = f' data-error="{error}"' if req else ''
            if kind == 'select':
                control = (f'<select class="ca-input" id="{fid}" name="{name}"{attrs}><option value="">Please choose</option><option value="female">Female</option>'
                           '<option value="male">Male</option><option value="unspecified">Prefer not to say</option></select>')
            else:
                extra = ' min="0" max="100" step="0.01" inputmode="decimal"' if kind == 'number' else ''
                control = f'<input class="ca-input" id="{fid}" name="{name}" type="{kind}"{extra}{attrs}>'
            fields.append(f'<div class="ca-field"{err}><label for="{fid}">{label}{star}</label>{control}</div>')
        fid = f'sr-d{n}-id'
        err = ' data-error="Upload a copy of the director’s national ID"' if req else ''
        upload = (f'<div class="ca-field"{err}><label for="{fid}">National ID copy{star}</label>'
                  f'<p class="ca-hint" id="{fid}-hint">{UPLOAD_HINT}</p><input class="ca-input" id="{fid}" name="cak_file_director_{n}_id" type="file" accept="{UPLOAD_TYPES}" aria-describedby="{fid}-hint"{attrs}></div>')
        legend = f'Director {n}' + ('' if req else ' <span class="ca-optional">(optional)</span>')
        out.append(f'<fieldset class="ca-fieldset" data-director>\n<legend>{legend}</legend>\n<div class="ca-fields-2">\n' + '\n'.join(fields) + f'\n</div>\n{upload}\n</fieldset>')
    return ('<div class="ca-directors" data-directors>\n' + '\n'.join(out)
            + f'\n<button class="ca-btn ca-btn--outline ca-directors__add" type="button" data-director-add data-js-only>{icon("plus")}Add another director</button>'
            + '\n<p class="ca-vh" role="status" data-director-status></p>\n</div>')


def deadline(job):
    return f'{long_date(job["deadline"])}, {job["deadline_time"]}'


def is_open(job):
    return date.fromisoformat(job['deadline']) >= date.today()


def status(job):
    return '<span class="ca-badge ca-badge--open">Open</span>' if is_open(job) else '<span class="ca-badge ca-badge--closed">Closed</span>'


def jobs():
    cards = []
    for j in DATA['jobs']:
        where = f'<span>{icon("pin", "ca-icon ca-icon--sm")}{esc(j["location"])}</span>' if j['location'] else ''
        cards.append(f'<li class="ca-job"><h3 class="ca-job__title"><a href="/careers/{j["slug"]}/">{esc(j["title"])}</a></h3>'
                     f'<p class="ca-job__meta">{status(j)}<span>{icon("calendar", "ca-icon ca-icon--sm")}Deadline: {esc(deadline(j))}</span>{where}</p></li>')
    return '<ul class="ca-jobs" role="list">\n' + '\n'.join(cards) + '\n</ul>'


DIALOG = rooted(re.search(r'    <dialog class="ca-video-dialog.*?</dialog>', INDEX, re.S).group(0))


def video(vid, opts):
    """One video that plays in the same in-page player as the homepage's video row."""
    o = dict(re.findall(r'(\w+)="([^"]*)"', opts))
    return (f'<div class="ca-video-cta" data-videos><a href="https://www.youtube.com/watch?v={vid}" data-video="{vid}" title="{esc(o["title"])}">'
            f'<span class="ca-video-cta__play">{icon("play")}</span><span>{esc(o["label"])}<small>Video, {o["duration"]}</small></span></a>\n{DIALOG}\n</div>')


SHORTCODES = {
    'video': lambda arg, opts, page: video(arg, opts),
    'docs': lambda arg, opts, page: docs(arg, opts),
    'people': lambda arg, opts, page: people(arg),
    'subpages': lambda arg, opts, page: subpages(arg, page['path']),
    'related': lambda arg, opts, page: related(opts or arg),
    'jobs': lambda arg, opts, page: jobs(),
    'library': lambda arg, opts, page: library(arg, opts),
    'covers': lambda arg, opts, page: covers(arg),
    'tenders': lambda arg, opts, page: open_tenders_notice(True) if arg == 'notice' else open_tenders_notice() + tenders(),
    'contracts': lambda arg, opts, page: contracts(),
    'publications': lambda arg, opts, page: publications(),
    'documents': lambda arg, opts, page: library_listing(),
    'news': lambda arg, opts, page: news(),
    'latestnews': lambda arg, opts, page: latest_news(arg),
    'directors': lambda arg, opts, page: directors(arg),
    'schools': lambda arg, opts, page: schools(),
    'toc': lambda arg, opts, page: toc(page),
}


def expand(body, page):
    return re.sub(r'<!--(\w+):([\w-]+)\s*([^>]*?)-->', lambda m: SHORTCODES[m.group(1)](m.group(2), m.group(3), page), body)


# ── Page assembly ──
def section_nav(section, path, ancestor=None):
    m = MENUS[section]
    groups = []
    for g in m['groups']:
        lis = []
        for l in g['links']:
            cur = ' aria-current="page"' if l['href'] == path else (' class="is-ancestor"' if l['href'] == ancestor else '')
            lis.append(f'<li><a href="{l["href"]}"{cur}>{l["label"]}</a></li>')
        groups.append(f'<p class="ca-subnav__heading">{g["title"]}</p>\n<ul role="list">{"".join(lis)}</ul>')
    over = ' aria-current="page"' if m['overview'] == path else ''
    return (f'<nav class="ca-subnav" aria-label="{m["title"]}">\n<details class="ca-subnav__box" open data-subnav>\n'
            f'<summary class="ca-subnav__summary">In this section: {m["title"]}{icon("chevron-down", "ca-icon ca-icon--sm")}</summary>\n'
            f'<div class="ca-subnav__body"><a class="ca-subnav__overview" href="{m["overview"]}"{over}>{m["title"]} overview</a>\n'
            + '\n'.join(groups) + '\n</div>\n</details>\n</nav>')


def crumbs(page):
    trail = [('Home', '/')]
    if page.get('section') and MENUS[page['section']]['overview'] != page['path']:
        trail.append((html.unescape(MENUS[page['section']]['title']), MENUS[page['section']]['overview']))  # menu text is HTML
    trail += page.get('trail', [])
    items = ''.join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in trail)
    nav = (f'<nav class="ca-breadcrumb" aria-label="Breadcrumb"><ol role="list">{items}'
           f'<li><span aria-current="page">{esc(page["title"])}</span></li></ol></nav>')
    ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': t, 'item': SITE + h} for i, (t, h) in enumerate(trail + [(page['title'], page['path'])], 1)]}
    return nav, json.dumps(ld, ensure_ascii=False)


def actions(spec):
    out = []
    for item in filter(None, (s.strip() for s in spec.split(';'))):
        label, href, style = (x.strip() for x in item.split('|'))
        ext = href.startswith('http') and not href.startswith(SITE)
        ico = icon('external') + '<span class="ca-vh">(external site)</span>' if ext else icon('arrow-right')
        out.append(f'<a class="ca-btn ca-btn--{style}" href="{esc(href)}">{esc(label)}{ico}</a>')
    return f'<div class="ca-actions">{"".join(out)}</div>' if out else ''


def render(page):
    path, section = page['path'], page.get('section')
    nav, ld = crumbs(page)
    title = f'{page["title"]} | {ORG}'
    desc = page.get('description') or re.sub(r'<[^>]+>', '', page.get('summary', ''))
    hero = f'''  <section class="ca-panel ca-panel--fx ca-on-dark ca-page-hero" aria-labelledby="page-title" data-fx data-fx-density="0.45" data-fx-static>
    <canvas class="ca-fx" aria-hidden="true" data-fx-canvas></canvas>
    <div class="ca-container">
      {nav}
      <h1 id="page-title">{esc(page["title"])}</h1>
      {f'<p class="ca-page-hero__summary">{page["summary"]}</p>' if page.get('summary') else ''}
      {actions(page.get('actions', ''))}
    </div>
  </section>'''
    body = expand(page['body'], page)
    if page.get('layout') == 'landing':
        main = hero + '\n' + body
    else:
        aside = f'<aside class="ca-page__aside">{section_nav(section, path, page.get("ancestor"))}</aside>' if section else ''
        main = f'''{hero}
  <div class="ca-panel ca-panel--white ca-page">
    <div class="ca-container ca-page__layout{"" if section else " ca-page__layout--single"}">
      {aside}
      <div class="ca-page__content ca-prose">
{body}
      </div>
    </div>
  </div>'''
    chrome_start = mark_current(BODY_START, path, section)
    chrome_end = mark_current(BODY_END, path, None)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <script>document.documentElement.classList.add('js');if(/[?&]placeholders\\b/.test(location.search))document.documentElement.classList.add('show-placeholders');</script>
  <link rel="canonical" href="{SITE}{path}">
  <meta name="theme-color" content="#1D51A3">
  <link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
  <link rel="icon" href="/assets/img/favicon-192.png" sizes="192x192">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{ORG}">
  <meta property="og:title" content="{esc(page["title"])}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:image" content="{SITE}/assets/img/og-placeholder.png">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="/assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/maitree-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/layout.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/sections.css">
  <link rel="stylesheet" href="/assets/css/overlays.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
  <link rel="stylesheet" href="/assets/css/motion.css">
  <script type="module" src="/assets/js/main.js"></script>
  <script type="application/ld+json">{ld}</script>
</head>
<body>{chrome_start}<main class="ca-main ca-main--page" id="main" tabindex="-1">
{main}
</main>{chrome_end}</body>
</html>
'''


def parse(path):
    text = path.read_text()
    m = re.match(r'\s*<!--\n(.*?)\n-->\n', text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        if line.strip():
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    meta['body'] = text[m.end():]
    meta['slug'] = path.stem
    meta['path'] = f'/{path.stem}/'
    if 'parent' in meta:  # a page not in the menu, e.g. a project under Universal Access Projects
        label, href = (x.strip() for x in meta['parent'].split('|'))
        meta['ancestor'], meta['trail'] = href, [(label, href)]
    return meta


def person_pages():
    pages = []
    for p in DATA['people']:
        if not has_bio(p):
            continue
        g = p['groups'][0]
        roles = '; '.join(dict.fromkeys(x['role'] for x in p['groups']))
        img = (f'<img src="{esc(p["photo"])}" srcset="{esc(p["srcset"])}" sizes="(min-width: 768px) 320px, 70vw" '
               f'alt="{esc(p["name"])}" width="400" height="480" decoding="async">')
        also = [GROUP_PAGES[x['group']] for x in p['groups'][1:]]
        member = f'<p class="ca-profile__also">Also listed under {" and ".join(also)}.</p>' if also else ''
        body = (f'<article class="ca-profile" data-profile-content>\n<div class="ca-profile__photo">{img}</div>\n'
                f'<div class="ca-profile__text"><p class="ca-profile__role">{esc(roles)}</p>\n{p["bio"]}\n{member}</div>\n</article>\n'
                f'<p class="ca-back"><a class="ca-link ca-link--back" href="/{g["group"]}/">{icon("arrow-left")}Back to {GROUP_PAGES[g["group"]]}</a></p>')
        pages.append({'title': p['name'], 'summary': esc(roles), 'description': f'{p["name"]}, {roles}, {ORG}.',
                      'section': 'about', 'path': f'/people/{p["slug"]}/', 'ancestor': f'/{g["group"]}/',
                      'trail': [(GROUP_PAGES[g['group']], f'/{g["group"]}/')], 'body': body})
    return pages


def job_pages():
    pages = []
    for j in DATA['jobs']:
        where = f'<li>{icon("pin", "ca-icon ca-icon--sm")}{esc(j["location"])}</li>' if j['location'] else ''
        body = (f'<ul class="ca-job__facts" role="list"><li>{status(j)}</li><li>{icon("calendar", "ca-icon ca-icon--sm")}Deadline: {esc(deadline(j))}</li>{where}</ul>\n'
                f'{j["body"]}\n<p class="ca-back"><a class="ca-link ca-link--back" href="/careers/">{icon("arrow-left")}All vacancies</a></p>')
        state = 'Open for applications' if is_open(j) else 'Applications have closed'
        pages.append({'title': j['title'], 'summary': f'{state}. Deadline: {esc(deadline(j))}.',
                      'section': 'about', 'path': f'/careers/{j["slug"]}/', 'ancestor': '/careers/',
                      'trail': [('Careers', '/careers/')], 'body': body})
    return pages


def article_body(n):
    """WordPress post content, tidied: a lead sentence set as a heading becomes a lead paragraph (no skipped levels), tables scroll in a labelled region."""
    body = n['body']
    if '<h2' not in body:
        body = re.sub(r'<h3>(.*?)</h3>', r'<p class="ca-lead">\1</p>', body, flags=re.S)

    def wrap(m):
        cap = re.search(r'<caption>(.*?)</caption>', m.group(0), re.S)
        label = f' aria-label="{esc(re.sub(r"<[^>]+>", "", cap.group(1)))}"' if cap else ' aria-label="Table"'
        return f'<div class="ca-tablewrap" role="region"{label} tabindex="0">{m.group(0)}</div>'
    return re.sub(r'<table>.*?</table>', wrap, body, flags=re.S)


def news_pages():
    pages = []
    for n in DATA['news']:
        fig = ''
        if n['image']:
            i = n['image']
            fig = (f'<figure class="ca-article__figure"><img src="{esc(i["src"])}" srcset="{esc(i["srcset"])}" sizes="(min-width: 1100px) 800px, 92vw" '
                   f'alt="{esc(i["alt"])}" width="{i["width"]}" height="{i["height"]}" decoding="async"></figure>')
        more = [m for m in DATA['news'] if m is not n][:3]
        body = (f'<article class="ca-article">{fig}\n<div class="ca-article__body">\n{article_body(n)}\n</div></article>\n'
                f'<h2>More news</h2>\n<ul class="ca-storygrid ca-storygrid--3" role="list">' + ''.join(f'<li>{news_card(m, "h3")}</li>' for m in more) + '</ul>\n'
                f'<p class="ca-back"><a class="ca-link ca-link--back" href="/news/">{icon("arrow-left")}All news</a></p>')
        pages.append({'title': n['title'], 'summary': f'<time datetime="{n["date"]}">{long_date(n["date"])}</time>', 'description': n['excerpt'][:300],
                      'section': 'info', 'path': f'/{n["slug"]}/', 'ancestor': '/news/', 'trail': [('News', '/news/')], 'body': body, 'kind': 'article'})
    return pages


def build():
    pages = [parse(p) for p in sorted((ROOT / 'src/pages').glob('*.html'))] + person_pages() + job_pages() + news_pages()
    for page in pages:
        out = ROOT / page['path'].strip('/') / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(page))
    return pages


# ── Flat preview copy (relative links, no folders) ──
def preview(pages, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    flat = {p['path']: p['path'].strip('/').replace('/', '-') + '.html' for p in pages}
    flat['/'] = 'index.html'

    def relink(s):
        s = re.sub(r'(?<=["\s,(])/assets/', 'assets/', s)

        def href(m):
            url = m.group(2)
            target = url.split('#')[0].split('?')[0]
            if target in flat:
                return f'{m.group(1)}"{flat[target]}{url[len(target):]}"'
            return f'{m.group(1)}"{SITE}{url}"'  # pages not built yet open on the WordPress site
        return re.sub(r'(\b(?:href|action)=)"(/(?!/)[^"]*)"', href, s)

    for p in pages:
        (outdir / flat[p['path']]).write_text(relink(render(p)))
    # the homepage, in the wrapper-less form the preview host expects
    home = relink(INDEX)
    home = re.sub(r'^<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>',
                  '<!-- Preview build of index.html (document wrapper supplied by the host) -->\n<title>', home)
    home = home.replace("<script>document.documentElement.classList.add('js');", "<script>document.documentElement.lang='en';document.documentElement.classList.add('js');", 1)
    home = home.replace('</head>\n<body>\n', '\n', 1)
    home = home[:home.rindex('</body>')]
    (outdir / 'ca-homepage.html').write_text(home)
    return flat


if __name__ == '__main__':
    built = build()
    print(f'built {len(built)} pages')
    if '--preview' in sys.argv:
        files = preview(built, sys.argv[sys.argv.index('--preview') + 1])
        print(f'preview: {len(files)} files')
