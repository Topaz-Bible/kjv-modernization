"""Audit the KJVo quote regions word by word against two independent Bibles.

Every KJV word gets three readings: quoted or not in the KJVo, in the WEB, and in the BSB.

- The WEB (World English Bible, public domain) descends from the KJV through the ASV, so most of its
  words line up with the KJV's in order. Words are matched by sequence alignment within each verse,
  after modernizing the KJV's forms (thou → you, saith → says, …).
- The BSB is matched as in build_quotes: same verse, same Strong's number.

The audit finds every stretch where the KJVo disagrees with a reference. It names the edge at fault
("ends 4 words early", "missing quote", "takes in the narrator"). A stretch where BOTH references
disagree with the KJVo is almost certainly an error. Where only one does, it is often just that
Bible's style (the WEB quotes some reported speech; the BSB rewords some sayings as reported speech).

Run:
  python3 tools/audit_quotes.py            summary and per-book counts
  python3 tools/audit_quotes.py --list     also writes quotes/review/audit.md (every suspect)
"""
import collections
import difflib
import json
import re
import sys
from pathlib import Path

LISTING = '--list' in sys.argv
sys.argv = [a for a in sys.argv if a != '--list']  # build_quotes reads argv[1] as a package dir
sys.path.insert(0, str(Path(__file__).parent))
import build_quotes as B  # noqa: E402

TOPAZ = B.REPO.parent / 'topaz'
MOD = TOPAZ / 'packages' / 'eng.bible.kjv' / 'eng.bible.kjv.mod.json'
WEB = TOPAZ / 'packages' / 'eng.bible.web' / 'engwebu_usfm'
OUT = B.REPO / 'quotes' / 'review' / 'audit.md'

# ─── WEB: words with their quote depth ─────────────────────────────────────────

ARCHAIC = {
    'thou': 'you', 'thee': 'you', 'ye': 'you', 'thy': 'your', 'thine': 'your', 'yours': 'your',
    'hath': 'has', 'hast': 'have', 'doth': 'does', 'dost': 'do', 'art': 'are', 'wast': 'were',
    'saith': 'says', 'shalt': 'shall', 'wilt': 'will', 'canst': 'can', 'didst': 'did', 'unto': 'to',
    'spake': 'spoke', 'shew': 'show', 'shewed': 'showed', 'thereof': 'of', 'lo': 'behold',
    'begat': 'father', 'yea': 'yes', 'nay': 'no', 'hither': 'here', 'thither': 'there',
    'whither': 'where', 'wherefore': 'why', 'brethren': 'brothers', 'gat': 'got', 'mine': 'my',
}


def norm(word):
    w = re.sub(r"[^a-z]", '', word.lower().replace('’s', '').replace("'s", ''))
    w = ARCHAIC.get(w, w)
    if len(w) > 4 and w.endswith('eth'):
        w = w[:-3] + 's'
    elif len(w) > 4 and w.endswith('est'):
        w = w[:-3]
    return w


USFM_DROP = re.compile(r'\\(f|x|fe)\b.*?\\\1\*', re.S)
WORD_TAG = re.compile(r'\\\+?w\s+([^|\\]*?)(?:\|[^\\]*?)?\\\+?w\*')


def web_book(bk):
    """{(chapter, verse): [(word, depth)]}, depth = quote nesting at that word (0 = narrator)."""
    files = list(WEB.glob(f'*-{bk}engwebu.usfm'))
    if not files:
        return {}
    text = files[0].read_text()
    text = USFM_DROP.sub(' ', text)
    text = WORD_TAG.sub(r'\1', text)
    out = collections.defaultdict(list)
    ch = vs = 0
    stack = []
    seg = 0
    para_start = False
    for line in text.splitlines():
        m = re.match(r'\\(\w+)\s*(.*)', line)
        if not m:
            continue
        tag, rest = m.groups()
        if tag == 'c':
            ch, vs = int(rest.split()[0]), 0
            continue
        if ch == 0 and tag != 'c':
            continue  # introduction matter
        if tag in ('sp', 'id', 'ide', 'h', 'toc1', 'toc2', 'toc3', 'mt', 'mt1', 'mt2', 'ms', 'ms1', 'mr', 's', 's1', 's2', 'r', 'd', 'cl', 'rem', 'usfm'):
            continue
        if tag in ('p', 'm', 'mi', 'pi', 'pi1', 'pc', 'q', 'q1', 'q2', 'q3', 'li', 'li1', 'nb', 'pmo', 'b', 'qc', 'qr'):
            para_start = True
        if tag == 'v':
            num, _, rest = rest.partition(' ')
            vs = int(re.match(r'\d+', num).group())
        rest = re.sub(r'\\\w+\*?', ' ', rest)
        # Walk characters; words collected between quote marks.
        i = 0
        while i < len(rest):
            c = rest[i]
            # A stack of open marks: ” closes back to its own “ even when the WEB leaves an inner
            # ‘ unclosed (Gen 24:7); a new paragraph re-opens a running quote, it doesn't nest.
            if c in '“‘':
                if not ((para_start and c in stack) or (stack and stack[-1] == c)):  # reopened, not nested
                    if not stack:
                        seg += 1          # a new outer quote
                    stack.append(c)
                i += 1
                continue
            if c == '”' and '“' in stack:
                while stack.pop() != '“':
                    pass
                i += 1
                continue
            if c == '’' and stack and stack[-1] == '‘' and not (i + 1 < len(rest) and rest[i + 1].isalpha()):
                stack.pop()
                i += 1
                continue
            depth = len(stack)
            m2 = re.match(r"[A-Za-z]+(?:[’'\-][A-Za-z]+)*", rest[i:])  # a closing ’ is never part of a word
            if m2 and ch and vs:
                out[(ch, vs)].append((m2.group(), depth, seg if depth else 0))
                para_start = False
                i += m2.end()
                continue
            i += 1
    return out


# ─── Reading every KJV word three ways ────────────────────────────────────────

def kjvo_depths(regions, K):
    depth = {}
    for q in regions:
        s, e = B.parse(q['start']), B.parse(q['end'])
        for c in range(s[0], e[0] + 1):
            for w in K.get(c, []):
                if s <= (c, w.v, w.n) <= e:
                    depth[(c, w.v, w.n)] = max(depth.get((c, w.v, w.n), 0), q['level'])
    return depth


def bsb_quoted(bk, K):
    """KJV word → (quoted 0/1, BSB outer-quote id) when every same-Strong's BSB word in the verse
    agrees, else absent."""
    bsb = B.read(B.bsb_zip, f'{bk}.json')
    bch = B.bsb_chapters(bsb)
    seg_of = {}
    for qi, q in enumerate(bsb.get('quotes', []), 1):
        s, e = B.parse(q['start']), B.parse(q['end'])
        for c in range(s[0], e[0] + 1):
            for w in bch.get(c, []):
                if s <= (c, w.v, w.n) <= e and (q['level'] == 1 or (c, w.v, w.n) not in seg_of):
                    seg_of[(c, w.v, w.n)] = qi if q['level'] == 1 else seg_of.get((c, w.v, w.n), qi)
    by_verse = collections.defaultdict(list)
    for c, ws in bch.items():
        for w in ws:
            if w.S:
                by_verse[(c, w.v)].append(w)
    out = {}
    for c, ws in K.items():
        for w in ws:
            if not w.S:
                continue
            same = [x for x in by_verse.get((c, w.v), []) if x.S & w.S]
            if not same:
                continue
            segs = {seg_of.get((c, x.v, x.n), 0) for x in same}
            if len(segs) == 1:
                sg = segs.pop()
                out[(c, w.v, w.n)] = (1 if sg else 0, sg)
    return out


def web_quoted(K, W):
    """KJV word → WEB depth, for words the alignment pairs with a WEB word."""
    out = {}
    verses = collections.defaultdict(list)
    for c, ws in K.items():
        for w in ws:
            if 'pre' not in w.f:
                verses[(c, w.v)].append(w)
    for cv, kws in verses.items():
        wws = W.get(cv)
        if not wws:
            continue
        a = [norm(w.t) for w in kws]
        b = [norm(t) for t, _, _ in wws]
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for i, j, n in sm.get_matching_blocks():
            for k in range(n):
                if a[i + k]:
                    out[(cv[0], cv[1], kws[i + k].n)] = wws[j + k][1:]
    return out


# ─── Disagreements ─────────────────────────────────────────────────────────────

def stretches(order, kjvo, ref, level):
    """Runs of words (in reading order) where ref and KJVo disagree about quoting at `level`.
    Unmatched words neither break nor extend a run."""
    runs, cur = [], None
    for key in order:
        r = ref.get(key)
        if r is None:
            continue
        mine = kjvo.get(key, 0) >= level
        theirs = r[0] >= level
        if mine != theirs:
            if cur and cur['kjvo'] == mine:
                cur['keys'].append(key)
            else:
                cur = {'kjvo': mine, 'keys': [key]}
                runs.append(cur)
        else:
            cur = None
    return runs


def main():
    listing = LISTING
    mod = json.loads(MOD.read_text())['quote_regions']
    totals = collections.Counter()
    rows = []
    per_book = []
    for bk in B.BOOKS:
        K = B.kjv_chapters(bk)
        W = web_book(bk)
        regions = mod.get(bk, [])
        kjvo = kjvo_depths(regions, K)
        web = web_quoted(K, W)
        bsb = bsb_quoted(bk, K)
        order = [(c, w.v, w.n) for c in sorted(K) for w in K[c] if 'pre' not in w.f]
        text = {(c, w.v, w.n): w.t for c in K for w in K[c]}
        index = {k: i for i, k in enumerate(order)}
        wruns = stretches(order, kjvo, web, 1)
        bruns = stretches(order, kjvo, bsb, 1)
        bkeys = {k: r['kjvo'] for r in bruns for k in r['keys']}
        both = 0
        for r in wruns:
            ks = r['keys']
            # BSB verdict on the same words: agrees with the WEB against the KJVo?
            bs = [bkeys.get(k) for k in ks if bsb.get(k) is not None]
            agree_bsb = [x for x in bs if x is not None]
            bsb_checked = len([k for k in ks if bsb.get(k) is not None])
            vote = 'both' if agree_bsb and len(agree_bsb) >= max(1, bsb_checked // 2) else ('bsb-sides-kjvo' if bsb_checked else 'web-only')
            if vote == 'both':
                both += 1
            first, last = index[ks[0]], index[ks[-1]]
            before = order[first - 1] if first > 0 else None
            after = order[last + 1] if last + 1 < len(order) else None
            kind = ('extra' if r['kjvo'] else 'missing')
            if before and kjvo.get(before, 0) and not r['kjvo']:
                kind = 'ends early'
            elif after and kjvo.get(after, 0) and not r['kjvo']:
                kind = 'starts late'
            elif r['kjvo'] and before and not kjvo.get(before, 0):
                kind = 'starts early'
            elif r['kjvo'] and after and not kjvo.get(after, 0):
                kind = 'ends late'
            elif r['kjvo']:
                kind = 'extra quote'
            elif not r['kjvo']:
                kind = 'missing quote'
            totals[(kind, vote)] += 1
            c, v, n = ks[0]
            rows.append((bk, c, v, kind, vote, len(ks), ' '.join(text[k] for k in ks[:14]) + (' …' if len(ks) > 14 else '')))
        # Boundaries: one KJVo quote spanning two quotes in both Bibles (two speakers joined), or
        # two KJVo quotes inside one quote in both (one saying split). Word-level quoting can't see
        # these: every word is quoted either way.
        outer = sorted((q for q in regions if q['level'] == 1), key=lambda q: q['start'])
        spans = []
        for q in outer:
            s0, e0 = B.parse(q['start']), B.parse(q['end'])
            ks = [k for k in order if s0 <= k <= e0]
            wsegs = [web[k][1] for k in ks if k in web and web[k][1]]
            bsegs = [bsb[k][1] for k in ks if k in bsb and bsb[k][1]]
            spans.append((q, ks, wsegs, bsegs))
            # A change of quote must be seen in both, and each side must hold 2+ matched words.
            def changes(segs):
                return [i for i in range(1, len(segs)) if segs[i] != segs[i - 1]]
            def solid(segs):
                cnt = collections.Counter(segs)
                return len([x for x in cnt.values() if x >= 2]) >= 2
            if changes(wsegs) and changes(bsegs) and solid(wsegs) and solid(bsegs):
                c, v, _ = ks[0]
                totals[('joined', 'both')] += 1
                rows.append((bk, c, v, 'joined', 'both', len(ks), ' '.join(text[k] for k in ks[:14]) + (' …' if len(ks) > 14 else '')))
        for (q1, k1, w1, b1), (q2, k2, w2, b2) in zip(spans, spans[1:]):
            if not (k1 and k2 and w1 and w2 and b1 and b2):
                continue
            between = [k for k in order[index[k1[-1]] + 1:index[k2[0]]]]
            if len(between) > 12:
                continue
            if w1[-1] == w2[0] and b1[-1] == b2[0]:
                c, v, _ = k1[-1]
                totals[('split', 'both')] += 1
                rows.append((bk, c, v, 'split', 'both', len(between), ' '.join(text[k] for k in k1[-4:]) + ' ‖ ' + ' '.join(text[k] for k in between) + ' ‖ ' + ' '.join(text[k] for k in k2[:4])))
        per_book.append((bk, len([q for q in regions if q['level'] == 1]), len(wruns), both))
        totals['regions'] += len([q for q in regions if q['level'] == 1])
        totals['words'] += len(order)
        totals['web-matched'] += len(web)
        totals['bsb-matched'] += len(bsb)

    print(f"Level-1 regions: {totals['regions']:,}; KJV words {totals['words']:,}; "
          f"WEB-matched {totals['web-matched'] / totals['words']:.0%}, BSB-matched {totals['bsb-matched'] / totals['words']:.0%}")
    for kind in ('ends early', 'ends late', 'starts late', 'starts early', 'missing quote', 'extra quote', 'joined', 'split'):
        row = {vote: totals[(kind, vote)] for vote in ('both', 'web-only', 'bsb-sides-kjvo')}
        print(f"  {kind:14} both refs disagree {row['both']:5}   WEB only {row['web-only']:5}   BSB sides with KJVo {row['bsb-sides-kjvo']:5}")
    if listing:
        OUT.parent.mkdir(exist_ok=True)
        with OUT.open('w') as f:
            f.write('# Quote audit: KJVo vs WEB and BSB\n\nGenerated by tools/audit_quotes.py. One row per stretch where the WEB disagrees; '
                    '`both` = the BSB disagrees too.\n\n| Book | Ref | What | Refs | Words | Text |\n|---|---|---|---|---|---|\n')
            for bk, c, v, kind, vote, n, t in rows:
                f.write(f'| {bk} | {c}:{v} | {kind} | {vote} | {n} | {t} |\n')
        print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
