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
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://ca.programmer.co.ke'  # canonical base and asset host (the WordPress site); switch at launch
ORG = 'Communications Authority of Kenya'
SECTIONS = {'about': 'dd-about', 'consumer': 'dd-consumer'}  # sections built so far
MENU_IDS = ['dd-about', 'dd-licensing', 'dd-consumer', 'dd-procurement', 'dd-info']
DATA = {name: json.loads((ROOT / f'src/data/{name}.json').read_text()) for name in ('documents', 'people', 'jobs')}
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
        groups.append({'title': g.group(1), 'links': [{'href': h, 'icon': i, 'label': l, 'desc': d} for h, i, l, d in links]})
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


def docs(list_id, opts=''):
    items = DATA['documents'][list_id]
    cols = ' ca-docs--2' if 'cols=2' in opts else ''
    lis = []
    for d in items:
        lang = f' lang="{d["lang"]}"' if d.get('lang') else ''
        lis.append(
            f'<li><a class="ca-doc" href="{esc(d["url"])}">'
            f'{file_icon(d["type"])}'
            f'<span class="ca-doc__text"><span class="ca-doc__title"{lang}>{esc(d["title"])}</span>'
            f'<span class="ca-doc__meta">{d["type"]}, {file_size(d["bytes"])}</span></span>'
            f'{icon("download", "ca-icon ca-doc__icon")}</a></li>')
    return f'<ul class="ca-docs{cols}" role="list">\n' + '\n'.join(lis) + '\n</ul>'


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
        trail.append((MENUS[page['section']]['title'], MENUS[page['section']]['overview']))
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
    updated = f'<p class="ca-page__updated">Page last updated <time datetime="{page["updated"]}">{long_date(page["updated"])}</time></p>' if page.get('updated') else ''
    if page.get('layout') == 'landing':
        main = hero + '\n' + body + (f'\n  <div class="ca-container ca-page__foot">{updated}</div>' if updated else '')
    else:
        aside = f'<aside class="ca-page__aside">{section_nav(section, path, page.get("ancestor"))}</aside>' if section else ''
        main = f'''{hero}
  <div class="ca-panel ca-panel--white ca-page">
    <div class="ca-container ca-page__layout{"" if section else " ca-page__layout--single"}">
      {aside}
      <div class="ca-page__content ca-prose">
{body}
      {updated}
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
                      'trail': [(GROUP_PAGES[g['group']], f'/{g["group"]}/')], 'updated': p['updated'], 'body': body})
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


def build():
    pages = [parse(p) for p in sorted((ROOT / 'src/pages').glob('*.html'))] + person_pages() + job_pages()
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
