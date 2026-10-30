# Pronouns for God (switched off)

**Off since 2026-10-28.** The KJV never capitalized pronouns for God, and neither do most modern Bibles
(NIV, ESV, NRSV, NLT, NET, CSB). The practice came back in the 1960s with the NASB and the NKJV; the
CSB, revising the HCSB, dropped it in 2017 because the Hebrew and Greek don't mark it and deciding who
"he" is would be interpretation. Here it rested almost wholly on the BSB, one of the few that still do
it. The KJVo keeps "he", "his" and "thee" (→ "you") lowercase. This folder and its tool stay as they
were, unused, in case that ever changes.

The KJV never capitalized pronouns for God; that convention came later and is now what most readers
expect. This layer capitalizes He, Him, His, Himself, Thou, Thee, Thy, Thine, Thyself, Me, My, Mine and
Myself where they refer to God.

Deciding who a pronoun refers to is sometimes interpretation:

- the messianic psalms
- Genesis 3:15
- people speaking to Jesus before they know who he is

So this layer makes **no decisions of its own**. It follows the Berean Standard Bible verse by verse:
where the BSB capitalizes, so does this. Where it doesn't, neither does this.

## How

Pronouns are compared in three groups (he/him/his, thou/thee/thy, me/my/mine).

- **Pairing:** within a verse, when the KJV has as many of a group as the BSB, they pair up in order.
- **Sentence starts:** a BSB pronoun at the start of a sentence or quote is capitalized anyway, so it
  tells us nothing. It follows the rest of its group in the verse when they all refer to God.
- **Uneven counts:** when the KJV and BSB have different numbers of a group's pronouns, they are paired
  through the Hebrew or Greek word each belongs to instead. Hebrew writes "his work" as one word,
  work-his, and both Bibles link their pronoun to it, so the KJV's *his* and the BSB's *His* meet there.
  The KJV's extra pronouns (the BSB often drops them: "He will destroy them and subdue them") are settled
  from the same word: a BSB "God" or "the LORD" there makes it His, another name or a lowercase he
  makes it someone else's. For I and you, one speaker in a verse is one speaker, unless the narrator
  has the pronoun ("the LORD said unto me") or the BSB has someone else's on that word ("The LORD is
  our God"). A verse is settled whole or not at all: anything unclear leaves it in
  [`review.md`](review.md), lowercase.
- **By hand:** a verse from the review list can be settled in [`by-hand.csv`](by-hand.csv), one row per
  pronoun.
- **Plurals:** KJV ye, you and your are plural, so they are never capitalized.

With word forms also on, the capital carries through: Thee → You, Thy → Your.

To rebuild, run `python3 tools/build_capitals.py`.
