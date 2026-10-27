#!/usr/bin/env python3
"""Old Testament names in the New Testament: give them the spelling the KJV itself uses in the Old Testament.

The KJV New Testament spells Old Testament people and places the way the Greek does: Elias for Elijah,
Esaias for Isaiah, Noe for Noah. Twice "Jesus" is Joshua (Acts 7:45, Hebrews 4:8). This layer swaps
in the KJV's own Old Testament spelling, so a reader meets one name for one person.

Most of these names mean only one person or place, and change everywhere. A few are shared with
New Testament people (Jonas, Juda, Judas, Jesus, Aram, Heber, Sala, Zara, Abia), and those change only
where the BSB has the Old Testament person in the same verse. That keeps "Simon son of Jonas" (BSB
"John") from becoming Jonah, and "Jesus" as Jesus everywhere except the two verses about Joshua. Every
place a shared name was left alone is listed.

Reads (read-only): eng.bible.kjv.zip and eng.bible.bsb.zip from the app's package folder.
Writes: names/names.json (the list and every change) and names/changes.md (for reading).

Run:  python3 tools/build_names.py [path/to/topaz-bible/assets/packages]
"""
import json, re, sys, zipfile, collections
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PKG = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO.parent / 'topaz-bible' / 'assets' / 'packages'
OUT = REPO / 'names'

# KJV New Testament form → KJV Old Testament form, and the name the BSB uses for the same person or place.
NAMES = [
    # prophets and patriarchs
    ('Elias', 'Elijah', 'Elijah'), ('Esaias', 'Isaiah', 'Isaiah'), ('Eliseus', 'Elisha', 'Elisha'),
    ('Jeremy', 'Jeremiah', 'Jeremiah'), ('Jeremias', 'Jeremiah', 'Jeremiah'), ('Osee', 'Hosea', 'Hosea'),
    ('Jonas', 'Jonah', 'Jonah'), ('Noe', 'Noah', 'Noah'), ('Jesus', 'Joshua', 'Joshua'),
    ('Core', 'Korah', 'Korah'), ('Melchisedec', 'Melchizedek', 'Melchizedek'), ('Balac', 'Balak', 'Balak'),
    ('Bosor', 'Beor', 'Beor'), ('Cis', 'Kish', 'Kish'), ('Gedeon', 'Gideon', 'Gideon'),
    ('Jephthae', 'Jephthah', 'Jephthah'), ('Emmor', 'Hamor', 'Hamor'),
    # women
    ('Sara', 'Sarah', 'Sarah'), ('Agar', 'Hagar', 'Hagar'), ('Rachab', 'Rahab', 'Rahab'),
    ('Thamar', 'Tamar', 'Tamar'), ('Rebecca', 'Rebekah', 'Rebekah'),
    # tribes
    ('Juda', 'Judah', 'Judah'), ('Judas', 'Judah', 'Judah'), ('Zabulon', 'Zebulun', 'Zebulun'),
    ('Nephthalim', 'Naphtali', 'Naphtali'), ('Nepthalim', 'Naphtali', 'Naphtali'), ('Aser', 'Asher', 'Asher'),
    ('Manasses', 'Manasseh', 'Manasseh'), ('Ruben', 'Reuben', 'Reuben'),
    # kings of Judah (Matthew 1)
    ('Roboam', 'Rehoboam', 'Rehoboam'), ('Abia', 'Abijah', 'Abijah'), ('Josaphat', 'Jehoshaphat', 'Jehoshaphat'),
    ('Ozias', 'Uzziah', 'Uzziah'), ('Joatham', 'Jotham', 'Jotham'), ('Achaz', 'Ahaz', 'Ahaz'),
    ('Ezekias', 'Hezekiah', 'Hezekiah'), ('Josias', 'Josiah', 'Josiah'), ('Jechonias', 'Jeconiah', 'Jeconiah'),
    ('Zorobabel', 'Zerubbabel', 'Zerubbabel'), ('Urias', 'Uriah', 'Uriah'),
    # ancestors (Matthew 1, Luke 3)
    ('Phares', 'Pharez', 'Perez'), ('Zara', 'Zarah', 'Zerah'), ('Esrom', 'Hezron', 'Hezron'), ('Aram', 'Ram', 'Ram'),
    ('Aminadab', 'Amminadab', 'Amminadab'), ('Naasson', 'Nahshon', 'Nahshon'), ('Booz', 'Boaz', 'Boaz'),
    ('Nachor', 'Nahor', 'Nahor'), ('Thara', 'Terah', 'Terah'), ('Saruch', 'Serug', 'Serug'), ('Ragau', 'Reu', 'Reu'),
    ('Phalec', 'Peleg', 'Peleg'), ('Heber', 'Eber', 'Eber'), ('Sala', 'Salah', 'Shelah'), ('Sem', 'Shem', 'Shem'),
    ('Mathusala', 'Methuselah', 'Methuselah'), ('Maleleel', 'Mahalaleel', 'Mahalalel'),
    # titles
    ('Messias', 'Messiah', 'Messiah'), ('Emmanuel', 'Immanuel', 'Immanuel'),
    # places
    ('Sion', 'Zion', 'Zion'), ('Sodoma', 'Sodom', 'Sodom'), ('Gomorrha', 'Gomorrah', 'Gomorrah'),
    ('Sina', 'Sinai', 'Sinai'), ('Chanaan', 'Canaan', 'Canaan'), ('Charran', 'Haran', 'Haran'),
    ('Sychem', 'Shechem', 'Shechem'), ('Madian', 'Midian', 'Midian'), ('Nineve', 'Nineveh', 'Nineveh'),
    ('Sarepta', 'Zarephath', 'Zarephath'), ('Rama', 'Ramah', 'Ramah'), ('Saron', 'Sharon', 'Sharon'),
    ('Cedron', 'Kidron', 'Kidron'), ('Moloch', 'Molech', 'Molech'),
]

SHARED = {'Jonas', 'Juda', 'Judas', 'Jesus', 'Aram', 'Heber', 'Sala', 'Zara', 'Abia'}
# Shared names where the BSB follows a different Greek text and so can't confirm the person.
CONFIRMED = {('LUK', 3, 33, 'Aram')}  # "which was the son of Aram": Ram of Ruth 4:19 (BSB "Admin, … Arni")

kjv = zipfile.ZipFile(PKG / 'eng.bible.kjv.zip')
bsb = zipfile.ZipFile(PKG / 'eng.bible.bsb.zip')
manifest = json.loads(kjv.read('manifest.json'))
NT_BOOKS = [b['book_id'] for b in manifest['books'] if b['canon'] == 'nt']
BOOK_ORDER = {b['book_id']: i for i, b in enumerate(manifest['books'])}
by_form = {nt: (ot, b) for nt, ot, b in NAMES}
POSS = re.compile(r'^(.*?)(’s|’)?$')

changes, skipped, counts = [], [], collections.Counter()
for bk in NT_BOOKS:
    K = json.loads(kjv.read(f'{bk}.json'))
    B = json.loads(bsb.read(f'{bk}.json'))
    bsb_words = {(c['chapter'], v['verse']): {re.sub(r'’s?$', '', t['t']) for t in v['tokens']}
                 for c in B['chapters'] for v in c['verses']}
    for c in K['chapters']:
        for v in c['verses']:
            for t in v['tokens']:
                base, poss = POSS.match(t['t']).groups()
                if base not in by_form:
                    continue
                ot, b = by_form[base]
                row = {'book': bk, 'chapter': c['chapter'], 'verse': v['verse'], 'word': t['n'],
                       'kjv': t['t'], 'modernized': ot + (poss or '')}
                if (base not in SHARED or b in bsb_words.get((c['chapter'], v['verse']), ())
                        or (bk, c['chapter'], v['verse'], base) in CONFIRMED):
                    changes.append(row)
                    counts[base] += 1
                else:
                    skipped.append(row)

# ── Modern spellings, following the BSB (both Testaments) ──
# A KJV name takes the BSB's spelling where the BSB has the same name in the same verse (paired through
# the Hebrew or Greek word): Phebe → Phoebe, Maachah → Maacah, Nebuchadrezzar → Nebuchadnezzar. Where
# the BSB has no word to pair, it changes only when the BSB spells that KJV name one way everywhere.
# Not where the BSB uses another name (Syria → Aram, Ahasuerus → Xerxes: that is translating), nor where
# only the word's form changes (Egypt → Egyptians, Ludim → Ludites). See LEFT-ALONE.md.
RENAMES = {  # the BSB's other name for the place or person; similar enough to slip past the test below
    ('Shushan', 'Susa'), ('Chittim', 'Cyprus'), ('Noph', 'Memphis'), ('Idumea', 'Edom'), ('Jewry', 'Judea'),
    ('Mesopotamia', 'Aram-naharaim'), ('Palestina', 'Philistia'), ('Palestina', 'Philistines'),
    ('Asshur', 'Assyria'), ('Assur', 'Assyria'), ('Euphrates', 'Perath'), ('Grecia', 'Javan'),
    ('Babel', 'Babylon'), ('Assyria', 'Asshur'), ('Olivet', 'Olives'), ('Appii', 'Appius'),
    ('Hoshea', 'Joshua'), ('Jeshua', 'Joshua'), ('Saul', 'Shaul'), ('Judah', 'Yehudah'), ('Judea', 'Judah'),
    ('Rebekah', 'Rebecca'),  # EJ: Rebekah stays
    ('Beelzebub', 'Beelzebul'),  # EJ: kept for familiarity, like "begat"
}
FORMS = {  # the same name as another kind of word: people for land, a plural for one
    ('Philistines', 'Philistia'), ('Benjamin', 'Benjamites'), ('Benjamin', 'Benjamite'), ('Jews', 'Jewish'),
    ('Maachathites', 'Maacath'), ('Medes', 'Media'), ('Galilee', 'Galilean'), ('Samaria', 'Samaritan'),
    ('Cyrenian', 'Cyrene'), ('Chaldees', 'Chaldeans'), ('Chaldees', 'Chaldean'), ('Assyrian', 'Assyrians'),
    ('Cretes', 'Cretans'), ('Thessalonians', 'Thessalonica'), ('Cyprus', 'Cypriot'), ('Jimnites', 'Imnite'),
}
TEXT = {  # the BSB reads another word in the Hebrew or Greek (another manuscript, the Qere, a parallel passage)
    ('Juda', 'Judas'), ('Johanan', 'Jehohanan'), ('Hadar', 'Hadad'), ('Gibeah', 'Geba'), ('Salma', 'Salmon'),
    ('Malcham', 'Milcom'), ('Jehiel', 'Jeiel'), ('Jehonathan', 'Jonathan'), ('Reuel', 'Deuel'), ('Hebron', 'Ebron'),
    ('Heleb', 'Heled'), ('Hezrai', 'Hezro'), ('Ebal', 'Obal'), ('Elishama', 'Elishua'), ('Hezekiah', 'Hizkiah'),
    ('Jehoshaphat', 'Joshaphat'), ('Abimelech', 'Ahimelech'), ('Shimea', 'Shimei'), ('Elioenai', 'Eliehoenai'),
    ('Elihoenai', 'Eliehoenai'), ('Ephrain', 'Ephron'), ('Jeiel', 'Jeuel'), ('Chelluh', 'Cheluhi'),
    ('Jadau', 'Jaddai'), ('Jaasau', 'Jaasu'), ('Jehoiada', 'Joiada'), ('Joiada', 'Jehoiada'), ('Gashmu', 'Geshem'),
    ('Zidkijah', 'Zedekiah'), ('Hizkijah', 'Hezekiah'), ('Hizkiah', 'Hezekiah'), ('Pul', 'Put'),
    ('Magdala', 'Magadan'), ('Joses', 'Joseph'), ('Simeon', 'Simon'), ('Jonan', 'Jonam'), ('Clauda', 'Cauda'),
    ('Amplias', 'Ampliatus'), ('The', 'He'), ('Esther', 'She'),
    # one word of a name the KJV writes as two
    ('Koz', 'Hakkoz'), ('Eleph', 'Haeleph'), ('Shophan', 'Atroth-shophan'), ('Hadattah', 'Hazor-hadattah'),
    ('Berith', 'El-berith'),
    ('Rimmon', 'Rimmono'), ('Selah', 'Sela'),
}
EVEN = {  # another name the KJV itself also uses for the same place, which the BSB evens out to
    ('Azzah', 'Gaza'),
}
SUFFIX = re.compile(r'(ites?|ians?|ans?|ims?|im|s)$')


def strongs(s):
    m = re.match(r'([GH])0*(\d+)', s or '')
    return m.group(1) + m.group(2) if m else None


def same_name(k, b):
    """True when b is k spelled another way, not another name or another form of the word."""
    if (k, b) in RENAMES | FORMS | TEXT or (b, k) in spell_pairs:  # both ways round: the BSB follows the Hebrew, not one spelling
        return False
    if (k, b) in EVEN:
        return True
    a, c = k.lower(), b.lower()
    if a + 's' == c or c + 's' == a:
        return a.endswith('ims')  # Anakims → Anakim only
    if a.startswith(c) or c.startswith(a):  # Tekoah → Tekoa, Enos → Enosh; not Canaan → Canaanite
        return max(a, c, key=len)[min(len(a), len(c)):] in ('h', 'a', 'ah', 'e', 'u', 'hu')
    if SUFFIX.sub('', a) == SUFFIX.sub('', c) or (a.endswith(('im', 'ims')) and c.endswith(('ites', 'ite'))):
        return False
    import difflib
    return difflib.SequenceMatcher(None, a, c).ratio() >= 0.6


current = {(r['book'], r['chapter'], r['verse'], r['word']): r for r in changes}
keys = {'nt': zipfile.ZipFile(PKG / 'grc.key.nt.zip'), 'ot': zipfile.ZipFile(PKG / 'hbo.key.ot.zip')}
PROPER = re.compile(r'Np|^N-PRI|^N-.*-(P|L|T|LG|PG|LI)$')
seen, pairs = [], collections.defaultdict(collections.Counter)
for b in manifest['books']:
    bk = b['book_id']
    if b['canon'] not in ('ot', 'nt') or f'{bk}.json' not in keys[b['canon']].namelist():
        continue
    KP = json.loads(keys[b['canon']].read(f'{bk}.json'))['verses']
    BV, BA = collections.defaultdict(set), set()
    for c in json.loads(bsb.read(f'{bk}.json'))['chapters']:
        for v in c['verses']:
            for t in v['tokens']:
                s = strongs(t.get('s'))
                BA.add((c['chapter'], v['verse'], s))
                if s and t['t'][:1].isupper() and PROPER.search(t.get('m') or ''):
                    BV[(c['chapter'], v['verse'], s)].add(re.sub(r'’s?$', '', t['t']))
    for c in json.loads(kjv.read(f'{bk}.json'))['chapters']:
        kv = {}
        for v in c['verses']:
            kv = KP.get(f"{c['chapter']}:{v['verse']}", {})
            for t in v['tokens']:
                loc = (bk, c['chapter'], v['verse'], t['n'])
                word = current[loc]['modernized'] if loc in current else t['t']
                base, poss = POSS.match(word).groups()
                if not base[:1].isupper() or not base.isalpha():
                    continue
                S = {strongs(kv[k][1]) for k in [t.get('k')] + (t.get('ka') or []) if k and k in kv}
                found = set().union(*(BV.get((c['chapter'], v['verse'], s), set()) for s in S)) if S else set()
                pair = next(iter(found)) if len(found) == 1 else None
                if pair:
                    pairs[base][pair] += 1
                bare = not any((c['chapter'], v['verse'], s) in BA for s in S)  # nothing in the BSB to pair with
                seen.append((loc, t['t'], base, poss or '', pair, bare))
# A KJV name the BSB spells one way everywhere it pairs: that spelling also serves where nothing pairs.
only = {k: next(iter(bc)) for k, bc in pairs.items() if len(bc) == 1}
spell_pairs = {(k, b) for k, bc in pairs.items() for b in bc if b != k}
spell_counts = collections.Counter()
for loc, kjv_word, base, poss, pair, bare in seen:
    target = pair or (only.get(base) if bare else None)
    if not target or target == base or not same_name(base, target):
        continue
    row = current.get(loc)
    if row:
        row['modernized'] = target + poss
    else:
        bk, ch, v, n = loc
        row = {'book': bk, 'chapter': ch, 'verse': v, 'word': n, 'kjv': kjv_word, 'modernized': target + poss}
        changes.append(row)
        current[loc] = row
    spell_counts[(base, target)] += 1
changes.sort(key=lambda r: (BOOK_ORDER[r['book']], r['chapter'], r['verse'], r['word']))

OUT.mkdir(exist_ok=True)
json.dump({'kjv_package': manifest['package_version'],
           'names': [{'kjv_nt': nt, 'kjv_ot': ot, 'bsb': b, 'changed': counts[nt]} for nt, ot, b in NAMES],
           'spellings': [{'kjv': k, 'modernized': b, 'changed': n} for (k, b), n in sorted(spell_counts.items())],
           'changes': changes, 'skipped': skipped},
          open(OUT / 'names.json', 'w'), indent=1, ensure_ascii=False)
lines = [f'# Names\n',
         f'Generated by `tools/build_names.py` from KJV {manifest["package_version"]}. '
         f'{len(changes)} words changed; {len(skipped)} left alone because the BSB names someone else there.\n',
         '| KJV New Testament | KJV Old Testament | Changed |', '|---|---|---:|']
lines += [f'| {nt} | {ot} | {counts[nt]} |' for nt, ot, _ in NAMES if counts[nt]]
lines += ['\n## Modern spellings (from the BSB)\n', f'{sum(spell_counts.values())} words, {len(spell_counts)} spellings. '
          'A name the first table changes may change again here (Phares → Pharez → Perez).\n',
          '| KJV | KJVm | Changed |', '|---|---|---:|']
lines += [f'| {k} | {b} | {n} |' for (k, b), n in sorted(spell_counts.items(), key=lambda x: (-x[1], x[0]))]
lines += ['\n## Every change\n'] + [f"- {r['book']} {r['chapter']}:{r['verse']} {r['kjv']} → {r['modernized']}" for r in changes]
lines += ['\n## Left alone\n'] + [f"- {r['book']} {r['chapter']}:{r['verse']} {r['kjv']}" for r in skipped
                                   if not r['kjv'].startswith('Jesus')]
lines += [f"- “Jesus” everywhere except the verses above ({sum(r['kjv'].startswith('Jesus') for r in skipped)} places)"]
(OUT / 'changes.md').write_text('\n'.join(lines) + '\n')
print(len(changes), 'changed', len(skipped), 'skipped')
print('spellings:', sum(spell_counts.values()), len(spell_counts))
print(collections.Counter(r['kjv'] for r in skipped if not r['kjv'].startswith('Jesus')).most_common(30))
