# Names (draft)

The KJV New Testament spells Old Testament people and places the way the Greek does, so one person
can appear under two names: Elijah in Kings, Elias in Matthew. This layer first gives them the spelling
**the KJV itself uses in the Old Testament**: Elias → Elijah, Esaias → Isaiah, Noe → Noah,
Sion → Zion, Booz → Boaz, Phares → Pharez.

Then every name, in both Testaments, takes **the BSB's spelling** where it is only a spelling:
Phebe → Phoebe, Cesar → Caesar, Tyrus → Tyre, Zidon → Sidon, Timotheus → Timothy, Pharez → Perez,
Maachah → Maacah. The BSB stands in for what modern translations do on the whole. Where the KJV spells
one person or place two ways and the BSB evens them out, the KJVm follows (Nebuchadrezzar →
Nebuchadnezzar, Urijah → Uriah, Azzah → Gaza). Rebekah stays: the BSB's Rebecca in Romans 9:10 is the
Greek spelling. Beelzebub stays too (the BSB's Beelzebul): like "begat", it is too familiar to change.

It's the same name in another form, not a different word, so it stays within "form, not translation".
Where the BSB uses another name (Syria → Aram, Ahasuerus → Xerxes, Diana → Artemis), the KJV's stays;
see [LEFT-ALONE.md](../LEFT-ALONE.md).

## How the spellings are matched

A KJV name and a BSB name in the same verse that translate the same Hebrew or Greek word are paired.
The KJV word takes the BSB's spelling when the two are the same name spelled another way: close in
letters, not a people for a land (Philistines, Philistia) or a plural for one, not the BSB reading
another word in the manuscripts (Heleb, Heled). `tools/build_names.py` lists those it leaves alone by
hand. A name the BSB has no word to pair with takes the spelling the BSB uses for it everywhere else,
if there is only one. The Apocrypha has no BSB, so its names are left as they are.

## The hard calls

Most of these names belong to only one person or place and change everywhere. A few are shared with
New Testament people, and those change only where the BSB names the Old Testament person in the same
verse:

- **Jesus → Joshua** only in Acts 7:45 and Hebrews 4:8, where the Greek name means Joshua.
- **Jonas → Jonah** only for the prophet. "Simon, son of Jonas" (John 21) stays.
- **Judas → Judah** only for the patriarch (Matthew 1:2–3). Judas Iscariot and the others stay.
- **Aram → Ram** in Luke 3:33 is confirmed by hand. The BSB follows a different Greek text there.

## The genealogies

The genealogies of Jesus (Matthew 1, Luke 3) change too, as in the BSB, NKJV, ESV and NIV: Phares → Pharez,
Booz → Boaz, Ozias → Uzziah, Mathusala → Methuselah.

## Files

- [`changes.md`](changes.md): every change, and every shared name left alone.
- `names.json`: the same for software. Each change gives book, chapter, verse, word number, the KJV
  word and its replacement, like the word-forms list.

To rebuild, run `python3 tools/build_names.py`.
