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

OUT.mkdir(exist_ok=True)
json.dump({'kjv_package': manifest['package_version'],
           'names': [{'kjv_nt': nt, 'kjv_ot': ot, 'bsb': b, 'changed': counts[nt]} for nt, ot, b in NAMES],
           'changes': changes, 'skipped': skipped},
          open(OUT / 'names.json', 'w'), indent=1, ensure_ascii=False)
lines = [f'# Old Testament names in the New Testament\n',
         f'Generated by `tools/build_names.py` from KJV {manifest["package_version"]}. '
         f'{len(changes)} words changed; {len(skipped)} left alone because the BSB names someone else there.\n',
         '| KJV New Testament | KJV Old Testament | Changed |', '|---|---|---:|']
lines += [f'| {nt} | {ot} | {counts[nt]} |' for nt, ot, _ in NAMES if counts[nt]]
lines += ['\n## Every change\n'] + [f"- {r['book']} {r['chapter']}:{r['verse']} {r['kjv']} → {r['modernized']}" for r in changes]
lines += ['\n## Left alone\n'] + [f"- {r['book']} {r['chapter']}:{r['verse']} {r['kjv']}" for r in skipped
                                   if not r['kjv'].startswith('Jesus')]
lines += [f"- “Jesus” everywhere except the verses above ({sum(r['kjv'].startswith('Jesus') for r in skipped)} places)"]
(OUT / 'changes.md').write_text('\n'.join(lines) + '\n')
print(len(changes), 'changed', len(skipped), 'skipped')
print(collections.Counter(r['kjv'] for r in skipped if not r['kjv'].startswith('Jesus')).most_common(30))
