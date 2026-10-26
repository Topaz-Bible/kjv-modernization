# Names (draft)

The KJV New Testament spells Old Testament people and places the way the Greek does, so one person
can appear under two names: Elijah in Kings, Elias in Matthew. This layer gives them the spelling
**the KJV itself uses in the Old Testament**: Elias → Elijah, Esaias → Isaiah, Noe → Noah,
Sion → Zion, Booz → Boaz, Phares → Pharez. The target is always the KJV's own Old Testament spelling,
not a modern one (so Pharez, not Perez).

It's the same name in another form, not a different word, so it stays within "form, not translation".

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
