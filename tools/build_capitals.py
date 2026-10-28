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

Only capitals that the BSB uses mid-sentence count (after a semicolon counts: "He makes me lie down in
green pastures; He leads me"). A capital that starts a sentence, a quote or a clause after a colon
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
ENDS_SENTENCE = re.compile(r'[.?!:]\s*$')


def group(word, groups):
    w = word.lower()
    return next((g for g, s in groups.items() if w in s), None)


def strongs(s):
    m = re.match(r'([GH])0*(\d+)', s or '')
    return m.group(1) + m.group(2) if m else None


# Which Hebrew or Greek word a KJV pronoun belongs to. Its own link when it has one (Greek αὐτοῦ);
# otherwise the word it hangs on, as Hebrew writes it: "his work" is one word, work-his; "he rested"
# is the verb; "unto him" the preposition. The BSB links its pronoun to the same word.
SUBJECT = {'he', 'thou', 'ye'}
OBJECT = {'him', 'himself', 'thee', 'thyself', 'you', 'yourself', 'me', 'myself'}


def host(i, tokens, kv):
    linked = lambda t: t.get('k') in kv
    if linked(tokens[i]):
        return strongs(kv[tokens[i]['k']][1])
    w = tokens[i]['t'].lower()
    near = tokens[max(0, i - 3):i][::-1] if w in OBJECT else tokens[i + 1:i + 4]
    t = next((t for t in near if linked(t)), None)
    return strongs(kv[t['k']][1]) if t else None


PLURAL = {'ye', 'you', 'your', 'yours', 'yourself'}
DIVINE = {'God', 'LORD', 'Lord', 'GOD', 'Jesus', 'Christ', 'Spirit', 'He', 'Him', 'His', 'Himself', 'One', 'Avenger',
          'Father', 'Son', 'Redeemer', 'Creator', 'Maker', 'Mighty', 'Holy', 'Most', 'High'}
SOMEONE_ELSE = {'me': {'we', 'us', 'our', 'ours', 'me', 'my', 'mine'}, 'you': {'you', 'your', 'yours'}}
SPEECH = {'said', 'saith', 'spake', 'say', 'saying', 'answered', 'called', 'cried', 'commanded', 'told', 'shewed'}
OTHERS = {'he', 'him', 'his', 'himself'}  # not they, them, it: Hebrew writes "he brought them" as one word
PRONOUN_WORDS = {'G846', 'G1438', 'G1473', 'G4771', 'G848'}  # αὐτός and the like: every person's
NAME = re.compile(r'Np|^N-PRI|^N-.*-(P|L|T|LG|PG|LI)$')


def pair_by_word(g, ks, flags, bs, tokens, kv, btokens):
    """Pair a verse's pronouns one to one through the Hebrew or Greek word each belongs to.

    Returns the KJV pronouns to capitalize, or None to leave the verse for review. Pronouns on one word
    pair in order when both Bibles have as many there; a BSB pronoun with no KJV one on its word is the
    BSB's own wording and pairs nobody. The KJV has more pronouns than the
    BSB in most of these verses ("he shall destroy them, and he shall bring them down" against "He will
    destroy them and subdue them"). Those left over follow what the BSB does with their word instead,
    so a verse is settled whole or not at all:
      I/you  the BSB's pronouns in the verse are all God's: one speaker, so these are His too, unless
             the BSB has another person's pronoun on that word ("The LORD is our God")
      he     the BSB names God on that word ("God gave", "the Mighty One") → His; it names someone else
             or writes a pronoun of theirs there → stays lowercase; anything else leaves the verse for review
    """
    index = {t['n']: i for i, t in enumerate(tokens)}
    kh = [host(index[t['n']], tokens, kv) for t in ks]
    hosts = list(kh)
    kc, bc = collections.Counter(kh), collections.Counter(bs)
    known = [f for f in flags if f is not None]
    if not known or False in known and g != 'he':
        return None
    mine, seen = set(), collections.Counter()
    for f, s in zip(flags, bs):
        if not s or kc[s] == 0:
            continue  # the BSB's own wording ("His covenant" for "the covenant"): no KJV pronoun to pair
        if kc[s] != bc[s]:
            if f is False:
                continue
            return None
        # One pronoun each on the word, or as many in both Bibles: they pair in order.
        i = [j for j, h in enumerate(hosts) if h == s][seen[s]]
        seen[s] += 1
        if f is None:  # a capital that opens a sentence says nothing
            return None
        if f:
            mine.add(i)
        else:
            kh[i] = 'not God'
    out = [ks[i] for i in mine]
    for i, (t, s) in enumerate(zip(ks, kh)):
        if i in mine or s == 'not God' or t['t'].lower() in PLURAL:
            continue
        if g != 'he':
            # Another speaker's pronoun on the same word ("The LORD is our God") → not His.
            on = [b for b in btokens if s and strongs(b.get('s')) == s]
            i0 = index[t['n']]
            if any(x['t'].lower() in SPEECH for x in tokens[max(0, i0 - 2):i0 + 3]):
                return None  # "the LORD said unto me", "shalt thou say": the one who speaks, not the one spoken of
            if not any(b['t'].lower() in SOMEONE_ELSE[g] and b['t'][:1].islower() for b in on):
                out.append(t)
            continue
        if not s or kc[s] != 1 or s in PRONOUN_WORDS:  # several pronouns on one word: can't tell which
            return None
        on = [b for b in btokens if strongs(b.get('s')) == s]
        god = any(b['t'] in DIVINE for b in on)
        other = any(b['t'].lower() in OTHERS or NAME.search(b.get('m') or '') and b['t'] not in DIVINE for b in on)
        if god and not other:
            out.append(t)
        elif other and not god:
            continue
        else:
            return None
    return [t for t in out if not t['t'][:1].isupper()]


kjv = zipfile.ZipFile(PKG / 'eng.bible.kjv.zip')
keys = {'nt': zipfile.ZipFile(PKG / 'grc.key.nt.zip'), 'ot': zipfile.ZipFile(PKG / 'hbo.key.ot.zip')}
by_word = collections.Counter()
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
    bverses, btok, bstrongs = {}, {}, collections.defaultdict(lambda: collections.defaultdict(list))
    kp = keys[b['canon']]
    KP = json.loads(kp.read(f'{bk}.json'))['verses'] if f'{bk}.json' in kp.namelist() else {}
    prev_a, prev_t = '.', ''
    for c in B['chapters']:
        for v in c['verses']:
            out = collections.defaultdict(list)
            for i, t in enumerate(v['tokens']):
                before = v['tokens'][i - 1].get('a', '') if i else prev_a
                g = group(t['t'], BSB_GROUPS)
                if g:
                    starts = (ENDS_SENTENCE.search(before or '') or (i and v['tokens'][i - 1]['t'] == 'Selah') or
                              (not i and prev_t == 'Selah') or
                              f"{c['chapter']:03}.{v['verse']:03}:{t['n']:03}" in quote_starts)
                    # None = can't tell (sentence start); True = capital mid-sentence; False = lower case
                    out[g].append(None if starts and t['t'][:1].isupper() else t['t'][:1].isupper())
                    bstrongs[(c['chapter'], v['verse'])][g].append(strongs(t.get('s')))
            if v['tokens']:
                prev_a, prev_t = v['tokens'][-1].get('a', ''), v['tokens'][-1]['t']
            bverses[(c['chapter'], v['verse'])] = out
            btok[(c['chapter'], v['verse'])] = v['tokens']
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
                    paired = pair_by_word(g, ks, flags, bstrongs[(c['chapter'], v['verse'])][g], v['tokens'],
                                          KP.get(f"{c['chapter']}:{v['verse']}", {}), btok[(c['chapter'], v['verse'])])
                    for t in paired or []:
                        changes.append({'book': bk, 'chapter': c['chapter'], 'verse': v['verse'], 'word': t['n'],
                                        'kjv': t['t'], 'modernized': t['t'][:1].upper() + t['t'][1:], 'by': 'word'})
                        counts[t['t'].lower()] += 1
                        by_word[g] += 1
                    if paired is not None:
                        continue
                    review.append({'book': bk, 'chapter': c['chapter'], 'verse': v['verse'], 'group': g,
                                   'bsb': len(flags), 'kjv': len(ks),
                                   # The BSB's pronouns of the group in order: G = God's, o = someone else's,
                                   # ? = can't tell (capital at a sentence or quote start).
                                   'bsb_pattern': ''.join('?' if f is None else 'G' if f else 'o' for f in flags),
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
print(len(changes), 'changed;', len(review), 'verses to review'); print(counts.most_common()); print('by word:', by_word)
