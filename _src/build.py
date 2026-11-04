#!/usr/bin/env python3
"""Theme Radar static site builder.

Usage: python3 build.py DATA_DIR OUT_DIR [--asof YYYY-MM-DD] [--base https://example.github.io]

DATA_DIR holds the radar outputs: baskets.json (own baskets), members.json,
etfs.json, themes.json, rrg.json, theme_members.json.
Content (research markdown, baskets.yaml, threads.yaml, img/) lives in ./content.
Everything public is built from an allow-list of fields. Private datasets
(Citrini, methodology, book weights) are never read.
"""
import json, os, re, sys, shutil, html, math, datetime as dt, subprocess
from email.utils import format_datetime
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
SITE_NAME = 'Theme Radar'
TAGLINE = 'Thematic equity research and the baskets that track it.'

# ---------- helpers ----------
E = html.escape
def pct(v, d=1):
    if v is None or (isinstance(v, float) and math.isnan(v)): return '—'
    return f"{v*100:+.{d}f}%"
def cls(v):
    if v is None: return ''
    return 'up' if v > 0 else ('dn' if v < 0 else '')
def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def dfmt(d):
    if isinstance(d, str): d = dt.date.fromisoformat(d)
    return f"{d.day} {d.strftime('%b %Y')}"

LABEL_TEXT = {
    'Research now': 'Turning up after a weak six months. Early, so the reason behind the move needs checking.',
    'Already moving': 'A broad move inside an established uptrend, not yet stretched to highs.',
    "Don't chase": 'Many names already near 52-week highs.',
    'Watch': 'Early improvement, not broad enough to act on yet.',
    'Avoid for now': 'Broad selling across the group this week.',
    'No signal': 'Nothing clear either way.',
}
LABEL_CLASS = {'Research now': 'l-res', 'Already moving': 'l-mov', "Don't chase": 'l-chase',
               'Watch': 'l-watch', 'Avoid for now': 'l-avoid', 'No signal': 'l-none'}
QUAD_CLASS = {'Leading': 'q-lead', 'Weakening': 'q-weak', 'Lagging': 'q-lag', 'Improving': 'q-imp'}
def chip(label):
    return f'<span class="chip {LABEL_CLASS.get(label, "l-none")}">{E(label or "—")}</span>'
def qchip(q):
    return f'<span class="chip {QUAD_CLASS.get(q, "")}">{E(q or "—")}</span>'

CSS = r"""
:root{--bg:#fbfaf7;--fg:#1c1b19;--mute:#6b675f;--line:#e4e0d8;--card:#ffffff;--acc:#1f4e79;--up:#1b7a3a;--dn:#b3261e;
--lead:#1b7a3a;--weak:#b7791f;--lag:#b3261e;--imp:#1f4e79}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141412;--fg:#ecebe6;--mute:#a19d93;--line:#2c2b28;--card:#1c1b19;--acc:#8fb8e0;--up:#5cc27c;--dn:#ef7a6f;--lead:#5cc27c;--weak:#e2b155;--lag:#ef7a6f;--imp:#8fb8e0}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header.site{border-bottom:1px solid var(--line);background:var(--card)}
.wrap{max-width:860px;margin:0 auto;padding:0 16px}
.top{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 20px;padding:14px 0}
.brand{font-weight:700;font-size:18px;color:var(--fg);letter-spacing:.2px}
nav a{margin-right:16px;color:var(--mute);font-size:15px}nav a.on{color:var(--fg);font-weight:600}
main{padding:24px 0 48px}
h1{font-size:28px;line-height:1.25;margin:4px 0 8px;font-family:Georgia,"Times New Roman",serif}
h2{font-size:20px;margin:32px 0 10px;font-family:Georgia,"Times New Roman",serif}
h3{font-size:17px;margin:22px 0 8px}
.mute{color:var(--mute)}.small{font-size:14px}
.up{color:var(--up)}.dn{color:var(--dn)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:10px 0}
.card h3{margin:0 0 4px}
.row{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap}
.chip{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:999px;border:1px solid currentColor;white-space:nowrap}
.l-res{color:var(--imp)}.l-mov{color:var(--lead)}.l-chase{color:var(--weak)}.l-watch{color:var(--mute)}.l-avoid{color:var(--lag)}.l-none{color:var(--mute)}
.q-lead{color:var(--lead)}.q-weak{color:var(--weak)}.q-lag{color:var(--lag)}.q-imp{color:var(--imp)}
.tbl{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:7px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left;white-space:normal}
th{font-weight:600;color:var(--mute);font-size:12px;text-transform:uppercase;letter-spacing:.3px}
td.l{text-align:left}
@media (max-width:600px){.hs{display:none}h1{font-size:24px}}
.kv{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:14px;color:var(--mute);margin:6px 0}
.kv b{color:var(--fg);font-weight:600}
article{font-size:17px;line-height:1.7;overflow-wrap:anywhere}article pre{overflow-x:auto;white-space:pre-wrap}
article h2{font-size:22px}article img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;margin:8px 0}
article table{font-size:14px}article .tbl td,article .tbl th{white-space:normal;text-align:left}
article blockquote{margin:12px 0;padding:2px 14px;border-left:3px solid var(--line);color:var(--mute)}
.tags a{font-size:13px;margin-right:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}@media (max-width:600px){.grid{grid-template-columns:1fr}}
.grid svg{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
svg text{fill:var(--mute);font:10px -apple-system,Segoe UI,Roboto,sans-serif}
footer{border-top:1px solid var(--line);padding:18px 0 30px;color:var(--mute);font-size:13px}
"""

def page(title, body, active='', desc='', md_href=None, canonical=''):
    nav = [('/', 'Home', 'home'), ('/research/', 'Research', 'research'), ('/baskets/', 'Baskets', 'baskets'),
           ('/rotation/', 'Rotation', 'rotation'), ('/etfs/', 'Sector ETFs', 'etfs'), ('/about/', 'About', 'about')]
    navh = ''.join(f'<a href="{h}" class="{"on" if k == active else ""}">{t}</a>' for h, t, k in nav)
    alt = f'<link rel="alternate" type="text/markdown" href="{md_href}">' if md_href else ''
    full = title if title == SITE_NAME else f'{title} · {SITE_NAME}'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(full)}</title><meta name="description" content="{E(desc or TAGLINE)}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME} research" href="/feed.xml">
{alt}<link rel="canonical" href="{E(canonical)}"><style>{CSS}</style></head><body>
<header class="site"><div class="wrap top"><a class="brand" href="/">{SITE_NAME}</a><nav>{navh}</nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">Not investment advice. Prices are daily closes from public market data and may contain errors.
Machine-readable: <a href="/llms.txt">llms.txt</a> · <a href="/data/">data</a> · <a href="/feed.xml">RSS</a>{f' · <a href="{md_href}">this page as markdown</a>' if md_href else ''}</div></footer>
</body></html>"""

class Site:
    def __init__(self, data, out, asof, base):
        self.data, self.out, self.asof, self.base = data, out, asof, base.rstrip('/')
        self.urls = []
    def write(self, path, text):
        p = os.path.join(self.out, path.lstrip('/'))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(text)
    def html(self, url, title, body, active='', desc='', md=None):
        md_href = None
        if md is not None:
            md_href = url.rstrip('/') + '.md' if url != '/' else '/index.md'
            self.write(md_href, md)
        self.write(url + ('index.html' if url.endswith('/') else ''),
                   page(title, body, active, desc, md_href, self.base + url))
        self.urls.append(url)
    def load(self, name):
        return json.load(open(os.path.join(self.data, name)))

def table(head, rows, hide=()):
    th = ''.join(f'<th class="{"hs" if i in hide else ""}">{h}</th>' for i, h in enumerate(head))
    tr = ''.join('<tr>' + ''.join(f'<td class="{"hs " if i in hide else ""}{c}">{v}</td>' for i, (v, c) in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def md_table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    out += ['| ' + ' | '.join(str(x) for x in r) + ' |' for r in rows]
    return '\n'.join(out)

def md_to_html(md):
    r = subprocess.run(['pandoc', '-f', 'gfm', '-t', 'html5', '--no-highlight'], input=md, capture_output=True, text=True, check=True)
    h = r.stdout
    return h.replace('<table>', '<div class="tbl"><table>').replace('</table>', '</table></div>')

# ---------- rotation chart ----------
def rrg_svg(sector, trails, themes_by_name, size=360):
    pts = [t[-1] for t in trails.values() if t]
    if not pts: return ''
    span = max(max(abs(p['rr'] - 100) for p in pts), max(abs(p['rm'] - 100) for p in pts), 2.0) * 1.25
    pad = 22
    def cl(v): return min(max(v, 100 - span), 100 + span)
    def X(v): return pad + (cl(v) - (100 - span)) / (2 * span) * (size - 2 * pad)
    def Y(v): return size - pad - (cl(v) - (100 - span)) / (2 * span) * (size - 2 * pad)
    c = X(100)
    s = [f'<svg viewBox="0 0 {size} {size}" role="img" aria-label="Rotation chart for {E(sector)}">',
         f'<rect x="{c}" y="{pad}" width="{size-pad-c}" height="{c-pad}" fill="var(--lead)" opacity=".07"/>',
         f'<rect x="{c}" y="{c}" width="{size-pad-c}" height="{size-pad-c}" fill="var(--weak)" opacity=".07"/>',
         f'<rect x="{pad}" y="{c}" width="{c-pad}" height="{size-pad-c}" fill="var(--lag)" opacity=".07"/>',
         f'<rect x="{pad}" y="{pad}" width="{c-pad}" height="{c-pad}" fill="var(--imp)" opacity=".07"/>',
         f'<line x1="{pad}" y1="{c}" x2="{size-pad}" y2="{c}" stroke="var(--line)"/><line x1="{c}" y1="{pad}" x2="{c}" y2="{size-pad}" stroke="var(--line)"/>',
         f'<text x="{size-pad-2}" y="{pad+10}" text-anchor="end">Leading</text><text x="{size-pad-2}" y="{size-pad-4}" text-anchor="end">Weakening</text>',
         f'<text x="{pad+2}" y="{size-pad-4}">Lagging</text><text x="{pad+2}" y="{pad+10}">Improving</text>',
         f'<text x="{size/2}" y="{size-6}" text-anchor="middle">Relative strength →</text>',
         f'<text x="10" y="{size/2}" text-anchor="middle" transform="rotate(-90 10 {size/2})">Momentum →</text>',
         f'<text x="{size/2}" y="14" text-anchor="middle" style="font-weight:600;fill:var(--fg)">{E(sector)}</text>']
    placed = []
    for name, tr in sorted(trails.items(), key=lambda kv: -kv[1][-1]['rm']):
        q = themes_by_name.get(name, {}).get('quadrant')
        col = {'Leading': 'var(--lead)', 'Weakening': 'var(--weak)', 'Lagging': 'var(--lag)', 'Improving': 'var(--imp)'}.get(q, 'var(--mute)')
        path = ' '.join(f'{X(p["rr"]):.1f},{Y(p["rm"]):.1f}' for p in tr)
        last = tr[-1]
        s.append(f'<polyline points="{path}" fill="none" stroke="{col}" stroke-width="1.3" opacity=".75"/>')
        s.append(f'<circle cx="{X(last["rr"]):.1f}" cy="{Y(last["rm"]):.1f}" r="3.2" fill="{col}"><title>{E(name)}</title></circle>')
        lx = X(last['rr']); anchor = 'end' if lx > size * .62 else 'start'
        ly = Y(last['rm']) - 4
        while any(abs(ly - y0) < 11 and abs(lx - x0) < 90 for x0, y0 in placed): ly += 11
        placed.append((lx, ly))
        s.append(f'<text x="{lx + (-5 if anchor == "end" else 5):.1f}" y="{ly:.1f}" text-anchor="{anchor}" style="fill:var(--fg)">{E(name)}</text>')
    s.append('</svg>')
    return ''.join(s)

# ---------- build ----------
def build(data, out, asof, base):
    if os.path.exists(out):
        for n in os.listdir(out):
            if n in ('.git', 'CNAME', 'README.md', '_src'): continue
            p = os.path.join(out, n)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(out, exist_ok=True)
    S = Site(data, out, asof, base)
    shutil.copytree(os.path.join(CONTENT, 'img'), os.path.join(out, 'img'), dirs_exist_ok=True)
    open(os.path.join(out, '.nojekyll'), 'w').close()

    threads = yaml.safe_load(open(os.path.join(CONTENT, 'threads.yaml')))
    bdefs = yaml.safe_load(open(os.path.join(CONTENT, 'baskets.yaml')))
    braw = {b['basket']: b for b in S.load('baskets.json')}
    mraw = S.load('members.json')
    etfs = S.load('etfs.json')
    themes = S.load('themes.json')
    rrg = [r for r in S.load('rrg.json') if r['bench'] == 'SPY']
    tmem = S.load('theme_members.json')
    thread_slug = {t['name']: t['slug'] for t in threads}

    # research
    posts = []
    rdir = os.path.join(CONTENT, 'research')
    for fn in sorted(os.listdir(rdir)):
        if not fn.endswith('.md'): continue
        raw = open(os.path.join(rdir, fn), encoding='utf-8').read()
        _, fm, body = raw.split('---', 2)
        meta = yaml.safe_load(fm); meta['body'] = body.strip()
        meta['date'] = str(meta['date']); meta['url'] = f"/research/{meta['slug']}/"
        posts.append(meta)
    posts.sort(key=lambda p: p['date'], reverse=True)

    # baskets (public allow-list)
    baskets = []
    for b in bdefs:
        r = braw.get(b['source'])
        if not r: continue
        mem = [m for m in mraw if m['basket'] == b['source']]
        baskets.append(dict(slug=b['slug'], name=b['name'], thread=b['thread'], start=str(b['start']),
            summary=' '.join(b['summary'].split()), label=r.get('stage'), since_start=r.get('since'),
            d5=r.get('d5'), d20=r.get('d20'), m6=r.get('m6'), y1=r.get('y1'),
            weighting='Equal weight' if r.get('weighting') == 'Equal weight' else 'Stated weights',
            research=[p['url'] for p in posts if b['slug'] in (p.get('baskets') or [])],
            members=[dict(ticker=m['ticker'], name=m['name'], weight=m['weight'], since_start=m.get('since'),
                          d5=m.get('d5'), d20=m.get('d20'), m6=m.get('m6'), off_high=m.get('off'), priced=m.get('priced'))
                     for m in mem]))
    bslug = {b['slug']: b for b in baskets}

    # themes + trails
    tby = {t['theme']: t for t in themes}
    trails = {}
    for r in sorted(rrg, key=lambda x: x['date']):
        trails.setdefault(r['theme'], []).append(r)
    for k in trails: trails[k] = trails[k][-6:]
    themes_pub = [dict(theme=t['theme'], slug=slugify(t['theme']), sector=t['sector'], label=t['stage'],
                       names=t['n'], d5=t['d5'], d20=t['d20'], m6=t['m6'], y1=t['y1'],
                       rs_ratio=round(t['rs_ratio'], 2) if t.get('rs_ratio') is not None else None,
                       rs_momentum=round(t['rs_mom'], 2) if t.get('rs_mom') is not None else None,
                       quadrant=t.get('quadrant'), heading_to=t.get('toward'), weeks_in_quadrant=t.get('weeks_in_quadrant'))
                  for t in themes]
    sectors = sorted({t['sector'] for t in themes})

    # ---------- research pages ----------
    for p in posts:
        bl = ''.join(f'<a href="/baskets/{s}/">{E(bslug[s]["name"])} basket</a>' for s in p.get('baskets') or [] if s in bslug)
        head = (f'<p class="mute small"><a href="/research/#{thread_slug.get(p["thread"], "")}">{E(p["thread"])}</a> · {dfmt(p["date"])}</p>'
                f'<h1>{E(p["title"])}</h1><p class="mute">{E(p["summary"])}</p>'
                f'<div class="kv">Tickers: <b>{", ".join(E(t) for t in p.get("tickers", []))}</b></div>'
                + (f'<div class="tags">Tracked in: {bl}</div>' if bl else ''))
        md = (f'# {p["title"]}\n\nDate: {p["date"]}\nThread: {p["thread"]}\nTickers: {", ".join(p.get("tickers", []))}\n'
              f'Canonical: {base}{p["url"]}\n\nSummary: {p["summary"]}\n\n{p["body"]}\n')
        S.html(p['url'], p['title'], head + '<hr style="border:0;border-top:1px solid var(--line)"><article>' + md_to_html(p['body']) + '</article>',
               'research', p['summary'], md)
    # research index
    body = f'<h1>Research</h1><p class="mute">Thought pieces, grouped by thread. Each links to the basket that tracks it.</p>'
    mdl = ['# Research', '']
    for t in threads:
        tp = [p for p in posts if p['thread'] == t['name']]
        tb = [b for b in baskets if b['thread'] == t['name']]
        body += f'<h2 id="{t["slug"]}">{E(t["name"])}</h2><p class="mute small">{E(t["summary"])}</p>'
        mdl += [f'## {t["name"]}', '', t['summary'], '']
        for p in tp:
            body += f'<div class="card"><h3><a href="{p["url"]}">{E(p["title"])}</a></h3><div class="mute small">{dfmt(p["date"])} · {", ".join(p.get("tickers", []))}</div><p class="small" style="margin:6px 0 0">{E(p["summary"])}</p></div>'
            mdl.append(f'- [{p["title"]}]({base}{p["url"].rstrip("/")}.md) ({p["date"]}): {p["summary"]}')
        if not tp:
            body += '<p class="small mute">No published piece yet.</p>'
        if tb:
            body += '<p class="small">Basket: ' + ' · '.join(f'<a href="/baskets/{b["slug"]}/">{E(b["name"])}</a>' for b in tb) + '</p>'
        mdl.append('')
    S.html('/research/', 'Research', body, 'research', 'Thought pieces grouped by thread.', '\n'.join(mdl))

    # ---------- basket pages ----------
    def bcard(b):
        return (f'<div class="card"><div class="row"><h3><a href="/baskets/{b["slug"]}/">{E(b["name"])}</a></h3>{chip(b["label"])}</div>'
                f'<div class="kv">Since {dfmt(b["start"])}: <b class="{cls(b["since_start"])}">{pct(b["since_start"])}</b> 5D: <b class="{cls(b["d5"])}">{pct(b["d5"])}</b> 20D: <b class="{cls(b["d20"])}">{pct(b["d20"])}</b></div>'
                f'<p class="small" style="margin:4px 0 0">{E(b["summary"])}</p></div>')
    body = (f'<h1>Baskets</h1><p class="mute">Each basket is fixed at its start date and tracked from the first close on or after it. '
            f'Returns are price only, in each stock\'s home currency. Data to the {dfmt(asof)} close.</p>' + ''.join(bcard(b) for b in baskets))
    md = ['# Baskets', '', f'Data to the {asof} close. Price returns, home currency.', '',
          md_table(['Basket', 'Start', 'Since start', '5D', '20D', 'Label'],
                   [[f'[{b["name"]}]({base}/baskets/{b["slug"]}.md)', b['start'], pct(b['since_start']), pct(b['d5']), pct(b['d20']), b['label']] for b in baskets])]
    S.html('/baskets/', 'Baskets', body, 'baskets', 'Thematic baskets tracked from their start dates.', '\n'.join(md))
    for b in baskets:
        rows = [[(f'<b>{E(m["ticker"])}</b><br><span class="mute small">{E(m["name"])}</span>', ''),
                 (f'{m["weight"]*100:.1f}%' if m['weight'] is not None else '—', 'hs'),
                 (pct(m['since_start']), cls(m['since_start'])), (pct(m['d5']), cls(m['d5'])), (pct(m['d20']), cls(m['d20'])),
                 (pct(m['off_high'], 0), '')] for m in sorted(b['members'], key=lambda m: -(m['since_start'] or -9))]
        rl = ''.join(f'<li><a href="{u}">{E(next(p["title"] for p in posts if p["url"] == u))}</a></li>' for u in b['research'])
        body = (f'<p class="mute small"><a href="/baskets/">Baskets</a> · {E(b["thread"])}</p><h1>{E(b["name"])}</h1>'
                f'<div class="row">{chip(b["label"])}</div><p>{E(b["summary"])}</p>'
                f'<div class="kv">Start <b>{dfmt(b["start"])}</b> · Since start <b class="{cls(b["since_start"])}">{pct(b["since_start"])}</b> · 6M <b class="{cls(b["m6"])}">{pct(b["m6"])}</b> · {b["weighting"]} · {len(b["members"])} names</div>'
                + table(['Name', 'Weight', 'Since start', '5D', '20D', 'Off high'], rows, hide=(1, 5))
                + f'<p class="small mute">{E(b["label"] or "")}: {E(LABEL_TEXT.get(b["label"], ""))}</p>'
                + (f'<h2>Research</h2><ul>{rl}</ul>' if rl else ''))
        md = [f'# {b["name"]} basket', '', b['summary'], '', f'Start: {b["start"]}. Weighting: {b["weighting"]}. Label: {b["label"]}. Since start: {pct(b["since_start"])}. Data to the {asof} close.', '',
              md_table(['Ticker', 'Name', 'Weight', 'Since start', '5D', '20D'],
                       [[m['ticker'], m['name'], f'{m["weight"]*100:.1f}%' if m['weight'] is not None else '', pct(m['since_start']), pct(m['d5']), pct(m['d20'])] for m in b['members']])]
        if b['research']: md += ['', 'Research:'] + [f'- {base}{u.rstrip("/")}.md' for u in b['research']]
        S.html(f'/baskets/{b["slug"]}/', b['name'] + ' basket', body, 'baskets', b['summary'], '\n'.join(md))

    # ---------- rotation ----------
    charts = ''.join(rrg_svg(sec, {t['theme']: trails[t['theme']] for t in themes if t['sector'] == sec and t['theme'] in trails}, tby) for sec in sectors)
    qcount = {q: sum(1 for t in themes if t.get('quadrant') == q) for q in ['Leading', 'Weakening', 'Lagging', 'Improving']}
    body = (f'<h1>Rotation</h1><p class="mute">Where {len(themes)} themes sit against the S&amp;P 500 (SPY), on weekly closes to {dfmt(max(r["date"] for r in rrg))}. '
            f'Right of centre means stronger than the market. Above centre means that strength is gaining. Themes usually rotate clockwise: '
            f'Improving → Leading → Weakening → Lagging. Each tail shows the last six weeks.</p>'
            f'<div class="kv">' + ' '.join(f'{qchip(q)} <b>{n}</b>' for q, n in qcount.items()) + '</div>'
            f'<div class="grid">{charts}</div>')
    md = ['# Rotation', '', f'{len(themes)} themes against SPY, weekly closes to {max(r["date"] for r in rrg)}. RS-Ratio > 100 = stronger than market. RS-Momentum > 100 = strength gaining.', '']
    for sec in sectors:
        st = [t for t in themes_pub if t['sector'] == sec]
        body += f'<h2>{E(sec)}</h2>' + table(['Theme', 'Label', 'Quadrant', 'Heading', '20D', '6M'],
            [[(f'<a href="/rotation/{t["slug"]}/">{E(t["theme"])}</a>', ''), (chip(t['label']), ''), (qchip(t['quadrant']), 'hs'),
              (E(t['heading_to'] or '—'), 'hs'), (pct(t['d20']), cls(t['d20'])), (pct(t['m6']), cls(t['m6']))] for t in st], hide=(2, 3))
        md += [f'## {sec}', '', md_table(['Theme', 'Label', 'Quadrant', 'Heading to', 'RS-Ratio', 'RS-Momentum', '20D', '6M'],
               [[f'[{t["theme"]}]({base}/rotation/{t["slug"]}.md)', t['label'], t['quadrant'], t['heading_to'], t['rs_ratio'], t['rs_momentum'], pct(t['d20']), pct(t['m6'])] for t in st]), '']
    body += '<h2>What the labels mean</h2>' + ''.join(f'<p class="small">{chip(k)} {E(v)}</p>' for k, v in LABEL_TEXT.items())
    S.html('/rotation/', 'Rotation', body, 'rotation', 'Weekly relative rotation of themes against the S&P 500.', '\n'.join(md))
    for t in themes_pub:
        mem = [m for m in tmem if m['theme'] == t['theme']]
        rows = [[(f'<b>{E(m["ticker"])}</b><br><span class="mute small">{E(m["name"])}</span>', ''), (pct(m['d5']), cls(m['d5'])),
                 (pct(m['d20']), cls(m['d20'])), (pct(m['m6']), cls(m['m6']) + ' hs'), (pct(m['off'], 0), 'hs')]
                for m in sorted(mem, key=lambda m: -(m['d20'] or -9))]
        body = (f'<p class="mute small"><a href="/rotation/">Rotation</a> · {E(t["sector"])}</p><h1>{E(t["theme"])}</h1>'
                f'<div class="row">{chip(t["label"])} {qchip(t["quadrant"])}</div>'
                f'<div class="kv">Heading to <b>{E(t["heading_to"] or "—")}</b> · {t["weeks_in_quadrant"] or "—"} weeks in quadrant · 5D <b class="{cls(t["d5"])}">{pct(t["d5"])}</b> · 20D <b class="{cls(t["d20"])}">{pct(t["d20"])}</b> · 6M <b class="{cls(t["m6"])}">{pct(t["m6"])}</b></div>'
                + table(['Name', '5D', '20D', '6M', 'Off high'], rows, hide=(3, 4)))
        md = [f'# {t["theme"]}', '', f'Sector: {t["sector"]}. Label: {t["label"]}. Quadrant: {t["quadrant"]}, heading to {t["heading_to"]}. Data to {asof}.', '',
              md_table(['Ticker', 'Name', '5D', '20D', '6M'], [[m['ticker'], m['name'], pct(m['d5']), pct(m['d20']), pct(m['m6'])] for m in mem])]
        S.html(f'/rotation/{t["slug"]}/', t['theme'], body, 'rotation', f'{t["theme"]}: {t["label"]}, {t["quadrant"]}.', '\n'.join(md))

    # ---------- ETFs ----------
    erows = [[(f'<b>{E(e["etf"])}</b><br><span class="mute small">{E(e["tracks"])}</span>', ''), (pct(e['d1']), cls(e['d1']) + ' hs'),
              (pct(e['d5']), cls(e['d5'])), (pct(e['d20']), cls(e['d20'])), (pct(e['m6']), cls(e['m6'])), (pct(e['y1']), cls(e['y1']) + ' hs')] for e in etfs]
    body = f'<h1>Sector ETFs</h1><p class="mute">Index, sector and country ETFs for context. Daily closes to {dfmt(asof)}.</p>' + table(['ETF', '1D', '5D', '20D', '6M', '1Y'], erows, hide=(1, 5))
    md = ['# Sector ETFs', '', f'Daily closes to {asof}.', '', md_table(['ETF', 'Tracks', '1D', '5D', '20D', '6M', '1Y'],
          [[e['etf'], e['tracks'], pct(e['d1']), pct(e['d5']), pct(e['d20']), pct(e['m6']), pct(e['y1'])] for e in etfs])]
    S.html('/etfs/', 'Sector ETFs', body, 'etfs', 'Index, sector and country ETF performance.', '\n'.join(md))

    # ---------- about ----------
    about_md = f"""# About

{SITE_NAME} publishes thematic equity research and tracks each idea as a basket of listed stocks from the day it is written.

- **Research** holds the thought pieces, grouped by thread. Threads build over time as earnings and news add evidence.
- **Baskets** are fixed at their start date and tracked from the first close on or after it. Price returns only, in each stock's home currency, no costs.
- **Rotation** places market themes on a relative rotation chart against the S&P 500, using weekly closes.
- **Sector ETFs** give market context.

Labels are computed daily from the price action of the names in each group:

{chr(10).join(f'- **{k}**: {v}' for k, v in LABEL_TEXT.items())}

## For AI agents and researchers

Everything here is free to read and reuse with attribution. No sign-up, no paywall.

- [{base}/llms.txt]({base}/llms.txt): site map for language models
- [{base}/llms-full.txt]({base}/llms-full.txt): all research in one file
- [{base}/data/]({base}/data/): JSON for baskets, themes, rotation and ETFs, refreshed after each US close
- Every page has a markdown twin at the same path ending in `.md`
- [{base}/feed.xml]({base}/feed.xml): RSS feed of new research

## Disclaimer

Not investment advice. The author may hold positions in the securities discussed. Figures come from company filings, earnings materials and public market data, and may contain errors.
"""
    S.html('/about/', 'About', md_to_html(about_md), 'about', 'What this site is and how to use its data.', about_md)

    # ---------- home ----------
    lead = sorted([t for t in themes_pub if t['quadrant'] in ('Improving', 'Leading') and t['heading_to'] == 'Leading'], key=lambda t: -(t['d20'] or 0))[:8]
    body = (f'<h1>{SITE_NAME}</h1><p class="mute">{TAGLINE} Market data to the {dfmt(asof)} close.</p>'
            '<h2>Latest research</h2>' + ''.join(f'<div class="card"><div class="mute small">{E(p["thread"])} · {dfmt(p["date"])}</div><h3><a href="{p["url"]}">{E(p["title"])}</a></h3><p class="small" style="margin:4px 0 0">{E(p["summary"])}</p></div>' for p in posts[:5])
            + '<h2>Baskets</h2>' + table(['Basket', 'Since start', '20D', 'Label'], hide=(2,), rows=
                [[(f'<a href="/baskets/{b["slug"]}/">{E(b["name"])}</a><br><span class="mute small">from {dfmt(b["start"])}</span>', ''),
                  (pct(b['since_start']), cls(b['since_start'])), (pct(b['d20']), cls(b['d20'])), (chip(b['label']), '')] for b in baskets])
            + '<h2>Heading into Leading</h2><p class="small mute">Themes in Improving or Leading whose weekly path points toward Leading.</p>'
            + table(['Theme', 'Quadrant', '20D', 'Label'], hide=(1,), rows=[[(f'<a href="/rotation/{t["slug"]}/">{E(t["theme"])}</a>', ''), (qchip(t['quadrant']), ''),
                (pct(t['d20']), cls(t['d20'])), (chip(t['label']), '')] for t in lead])
            + '<p><a href="/rotation/">Full rotation map →</a> · <a href="/etfs/">Sector ETFs →</a></p>')
    md = [f'# {SITE_NAME}', '', TAGLINE, f'Market data to the {asof} close.', '', '## Latest research', '']
    md += [f'- [{p["title"]}]({base}{p["url"].rstrip("/")}.md) ({p["date"]}, {p["thread"]})' for p in posts[:10]]
    md += ['', '## Baskets', '', md_table(['Basket', 'Start', 'Since start', 'Label'], [[f'[{b["name"]}]({base}/baskets/{b["slug"]}.md)', b['start'], pct(b['since_start']), b['label']] for b in baskets])]
    S.html('/', SITE_NAME, body, 'home', TAGLINE, '\n'.join(md))

    # ---------- data ----------
    now = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    meta = dict(site=SITE_NAME, asof=asof, generated=now, units='returns are decimal fractions (0.05 = +5%)', source='daily closes, public market data')
    D = {'baskets.json': dict(meta, baskets=baskets), 'themes.json': dict(meta, benchmark='SPY', themes=themes_pub),
         'rotation.json': dict(meta, benchmark='SPY', trails={k: [dict(date=p['date'], rs_ratio=p['rr'], rs_momentum=p['rm']) for p in v] for k, v in trails.items()}),
         'theme_members.json': dict(meta, members=[dict(theme=m['theme'], ticker=m['ticker'], name=m['name'], d5=m['d5'], d20=m['d20'], m6=m['m6'], y1=m['y1'], off_high=m['off']) for m in tmem]),
         'etfs.json': dict(meta, etfs=etfs),
         'research.json': dict(meta, research=[dict(title=p['title'], date=p['date'], thread=p['thread'], tickers=p.get('tickers', []), baskets=p.get('baskets', []),
                               summary=p['summary'], url=base + p['url'], markdown=base + p['url'].rstrip('/') + '.md') for p in posts])}
    for k, v in D.items(): S.write('/data/' + k, json.dumps(v, indent=1, ensure_ascii=False))
    dbody = '<h1>Data</h1><p class="mute">Free to use with attribution. Refreshed after each US close.</p><ul>' + ''.join(f'<li><a href="/data/{k}">{k}</a></li>' for k in D) + '</ul>'
    S.html('/data/', 'Data', dbody, '', 'JSON datasets behind this site.', '# Data\n\n' + '\n'.join(f'- {base}/data/{k}' for k in D))

    # ---------- llms.txt, feed, sitemap ----------
    llms = [f'# {SITE_NAME}', '', f'> {TAGLINE} Free and open. Market data to the {asof} close.', '',
            'Research pieces are written as theses with named tickers, dated numbers and sources. Each idea is tracked as a basket from its start date.', '',
            '## Research']
    llms += [f'- [{p["title"]}]({base}{p["url"].rstrip("/")}.md): {p["date"]}. {p["thread"]}. {", ".join(p.get("tickers", []))}. {p["summary"]}' for p in posts]
    llms += ['', '## Baskets'] + [f'- [{b["name"]}]({base}/baskets/{b["slug"]}.md): from {b["start"]}, {pct(b["since_start"])} since start, label {b["label"]}. {b["summary"]}' for b in baskets]
    llms += ['', '## Market views', f'- [Rotation]({base}/rotation.md): {len(themes)} themes on a weekly rotation chart against SPY', f'- [Sector ETFs]({base}/etfs.md)', '',
             '## Data', ] + [f'- [{k}]({base}/data/{k})' for k in D] + ['', '## Optional', f'- [All research in one file]({base}/llms-full.txt)', f'- [About]({base}/about.md)']
    S.write('/llms.txt', '\n'.join(llms) + '\n')
    S.write('/llms-full.txt', '\n\n---\n\n'.join(f'# {p["title"]}\n\nDate: {p["date"]}\nThread: {p["thread"]}\nURL: {base}{p["url"]}\n\n{p["body"]}' for p in posts) + '\n')
    items = ''.join(f'<item><title>{E(p["title"])}</title><link>{base}{p["url"]}</link><guid>{base}{p["url"]}</guid>'
                    f'<pubDate>{format_datetime(dt.datetime.fromisoformat(p["date"]).replace(tzinfo=dt.timezone.utc))}</pubDate><category>{E(p["thread"])}</category>'
                    f'<description>{E(p["summary"])}</description></item>' for p in posts)
    S.write('/feed.xml', f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{SITE_NAME}</title><link>{base}/</link><description>{E(TAGLINE)}</description>{items}</channel></rss>')
    S.write('/sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{base}{u}</loc></url>' for u in S.urls) + '</urlset>')
    S.write('/robots.txt', f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n')
    S.write('/404.html', page('Not found', '<h1>Not found</h1><p><a href="/">Back to the home page</a></p>'))
    return len(S.urls)

if __name__ == '__main__':
    a = sys.argv[1:]
    asof = a[a.index('--asof') + 1] if '--asof' in a else str(dt.date.today() - dt.timedelta(days=1))
    base = a[a.index('--base') + 1] if '--base' in a else 'https://theme-radar.github.io'
    print('pages', build(a[0], a[1], asof, base))
