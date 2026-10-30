# Word forms

**Every word the [Topaz Bible](https://topaz.bible) changes when you turn on "Modernize spelling" for the King James Version, as open, reusable data.**

*thou → you · hath → has · believeth → believes · thou knowest → you know · spake → spoke · shew → show · whither → where*

The King James text itself is never edited. These rules are a display layer: the reader shows the modern form of a word in place of the old one, and switching the option off brings back the original word for word. The changes are to word *forms* only. Archaic *words* (wist, wot, sith, betwixt) and words whose *meaning* has shifted ("let" for *hinder*, "prevent" for *go before*) are left alone, because changing them would be translation.

| | |
|---:|---|
| **41,312** | words changed, out of 931,532 in the KJV (4.4%) |
| **1,228** | word rules |
| **61** | single-verse exceptions |

## What's here

| File | What it is |
|---|---|
| [`substitutions.md`](substitutions.md) | **For readers.** Every change, grouped by kind, with how often it happens |
| [`every-change.csv`](every-change.csv) | **The simplest way to use this.** Every changed word, with its verse, its position in the verse, the KJV word and the replacement. No rules to implement |
| [`rules.json`](rules.json) | The full rule set: matching settings, conditions, exceptions, and counts |
| [`rules.csv`](rules.csv) | The same rules, one row each, for spreadsheets |
| [`how-it-works.md`](how-it-works.md) | How matching works, how the rules were made, caveats for reuse |
| [`../tools/build_lists.py`](../tools/build_lists.py) | Rebuilds every file above from a Topaz KJV package (Python 3, no dependencies) |

## Words now written as one

[`joins.csv`](joins.csv) lists word pairs the KJV prints as two words that are one word today: *to day*
→ *today*, *for ever* → *forever*, *any thing* → *anything*, *strong hold* → *stronghold* (17 pairs,
912 places). The KJVm closes up the space between them; the two words stay two words in the data, each
with its own Strong's number. Left out on purpose: *every one* and *any more* (often still "each one",
"any longer"), *in ward* ("in custody"), *head stone* (now a grave marker), *high way*, *up on*. Not
where punctuation, a line break or a quotation mark falls between the two.

## Words now written as two

[`splits.csv`](splits.csv) goes the other way: words the KJV prints as one that are two words, or
hyphenated, today: *stumblingblock* → *stumbling block*, *dwellingplace* → *dwelling place*,
*threshingfloor* → *threshing floor*, *fellowservant* → *fellow servant*, *twoedged* → *two-edged*
(60 words, 166 places). Each is an ordinary word rule of category `split`; the word stays one token,
with its one Strong's number. Found by listing every KJV word that splits into two English words
which the BSB writes apart, then read by hand. Left as they are: words still written as one
(*straightway*, *firstborn*, *winepress*, *marketplace*, *castaway*), *lovingkindness* and
*longsuffering* (set terms), *goodman* ("master of the house", not a good man), *eveningtide*.

## Three ways to use it

1. **Read it.** [`substitutions.md`](substitutions.md) lists every change.
2. **Apply the list.** For each row of [`every-change.csv`](every-change.csv):
   - find the verse
   - find the word by its position (punctuation doesn't count as a word)
   - check that it is the `kjv` word
   - show `modernized` instead

   You need no Greek or Hebrew and no rule logic.
3. **Run the rules.** Implement the matcher in [`how-it-works.md`](how-it-works.md) over [`rules.json`](rules.json):
   - single-verse exceptions first
   - then rules in order
   - first match wins
   - the original word's capitalization is kept

## A few of the harder calls

- **Yea and nay.**
  - "Yea" becomes "yes" only where the Greek underneath is ναί (*yes*).
  - "Nay" becomes "no" only where the Greek is οὐ or οὐχί (*no*).
  - Everywhere else they mean "indeed", "even" or "rather", and they stay. 1 Corinthians 2:10 keeps "yea, the deep things of God".
  - The Old Testament keeps both throughout, because Hebrew has no word for *yes*.
- **Tables.** "Tables" becomes "tablets" where they are written on: the tables of stone, "the table of
  thine heart" (Proverbs 3:3), Zacharias's "writing table" (Luke 1:63), "tables of brass" (1 Maccabees).
  The Hebrew לוּחַ and the Greek πλάξ and πινακίδιον mark the 46 places. A table to eat at or set
  bread on (שֻׁלְחָן, τράπεζα) stays a table.
- **Bare.** "Bare" becomes "bore", except in the 14 verses where it means *naked* ("made bare his holy arm").
- **Lookalikes.** Some words end like old verb forms but aren't, and stay as written:
  - nouns: priest, harvest
  - superlatives: greatest, eldest
  - ordinals: twentieth
  - names: Nazareth, Japheth
- **What "you" costs.** "Thou" was singular and "ye" plural; modern "you" merges them. The original is always one tap away.
