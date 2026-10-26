#!/usr/bin/env python3
"""Regenerate every list in this repository from a Topaz KJV package.

Reads (read-only): a Topaz KJV package zip (its mod.json and per-book token files).
Writes:
  words/substitutions.md     human-readable list with counts
  words/rules.json           full profile + per-rule counts
  words/rules.csv            one row per rule or single-verse exception
  words/every-change.csv     every changed word, no rules needed

It applies the rules exactly as the app does (topaz-bible/src/data/modernizer.ts):
location overrides first, then rules in file order, first match wins, case copied
from the original word. `strongs_in` never matches (1.4 tokens carry no Strong's).

Run:  python3 tools/build_lists.py [path/to/eng.bible.kjv.zip]
      (default: ../topaz-bible/assets/packages/eng.bible.kjv.zip, beside this repo)
"""
import csv, json, re, sys, zipfile, collections
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ZIP = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO.parent / 'topaz-bible' / 'assets' / 'packages' / 'eng.bible.kjv.zip'

z = zipfile.ZipFile(ZIP)
m = json.loads(z.read('mod.json'))
version = json.loads(z.read('manifest.json'))['package_version']

by_text = collections.defaultdict(list)
for r in m['rules']:
    if r.get('enabled'):
        by_text[r['match']['text'].lower()].append(r)
overrides = {(o['location']['book_id'], o['location']['chapter'], o['location']['verse'], o['location']['token']): o
             for o in m['location_overrides'] if o.get('enabled')}


def keep_case(src, rep):
    if len(src) > 1 and src.isupper():
        return rep.upper()
    if src[:1].isupper():
        return rep[:1].upper() + rep[1:]
    return rep


def holds(when, ts, i, book):
    if not when:
        return True
    low = lambda xs: [x.lower() for x in xs]
    if 'previous_text_in' in when and (i == 0 or ts[i - 1]['t'].lower() not in low(when['previous_text_in'])):
        return False
    if 'next_text_in' in when and (i + 1 >= len(ts) or ts[i + 1]['t'].lower() not in low(when['next_text_in'])):
        return False
    if when.get('after_punctuation_present') and not ts[i].get('a'):
        return False
    if 'book_id_in' in when and book not in when['book_id_in']:
        return False
    if 'flags_include' in when and not all(f in (ts[i].get('f') or []) for f in when['flags_include']):
        return False
    if 'strongs_in' in when:
        return False
    return True


hits = collections.Counter()
changes = []
tokens = 0
for name in z.namelist():
    if not re.fullmatch(r'[1-4A-Z]{3}\.json', name):
        continue
    book = json.loads(z.read(name))
    b = book['book_id']
    for ch in book['chapters']:
        for v in ch['verses']:
            ts = v['tokens']
            for i, t in enumerate(ts):
                tokens += 1
                o = overrides.get((b, ch['chapter'], v['verse'], t['n']))
                if o and o['match']['text'].lower() == t['t'].lower():
                    hits[o['id']] += 1
                    if o['replace']['text'].lower() != t['t'].lower():
                        changes.append([b, ch['chapter'], v['verse'], t['n'], t['t'], keep_case(t['t'], o['replace']['text']), o['id']])
                    continue
                for r in by_text.get(t['t'].lower(), []):
                    if holds(r.get('when'), ts, i, b):
                        hits[r['id']] += 1
                        changes.append([b, ch['chapter'], v['verse'], t['n'], t['t'], keep_case(t['t'], r['replace']['text']), r['id']])
                        break
changed = len(changes)
dead = [r['id'] for r in m['rules'] if r.get('enabled') and not hits[r['id']]]

AUX = {'hath', 'doth', 'saith', 'art', 'wilt', 'shalt', 'wert', 'hast', 'didst', 'canst', 'wast', 'dost',
       'mayest', 'shouldest', 'wouldest', 'couldest'}


def group(r):
    w, c = r['match']['text'].lower(), r['category']
    if c in ('pronoun', 'spelling', 'direction'):
        return c
    if w in AUX:
        return 'auxiliary'
    if w.endswith('eth'):
        return 'third_person_eth'
    if w.endswith('st'):
        return 'second_person_est'
    return 'old_past_tense'


def condition(when):
    if not when:
        return ''
    parts = []
    if 'previous_text_in' in when:
        parts.append('after ' + ' / '.join(f'“{x}”' for x in when['previous_text_in']))
    if 'next_text_in' in when:
        xs = when['next_text_in']
        parts.append('before ' + (' / '.join(f'“{x}”' for x in xs) if len(xs) <= 4 else f'one of {len(xs)} listed words'))
    if when.get('after_punctuation_present'):
        parts.append('when followed by punctuation')
    if 'book_id_in' in when:
        parts.append('only in ' + ', '.join(when['book_id_in']))
    if 'strongs_in' in when:
        parts.append('only over listed Strong’s numbers (inactive)')
    return '; '.join(parts)


rows = []
for i, r in enumerate(m['rules']):
    rows.append(dict(id=r['id'], type='rule', category=r['category'], group=group(r), match=r['match']['text'],
                     replace=r['replace']['text'], condition=condition(r.get('when')),
                     when=json.dumps(r.get('when'), ensure_ascii=False) if r.get('when') else '', location='',
                     occurrences=hits[r['id']], order=i))
for o in m['location_overrides']:
    L = o['location']
    rows.append(dict(id=o['id'], type='override', category=o.get('category', ''), group='override', match=o['match']['text'],
                     replace=o['replace']['text'], condition='', when='',
                     location=f"{L['book_id']} {L['chapter']}:{L['verse']} #{L['token']}", occurrences=hits[o['id']], order=''))

with open(REPO / 'words' / 'rules.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(REPO / 'words' / 'every-change.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['book', 'chapter', 'verse', 'word', 'kjv', 'modernized', 'rule']); w.writerows(changes)
json.dump({
    'name': 'Topaz Bible — KJV Modernized Word Forms', 'licence': 'CC0-1.0', 'source_profile': m['profile_id'],
    'package_version': version, 'mode': 'display_only', 'matching': m['matching'],
    'case_strategy': m['case_strategy_notes'], 'condition_language': m['condition_language']['supported_conditions'],
    'stats': {'tokens_in_kjv': tokens, 'tokens_changed': changed, 'rules': len(m['rules']), 'location_overrides': len(m['location_overrides'])},
    'rules': m['rules'], 'location_overrides': m['location_overrides'], 'occurrences': dict(hits),
}, open(REPO / 'words' / 'rules.json', 'w'), ensure_ascii=False, indent=1)

# ─── Human-readable list ──────────────────────────────────────────────────────
LAB = {'pronoun': 'Pronouns (thou, thee, ye, thy, thine, mine)',
       'auxiliary': 'Helping verbs and irregular forms (hath, doth, art, shalt…)',
       'third_person_eth': 'Third-person “-eth” verbs (believeth → believes)',
       'second_person_est': 'Second-person “-est” verbs (thou knowest → you know)',
       'old_past_tense': 'Old past tenses (spake → spoke, bare → bore)',
       'spelling': 'Old spellings (shew → show)',
       'direction': 'Here, there and where (hither → here, from thence → from there)'}
rule_rows = collections.defaultdict(list)
total = collections.Counter()
for r in rows:
    total[r['group']] += r['occurrences'] if r['type'] == 'rule' or r['replace'].lower() != r['match'].lower() else 0
    if r['type'] == 'rule':
        rule_rows[r['group']].append(r)

BN = dict(GEN='Genesis', EXO='Exodus', LEV='Leviticus', NUM='Numbers', DEU='Deuteronomy', JOS='Joshua', JDG='Judges',
          RUT='Ruth', ISA='Isaiah', JER='Jeremiah', EZK='Ezekiel', JOL='Joel', PSA='Psalm', MAT='Matthew', MRK='Mark',
          LUK='Luke', JHN='John', ACT='Acts', ROM='Romans', **{'1CO': '1 Corinthians', '2CO': '2 Corinthians'},
          PHM='Philemon', JAS='James', REV='Revelation', SIR='Sirach')
ORDER = list(BN)

out = ['# Every word the modernized KJV changes\n',
       f"The Topaz Bible's “Modernize spelling” option changes **{changed:,}** of the KJV's **{tokens:,}** words "
       f"(about {changed * 100 / tokens:.1f}%). It uses {len(m['rules']):,} word rules and {len(m['location_overrides'])} "
       "single-verse exceptions. The underlying text never changes: switch the option off and every word is back to the "
       "King James text.\n",
       f'Counts are how many times each change happens in the KJV, Apocrypha included. Generated from KJV package {version}.\n',
       '## At a glance\n', '| Kind of change | Rules | Words changed |', '|---|---:|---:|']
for g in LAB:
    out.append(f'| {LAB[g]} | {len(rule_rows[g]):,} | {total[g]:,} |')
ov_changes = sum(1 for c in changes if c[6] in overrides_ids) if (overrides_ids := {o['id'] for o in m['location_overrides']}) else 0
out.append(f"| Single-verse exceptions | {len(m['location_overrides'])} | {ov_changes:,} changed, the rest kept as written |\n")


def table(g, by_count):
    rs = sorted(rule_rows[g], key=(lambda r: (-r['occurrences'], r['match'])) if by_count else (lambda r: r['match'].lower()))
    t = ['| KJV | Modernized | Only when | Times |', '|---|---|---|---:|']
    t += [f"| {r['match']} | {r['replace']} | {r['condition']} | {r['occurrences']:,} |" for r in rs]
    return t


INTRO = {
    'pronoun': 'The singular “thou/thee/thy/thine” and the plural “ye” all become “you/your”. Modern English no longer marks singular and plural here, so the change loses that distinction; the original keeps it. “Mine” and “thine” before a vowel sound (“mine eyes”, “thine house”) become “my/your”; at the end of a phrase “thine” becomes “yours”.',
    'auxiliary': 'The most common archaic forms. They follow the pronoun change: “thou art” becomes “you are”, “thou shalt” becomes “you shall”.',
    'old_past_tense': 'Past tenses that English later regularized. “Bare” becomes “bore” everywhere except the 14 verses where it is the adjective (“naked and bare”); those are listed under single-verse exceptions.',
    'spelling': 'Same word, modern spelling.',
    'direction': 'Old English had separate words for “to here” (hither) and “from here” (hence). Today “here”, “there” and “where” do all three jobs. “Hither”, “thither”, “whither” and “whithersoever” always change. “Hence”, “thence” and “whence” change only after “from”, where the “from” is already written (“from thence” → “from there”); on their own they would need two words, so they stay, as do “hitherto” and “thitherward”.',
    'second_person_est': 'The verb ending that went with “thou”. With “thou” becoming “you”, the verb loses its ending: “thou knowest” becomes “you know”, “thou mightest” becomes “you might”.',
    'third_person_eth': 'The old “-eth” ending, the forerunner of today’s “-s”: “he believeth” becomes “he believes”. Words that only look like these are left alone: nouns (priest, harvest), superlatives (greatest, eldest), ordinals (twentieth) and names (Nazareth, Japheth).',
}
for g, by_count in [('pronoun', True), ('auxiliary', True), ('old_past_tense', True), ('spelling', True), ('direction', True),
                    ('second_person_est', False), ('third_person_eth', False)]:
    out += [f'## {LAB[g]}\n', INTRO[g] + '\n'] + table(g, by_count) + ['']

out += ['## Single-verse exceptions\n',
        'A few words are decided verse by verse. In the New Testament, “yea” becomes “yes” only where the Greek underneath is ναί (“yes”), and “nay” becomes “no” only where it is οὐ or οὐχί (“no”). Everywhere else these words mean “indeed”, “even” or “rather” (as in 1 Corinthians 2:10, “yea, the deep things of God”) and stay. In the Old Testament both stay throughout, because Hebrew has no word for “yes”. “Bare” stays “bare” where it means “naked”, and “thine” becomes “yours” in a few places where it stands alone.\n',
        '| Verse | KJV | Shown as |', '|---|---|---|']


def place_key(o):
    L = o['location']
    return (ORDER.index(L['book_id']) if L['book_id'] in ORDER else 99, L['chapter'], L['verse'], L['token'])


for o in sorted(m['location_overrides'], key=place_key):
    L = o['location']
    shown = o['replace']['text'] if o['replace']['text'].lower() != o['match']['text'].lower() else f"{o['replace']['text']} (unchanged)"
    out.append(f"| {BN.get(L['book_id'], L['book_id'])} {L['chapter']}:{L['verse']} | {o['match']['text']} | {shown} |")
out += ['\n## What is not changed\n',
        '- **Meaning words.** Obsolete or shifted words (“let” meaning hinder, “prevent” meaning go before, “conversation” meaning conduct) are left alone. Changing them would be translation, not modernizing.',
        '- **Word order and grammar** beyond the verb endings.',
        '- **Names, italics (words the translators supplied), punctuation and verse divisions.**',
        '- **The underlying text.** Every change happens on screen as the page is drawn.\n',
        '---\n',
        'This list and the files behind it are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).\n']
(REPO / 'words' / 'substitutions.md').write_text('\n'.join(out))

print(f'KJV {version}: {tokens:,} words, {changed:,} changed; {len(m["rules"])} rules, '
      f'{len(m["location_overrides"])} overrides; rules that never fire: {dead or "none"}')
