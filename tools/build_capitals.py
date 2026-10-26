#!/usr/bin/env python3
"""Capitalize pronouns that refer to God (He, Him, His, Thou, Thee, Thy, Me, My…), following the BSB.

The KJV never capitalized these. Many modern Bibles do, and the BSB is the template here: whatever it
capitalizes, this layer capitalizes in the same verse, which also settles the hard cases (messianic
psalms, people speaking to Jesus before they know who he is) the BSB's way.

How a BSB capital is found in the KJV. Pronouns are sorted into three groups:
  he    he, him, his, himself
  you   thou, thee, thy, thine, thyself (and you, ye, your… in the KJV)
  me    me, my, mine, myself
Within one verse, when the KJV has the same number of a group's pronouns as the BSB, they pair up in
order. When the counts differ, nothing is changed and the verse is listed for review.

Only capitals that the BSB uses mid-sentence count. A capital that starts a sentence or a quote
says nothing about who is meant, so such a pronoun follows the others of its group in the verse when
they all refer to God, and is otherwise left alone.

Reads (read-only): eng.bible.kjv.zip and eng.bible.bsb.zip from the app's package folder.
Writes: capitals/capitals.json (every change, and the verses left for review) and capitals/review.md.

Run:  python3 tools/build_capitals.py [path/to/topaz-bible/assets/packages]
"""
import json, re, sys, zipfile, collections
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PKG = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO.parent / 'topaz-bible' / 'assets' / 'packages'
OUT = REPO / 'capitals'

BSB_GROUPS = {'he': {'he', 'him', 'his', 'himself'}, 'you': {'you', 'your', 'yours', 'yourself'},
              'me': {'me', 'my', 'mine', 'myself'}}
KJV_GROUPS = {'he': {'he', 'him', 'his', 'himself'},
              'you': {'thou', 'thee', 'thy', 'thine', 'thyself', 'you', 'ye', 'your', 'yours', 'yourself'},
              'me': {'me', 'my', 'mine', 'myself'}}
ENDS_SENTENCE = re.compile(r'[.?!:;]\s*$')


def group(word, groups):
    w = word.lower()
    return next((g for g, s in groups.items() if w in s), None)


kjv = zipfile.ZipFile(PKG / 'eng.bible.kjv.zip')
bsb = zipfile.ZipFile(PKG / 'eng.bible.bsb.zip')
manifest = json.loads(kjv.read('manifest.json'))
changes, review, counts = [], [], collections.Counter()

for b in manifest['books']:
    bk = b['book_id']
    if f'{bk}.json' not in bsb.namelist():
        continue
    K = json.loads(kjv.read(f'{bk}.json'))
    B = json.loads(bsb.read(f'{bk}.json'))
    quote_starts = {q['start'] for q in B.get('quotes', [])}
    bverses = {}
    prev_a = '.'
    for c in B['chapters']:
        for v in c['verses']:
            out = collections.defaultdict(list)
            for i, t in enumerate(v['tokens']):
                before = v['tokens'][i - 1].get('a', '') if i else prev_a
                g = group(t['t'], BSB_GROUPS)
                if g:
                    starts = (ENDS_SENTENCE.search(before or '') or
                              f"{c['chapter']:03}.{v['verse']:03}:{t['n']:03}" in quote_starts)
                    # None = can't tell (sentence start); True = capital mid-sentence; False = lower case
                    out[g].append(None if starts and t['t'][:1].isupper() else t['t'][:1].isupper())
            if v['tokens']:
                prev_a = v['tokens'][-1].get('a', '')
            bverses[(c['chapter'], v['verse'])] = out
    for c in K['chapters']:
        for v in c['verses']:
            bv = bverses.get((c['chapter'], v['verse']), {})
            kv = collections.defaultdict(list)
            for t in v['tokens']:
                g = group(t['t'], KJV_GROUPS)
                if g:
                    kv[g].append(t)
            for g, flags in bv.items():
                if True not in flags:
                    continue
                ks = kv.get(g, [])
                if len(ks) != len(flags):
                    review.append({'book': bk, 'chapter': c['chapter'], 'verse': v['verse'], 'group': g,
                                   'bsb': len(flags), 'kjv': len(ks),
                                   'text': ' '.join(t['t'] + (t.get('a') or '') for t in v['tokens'])})
                    continue
                # A pronoun at a sentence or quote start hides the BSB's choice. When every other one of
                # the group in the verse refers to God, so does it ("Sir, thou hast nothing to draw with…").
                if False not in flags:
                    flags = [True] * len(flags)
                for t, f in zip(ks, flags):
                    # KJV ye/you/your are plural, so never one person (they only keep the pairing in step).
                    if f and not t['t'][:1].isupper() and t['t'].lower() not in ('ye', 'you', 'your', 'yours', 'yourself'):
                        changes.append({'book': bk, 'chapter': c['chapter'], 'verse': v['verse'], 'word': t['n'],
                                        'kjv': t['t'], 'modernized': t['t'][:1].upper() + t['t'][1:]})
                        counts[t['t'].lower()] += 1

OUT.mkdir(exist_ok=True)
json.dump({'kjv_package': manifest['package_version'], 'bsb_package': json.loads(bsb.read('manifest.json'))['package_version'],
           'counts': dict(counts.most_common()), 'changes': changes, 'review': review},
          open(OUT / 'capitals.json', 'w'), indent=1, ensure_ascii=False)
lines = ['# Pronouns for God: verses left for review\n',
         f'Generated by `tools/build_capitals.py`. {len(changes)} pronouns capitalized; these {len(review)} '
         'verses were left alone because the KJV and BSB have a different number of pronouns, so they '
         "can't be paired up automatically.\n"]
lines += [f"- **{r['book']} {r['chapter']}:{r['verse']}** ({r['group']}: BSB {r['bsb']}, KJV {r['kjv']}) {r['text']}"
          for r in review]
(OUT / 'review.md').write_text('\n'.join(lines) + '\n')
print(len(changes), 'changed;', len(review), 'verses to review'); print(counts.most_common())
