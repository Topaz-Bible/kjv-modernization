#!/usr/bin/env python3
"""Fold the KJVm layers into the KJV modernization profile (mod.json) that the Topaz app reads.

The word rules already live in mod.json. This adds, from this repository's layer files:
  token_edits    single-word changes made before the word rules run:
                   name     Elias → Elijah             (names/names.json)
                   capital  thee → Thee                (capitals/capitals.json)
                   case     "said, That …" → "that"   (worked out here; see quotes/README.md)
  quote_regions  {book: [{start, end, level}]}         (quotes/kjv-quotes.json, tiers 1–2 until the rest are reviewed)

A quote that opens on a lowercased "that" opens on the next word instead:
it was said, that “in Isaac shall thy seed be called.”

Everything else in mod.json is left byte-for-byte as it was.

Run:  python3 tools/compose_profile.py [path/to/eng.bible.kjv.mod.json] [path/to/packages]
      (defaults: ../topaz/packages/eng.bible.kjv/eng.bible.kjv.mod.json and ../topaz-bible/assets/packages)
"""
import json, re, sys, zipfile, collections
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MOD = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO.parent / 'topaz' / 'packages' / 'eng.bible.kjv' / 'eng.bible.kjv.mod.json'
PKG = Path(sys.argv[2]) if len(sys.argv) > 2 else REPO.parent / 'topaz-bible' / 'assets' / 'packages'
QUOTE_TIERS = {1, 2}
# The Greek and Hebrew words that introduce a saying: ὅτι, כִּי, אֲשֶׁר.
SAYING_THAT = {'G3754', 'H3588', 'H834'}


def strongs(s):
    m = re.match(r'([GH])0*(\d+)', s or '')
    return m.group(1) + m.group(2) if m else None


def edit(book, ch, v, n, kjv, new, category):
    return {'location': {'book_id': book, 'chapter': ch, 'verse': v, 'token': n},
            'match': {'text': kjv}, 'replace': {'text': new}, 'category': category}


def that_edits():
    """Capital "That" after a comma or colon, where the Greek or Hebrew is the word that introduces a saying."""
    kjv = zipfile.ZipFile(PKG / 'eng.bible.kjv.zip')
    keys = {'nt': zipfile.ZipFile(PKG / 'grc.key.nt.zip'), 'ot': zipfile.ZipFile(PKG / 'hbo.key.ot.zip')}
    out = []
    for b in json.loads(kjv.read('manifest.json'))['books']:
        kp = keys['nt' if b['canon'] == 'nt' else 'ot']
        if f"{b['book_id']}.json" not in kp.namelist():
            continue
        KP = json.loads(kp.read(f"{b['book_id']}.json"))['verses']
        for c in json.loads(kjv.read(f"{b['book_id']}.json"))['chapters']:
            for v in c['verses']:
                T, kv = v['tokens'], KP.get(f"{c['chapter']}:{v['verse']}", {})
                for i in range(1, len(T)):
                    if (T[i]['t'] == 'That' and re.search(r'[,:;]\s*$', T[i - 1].get('a') or '')
                            and strongs(kv.get(T[i].get('k'), [None, None])[1]) in SAYING_THAT):
                        out.append(edit(b['book_id'], c['chapter'], v['verse'], T[i]['n'], 'That', 'that', 'case'))
    return out


def main():
    raw = MOD.read_text()
    m = json.loads(raw)
    edits = []
    for r in json.load(open(REPO / 'names' / 'names.json'))['changes']:
        edits.append(edit(r['book'], r['chapter'], r['verse'], r['word'], r['kjv'], r['modernized'], 'name'))
    for r in json.load(open(REPO / 'capitals' / 'capitals.json'))['changes']:
        edits.append(edit(r['book'], r['chapter'], r['verse'], r['word'], r['kjv'], r['modernized'], 'capital'))
    thats = that_edits()
    edits += thats
    lowered = {(e['location']['book_id'], f"{e['location']['chapter']:03}.{e['location']['verse']:03}:{e['location']['token']:03}")
               for e in thats}

    quotes = collections.defaultdict(list)
    for r in json.load(open(REPO / 'quotes' / 'kjv-quotes.json'))['regions']:
        if r['tier'] not in QUOTE_TIERS or 'overlaps another quote' in r['checks']:
            continue
        start = r['start']
        if (r['book'], start) in lowered:
            cv, n = start.split(':')
            start = f'{cv}:{int(n) + 1:03}'
        quotes[r['book']].append({'start': start, 'end': r['end'], 'level': r['level']})

    m['token_edits'] = edits
    m['quote_regions'] = dict(quotes)
    out = json.dumps(m, indent=2, ensure_ascii=False) + '\n'
    MOD.write_text(out)
    counts = collections.Counter(e['category'] for e in edits)
    print(f"{MOD.name}: {dict(counts)} token edits; {sum(map(len, quotes.values()))} quote regions in {len(quotes)} books")


main()
