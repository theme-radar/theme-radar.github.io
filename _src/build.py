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

THREADS = yaml.safe_load(open(os.path.join(CONTENT, 'threads.yaml')))
THREAD = {t['name']: t for t in THREADS}

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
.top{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 20px;padding:14px 16px}
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
.kv b{color:var(--fg);font-weight:600}.kv b.up,b.up{color:var(--up)}.kv b.dn,b.dn{color:var(--dn)}
article{font-size:17px;line-height:1.7;overflow-wrap:anywhere}article pre{overflow-x:auto;white-space:pre-wrap}
article h2{font-size:22px}article img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;margin:8px 0}
article table{font-size:14px}article .tbl td,article .tbl th{white-space:normal;text-align:left}
article blockquote{margin:12px 0;padding:2px 14px;border-left:3px solid var(--line);color:var(--mute)}
.tags a{font-size:13px;margin-right:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}@media (max-width:600px){.grid{grid-template-columns:1fr}}
.grid svg{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
svg text{fill:var(--mute);font:10px -apple-system,Segoe UI,Roboto,sans-serif}
body.wide .wrap{max-width:1240px}
.fbtn{font:inherit;font-size:13px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--mute);cursor:pointer;margin:0 6px 6px 0}
.fbtn[aria-pressed="true"]{color:var(--fg);border-color:var(--fg);font-weight:600}
.ctl{display:flex;flex-wrap:wrap;align-items:center;gap:0 4px;margin:6px 0}.ctl .lab{font-size:13px;color:var(--mute);margin-right:8px}
.rrg-layout{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;margin-top:10px}
@media (min-width:1000px){.rrg-layout{grid-template-columns:minmax(0,1fr) 330px}}
#rot-chart{position:relative;background:var(--card);border:1px solid var(--line);border-radius:10px;min-height:340px}
.rtip{position:absolute;pointer-events:none;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:12px;max-width:16rem;box-shadow:0 4px 14px rgba(0,0,0,.12)}
.formula{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;font-size:14px}
.formula h3{margin:0 0 8px}.formula ol{padding-left:20px;margin:8px 0}.formula li{margin:8px 0}
.formula .eq{font-family:Georgia,"Times New Roman",serif;font-size:15px;display:block;margin-top:2px;color:var(--fg)}
nav.util a{margin-right:14px}
.tabs{border-top:1px solid var(--line);background:var(--card)}
.tabs .wrap{display:flex;flex-wrap:wrap;gap:6px;padding-top:8px;padding-bottom:8px}
.tab{display:inline-flex;align-items:center;gap:7px;white-space:nowrap;padding:5px 12px 5px 6px;border-radius:999px;border:1px solid var(--line);color:var(--fg);font-size:14px}
.tab:hover{text-decoration:none;border-color:var(--tc)}
.tab.on{border-color:var(--tc);background:color-mix(in srgb,var(--tc) 12%,transparent);font-weight:600}
.ico{display:inline-flex;align-items:center;justify-content:center;border-radius:8px;background:var(--tc);color:#fff;flex:none}
.ico svg{fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.themegrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px;margin:10px 0}
.tcard{display:block;background:var(--card);border:1px solid var(--line);border-top:4px solid var(--tc);border-radius:10px;padding:14px;color:var(--fg)}
.tcard:hover{text-decoration:none;border-color:var(--tc)}
.tcard .nm{font-weight:700;margin:10px 0 4px}.tcard .ct{font-size:13px;color:var(--mute)}
.thead{display:flex;align-items:center;gap:14px;margin:4px 0 6px}.thead h1{margin:0}
.pcard{border-left:4px solid var(--tc)}
.tlabel{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--tc);font-weight:600}
.tpanel{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 22px 6px;margin:8px 0 18px}
.tpanel .thead h1{font-size:30px}.tpanel .incep{color:var(--mute);font-size:15px;margin-top:2px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 0}
@media (max-width:600px){.stats{grid-template-columns:1fr}}
.stat{background:color-mix(in srgb,var(--fg) 4%,transparent);border-radius:12px;padding:16px 18px}
.stat .k{font-size:13px;color:var(--mute)}.stat .big{font-size:34px;font-weight:700;line-height:1.15;margin:6px 0 4px;letter-spacing:-.5px}
.stat .mid{font-size:20px;font-weight:600;margin:2px 0}.stat .sub{font-size:14px;color:var(--mute)}
.tick{font-size:12px;color:var(--mute);line-height:1.6;margin-top:6px;letter-spacing:.2px}
.rlist{margin:6px 0 4px}.ritem{display:flex;gap:12px;padding:12px 0;border-top:1px solid var(--line)}
.ritem:first-child{border-top:0}.ritem .di{flex:none;color:var(--tc);margin-top:3px}
.ritem>div:nth-child(2){flex:1;min-width:0}.ritem .dt{flex:none;font-size:14px;color:var(--mute);white-space:nowrap;margin-top:3px}
.tgrid{display:grid;grid-template-columns:minmax(0,1fr);grid-template-areas:"head" "basket" "research";gap:0 24px}
@media (min-width:1000px){.tgrid{grid-template-columns:minmax(0,1fr) 420px;grid-template-areas:"head head" "research basket"}.tgrid .tb{position:sticky;top:12px;align-self:start}}
.tgrid .th{grid-area:head}.tgrid .tr{grid-area:research;align-self:start}.tgrid .tb{grid-area:basket}
.tbox{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:0 0 18px}
.tbox h3{margin:0 0 4px}
.ritem a{font-weight:600;font-size:17px;color:var(--fg)}.ritem .meta{font-size:14px;color:var(--mute);margin-top:2px}
.tpanel h3{font-size:17px;margin:20px 0 4px}
footer{border-top:1px solid var(--line);padding:18px 0 30px;color:var(--mute);font-size:13px}
"""

def icon(t, size=28):
    px = round(size * 0.62)
    return f'<span class="ico" style="--tc:{t["color"]};width:{size}px;height:{size}px"><svg viewBox="0 0 24 24" width="{px}" height="{px}" aria-hidden="true">{t["icon"]}</svg></span>'

def page(title, body, active='', desc='', md_href=None, canonical='', wide=False, scripts=''):
    nav = [('/', 'Home', 'home'), ('/baskets/', 'Thematic Baskets', 'baskets'),
           ('/rotation/', 'Rotation', 'rotation'), ('/etfs/', 'Sector ETFs', 'etfs'), ('/about/', 'About', 'about')]
    navh = ''.join(f'<a href="{h}" class="{"on" if k == active else ""}">{t}</a>' for h, t, k in nav)
    tabs = ''.join(f'<a class="tab {"on" if active == "t:" + t["slug"] else ""}" style="--tc:{t["color"]}" href="/themes/{t["slug"]}/">{icon(t, 24)}{E(t["name"])}</a>' for t in THREADS)
    alt = f'<link rel="alternate" type="text/markdown" href="{md_href}">' if md_href else ''
    full = title if title == SITE_NAME else f'{title} · {SITE_NAME}'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(full)}</title><meta name="description" content="{E(desc or TAGLINE)}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME} research" href="/feed.xml">
{alt}<link rel="canonical" href="{E(canonical)}"><style>{CSS}</style></head><body class="{'wide' if wide else ''}">
<header class="site"><div class="wrap top"><a class="brand" href="/">{SITE_NAME}</a><nav class="util">{navh}</nav></div><div class="tabs" aria-label="Research themes"><div class="wrap">{tabs}</div></div></header>
<main><div class="wrap">{body}</div></main>{scripts}
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
    def html(self, url, title, body, active='', desc='', md=None, wide=False, scripts=''):
        md_href = None
        if md is not None:
            md_href = url.rstrip('/') + '.md' if url != '/' else '/index.md'
            self.write(md_href, md)
        self.write(url + ('index.html' if url.endswith('/') else ''),
                   page(title, body, active, desc, md_href, self.base + url, wide, scripts))
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

FORMULA_HTML = """<aside class="formula"><h3>How the axes are calculated</h3>
<p class="small mute" style="margin:0">Each theme is an equal-weight index of its stocks (daily returns averaged across names). B is the benchmark, SPY or RSP. Weekly points use the last close of each week.</p>
<ol>
<li>Relative strength<span class="eq">RS<sub>t</sub> = 100 &times; P<sub>t</sub> / B<sub>t</sub></span></li>
<li>Trend of relative strength<span class="eq">R<sub>t</sub> = EMA<sub>3</sub>( 100 &times; RS<sub>t</sub> / SMA<sub>10</sub>(RS)<sub>t</sub> )</span></li>
<li>RS-Ratio (x-axis)<span class="eq">RS-Ratio<sub>t</sub> = 100 + ( R<sub>t</sub> &minus; &mu;<sub>40</sub>(R) ) / &sigma;<sub>40</sub>(R)</span></li>
<li>Change in RS-Ratio<span class="eq">M<sub>t</sub> = EMA<sub>3</sub>( RS-Ratio<sub>t</sub> &minus; RS-Ratio<sub>t&minus;1</sub> )</span></li>
<li>RS-Momentum (y-axis)<span class="eq">RS-Momentum<sub>t</sub> = 100 + ( M<sub>t</sub> &minus; &mu;<sub>40</sub>(M) ) / &sigma;<sub>40</sub>(M)</span></li>
</ol>
<p class="small" style="margin:6px 0">SMA<sub>10</sub> = 10-week simple average. EMA<sub>3</sub> = 3-week exponential average (&alpha; = 0.5). &mu;<sub>40</sub> and &sigma;<sub>40</sub> = mean and standard deviation over the last 40 weeks.</p>
<p class="small" style="margin:6px 0"><b>Reading it.</b> 100 is neutral on both axes. One point is one standard deviation of the theme's own history, so themes are comparable. RS-Ratio above 100: the theme is beating the benchmark by more than its recent trend. RS-Momentum above 100: that lead is widening.</p>
<p class="small" style="margin:6px 0"><b>Quadrants.</b> Leading: both above 100. Weakening: RS-Ratio above, RS-Momentum below. Lagging: both below. Improving: RS-Ratio below, RS-Momentum above. Heading is the direction of the latest weekly move.</p>
</aside>"""

FORMULA_MD = """Each theme is an equal-weight index of its stocks (daily returns averaged across names). B is the benchmark (SPY or RSP). Weekly points use the last close of each week.

1. Relative strength: RS_t = 100 × P_t / B_t
2. Trend of relative strength: R_t = EMA3( 100 × RS_t / SMA10(RS)_t )
3. RS-Ratio (x-axis): RS-Ratio_t = 100 + ( R_t − mean40(R) ) / sd40(R)
4. Change in RS-Ratio: M_t = EMA3( RS-Ratio_t − RS-Ratio_(t−1) )
5. RS-Momentum (y-axis): RS-Momentum_t = 100 + ( M_t − mean40(M) ) / sd40(M)

SMA10 = 10-week simple average. EMA3 = 3-week exponential average (alpha = 0.5). mean40 and sd40 = mean and standard deviation over the last 40 weeks. 100 is neutral on both axes. Quadrants: Leading (both > 100), Weakening (RS-Ratio > 100, RS-Momentum < 100), Lagging (both < 100), Improving (RS-Ratio < 100, RS-Momentum > 100). Heading is the direction of the latest weekly move."""

METHOD = [
    "Each basket expresses a research theme. The theme matters more than any single ticker.",
    "Equal weight at the start date, then buy-and-hold. Price returns from the first close on or after the start date, in each stock's home currency, no dividends or costs.",
]
METHOD_HTML = '<ul class="small">' + ''.join(f'<li>{E(x)}</li>' for x in METHOD) + '</ul>'
METHOD_MD = '\n'.join(f'- {x}' for x in METHOD)

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
    shutil.copytree(os.path.join(CONTENT, 'assets'), os.path.join(out, 'assets'), dirs_exist_ok=True)
    open(os.path.join(out, '.nojekyll'), 'w').close()

    threads = THREADS
    bdefs = yaml.safe_load(open(os.path.join(CONTENT, 'baskets.yaml')))
    braw = {b['basket']: b for b in S.load('baskets.json')}
    mraw = S.load('members.json')
    etfs = S.load('etfs.json')
    themes = S.load('themes.json')
    rrg_all = S.load('rrg.json')
    rrg = [r for r in rrg_all if r['bench'] == 'SPY']
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
            weighting='Equal weight',
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

    def tl(name):
        t = THREAD[name]
        return f'<a class="tlabel" style="--tc:{t["color"]}" href="/themes/{t["slug"]}/">{icon(t, 20)}{E(t["name"])}</a>'
    def pcard(p):
        t = THREAD[p['thread']]
        return (f'<div class="card pcard" style="--tc:{t["color"]}"><div class="row">{tl(p["thread"])}<span class="mute small">{dfmt(p["date"])}</span></div>'
                f'<h3 style="margin:8px 0 4px"><a href="{p["url"]}">{E(p["title"])}</a></h3><p class="small" style="margin:0">{E(p["summary"])}</p>'
                f'<div class="mute small" style="margin-top:6px">{", ".join(E(x) for x in p.get("tickers", []))}</div></div>')
    def tcard(t):
        n = sum(1 for p in posts if p['thread'] == t['name']); nb = sum(1 for b in baskets if b['thread'] == t['name'])
        return (f'<a class="tcard" style="--tc:{t["color"]}" href="/themes/{t["slug"]}/">{icon(t, 40)}<div class="nm">{E(t["name"])}</div>'
                f'<div class="small">{E(t["summary"])}</div><div class="ct" style="margin-top:6px">{n} piece{"s" if n != 1 else ""} · {nb} basket{"s" if nb != 1 else ""}</div></a>')

    def bcard(b):
        return (f'<div class="card pcard" style="--tc:{THREAD[b["thread"]]["color"]}"><div class="row">{tl(b["thread"])}{chip(b["label"])}</div><h3 style="margin:8px 0 2px"><a href="/baskets/{b["slug"]}/">{E(b["name"])}</a></h3>'
                f'<div class="kv">Since {dfmt(b["start"])}: <b class="{cls(b["since_start"])}">{pct(b["since_start"])}</b> 5D: <b class="{cls(b["d5"])}">{pct(b["d5"])}</b> 20D: <b class="{cls(b["d20"])}">{pct(b["d20"])}</b> 6M: <b class="{cls(b["m6"])}">{pct(b["m6"])}</b></div>'
                f'<p class="small" style="margin:4px 0 0">{E(b["summary"])}</p></div>')

    # ---------- research pages ----------
    for p in posts:
        bl = ''.join(f'<a href="/baskets/{s}/">{E(bslug[s]["name"])} basket</a>' for s in p.get('baskets') or [] if s in bslug)
        head = (f'<div class="row" style="justify-content:flex-start">{tl(p["thread"])}<span class="mute small">{dfmt(p["date"])}</span></div>'
                f'<h1>{E(p["title"])}</h1><p class="mute">{E(p["summary"])}</p>'
                f'<div class="kv">Tickers: <b>{", ".join(E(t) for t in p.get("tickers", []))}</b></div>'
                + (f'<div class="tags">Tracked in: {bl}</div>' if bl else ''))
        md = (f'# {p["title"]}\n\nDate: {p["date"]}\nTheme: {p["thread"]}\nTickers: {", ".join(p.get("tickers", []))}\n'
              f'Canonical: {base}{p["url"]}\n\nSummary: {p["summary"]}\n\n{p["body"]}\n')
        S.html(p['url'], p['title'], head + '<hr style="border:0;border-top:1px solid var(--line)"><article>' + md_to_html(p['body']) + '</article>',
               't:' + THREAD[p['thread']]['slug'], p['summary'], md)
    DOC = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M9 9h6M9 13h6M9 17h4"/></svg>'
    def theme_panel(t, tp, b):
        if b is None:
            items = ''.join(f'<div class="ritem" style="--tc:{t["color"]}"><span class="di">{DOC}</span><div><a href="{p["url"]}">{E(p["title"])}</a>'
                            f'<div class="meta">{E(p.get("kind", "Research"))} · {", ".join(E(x) for x in p.get("tickers", []))}</div></div><span class="dt">{dfmt(p["date"])}</span></div>' for p in tp)
            start = min((p['date'] for p in tp), default=None)
            head = (f'<div class="th tpanel"><div class="thead">{icon(t, 44)}<div><h1>{E(t["name"])}</h1>'
                    + (f'<div class="incep">Theme inception · {b_long(start)}</div>' if start else '') + '</div></div>'
                    '<div class="stats"><div class="stat"><div class="k">Basket</div><div class="big">Coming soon</div><div class="sub">Equal-weighted at inception</div></div>'
                    '<div class="stat"><div class="k">Performance since inception</div><div class="big">—</div><div class="sub">Starts when the basket is published</div></div></div></div>')
            research = f'<div class="tr tbox"><h3>Latest research</h3><div class="rlist">{items or "<p class=\"mute small\">No published piece yet.</p>"}</div></div>'
            return f'<div class="tgrid">{head}{research}<div class="tb tbox"><h3>Basket constituents</h3><p class="mute small">The basket for this theme has not been published yet.</p></div></div>'
        mem = sorted(b['members'], key=lambda m: -(m['since_start'] if m['since_start'] is not None else -9))
        ticks = ' · '.join(E(m['ticker']) for m in sorted(b['members'], key=lambda m: m['ticker']))
        items = ''.join(f'<div class="ritem" style="--tc:{t["color"]}"><span class="di">{DOC}</span><div><a href="{p["url"]}">{E(p["title"])}</a>'
                        f'<div class="meta">{E(p.get("kind", "Research"))} · {", ".join(E(x) for x in p.get("tickers", []))} · {dfmt(p["date"])}</div></div></div>' for p in tp)
        rows = [[(f'<b>{E(m["ticker"])}</b><br><span class="mute small">{E(m["name"])}</span>', ''),
                 (pct(m['since_start']), cls(m['since_start'])), (pct(m['d20']), cls(m['d20'])), (pct(m['m6']), cls(m['m6']) + ' hs')] for m in mem]
        items = ''.join(f'<div class="ritem" style="--tc:{t["color"]}"><span class="di">{DOC}</span><div><a href="{p["url"]}">{E(p["title"])}</a>'
                        f'<div class="meta">{E(p.get("kind", "Research"))} · {", ".join(E(x) for x in p.get("tickers", []))}</div></div><span class="dt">{dfmt(p["date"])}</span></div>' for p in tp)
        rows = [[(f'<b>{E(m["ticker"])}</b><br><span class="mute small">{E(m["name"])}</span>', ''),
                 (pct(m['since_start']), cls(m['since_start'])), (pct(m['m6']), cls(m['m6']))] for m in mem]
        head = (f'<div class="th tpanel"><div class="thead">{icon(t, 44)}<div><h1>{E(t["name"])}</h1>'
                f'<div class="incep">Theme inception · {b_long(b["start"])}</div></div></div>'
                '<div class="stats">'
                f'<div class="stat"><div class="k">Basket</div><div class="big">{len(b["members"])} stocks</div><div class="sub">Equal-weighted at inception</div><div class="tick">{ticks}</div></div>'
                f'<div class="stat"><div class="k">Performance since inception</div><div class="big {cls(b["since_start"])}">{pct(b["since_start"])}</div>'
                f'<div class="mid">{b_long(b["start"])}</div><div class="sub">Buy-and-hold · {chip(b["label"])}</div></div></div></div>')
        research = f'<div class="tr tbox"><h3>Latest research</h3><div class="rlist">{items or "<p class=\"mute small\">No published piece yet.</p>"}</div></div>'
        basket = (f'<div class="tb tbox"><h3>Basket constituents</h3><p class="mute small" style="margin:0 0 6px">All {len(b["members"])} tickers, performance since inception. Data to the {dfmt(asof)} close.</p>'
                  + table(['Name', 'Since inception', '6M'], rows) + '</div>')
        return f'<div class="tgrid">{head}{research}{basket}</div>'
    def b_long(d):
        d = dt.date.fromisoformat(str(d)); return f'{d.day} {d.strftime("%B %Y")}'
    # theme pages
    for t in threads:
        tp = [p for p in posts if p['thread'] == t['name']]
        tb = [b for b in baskets if b['thread'] == t['name']]
        wide = True
        if wide:
            body = theme_panel(t, tp, tb[0] if tb else None)
        else:
            body = (f'<div class="thead">{icon(t, 52)}<div><h1>{E(t["name"])}</h1><div class="mute">{E(t["summary"])}</div></div></div>'
                    f'<h2>Research ({len(tp)})</h2>' + (''.join(pcard(p) for p in tp) or '<p class="mute small">No published piece yet.</p>'))
            if tb:
                body += '<h2>Thematic Baskets</h2>' + ''.join(bcard(b) for b in tb)
        md = [f'# {t["name"]}', '', t['summary'], '', '## Research', '']
        md += [f'- [{p["title"]}]({base}{p["url"].rstrip("/")}.md) ({p["date"]}): {p["summary"]}' for p in tp] or ['None yet.']
        if tb:
            md += ['', '## Thematic Baskets', '', md_table(['Basket', 'Start', 'Since start', '20D', '6M', 'Label'],
                   [[f'[{b["name"]}]({base}/baskets/{b["slug"]}.md)', b['start'], pct(b['since_start']), pct(b['d20']), pct(b['m6']), b['label']] for b in tb])]
        S.html(f'/themes/{t["slug"]}/', t['name'], body, 't:' + t['slug'], t['summary'], '\n'.join(md), wide=wide)
    # research library (all themes)
    body = ('<h1>Research library</h1><p class="mute">Thematic research, organised by theme. Pick a theme to see every piece and the baskets that track it.</p>'
            f'<div class="themegrid">{"".join(tcard(t) for t in threads)}</div><h2>All pieces, newest first</h2>' + ''.join(pcard(p) for p in posts))
    mdl = ['# Research library', ''] + [f'- [{t["name"]}]({base}/themes/{t["slug"]}.md): {t["summary"]}' for t in threads] + ['', '## All pieces', '']
    mdl += [f'- [{p["title"]}]({base}{p["url"].rstrip("/")}.md) ({p["date"]}, {p["thread"]})' for p in posts]
    S.html('/research/', 'Research library', body, '', 'All research, organised by theme.', '\n'.join(mdl))

    # ---------- basket pages ----------
    body = (f'<h1>Thematic Baskets</h1><p class="mute">Reference baskets for each research theme. Data to the {dfmt(asof)} close.</p>'
            + ''.join(bcard(b) for b in baskets) + '<h2>How the baskets work</h2>' + METHOD_HTML)
    md = ['# Thematic Baskets', '', f'Data to the {asof} close.', '', '## How the baskets work', '', METHOD_MD, '',
          md_table(['Basket', 'Start', 'Since start', '5D', '20D', '6M', 'Label'],
                   [[f'[{b["name"]}]({base}/baskets/{b["slug"]}.md)', b['start'], pct(b['since_start']), pct(b['d5']), pct(b['d20']), pct(b['m6']), b['label']] for b in baskets])]
    S.html('/baskets/', 'Thematic Baskets', body, 'baskets', 'Buy-and-hold thematic reference baskets, equal-weighted at inception.', '\n'.join(md))
    for b in baskets:
        rows = [[(f'<b>{E(m["ticker"])}</b><br><span class="mute small">{E(m["name"])}</span>', ''),
                 (f'{m["weight"]*100:.1f}%' if m['weight'] is not None else '—', 'hs'),
                 (pct(m['since_start']), cls(m['since_start'])), (pct(m['d5']), cls(m['d5'])), (pct(m['d20']), cls(m['d20'])), (pct(m['m6']), cls(m['m6'])),
                 (pct(m['off_high'], 0), '')] for m in sorted(b['members'], key=lambda m: -(m['since_start'] or -9))]
        rl = ''.join(f'<li><a href="{u}">{E(next(p["title"] for p in posts if p["url"] == u))}</a></li>' for u in b['research'])
        body = (f'<div class="row" style="justify-content:flex-start"><a class="small" href="/baskets/">Thematic Baskets</a> {tl(b["thread"])}</div><h1>{E(b["name"])}</h1>'
                f'<div class="row">{chip(b["label"])}</div><p>{E(b["summary"])}</p>'
                f'<div class="kv">Start <b>{dfmt(b["start"])}</b> · Since start <b class="{cls(b["since_start"])}">{pct(b["since_start"])}</b> · 6M <b class="{cls(b["m6"])}">{pct(b["m6"])}</b> · {b["weighting"]} · {len(b["members"])} names</div>'
                + table(['Name', 'Weight', 'Since start', '5D', '20D', '6M', 'Off high'], rows, hide=(1, 3, 6))
                + f'<p class="small mute">{E(b["label"] or "")}: {E(LABEL_TEXT.get(b["label"], ""))}</p>'
                + (f'<h2>Research</h2><ul>{rl}</ul>' if rl else '')
                )
        md = [f'# {b["name"]} basket', '', b['summary'], '', f'Start: {b["start"]}. Weighting: {b["weighting"]}. Label: {b["label"]}. Since start: {pct(b["since_start"])}. Data to the {asof} close.', '',
              md_table(['Ticker', 'Name', 'Weight', 'Since start', '5D', '20D', '6M'],
                       [[m['ticker'], m['name'], f'{m["weight"]*100:.1f}%' if m['weight'] is not None else '', pct(m['since_start']), pct(m['d5']), pct(m['d20']), pct(m['m6'])] for m in b['members']])]
        if b['research']: md += ['', 'Research:'] + [f'- {base}{u.rstrip("/")}.md' for u in b['research']]
        S.html(f'/baskets/{b["slug"]}/', b['name'] + ' basket', body, 'baskets', b['summary'], '\n'.join(md))

    # ---------- rotation ----------
    qcount = {q: sum(1 for t in themes if t.get('quadrant') == q) for q in ['Leading', 'Weakening', 'Lagging', 'Improving']}
    tidx = {t['theme']: i for i, t in enumerate(themes)}
    rdata = dict(themes=[dict(t=t['theme'], s=t['sector'], l=t['stage'], d5=t['d5'], d20=t['d20'], slug=slugify(t['theme'])) for t in themes],
                 pts=[[tidx[r['theme']], 0 if r['bench'] == 'SPY' else 1, r['date'], r['ago'], round(r['rr'], 3), round(r['rm'], 3)] for r in rrg_all if r['theme'] in tidx])
    body = (f'<h1>Rotation</h1><p class="mute">Each dot is one of {len(themes)} themes, plotted weekly against the market. Right of centre means stronger than the market. '
            f'Above centre means that strength is improving right now. Themes usually travel clockwise: Improving → Leading → Weakening → Lagging. The tail shows where each theme came from.</p>'
            f'<div class="kv">' + ' '.join(f'{qchip(q)} <b>{n}</b>' for q, n in qcount.items()) + ' <span>(against SPY)</span></div>'
            '<div class="rrg-layout"><div>'
            '<div class="ctl"><span class="lab">Benchmark</span><span id="rot-bench"></span></div>'
            '<div class="ctl"><span class="lab">Tail</span><span id="rot-trail"></span></div>'
            '<div class="ctl"><span id="rot-sectors"></span></div>'
            '<div id="rot-chart"><noscript><p class="small" style="padding:12px">The chart needs JavaScript. The same data is in the tables below and in <a href="/data/rotation.json">rotation.json</a>.</p></noscript></div>'
            '<p class="small mute" id="rot-asof"></p><p class="small" id="rot-picked"></p></div>'
            + FORMULA_HTML + '</div>'
            f'<script id="rrg-data" type="application/json">{json.dumps(rdata, separators=(",", ":"))}</script>')
    md = ['# Rotation', '', f'{len(themes)} themes against SPY, weekly closes to {max(r["date"] for r in rrg)}. RS-Ratio > 100 = stronger than market. RS-Momentum > 100 = strength gaining.', '']
    for sec in sectors:
        st = [t for t in themes_pub if t['sector'] == sec]
        body += f'<h2>{E(sec)}</h2>' + table(['Theme', 'Label', 'Quadrant', 'Heading', '20D', '6M'],
            [[(f'<a href="/rotation/{t["slug"]}/">{E(t["theme"])}</a>', ''), (chip(t['label']), ''), (qchip(t['quadrant']), 'hs'),
              (E(t['heading_to'] or '—'), 'hs'), (pct(t['d20']), cls(t['d20'])), (pct(t['m6']), cls(t['m6']))] for t in st], hide=(2, 3))
        md += [f'## {sec}', '', md_table(['Theme', 'Label', 'Quadrant', 'Heading to', 'RS-Ratio', 'RS-Momentum', '20D', '6M'],
               [[f'[{t["theme"]}]({base}/rotation/{t["slug"]}.md)', t['label'], t['quadrant'], t['heading_to'], t['rs_ratio'], t['rs_momentum'], pct(t['d20']), pct(t['m6'])] for t in st]), '']
    body += '<h2>What the labels mean</h2>' + ''.join(f'<p class="small">{chip(k)} {E(v)}</p>' for k, v in LABEL_TEXT.items())
    md += ['## How the axes are calculated', '', FORMULA_MD]
    S.html('/rotation/', 'Rotation', body, 'rotation', 'Weekly relative rotation of themes against the S&P 500.', '\n'.join(md), wide=True,
           scripts='<script src="/assets/d3.v7.9.0.min.js"></script><script src="/assets/rotation.js"></script>')
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

- **Themes** hold the research: Cybersecurity, AI Science, Agentic Commerce and US Dollar Devaluation. Each theme builds over time as earnings and news add evidence, and links to the baskets that track it.
- **Thematic Baskets** express each theme as a group of stocks, equal weight from the start date, buy-and-hold.
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

Not investment advice. Positions may be held in the securities discussed. Figures come from company filings, earnings materials and public market data, and may contain errors.
"""
    S.html('/about/', 'About', md_to_html(about_md), 'about', 'What this site is and how to use its data.', about_md)

    # ---------- home ----------
    lead = sorted([t for t in themes_pub if t['quadrant'] in ('Improving', 'Leading') and t['heading_to'] == 'Leading'], key=lambda t: -(t['d20'] or 0))[:8]
    body = (f'<h1>{SITE_NAME}</h1><p class="mute">{TAGLINE} Market data to the {dfmt(asof)} close.</p>'
            '<h2>Latest research</h2>' + ''.join(pcard(p) for p in posts[:2])
            + f'<h2>Research by theme</h2><div class="themegrid">{"".join(tcard(t) for t in threads)}</div>'
            + '<h2>Thematic Baskets</h2>' + table(['Basket', 'Since start', '20D', '6M'], hide=(2,), rows=
                [[(f'<a href="/baskets/{b["slug"]}/">{E(b["name"])}</a><br><span class="mute small">from {dfmt(b["start"])}</span><br>{chip(b["label"])}', ''),
                  (pct(b['since_start']), cls(b['since_start'])), (pct(b['d20']), cls(b['d20'])), (pct(b['m6']), cls(b['m6']))] for b in baskets])
            + '<h2>Heading into Leading</h2><p class="small mute">Themes in Improving or Leading whose weekly path points toward Leading.</p>'
            + table(['Theme', 'Quadrant', '20D', 'Label'], hide=(1,), rows=[[(f'<a href="/rotation/{t["slug"]}/">{E(t["theme"])}</a>', ''), (qchip(t['quadrant']), ''),
                (pct(t['d20']), cls(t['d20'])), (chip(t['label']), '')] for t in lead])
            + '<p><a href="/rotation/">Full rotation map →</a> · <a href="/etfs/">Sector ETFs →</a></p>')
    md = [f'# {SITE_NAME}', '', TAGLINE, f'Market data to the {asof} close.', '', '## Latest research', '']
    md += [f'- [{p["title"]}]({base}{p["url"].rstrip("/")}.md) ({p["date"]}, {p["thread"]})' for p in posts[:2]]
    md += ['', '## Themes', ''] + [f'- [{t["name"]}]({base}/themes/{t["slug"]}.md): {t["summary"]}' for t in threads]
    md += ['', '## Thematic Baskets', '', md_table(['Basket', 'Start', 'Since start', '6M', 'Label'], [[f'[{b["name"]}]({base}/baskets/{b["slug"]}.md)', b['start'], pct(b['since_start']), pct(b['m6']), b['label']] for b in baskets])]
    S.html('/', SITE_NAME, body, 'home', TAGLINE, '\n'.join(md))

    # ---------- data ----------
    now = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    meta = dict(site=SITE_NAME, asof=asof, generated=now, units='returns are decimal fractions (0.05 = +5%)', source='daily closes, public market data')
    D = {'baskets.json': dict(meta, methodology=METHOD, baskets=baskets), 'themes.json': dict(meta, benchmark='SPY', themes=themes_pub),
         'rotation.json': dict(meta, method=FORMULA_MD, points=[dict(theme=r['theme'], sector=r['sector'], benchmark=r['bench'], week=r['date'], weeks_ago=r['ago'], rs_ratio=round(r['rr'], 3), rs_momentum=round(r['rm'], 3)) for r in rrg_all]),
         'theme_members.json': dict(meta, members=[dict(theme=m['theme'], ticker=m['ticker'], name=m['name'], d5=m['d5'], d20=m['d20'], m6=m['m6'], y1=m['y1'], off_high=m['off']) for m in tmem]),
         'etfs.json': dict(meta, etfs=etfs),
         'research.json': dict(meta, research=[dict(title=p['title'], date=p['date'], theme=p['thread'], tickers=p.get('tickers', []), baskets=p.get('baskets', []),
                               summary=p['summary'], url=base + p['url'], markdown=base + p['url'].rstrip('/') + '.md') for p in posts])}
    for k, v in D.items(): S.write('/data/' + k, json.dumps(v, indent=1, ensure_ascii=False))
    dbody = '<h1>Data</h1><p class="mute">Free to use with attribution. Refreshed after each US close.</p><ul>' + ''.join(f'<li><a href="/data/{k}">{k}</a></li>' for k in D) + '</ul>'
    S.html('/data/', 'Data', dbody, '', 'JSON datasets behind this site.', '# Data\n\n' + '\n'.join(f'- {base}/data/{k}' for k in D))

    # ---------- llms.txt, feed, sitemap ----------
    llms = [f'# {SITE_NAME}', '', f'> {TAGLINE} Free and open. Market data to the {asof} close.', '',
            'Research pieces are written as theses with named tickers, dated numbers and sources. Each idea is tracked as a basket from its start date.', '',
            '## Research']
    llms += [f'- [{p["title"]}]({base}{p["url"].rstrip("/")}.md): {p["date"]}. Theme: {p["thread"]}. {", ".join(p.get("tickers", []))}. {p["summary"]}' for p in posts]
    llms += ['', '## Themes'] + [f'- [{t["name"]}]({base}/themes/{t["slug"]}.md): {t["summary"]}' for t in threads]
    llms += ['', '## Thematic Baskets (equal weight, buy-and-hold)'] + [f'- [{b["name"]}]({base}/baskets/{b["slug"]}.md): from {b["start"]}, {pct(b["since_start"])} since start, label {b["label"]}. {b["summary"]}' for b in baskets]
    llms += ['', '## Market views', f'- [Rotation]({base}/rotation.md): {len(themes)} themes on a weekly rotation chart against SPY', f'- [Sector ETFs]({base}/etfs.md)', '',
             '## Data', ] + [f'- [{k}]({base}/data/{k})' for k in D] + ['', '## Optional', f'- [All research in one file]({base}/llms-full.txt)', f'- [About]({base}/about.md)']
    S.write('/llms.txt', '\n'.join(llms) + '\n')
    S.write('/llms-full.txt', '\n\n---\n\n'.join(f'# {p["title"]}\n\nDate: {p["date"]}\nTheme: {p["thread"]}\nURL: {base}{p["url"]}\n\n{p["body"]}' for p in posts) + '\n')
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
