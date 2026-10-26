#!/usr/bin/env python3
"""Draft KJV quotation-mark regions, carried over from the BSB and checked against the KJV's own clues.

Reads (read-only), from the Topaz app's package folder:
  eng.bible.kjv.zip   KJV words (the 'k' links tie each word to a Greek/Hebrew word)
  eng.bible.bsb.zip   BSB words + its quote regions (start word, end word, nesting level)
  grc.key.nt.zip / hbo.key.ot.zip   Greek/Hebrew words with Strong's numbers

How a region is carried over:
  1. Every BSB word inside the region with a Strong's number is matched to the KJV word in the same
     verse with the same Strong's number (nearest by position when there are several).
  2. The KJV region runs from the first matched word to the last.
  3. Its start is moved back to the start of its clause (just after a comma, colon or semicolon, or
     the verse start). Its end is moved forward to the next punctuation mark.
  4. Neighbouring BSB pieces of one speech, split only by a BSB narrator tag ("he answered") that the
     KJV doesn't have, are joined into one region.

Each region is then sorted into a tier, easiest first:
  1  one verse, one speaker, nothing nested, both edges confirmed by KJV clues
  2  several verses, nothing nested, both edges confirmed
  3  contains or sits inside another quote (nesting)
  4  an edge isn't confirmed by a KJV clue; needs a human look
  5  couldn't be carried over at all

KJV clues: a speech opens with a capital letter after a comma or colon ("said unto him, Lovest");
it closes on . ? ! or at the end of a verse. In the Gospels and Revelation the KJV's own
words-of-Jesus marking must agree with the region's edges.

Writes:
  quotes/kjv-quotes.json   every region, with its tier, checks and the anchor words
  quotes/review/tier-N.md  each tier as readable text with the marks in place

Run:  python3 tools/build_quotes.py [path/to/topaz-bible/assets/packages]
"""
import json, re, sys, zipfile, collections
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PKG = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO.parent / 'topaz-bible' / 'assets' / 'packages'
OUT = REPO / 'quotes'

kjv_zip = zipfile.ZipFile(PKG / 'eng.bible.kjv.zip')
bsb_zip = zipfile.ZipFile(PKG / 'eng.bible.bsb.zip')
keys = {'nt': zipfile.ZipFile(PKG / 'grc.key.nt.zip'), 'ot': zipfile.ZipFile(PKG / 'hbo.key.ot.zip')}
kjv_version = json.loads(kjv_zip.read('manifest.json'))['package_version']
bsb_version = json.loads(bsb_zip.read('manifest.json'))['package_version']
NT = {n[:3] for n in keys['nt'].namelist() if n.endswith('.json')}
BOOKS = [n[:3] for n in bsb_zip.namelist() if re.fullmatch(r'[0-9A-Z]{3}\.json', n)]
ORDER = [b['book_id'] for b in json.loads(kjv_zip.read('manifest.json'))['books']]
BOOKS.sort(key=lambda b: ORDER.index(b) if b in ORDER else 999)

OPEN_PUNCT = re.compile(r'[,:;]\s*$')
ANY_PUNCT = re.compile(r'[.?!;:,]')
STOP = re.compile(r'[.?!]')
SPEECH = re.compile(r'(said|saith|say|saying|answered|spake|cried|asked)$', re.I)


def strongs(s):
    m = re.match(r'([GH])0*(\d+)', s or '')
    return m.group(1) + m.group(2) if m else None


def read(z, name):
    return json.loads(z.read(name))


class Word:
    __slots__ = ('v', 'n', 't', 'a', 'f', 'S')

    def __init__(self, v, tok, S):
        self.v, self.n, self.t, self.a, self.f, self.S = v, tok['n'], tok['t'], tok.get('a') or '', tok.get('f') or [], S

    def key(self, ch):
        return f'{ch:03}.{self.v:03}:{self.n:03}'


def kjv_chapters(bk):
    K = read(kjv_zip, f'{bk}.json')
    kp = keys['nt' if bk in NT else 'ot']
    KP = read(kp, f'{bk}.json')['verses'] if f'{bk}.json' in kp.namelist() else {}
    out = {}
    for c in K['chapters']:
        words = []
        for v in c['verses']:
            kv = KP.get(f"{c['chapter']}:{v['verse']}", {})
            for t in v['tokens']:
                S = {strongs(kv[k][1]) for k in [t.get('k')] + (t.get('ka') or []) if k and k in kv}
                words.append(Word(v['verse'], t, S - {None}))
        out[c['chapter']] = words
    return out


def bsb_chapters(B):
    out = {}
    for c in B['chapters']:
        words = []
        for v in c['verses']:
            for t in v['tokens']:
                # Only the word's own Strong's number: 'sa' adds helper words (articles, particles)
                # that would pull a region onto the narrator's words.
                words.append(Word(v['verse'], t, {strongs(t.get('s'))} - {None}))
        out[c['chapter']] = words
    return out


def parse(ref):
    cv, n = ref.split(':')
    c, v = cv.split('.')
    return int(c), int(v), int(n)


def heads(bl, ids, S):
    """BSB words with these Strong's numbers, counting a run of words that share one number once:
    the BSB gives every word of "serve as lights" the number for "lights"."""
    return [x for x in ids if bl[x].S & S and not (x > 0 and bl[x - 1].v == bl[x].v and bl[x - 1].S == bl[x].S)]


def carry_over(bk, B, K):
    bch = bsb_chapters(B)
    regions = []
    # Narrator words: BSB words outside every quote. Where one is anchored in the KJV, a quote edge may
    # not cross it.
    quoted = collections.defaultdict(set)
    for q in B.get('quotes', []):
        sc, sv, sn = parse(q['start'])
        ec, ev, en = parse(q['end'])
        if sc == ec and sc in bch:
            idx = {(w.v, w.n): i for i, w in enumerate(bch[sc])}
            quoted[sc].update(range(idx[(sv, sn)], idx[(ev, en)] + 1))
    for ch, bl in bch.items():
        if ch not in K:
            continue
        kl = K[ch]
        for bi, w in enumerate(bl):
            if bi in quoted[ch] or not w.S:
                continue
            same_k = [ki for ki, x in enumerate(kl) if x.v == w.v and x.S & w.S]
            same_b = heads(bl, [x for x, y in enumerate(bl) if y.v == w.v], w.S)
            if len(same_k) == 1 and len(same_b) == 1:
                NARRATOR[(bk, ch)].add(same_k[0])
    for q in B.get('quotes', []):
        sc, sv, sn = parse(q['start'])
        ec, ev, en = parse(q['end'])
        r = {'book': bk, 'chapter': sc, 'level': q['level'], 'bsb': [q['start'], q['end']], 'checks': []}
        regions.append(r)
        if sc != ec or sc not in K:
            r['checks'].append('crosses a chapter')
            continue
        bl, kl = bch[sc], K[sc]
        bidx = {(w.v, w.n): i for i, w in enumerate(bl)}
        by_verse_k = collections.defaultdict(list)
        for i, w in enumerate(kl):
            by_verse_k[w.v].append(i)
        by_verse_b = collections.defaultdict(list)
        for i, w in enumerate(bl):
            by_verse_b[w.v].append(i)
        # Anchors first: a Strong's number that occurs once in the verse in both Bibles can only mean one
        # word. Repeated ones ("the", "and", "him") are guessed by position, and used only when a region
        # has no anchor at all, so they can't drag an edge onto the narrator's words.
        anchors, guesses = [], []
        for bi in range(bidx[(sv, sn)], bidx[(ev, en)] + 1):
            w = bl[bi]
            if not w.S or not by_verse_k[w.v]:
                continue
            r.setdefault('_first', w.S)
            bv, kv = by_verse_b[w.v], by_verse_k[w.v]
            same_k = [ki for ki in kv if kl[ki].S & w.S]
            same_b = heads(bl, bv, w.S)
            if len(same_k) == 1 and len(same_b) == 1:
                anchors.append(same_k[0])
            elif same_k:
                rel = bv.index(bi) / max(1, len(bv) - 1)
                guesses.append(min((abs(kv.index(ki) / max(1, len(kv) - 1) - rel), ki) for ki in same_k)[1])
        # A name or term the BSB sets in quotes inside the narrator's sentence ('God called the light “day,”')
        # is carried over word for word: no walking back to a speech opener.
        b0 = bidx[(sv, sn)]
        if (bidx[(ev, en)] - b0 < 3 and b0 > 0 and bl[b0 - 1].v == sv and not ANY_PUNCT.search(bl[b0 - 1].a)
                and not SPEECH.match(bl[b0 - 1].t)):
            r['term'] = True
            # The KJV capitalizes such a name ("called the light Day"), which settles a guess.
            if not anchors and guesses and all(kl[g].t[:1].isupper() for g in guesses):
                anchors = guesses
            if not anchors:
                r['checks'].append('no matching words')
                continue
            # The KJV may word it differently ("Yet once more" for “Once more”); then only part would be quoted.
            if max(anchors) - min(anchors) < bidx[(ev, en)] - b0 - 1:
                r['checks'].append('term not carried over whole')
        hits = anchors or guesses
        if not hits:
            r['checks'].append('no matching words')
            continue
        r['_s'], r['_e'] = min(hits), max(hits)
    return regions


def clause_start(kl, i):
    """Walk back to the first word of the clause (after , : ; or at the verse start)."""
    j = i
    while j > 0 and kl[j - 1].v == kl[i].v and not ANY_PUNCT.search(kl[j - 1].a) and i - j < 8:
        j -= 1
    return j


def telling_capital(w):
    """A capital that the KJV chose, not one every word of its kind has (I, O, LORD, names)."""
    return w.t[:1].isupper() and w.t.lower() in LOWER_WORDS and w.t not in ('I', 'O')


def lead_in(kl, s):
    """Pull in a short clause the BSB set outside its quote or left unmatched:
    "Thus saith the LORD, Behold, I will" / "unto David, Go, and the LORD be with thee"."""
    while s > 0:
        j = clause_start(kl, s - 1)
        if (j == s or kl[j].v != kl[s].v or s - j > 3 or j == 0 or kl[j - 1].v != kl[j].v
                or not OPEN_PUNCT.search(kl[j - 1].a) or not telling_capital(kl[j])):
            return s
        s = j
    return s


def and_after(kl, i):
    """The narrator taking over after a colon or semicolon: 'Let there be light: and there was light.'"""
    return bool(re.search(r'[:;]\s*$', kl[i].a)) and i + 1 < len(kl) and kl[i + 1].v == kl[i].v and kl[i + 1].t == 'and'


def snap(regions, K):
    for r in regions:
        if '_s' not in r or r.get('term'):
            continue
        kl = K[r['chapter']]
        # Walk back clause by clause to where the speech opens: a capital after a comma or colon, or the
        # verse start. Never across a narrator word or the end of an earlier quote.
        stop = max([o['_e'] for o in regions if '_s' in o and o['chapter'] == r['chapter'] and o['_e'] < r['_s']
                    and o['level'] == r['level']] +
                   [i for i in NARRATOR[(r['book'], r['chapter'])] if i < r['_s']], default=-1)
        s = clause_start(kl, r['_s'])
        while s > 0 and s - 1 > stop and kl[s - 1].v == kl[s].v and not (
                OPEN_PUNCT.search(kl[s - 1].a) and kl[s].t[:1].isupper()):
            j = clause_start(kl, s - 1)
            if any(i in NARRATOR[(r['book'], r['chapter'])] for i in range(j, s)) or j <= stop:
                break
            s = j
        s = lead_in(kl, s)
        # The end runs on to the end of the sentence or verse, but never into the next quote or past a
        # speech verb ("…; and he said,"), which would swallow the narrator.
        nxt = min([o['_s'] for o in regions if '_s' in o and o['chapter'] == r['chapter'] and o['_s'] > r['_e']],
                  default=len(kl))
        # A narrator word is a wall too: "saith, Master, master; and kissed him" stops at the semicolon.
        wall = min([i for i in NARRATOR[(r['book'], r['chapter'])] if i > r['_e']], default=len(kl))
        e = r['_e']
        while (e < nxt - 1 and e < wall - 1 and not STOP.search(kl[e].a) and kl[e + 1].v == kl[e].v
               and not SPEECH.match(kl[e + 1].t) and not and_after(kl, e) and e - r['_e'] < 40):
            e += 1
        if e == wall - 1 and not STOP.search(kl[e].a):
            back = [i for i in range(r['_e'], e + 1) if ANY_PUNCT.search(kl[i].a)]
            e = back[-1] if back else r['_e']
        r['_s'], r['_e'] = s, e


def merge(regions, K):
    """Join pieces of one speech that the BSB splits with a narrator tag the KJV doesn't have."""
    out = []
    for r in regions:
        p = out[-1] if out else None
        # Touching or overlapping in either order: the KJV may put the pieces the other way round
        # ("And he said, If now I have found grace in thy sight, O Lord, …" vs the BSB's “O Lord,” he said, “if …”).
        kl = K.get(r['chapter'], [])
        if (p and '_s' in p and '_s' in r and not p.get('term') and not r.get('term') and p['chapter'] == r['chapter'] and p['level'] == r['level']
                and r['_s'] <= p['_e'] + 1 and p['_s'] <= r['_e'] + 1
                and not any(SPEECH.match(kl[i].t) for i in range(min(p['_s'], r['_s']), max(p['_e'], r['_e']) + 1))):
            p['_s'], p['_e'] = min(p['_s'], r['_s']), max(p['_e'], r['_e'])
            p['bsb'] = [p['bsb'][0], r['bsb'][1]]
            p.setdefault('joined', 1)
            p['joined'] += 1
            continue
        out.append(r)
    return out


def fit_woj(regions, K):
    """Fit quotes of Jesus to the KJV's own red letters, which say where His words start and stop.

    One unbroken stretch of red letters is one speech, so it gets one quote: from its first red word to
    its last ("Verily I say unto you, “Except…" → "“Verily…"; "“And he said unto them, What man…" →
    "What man…"). Two halves the BSB match left ("“There is no”", "“There is no man…”") become one.
    A quote whose red words are broken by the narrator ("(he saith to the sick of the palsy,)") keeps
    its edges, trimmed to red words. Returns the regions left.
    """
    runs = {}
    for r in regions:
        if '_s' not in r or r['level'] != 1 or r.get('term'):
            continue
        kl = K[r['chapter']]
        red = lambda i: 'woj' in kl[i].f
        s, e = r['_s'], r['_e']
        if sum(red(i) for i in range(s, e + 1)) * 2 <= e - s + 1:
            continue
        while not red(s):
            s += 1
        while not red(e):
            e -= 1
        if not all(red(i) for i in range(s, e + 1)):
            r['_s'], r['_e'] = s, e
            continue
        while s > 0 and red(s - 1):
            s -= 1
        while e < len(kl) - 1 and red(e + 1):
            e += 1
        runs.setdefault((r['chapter'], s, e), []).append(r)
    gone = set()
    for (ch, s, e), rs in runs.items():
        rs[0]['_s'], rs[0]['_e'] = s, e
        gone.update(id(r) for r in rs[1:])
    return [r for r in regions if id(r) not in gone]


def check(r, K, all_regions):
    kl = K[r['chapter']]
    s, e = r['_s'], r['_e']
    first, last = kl[s], kl[e]
    verse_start = s == 0 or kl[s - 1].v != first.v
    verse_end = e == len(kl) - 1 or kl[e + 1].v != last.v
    # A name ("unto Simon Peter, Simon, son of Jonas") is no clue by its capital, but it is when it is
    # the very word the BSB quote opens with.
    after_verb = any(SPEECH.match(kl[i].t) for i in range(max(0, s - 5), s) if kl[i].v == first.v)
    opener = verse_start or (OPEN_PUNCT.search(kl[s - 1].a) and (
        telling_capital(first) or (first.t[:1].isupper() and (after_verb or first.S & r.get('_first', set())))))
    closer = (bool(STOP.search(last.a)) or (verse_end and last.a.strip() in (':', ';', ','))
              or (ANY_PUNCT.search(last.a) and e + 1 in NARRATOR[(r['book'], r['chapter'])]) or and_after(kl, e))
    if r.get('term'):
        opener = closer = True
    if not opener:
        r['checks'].append('start not after a comma/colon + capital')
    if first.t == 'That' and not verse_start:
        r['checks'].append('opens with a capital "That"')
    if not closer:
        r['checks'].append('end not on . ? ! or a verse end')
    inside = [o for o in all_regions if o is not r and '_s' in o and o['chapter'] == r['chapter']
              and s <= o['_s'] and o['_e'] <= e]
    outside = [o for o in all_regions if o is not r and '_s' in o and o['chapter'] == r['chapter']
               and o['_s'] <= s and e <= o['_e']]
    overlap = [o for o in all_regions if o is not r and '_s' in o and o['chapter'] == r['chapter']
               and o['_s'] < s <= o['_e'] < e]
    # "…, Moses, Moses. And he said, Here am I." A speech verb opening a new capital inside the region
    # means either a second speaker swallowed or a quote within a quote the BSB didn't mark.
    for i in range(s + 1, e - 1):
        if (SPEECH.match(kl[i].t) and OPEN_PUNCT.search(kl[i].a) and kl[i + 1].t[:1].isupper()
                and not any(o['_s'] == i + 1 for o in inside)):
            r['checks'].append('a speech verb inside, with no quote after it')
            break
    if overlap:
        r['checks'].append('overlaps another quote')
    # Words of Jesus: the KJV marks them itself, so a quote of Jesus must start and stop where they do.
    if r['level'] == 1 and sum('woj' in kl[i].f for i in range(s, e + 1)) * 2 > e - s + 1:
        ws, we = s, e
        while ws > 0 and 'woj' in kl[ws - 1].f:
            ws -= 1
        while we < len(kl) - 1 and 'woj' in kl[we + 1].f:
            we += 1
        if ws != s:
            r['checks'].append('words of Jesus start earlier')
        if not all('woj' in kl[i].f for i in range(s, e + 1)):
            r['checks'].append('runs past the words of Jesus')
        elif we != e and not inside and not any(
                o['_s'] == e + 1 or o['_s'] == e + 2 for o in all_regions if '_s' in o and o['chapter'] == r['chapter']):
            r['checks'].append('words of Jesus continue after the end')
        r['woj'] = True
    if r['checks']:
        tier = 4
    elif inside or outside:
        tier = 3
    elif first.v != last.v:
        tier = 2
    else:
        tier = 1
    r['tier'] = tier
    r['start'], r['end'] = first.key(r['chapter']), last.key(r['chapter'])
    r['start_word'], r['end_word'] = first.t, last.t


def render(bk, ch, verses, K, regions):
    kl = K[ch]
    op, cl = collections.defaultdict(list), collections.defaultdict(list)
    for r in regions:
        if r.get('start') and r['chapter'] == ch:
            op[r['start']].append(r['level'])
            cl[r['end']].append(r['level'])
    lines = []
    for v in verses:
        out = []
        for w in kl:
            if w.v != v:
                continue
            k = w.key(ch)
            o = ''.join('“' if l % 2 else '‘' for l in sorted(op[k]))
            c = ''.join('”' if l % 2 else '’' for l in sorted(cl[k], reverse=True))
            out.append(f'{o}{w.t}{w.a}{c}')
        lines.append(f'**{v}** ' + ' '.join(out))
    return '\n'.join(lines)


LOWER_WORDS = set()
NARRATOR = collections.defaultdict(set)


def main():
    for bk in BOOKS:
        for c in read(kjv_zip, f'{bk}.json')['chapters']:
            for v in c['verses']:
                LOWER_WORDS.update(t['t'] for t in v['tokens'] if t['t'][:1].islower())
    everything = []
    rendered = collections.defaultdict(list)
    for bk in BOOKS:
        B = read(bsb_zip, f'{bk}.json')
        K = kjv_chapters(bk)
        regions = carry_over(bk, B, K)
        snap(regions, K)
        regions = merge(regions, K)
        regions = fit_woj(regions, K)
        for r in regions:
            if '_s' in r:
                check(r, K, regions)
            else:
                r['tier'] = 5
        for r in regions:
            if r['tier'] == 5:
                rendered[5].append(f"- {bk} {r['bsb'][0]}–{r['bsb'][1]}: {'; '.join(r['checks'])}")
                continue
            vs = sorted({K[r['chapter']][i].v for i in range(r['_s'], r['_e'] + 1)})
            text = render(bk, r['chapter'], vs, K, regions)
            note = f" — {'; '.join(r['checks'])}" if r['checks'] else ''
            rendered[r['tier']].append(f"### {bk} {r['chapter']}:{vs[0]}{'–' + str(vs[-1]) if len(vs) > 1 else ''}"
                                       f" (level {r['level']}){note}\n\n{text}\n")
        for r in regions:
            r.pop('_s', None), r.pop('_e', None), r.pop('_first', None)
        everything += regions
    for i, r in enumerate(everything, 1):
        r['id'] = f'q{i:05}'
        r['status'] = 'draft'
    OUT.mkdir(exist_ok=True)
    (OUT / 'review').mkdir(exist_ok=True)
    counts = collections.Counter(r['tier'] for r in everything)
    json.dump({'kjv_package': kjv_version, 'bsb_package': bsb_version,
               'anchors': 'chapter.verse:word-number in the KJV package; start_word/end_word guard against drift',
               'tiers': {str(k): counts[k] for k in sorted(counts)},
               'regions': [{k: r[k] for k in ('id', 'book', 'chapter', 'tier', 'status', 'level', 'start', 'end',
                                               'start_word', 'end_word', 'bsb', 'checks', 'woj', 'joined', 'term') if k in r}
                           for r in everything]},
              open(OUT / 'kjv-quotes.json', 'w'), indent=1, ensure_ascii=False)
    names = {1: 'One verse, nothing nested', 2: 'Several verses, nothing nested', 3: 'Nested quotes',
             4: 'Edge not confirmed by a KJV clue', 5: 'Not carried over'}
    for t in range(1, 6):
        (OUT / 'review' / f'tier-{t}.md').write_text(
            f'# Tier {t}: {names[t]} ({counts[t]})\n\nDraft, generated by tools/build_quotes.py from KJV {kjv_version} '
            f'and BSB {bsb_version}. Nested levels alternate “ ” and ‘ ’.\n\n' + '\n'.join(rendered[t]) + '\n')
    print(dict(sorted(counts.items())), 'total', len(everything))
    print(collections.Counter(c for r in everything for c in r['checks']).most_common())


main()
