# Pronouns for God (draft)

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
- **Uneven counts:** when the KJV and BSB have different numbers of a group's pronouns, the verse is
  left alone and listed in [`review.md`](review.md).
- **Plurals:** KJV ye, you and your are plural, so they are never capitalized.

With word forms also on, the capital carries through: Thee → You, Thy → Your.

To rebuild, run `python3 tools/build_capitals.py`.
