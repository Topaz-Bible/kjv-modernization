#!/usr/bin/env python3
"""Paragraph and poetry breaks of the Cambridge Paragraph Bible (Scrivener, 1873), placed on the KJV's words.

Source: eBible.org's "KJV Cambridge Paragraph Bible" (engkjvcpb), public domain, as USFM
(https://ebible.org/find/details.php?id=engkjvcpb). Its \\p, \\m, \\q1/\\q2 and \\b lines are Scrivener's
paragraphs, poetry lines and stanza breaks. They become Topaz package markers, the same way the
BSB's are made (topaz/scripts/bsb_pass2_usfm.py):

  \\p, \\m          paragraph                      (\\m: prose taking up again after poetry)
  \\q1, \\q2        line_break, level 1 or 2       and the verse joins a poetic region
  \\b               stanza_break inside poetry, paragraph outside it

A break is placed right after the KJV word that matches the last word before it (the two texts differ
in a few words; the words are matched in order).

Reads: keyway-data/sources/kjv-cambridge-paragraph-ebible/usfm/*.usfm and the app's KJV package.
Writes: breaks/cambridge/breaks.json, and with --apply the markers into the KJV package zip
(replacing its paragraph marks, which follow the 1611 ¶ signs; headings stay).

Run:  python3 tools/build_cambridge_breaks.py [--apply]
"""
import collections, difflib, json, re, sys, zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO.parent / 'keyway-data' / 'sources' / 'kjv-cambridge-paragraph-ebible' / 'usfm'
PKG = REPO.parent / 'topaz-bible' / 'assets' / 'packages' / 'eng.bible.kjv.zip'
OUT = REPO / 'breaks' / 'cambridge'
BREAKS = {'p', 'm', 'q1', 'q2', 'q3', 'b', 'nb', 'mi', 'pi'}


def norm(t):
    return re.sub(r'[^a-z]', '', t.lower())


def read_usfm(path):
    """{(chapter, verse): {'words': [...], 'breaks': [(word offset, marker)]}} and the verses set as poetry."""
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'\\f .*?\\f\*|\\x .*?\\x\*', ' ', text)
    verses, poetry = collections.defaultdict(lambda: {'words': [], 'breaks': []}), set()
    ch = v = 0
    pending, mode, in_title = [], None, False
    for tok in re.findall(r'\\[a-z0-9]+\*?|[^\s\\]+', text):
        if tok.startswith('\\'):
            m = tok[1:]
            if m == 'c':
                in_title = 'c'
                continue
            if m == 'v':
                in_title = 'v'
                continue
            if m == 'd':
                in_title = 'd'
                continue
            if m.rstrip('*') in ('add', 'sc', 'nd', 'w', 'wj', 'qs', 'it', 'bd', 'em', 'tl'):
                continue
            if m in BREAKS:
                in_title = False
                if m == 'b':
                    pending.append('stanza' if mode == 'q' else 'p')
                elif m != 'nb':
                    pending.append(m)
                    mode = 'q' if m.startswith('q') else 'p'
                continue
            in_title = 'skip'  # headings, titles, introductions
            continue
        if in_title == 'c':
            ch, v, in_title, pending = int(tok), 0, False, []
            continue
        if in_title == 'v':
            v, in_title = int(re.match(r'\d+', tok)[0]), False
            continue
        if in_title in ('d', 'skip') or not ch or not v:
            continue
        rec = verses[(ch, v)]
        for p in pending:
            rec['breaks'].append((len(rec['words']), p))
        pending = []
        if mode == 'q':
            poetry.add((ch, v))
        rec['words'].append(tok)
    return verses, poetry


def place(cpb_words, kjv_tokens):
    """CPB word offset → KJV token number, for the words that match."""
    a = [norm(w) for w in cpb_words]
    b = [norm(t['t']) for t in kjv_tokens]
    m = {}
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for d in range(blk.size):
            m[blk.a + d] = kjv_tokens[blk.b + d]['n']
    return m


def main():
    z = zipfile.ZipFile(PKG)
    books = [b['book_id'] for b in json.loads(z.read('manifest.json'))['books']]
    files = {p.name[3:6]: p for p in SRC.glob('*.usfm')}
    out, counts, problems = {}, collections.Counter(), []
    for bk in books:
        if bk not in files:
            problems.append(f'{bk}: not in the Cambridge USFM')
            continue
        verses, poetry = read_usfm(files[bk])
        K = json.loads(z.read(f'{bk}.json'))
        book = {'markers': {}, 'poetic_regions': []}
        run = None
        for c in K['chapters']:
            for vv in c['verses']:
                key = (c['chapter'], vv['verse'])
                body = [t for t in vv['tokens'] if 'pre' not in (t.get('f') or [])]
                rec = verses.get(key)
                if rec is None:
                    if body:
                        problems.append(f'{bk} {key[0]}:{key[1]}: verse not in the Cambridge USFM')
                    continue
                m = place(rec['words'], body)
                marks = []
                for off, kind in rec['breaks']:
                    if off == 0:
                        n = body[0]['n'] if body else 1
                    else:
                        # Right after the last matched word before the break, so a word the two texts
                        # word differently ("or who" / "And who") goes with the line it opens.
                        prev = next((m[j] for j in range(off - 1, -1, -1) if j in m), None)
                        n = prev + 1 if prev is not None and prev < body[-1]['n'] else None
                        if n is None:
                            problems.append(f'{bk} {key[0]}:{key[1]}: break before word {off + 1} not placed')
                            continue
                    if kind in ('p', 'm', 'mi', 'pi'):
                        mk = {'type': 'paragraph', 'position': n}
                    elif kind == 'stanza':
                        mk = {'type': 'stanza_break', 'position': n}
                    else:
                        mk = {'type': 'line_break', 'position': n, 'level': 2 if kind in ('q2', 'q3') else 1}
                    # Chapter starts are breaks already; a paragraph there adds nothing.
                    if mk['type'] == 'paragraph' and key[1] == 1 and n == (body[0]['n'] if body else 1):
                        continue
                    if mk not in marks:
                        marks.append(mk)
                        counts[mk['type']] += 1
                if marks:
                    book['markers'][f'{key[0]}:{key[1]}'] = marks
                loc = f'{bk}.{key[0]:03}.{key[1]:03}'
                if key in poetry:
                    if run and run['chapter'] == key[0]:
                        run['end'] = loc
                    else:
                        run = {'start': loc, 'end': loc, 'chapter': key[0]}
                        book['poetic_regions'].append(run)
                else:
                    run = None
        for r in book['poetic_regions']:
            r.pop('chapter', None)
        counts['poetic_regions'] += len(book['poetic_regions'])
        out[bk] = book
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump({'source': 'The Cambridge Paragraph Bible, ed. F. H. A. Scrivener (1873), via eBible.org engkjvcpb '
                         '(public domain): https://ebible.org/find/details.php?id=engkjvcpb',
               'anchors': 'position = word number in the Topaz KJV package verse',
               'kjv_package': json.loads(z.read('manifest.json'))['package_version'],
               'books': out}, open(OUT / 'breaks.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    (OUT / 'problems.txt').write_text('\n'.join(problems) + '\n')
    print(dict(counts), len(problems), 'problems')
    if '--apply' in sys.argv:
        apply(z, out)


def apply(z, out):
    files = {n: z.read(n) for n in z.namelist()}
    for bk, book in out.items():
        K = json.loads(files[f'{bk}.json'])
        for c in K['chapters']:
            for vv in c['verses']:
                keep = [m for m in vv.get('markers', []) if m['type'] not in ('paragraph', 'line_break', 'stanza_break')]
                new = book['markers'].get(f"{c['chapter']}:{vv['verse']}", []) + keep
                if new:
                    vv['markers'] = new
                else:
                    vv.pop('markers', None)
        K['poetic_regions'] = book['poetic_regions']
        files[f'{bk}.json'] = json.dumps(K, ensure_ascii=False, separators=(',', ':')).encode()
    m = json.loads(files['manifest.json'])
    m['distribution_revision'] += 1
    m['package_version'] = m['package_version'].rsplit('.', 1)[0] + f".{m['distribution_revision']}"
    files['manifest.json'] = json.dumps(m, ensure_ascii=False, indent=2).encode()
    with zipfile.ZipFile(str(PKG) + '.tmp', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as w:
        for n, d in files.items():
            w.writestr(n, d)
    Path(str(PKG) + '.tmp').replace(PKG)
    print('applied →', m['package_version'])


main()
