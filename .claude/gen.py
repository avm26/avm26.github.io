#!/usr/bin/env python3
"""
Generate the AVM'26 programme site from the single source of truth,
avm26-program.md.

Run it after editing avm26-program.md (add/remove/reorder talks, change
times, chairs, sessions):

    python3 .claude/gen.py

It (re)writes, at the repo root:
  - program.html            the schedule tables (proportional 15-min grid)
  - talks/<slug>.html        one page per talk (abstract, authors, slides TBA)
  - the "programme + talk pages" CSS block appended to style.css
  - .nojekyll                so GitHub Pages serves the .md verbatim

Hand-authored session-intro pages (session-intro-*.html) are NOT generated;
they are only linked from the schedule via the INTROS map below. Add an entry
there (session display name -> intro file) to surface a "Session intro" link.

Markdown conventions the parser expects:
  # Day - theme
  ## <session header>            e.g. "Research session (morning) - <name>"
  **When:** Day, HH:MM-HH:MM  ·  **Chair:** Name
  **HH:MM-HH:MM · Label**        break / meal / registration / closing band
  ### Talk title
  *short* | *long*               (research talks only; invited=90, tutorial=60)
  abstract paragraph(s), or TBA
  Presenter Name
  *Affiliation*
  Author, list
"""
import re, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "avm26-program.md")
lines = open(MD, encoding='utf-8').read().split('\n')

BREAK_RE = re.compile(r'^\*\*\s*(\d{1,2}:\d{2})\s*[-–]\s*(\d{1,2}:\d{2})\s*·\s*(.+?)\s*\*\*\s*$')

# session display name -> hand-authored intro page (lives at repo root)
INTROS = {
    'AI and Networked Systems': 'session-intro-ai-and-networked-systems.html',
    'Embedded- and Real-Time Systems': 'session-intro-embedded-and-real-time-systems.html',
    'Model Checking and Exchange Formats': 'session-intro-model-checking-and-exchange-formats.html',
    'SAT/SMT': 'session-intro-sat-smt.html',
    'Software Verification and Formalisation': 'session-intro-software-verification-and-formalisation.html',
}

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()

def to_min(hhmm):
    h, m = hhmm.split(':'); return int(h) * 60 + int(m)

def fmt(m):
    return f"{m // 60}:{m % 60:02d}"

# ---------- parse ----------
days = []; cur = sess = None; i = 0
while i < len(lines):
    l = lines[i]
    dm = re.match(r'^# (Tuesday|Wednesday|Thursday)\b', l)
    bm = BREAK_RE.match(l)
    if dm:
        cur = {'name': l[2:].strip(), 'items': []}; days.append(cur); sess = None
    elif l.startswith('## '):
        header = l[3:].strip(); when = lines[i + 1] if i + 1 < len(lines) else ''
        m = re.search(r'\*\*When:\*\*\s*[^,]+,\s*([0-9:]+)\s*[-–]\s*[0-9:]+.*?\*\*Chair:\*\*\s*(.+?)\s*$', when)
        stype = 'invited' if header.startswith('Invited') else 'tutorial' if header.startswith('Tutorial') else 'research'
        sess = {'header': header, 'start': m.group(1) if m else '', 'chair': m.group(2).strip() if m else '',
                'stype': stype, 'talks': []}
        cur['items'].append(('session', sess))
    elif bm and cur is not None:
        cur['items'].append(('break', {'start': bm.group(1), 'end': bm.group(2), 'label': bm.group(3).strip()}))
    elif l.startswith('### '):
        title = l[4:].strip(); j = i + 1; body = []
        while j < len(lines) and not re.match(r'^#+\s', lines[j]) and not BREAK_RE.match(lines[j]):
            body.append(lines[j]); j += 1
        while body and (body[-1].strip() in ('', '---')):
            body.pop()
        bb = body[:]; k = 0
        while k < len(bb) and bb[k].strip() == '':
            k += 1
        length = None
        if k < len(bb) and re.match(r'^\*(short|long)\*$', bb[k].strip()):
            length = bb[k].strip().strip('*'); bb = bb[k + 1:]
        paras = [p.strip() for p in re.split(r'\n\s*\n', '\n'.join(bb).strip('\n')) if p.strip()]
        pp = paras[-2].split('\n')
        presenter = pp[0].strip()
        affiliation = pp[1].strip().strip('*') if len(pp) > 1 else ''
        sess['talks'].append({'title': title, 'length': length, 'presenter': presenter, 'affiliation': affiliation,
                              'authors': paras[-1], 'abstract': '\n\n'.join(paras[:-2]),
                              'slug': slugify(presenter), 'session': sess, 'day': cur['name']})
        i = j - 1
    i += 1

# ---------- durations & talk times ----------
def talk_dur(t):
    st = t['session']['stype']
    return 90 if st == 'invited' else 60 if st == 'tutorial' else (30 if t['length'] == 'long' else 15)

for day in days:
    for kind, s in day['items']:
        if kind != 'session':
            continue
        start = to_min(s['start']); s['start_min'] = start; off = 0
        for t in s['talks']:
            d = talk_dur(t); t['_start'] = start + off; t['_end'] = start + off + d; t['_dur'] = d; off += d
        s['dur'] = off

# ---------- schedule rows ----------
def talk_cell(t):
    st = t['session']['stype']
    a = f'<a href="talks/{t["slug"]}.html">{esc(t["title"])}</a>'
    if st == 'research':
        badge = f' <span class="len-badge">{t["_dur"]} min</span>'; cls = 'talk ' + (t['length'] or 'short')
    else:
        badge = ''; cls = 'talk ' + st
    html = f'<span class="who">{esc(t["presenter"])}</span>{badge}<br>{a}'
    if t['affiliation']:
        html += f'<br><span class="aff">{esc(t["affiliation"])}</span>'
    return cls, html

def session_cell(s):
    if s['stype'] == 'research':
        tag = 'Morning' if '(morning)' in s['header'] else 'Afternoon' if '(afternoon)' in s['header'] else 'Session'
        name = s['header'].split(' - ', 1)[1] if ' - ' in s['header'] else s['header']
        inner = f'<div class="s-tag">{esc(tag)}</div><div class="s-name">{esc(name)}</div>'
    else:
        name = s['header']
        inner = f'<div class="s-name">{esc(name)}</div>'
    inner += f'<div class="s-meta">Chair: {esc(s["chair"])}</div>'
    intro = INTROS.get(name)
    if intro:
        inner += f'<div class="s-intro"><a href="{intro}">Session intro &rarr;</a></div>'
    return inner

def render_session(s):
    ticks = s['dur'] // 15
    tmap = {(t['_start'] - s['start_min']) // 15: t for t in s['talks']}
    rows = []
    for k in range(ticks):
        show = fmt(s['start_min'] + k * 15) if (k in tmap or k == 0) else ''
        r = f'<tr><td class="time">{show}</td>'
        if k == 0:
            r += f'<td class="session {s["stype"]}" rowspan="{ticks}">{session_cell(s)}</td>'
        if k in tmap:
            t = tmap[k]; cls, html = talk_cell(t)
            r += f'<td class="{cls}" rowspan="{t["_dur"] // 15}">{html}</td>'
        rows.append(r + '</tr>')
    return rows

def render_band(label, start, ticks, cls):
    rows = []
    for k in range(ticks):
        show = fmt(start + k * 15) if k == 0 else ''
        r = f'<tr><td class="time">{show}</td>'
        if k == 0:
            r += f'<td class="{cls}" colspan="2" rowspan="{ticks}">{esc(label)}</td>'
        rows.append(r + '</tr>')
    return rows

def render_compact(label, start, end, cls):
    return [f'<tr><td class="time"></td><td class="{cls}" colspan="2">{fmt(start)}-{fmt(end)} · {esc(label)}</td></tr>']

def build_day(day):
    rows = []; clock = None
    for kind, obj in day['items']:
        if kind == 'session':
            rows += render_session(obj); clock = obj['start_min'] + obj['dur']
        else:
            st = to_min(obj['start']); en = to_min(obj['end']); ticks = (en - st) // 15
            lab = obj['label'].lower()
            cls = 'break' if ('coffee' in lab or 'lunch' in lab) else 'aux'
            if clock is not None and st > clock:
                rows += render_compact(obj['label'], st, en, cls)
            else:
                rows += render_band(obj['label'], st, ticks, cls)
            clock = en
    return rows

# ---------- chrome ----------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">')

def nav(p):
    return (f'<nav><ul><li><a href="{p}index.html#about">About</a></li>'
            f'<li><a href="{p}index.html#participation">Participation</a></li>'
            f'<li><a href="{p}program.html">Program</a></li>'
            f'<li><a href="{p}index.html#venue">Venue</a></li>'
            f'<li><a href="{p}index.html#registration">Registration</a></li></ul></nav>')

def footer():
    return ('<footer><div class="container footer-inner">'
            "<p>AVM'26 · Alpine Verification Meeting · 22-24 September 2026 · Eger, Hungary</p></div></footer>")

# ---------- program.html ----------
day_html = []
for day in days:
    rows = '\n'.join(build_day(day))
    day_html.append(f'<h2 class="prog-day-title">{esc(day["name"])}</h2>\n'
                    f'<div class="schedule-wrap"><table class="schedule"><tbody>\n{rows}\n</tbody></table></div>')

program = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Program - AVM'26</title>
<link rel="stylesheet" href="style.css">
{FONTS}
</head>
<body>
{nav('')}
<header class="page-header">
<div class="container">
<h1>Program</h1>
<p class="subtitle">AVM'26 · 22-24 September 2026 · Eger</p>
</div>
</header>
<main>
<section class="section prog-page">
<div class="container">
<p class="prog-download"><a href="avm26-program.md" download>&#8595; Download as Markdown</a></p>
{chr(10).join(day_html)}
<p class="prog-legend">Short talks run 15 minutes and long talks 30 minutes (discussion included), so plan for roughly 10- and 20-minute talks. Invited talks are 90 minutes and tutorials 60 minutes (discussion included).</p>
<p class="prog-update-note">The organizers may update the program dynamically as new requests come in, so please check back from time to time.</p>
</div>
</section>
</main>
{footer()}
</body>
</html>
'''
open(os.path.join(ROOT, 'program.html'), 'w', encoding='utf-8').write(program)

# ---------- talk pages ----------
os.makedirs(os.path.join(ROOT, 'talks'), exist_ok=True)
def abstract_html(ab):
    if not ab or ab.strip() == 'TBA':
        return '<p>TBA</p>'
    return '\n'.join('<p>' + esc(p.replace('\n', ' ')) + '</p>' for p in ab.split('\n\n'))

n = 0
for day in days:
    dshort = day['name'].split(' - ')[0]
    for kind, s in day['items']:
        if kind != 'session':
            continue
        for t in s['talks']:
            n += 1
            timerange = f'{fmt(t["_start"])}-{fmt(t["_end"])}'
            if s['stype'] == 'research':
                nm = s['header'].split(' - ', 1)[1] if ' - ' in s['header'] else s['header']
                mid = f' · {esc(nm)}'; kindbadge = f'<span class="len-badge">{t["_dur"]} min talk</span>'
            elif s['stype'] == 'invited':
                mid = ''; kindbadge = '<span class="len-badge inv">Invited talk</span>'
            else:
                mid = ''; kindbadge = '<span class="len-badge tut">Tutorial</span>'
            aff = f'<br><em>{esc(t["affiliation"])}</em>' if t['affiliation'] else ''
            page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(t["title"])} - AVM'26</title>
<link rel="stylesheet" href="../style.css">
{FONTS}
</head>
<body>
{nav('../')}
<header class="page-header">
<div class="container">
<a class="back-link" href="../program.html">&larr; Back to program</a>
<h1>{esc(t["title"])}</h1>
</div>
</header>
<main>
<section class="section">
<div class="container talk-page">
<p class="talk-meta">{kindbadge} · {esc(dshort)}, {timerange}{mid} · Chair: {esc(s["chair"])}</p>
<h2>Presenter</h2>
<p>{esc(t["presenter"])}{aff}</p>
<h2>Authors</h2>
<p>{esc(t["authors"])}</p>
<h2>Abstract</h2>
{abstract_html(t["abstract"])}
<h2>Slides</h2>
<p>TBA</p>
</div>
</section>
</main>
{footer()}
</body>
</html>
'''
            open(os.path.join(ROOT, 'talks', t['slug'] + '.html'), 'w', encoding='utf-8').write(page)

# ---------- CSS (re-writable block appended after the marker) ----------
CSS_MARK = '/* === programme + talk pages === */'
css_path = os.path.join(ROOT, 'style.css')
css = open(css_path, encoding='utf-8').read()
CSS = CSS_MARK + '''
.page-header {
    background: linear-gradient(135deg, rgba(26,95,122,0.95) 0%, rgba(87,131,123,0.95) 100%);
    color: var(--color-white); padding: 7rem 2rem 2.5rem; text-align: center;
}
.page-header h1 { font-family:'Playfair Display',Georgia,serif; font-size:3rem; }
.page-header .subtitle { font-size:1.1rem; opacity:0.95; margin-top:0.5rem; }
.back-link { display:inline-block; color:var(--color-white); text-decoration:none; font-weight:600; margin-bottom:0.75rem; opacity:0.9; }
.back-link:hover { opacity:1; text-decoration:underline; }

.section.prog-page { padding-top:2rem; }
.prog-download { font-size:0.85rem; margin:0 0 0.5rem; }
.prog-download a { color:var(--color-accent); text-decoration:none; }
.prog-download a:hover { text-decoration:underline; }
.prog-download + .prog-day-title { margin-top:0.5rem; }
.prog-legend { color:var(--color-text-light); font-size:0.9rem; margin-top:2.5rem; }
.prog-update-note { margin-top:0.5rem; font-style:italic; color:var(--color-text-light); font-size:0.8rem; }
.prog-day-title { font-family:'Playfair Display',Georgia,serif; color:var(--color-primary); font-size:1.8rem; text-align:left; margin:2.5rem 0 0.75rem; }

.schedule-wrap { overflow-x:auto; box-shadow:var(--shadow); border-radius:8px; }
table.schedule { width:100%; border-collapse:collapse; background:var(--color-white); font-size:0.95rem; }
.schedule td { border:1px solid #e4ebe9; padding:0.55rem 0.8rem; vertical-align:top; }
.schedule .time { white-space:nowrap; color:var(--color-text-light); font-size:0.8rem; width:1%; text-align:right; }
.schedule .session { width:13rem; vertical-align:middle; background:var(--color-background-alt); }
.schedule .session .s-tag { font-size:0.72rem; text-transform:uppercase; letter-spacing:0.04em; color:var(--color-accent); font-weight:700; }
.schedule .session .s-name { font-weight:700; color:var(--color-primary); line-height:1.3; }
.schedule .session .s-meta { font-size:0.82rem; color:var(--color-text-light); margin-top:0.25rem; }
.schedule .session.invited { background:#f2ebf9; }
.schedule .session.tutorial { background:#f8f4e8; }
.schedule .talk { border-left:4px solid var(--color-accent); }
.schedule .talk.long { border-left-color:var(--color-primary); }
.schedule .talk.invited { border-left-color:#7d4a9e; background:#f7f1fb; }
.schedule .talk.tutorial { border-left-color:#c9a227; background:#fcfaf3; }
.schedule .talk .who { font-weight:600; color:var(--color-text); }
.schedule .talk .aff { font-size:0.78rem; color:var(--color-text-light); }
.schedule .talk a { color:var(--color-primary); text-decoration:none; }
.schedule .talk a:hover { text-decoration:underline; }
.schedule .break, .schedule .aux { text-align:center; color:var(--color-text-light); font-style:italic; background:#f5f8f7; }
.schedule .aux { font-size:0.85rem; }
.len-badge { display:inline-block; font-size:0.68rem; font-weight:700; color:var(--color-accent); background:#eaf1ef; border-radius:10px; padding:0.05rem 0.5rem; vertical-align:middle; }
.len-badge.inv { color:#6a3e8a; background:#ece0f5; }
.len-badge.tut { color:#8a6d1a; background:#f3ebd2; }

.schedule .session .s-intro { margin-top:0.4rem; font-size:0.8rem; }
.schedule .session .s-intro a { color:var(--color-accent); text-decoration:none; font-weight:600; }
.schedule .session .s-intro a:hover { text-decoration:underline; }

.talk-page { max-width:760px; }
.talk-page h2 { color:var(--color-primary); font-size:1.2rem; margin:1.75rem 0 0.4rem; text-align:left; }
.talk-page p { text-align:left; max-width:none; margin-left:0; margin-right:0; }
.talk-page .talk-meta { color:var(--color-text-light); }

.intro-page { max-width:760px; }
.intro-page p { text-align:left; max-width:none; margin-left:0; margin-right:0; margin-bottom:1.1rem; }
.intro-page h2 { color:var(--color-primary); font-size:1.2rem; margin:2rem 0 0.6rem; text-align:left; }
.intro-page .intro-keywords { background:var(--color-background-alt); border-radius:8px; padding:1rem 1.25rem; font-size:0.95rem; line-height:1.9; }
.intro-page ol.intro-sources { padding-left:1.4rem; margin-top:0.5rem; }
.intro-page ol.intro-sources li { padding:0.2rem 0; font-size:0.9rem; color:var(--color-text-light); }
.intro-page ol.intro-sources li a { color:var(--color-accent); overflow-wrap:anywhere; }

@media (max-width:600px) {
    .schedule .session { width:auto; }
    .page-header h1 { font-size:2rem; }
}
'''
if CSS_MARK in css:
    css = css[:css.index(CSS_MARK)].rstrip()
open(css_path, 'w', encoding='utf-8').write(css.rstrip() + '\n\n' + CSS)

open(os.path.join(ROOT, '.nojekyll'), 'a').close()
print(f"OK: program.html + {n} talk pages; style.css block written; .nojekyll ensured")
