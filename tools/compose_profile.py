#!/usr/bin/env python3
"""Fold the KJVo layers into the KJV modernization profile (mod.json) that the Topaz app reads.

The word rules already live in mod.json. This adds, from this repository's layer files:
  token_edits    single-word changes made before the word rules run:
                   name     Elias → Elijah             (names/names.json)
                   case     "said, That …" → "that"   (worked out here, and quotes/that-by-hand.csv where the
                            Hebrew word isn't one that introduces a saying; see quotes/README.md)
The pronoun capitals (capitals/) are switched off: most modern Bibles don't capitalize pronouns for God,
and deciding who "he" is would be interpretation (capitals/README.md).
                            "called the light Day" → “day”: a quoted term is lowercased where the BSB has
                            it lowercase and the KJV uses the word lowercase elsewhere (quotes or a capital,
                            not both)
                   join     "To day" → "Today": no space before the second word (words/joins.csv); the
                            two words stay two tokens, so each keeps its own Strong's number and tap
  split rules    "stumblingblock" → "stumbling block": word rules of category `split` (words/splits.csv),
                 replacing the ones the last run wrote; the word stays one token
  quote_regions  {book: [{start, end, level}]}         (quotes/kjv-quotes.json, tiers 1–2 until the rest are reviewed,
                                                        plus the ones quotes/reviewed.csv ships, less the ones it drops)

A quote that opens on a lowercased "that" opens on the next word instead:
it was said, that “in Isaac shall thy seed be called.”

Everything else in mod.json (the other word rules among them) is left byte-for-byte as it was.

Run:  python3 tools/compose_profile.py [path/to/eng.bible.kjv.mod.json] [path/to/packages]
      (defaults: ../topaz/packages/eng.bible.kjv/eng.bible.kjv.mod.json and ../topaz-bible/assets/packages)
"""
import csv, json, re, sys, zipfile, collections
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


def term_edits(regions):
    """Lowercase a capitalized term that the KJVo sets in quotation marks."""
    kjv = zipfile.ZipFile(PKG / 'eng.bible.kjv.zip')
    bsb = zipfile.ZipFile(PKG / 'eng.bible.bsb.zip')
    books, lower = {}, set()
    def verses(z, bk):
        if (z, bk) not in books:
            books[(z, bk)] = {(c['chapter'], v['verse']): v['tokens'] for c in json.loads(z.read(f'{bk}.json'))['chapters']
                              for v in c['verses']}
        return books[(z, bk)]
    for n in kjv.namelist():
        if re.fullmatch(r'[0-9A-Z]{3}\.json', n):
            lower.update(t['t'] for vs in verses(kjv, n[:3]).values() for t in vs if t['t'][:1].islower())
    out = []
    for r in regions:
        cv, n0 = r['start'].split(':')
        c, v = map(int, cv.split('.'))
        n1 = int(r['end'].split(':')[1])
        bc, bv, bn = r['bsb'][0].replace(':', '.').split('.')
        if not verses(bsb, r['book'])[(int(bc), int(bv))][int(bn) - 1]['t'][:1].islower():
            continue
        for t in verses(kjv, r['book'])[(c, v)]:
            if int(n0) <= t['n'] <= n1 and t['t'][:1].isupper() and t['t'].lower() in lower:
                out.append(edit(r['book'], c, v, t['n'], t['t'], t['t'].lower(), 'case'))
    return out


def split_rules():
    """Words the KJV prints as one that are written as two today (words/splits.csv): a word rule each."""
    rows = list(csv.DictReader(open(REPO / 'words' / 'splits.csv')))
    return [{'id': f"split-{r['joined']}", 'enabled': True, 'category': 'split',
             'match': {'text': r['joined']}, 'replace': {'text': r['split']}} for r in rows]


def join_edits(quotes):
    """Word pairs written as one word today ("to day" → "today"), set close up in the KJVo.

    Not where punctuation, a line break or a quotation mark falls between the two words.
    """

    pairs = {(r['first'], r['second']) for r in csv.DictReader(open(REPO / 'words' / 'joins.csv'))}
    # A quote that closes on the first word or opens on the second puts a mark between them.
    ends, starts = collections.defaultdict(set), collections.defaultdict(set)
    for bk, rs in quotes.items():
        for r in rs:
            ends[bk].add(r['end'])
            starts[bk].add(r['start'])
    kjv = zipfile.ZipFile(PKG / 'eng.bible.kjv.zip')
    out = []
    for b in json.loads(kjv.read('manifest.json'))['books']:
        bk = b['book_id']
        for c in json.loads(kjv.read(f'{bk}.json'))['chapters']:
            for v in c['verses']:
                T = v['tokens']
                breaks = {m['position'] for m in v.get('markers', []) if m['type'] != 'heading'}
                for a, t in zip(T, T[1:]):
                    if (a['t'].lower(), t['t']) not in pairs or a.get('a') or t.get('b') or t['n'] in breaks:
                        continue
                    loc = lambda x: f"{c['chapter']:03}.{v['verse']:03}:{x['n']:03}"
                    if loc(a) in ends[bk] or loc(t) in starts[bk]:
                        continue
                    out.append(edit(bk, c['chapter'], v['verse'], t['n'], t['t'], t['t'], 'join'))
    return out


def main():
    raw = MOD.read_text()
    m = json.loads(raw)
    edits = []
    for r in json.load(open(REPO / 'names' / 'names.json'))['changes']:
        edits.append(edit(r['book'], r['chapter'], r['verse'], r['word'], r['kjv'], r['modernized'], 'name'))
    for r in csv.DictReader(open(REPO / 'quotes' / 'that-by-hand.csv')):
        edits.append(edit(r['book'], int(r['chapter']), int(r['verse']), int(r['word']), r['kjv'], r['modernized'], 'case'))
    thats = that_edits()
    edits += thats
    lowered = {(e['location']['book_id'], f"{e['location']['chapter']:03}.{e['location']['verse']:03}:{e['location']['token']:03}")
               for e in thats}


    # A row applies to every region with its edges, or, with a level, only to the region at that level
    # (an outer and inner quote can share edges). An added row with the same edges replaces the region.
    reviewed = {(x['book'], x['start'], x['end'], 'add' if x['decision'] == 'add' else x.get('level') or ''): x
                for x in csv.DictReader(open(REPO / 'quotes' / 'reviewed.csv'))}

    def review(r):
        k = (r['book'], r.get('start'), r.get('end'))
        if k + ('add',) in reviewed:
            return reviewed[k + ('add',)]
        return reviewed.get(k + (str(r['level']),)) or reviewed.get(k + ('',))

    quotes, shipped = collections.defaultdict(list), []
    regions = json.load(open(REPO / 'quotes' / 'kjv-quotes.json'))['regions']
    # A speech shipped by hand takes the quotes inside it along.
    by_hand = collections.defaultdict(list)
    for r in regions:
        row = review(r)
        if row and row['decision'] in ('ship', 'fix') and r['level'] == 1:
            by_hand[r['book']].append((row['fix_start'] or r['start'], row['fix_end'] or r['end']))
    for r in regions:
        row = review(r)
        decision = row and row['decision']
        if decision in ('drop', 'add'):
            continue
        if decision == 'fix':
            # Edges set by hand. A quote within a quote waits for its outer one (the nested review).
            r = {**r, 'start': row['fix_start'], 'end': row['fix_end']}
            decision = 'ship' if r['level'] == 1 else None
        # Quotes the KJV's own speech tag found (no BSB anchor) were read one by one; the wrong ones
        # are dropped or fixed in reviewed.csv.
        found = r['checks'] == ['found by the KJV speech tag (no BSB anchor)']
        inside = r['level'] > 1 and any(a <= r.get('start', '') and r.get('end', '~') <= b for a, b in by_hand[r['book']])
        if decision != 'ship' and not found and not r.get('nested') and not inside and (r['tier'] not in QUOTE_TIERS or 'overlaps another quote' in r['checks']):
            continue
        if r.get('term'):
            shipped.append(r)
        start = r['start']
        if (r['book'], start) in lowered:
            cv, n = start.split(':')
            start = f'{cv}:{int(n) + 1:03}'
        quotes[r['book']].append({'start': start, 'end': r['end'], 'level': r['level']})

    # Quotes the BSB has that no rule could place in the KJV, added by hand (level 1 unless the row says).
    for x in reviewed.values():
        if x['decision'] == 'add':
            assert not (x['fix_start'] or x['fix_end']), f"add row with fix edges: {x}"
            quotes[x['book']].append({'start': x['start'], 'end': x['end'], 'level': int(x.get('level') or 1)})
    for bk, rs in quotes.items():
        # Of two quotes of one level that overlap, the longer stays; a quote within a quote ships only
        # inside its outer one, never as a lone ‘…’, nor as the very words of its outer one (“‘…’”).
        rs.sort(key=lambda q: (q['level'], q['start'], q['end']))
        kept = []
        for q in rs:
            prev = next((k for k in reversed(kept) if k['level'] == q['level']), None)
            if prev and q['start'] <= prev['end']:
                if (q['end'], q['start']) > (prev['end'], prev['start']) and q['start'] == prev['start']:
                    kept[kept.index(prev)] = q
                continue
            if q['level'] > 1 and not any(k['level'] == q['level'] - 1 and k['start'] <= q['start'] and q['end'] <= k['end'] for k in kept):
                continue
            if any(k['level'] < q['level'] and (k['start'], k['end']) == (q['start'], q['end']) for k in kept):
                continue
            kept.append(q)
        quotes[bk] = sorted(kept, key=lambda q: (q['start'], q['level']))
    edits += term_edits(shipped)
    edits += join_edits(quotes)
    m['token_edits'] = edits
    m['rules'] = [r for r in m['rules'] if r.get('category') != 'split'] + split_rules()
    m['quote_regions'] = dict(quotes)
    out = json.dumps(m, indent=2, ensure_ascii=False) + '\n'
    MOD.write_text(out)
    counts = collections.Counter(e['category'] for e in edits)
    print(f"{MOD.name}: {dict(counts)} token edits; {sum(map(len, quotes.values()))} quote regions in {len(quotes)} books")


main()
