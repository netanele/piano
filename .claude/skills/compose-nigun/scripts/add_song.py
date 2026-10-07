#!/usr/bin/env python3
"""Check a new song (JSON file) and add it to the end of NIGUNIM in index.html.

Usage: python3 -I add_song.py <song.json> [<index.html>] [--check]
--check only validates and prints the bar-by-bar summary; nothing is written."""
import json, re, subprocess, sys, tempfile, os

DURS = {'w': 4, 'h.': 3, 'h': 2, 'q.': 1.5, 'q': 1, '8.': .75, '8': .5, '16': .25}
TOK = re.compile(r'^(R|[A-G](?:#|b)?[1-7])/(w|h\.|h|q\.|q|8\.|8|16)(?:/[1-5])?~?$')
CHORD = re.compile(r'^[A-G](b|#)?(m|dim)?7?$')
GROUPS = {'ai'}  # songs made by this skill always go in the "AI created" section
NEED = ['id', 't', 'short', 'he', 'by', 'group', 'attribText', 'key', 'time', 'tempo', 'sec', 'form', 'lev', 'warm', 'warmName', 'about']
ANCHOR = '\n}\n];\n\n/* ---------------- song model'

def bars(src, meter):
    out = []
    for b in src.split('|'):
        t, depth, errs = 0.0, 0, []
        for tok in b.split():
            m = re.match(r'^\[(\d+)/4\]$', tok)
            if m: meter = int(m.group(1)); continue
            if tok == 'T3[': depth += 1; continue
            if tok == ']': depth -= 1; continue
            m = TOK.match(tok)
            if not m: errs.append('bad note "%s"' % tok); continue
            t += DURS[m.group(2)] * (2 / 3) ** depth
        out.append((round(t, 4), meter, errs))
    return out, meter

def check(s, src):
    errs = []
    for k in NEED:
        if k not in s: errs.append('missing field "%s"' % k)
    if errs: return errs
    if s['group'] not in GROUPS: errs.append('group must be "ai" (the "AI created" section)')
    if not re.match(r'^[a-z0-9-]+$', s['id']): errs.append('id should be lowercase letters, digits, dashes')
    if re.search(r'"id":\s*"%s",\s*"t":' % re.escape(s['id']), src): errs.append('id "%s" is already used' % s['id'])
    if not 1 <= s['lev'] <= 5: errs.append('lev must be 1-5')
    if len(s['warm']) != 5: errs.append('warm should list 5 notes')
    meter, ids = s['time'], set()
    if s.get('pick'):
        (p, _, e), = bars(s['pick'], meter)[0]
        errs += e
        if not 0 < p < meter: errs.append('pick-up must be shorter than a full bar (it is %s beats)' % p)
    for x in s['sec']:
        ids.add(x['id'])
        bl, meter = bars(x['n'], meter)
        ch = x.get('c', '').split('|')
        if len(ch) != len(bl): errs.append('section %s: %d bars of notes but %d bars of chords' % (x['id'], len(bl), len(ch)))
        for i, (t, m, e) in enumerate(bl):
            errs += ['section %s bar %d: %s' % (x['id'], i + 1, z) for z in e]
            if abs(t - m) > 1e-3: errs.append('section %s bar %d: %s beats, needs %s' % (x['id'], i + 1, t, m))
        for c in ' '.join(ch).split():
            if not CHORD.match(c): errs.append('section %s: unknown chord "%s"' % (x['id'], c))
    for f in s['form']:
        if f not in ids: errs.append('form uses unknown section "%s"' % f)
    return errs

def notes(n):
    out = []
    for tok in n.split():
        m = TOK.match(tok)
        if m and m.group(1) != 'R': out.append((m.group(1), m.group(2)))
    return out

def copied(s, src):
    """Runs of 5 notes (same pitches and lengths) or whole bars of 4+ notes that already exist in another song."""
    old5, oldbars = set(), set()
    for n in re.findall(r'"n":\s*"([^"]*)"', src):
        for b in n.split('|'):
            ns = notes(b)
            if len(ns) >= 4: oldbars.add(tuple(ns))
        ns = notes(n.replace('|', ' '))
        old5.update(tuple(ns[i:i + 5]) for i in range(len(ns) - 4))
    errs = []
    for x in s['sec']:
        for i, b in enumerate(x['n'].split('|')):
            if tuple(notes(b)) in oldbars: errs.append('section %s bar %d is identical to a bar of an existing song' % (x['id'], i + 1))
        ns = notes(x['n'].replace('|', ' '))
        for i in range(len(ns) - 4):
            if tuple(ns[i:i + 5]) in old5: errs.append('section %s: the run %s already appears in an existing song' % (x['id'], ' '.join('/'.join(t) for t in ns[i:i + 5])))
    return sorted(set(errs))

def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if not a: sys.exit(__doc__)
    song = json.load(open(a[0], encoding='utf-8'))
    path = a[1] if len(a) > 1 else 'index.html'
    src = open(path, encoding='utf-8').read()
    errs = check(song, src)
    if not errs: errs = copied(song, src)
    if errs: print('NOT ADDED. Fix these:'); [print(' -', e) for e in errs]; sys.exit(1)
    n = sum(len(x['n'].split('|')) for x in song['sec'])
    print('OK: "%s", %d sections, %d bars, form %s' % (song['t'], len(song['sec']), n, ' '.join(song['form'])))
    if '--check' in sys.argv: return
    if src.count(ANCHOR) != 1: sys.exit('Could not find the end of the NIGUNIM list in %s' % path)
    song.setdefault('attrib', ''); song.setdefault('credit', ''); song.setdefault('creditUrl', ''); song.setdefault('pick', ''); song.setdefault('partial', '')
    src = src.replace(ANCHOR, '\n},\n' + json.dumps(song, ensure_ascii=False, indent=0) + ANCHOR[2:], 1)
    open(path, 'w', encoding='utf-8').write(src)
    print('Added to NIGUNIM in', path)
    js = max(re.findall(r'<script>(.*?)</script>', src, re.S), key=len)
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f: f.write(js)
    try:
        r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
        print('Page script check:', 'OK' if r.returncode == 0 else 'FAILED\n' + r.stderr)
    except FileNotFoundError: print('Page script check skipped (node not installed)')
    finally: os.unlink(f.name)

main()
