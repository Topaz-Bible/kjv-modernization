# KJV quotation marks (draft)

The KJV has no quotation marks. This folder holds a **draft** set of quote regions for it: where each
speech or quoted saying starts and stops, and how deeply it is nested. Nothing here is in a release yet,
and nothing here changes a word of the KJV. The marks would be laid over the text when it is shown, the
same way the spelling rules are.

Adding quotation marks involves judgement. Sometimes it's unclear where a speech ends, or whether a
saying is quoted at all. So every region is listed with where it came from and what was checked.

## How the regions are found

They start from the Berean Standard Bible (BSB), which already marks its quotes. Both Bibles link
their words to the same Greek and Hebrew words, so each BSB quote can be found in the KJV:

1. **Match the words.** A Greek or Hebrew word that occurs only once in the verse can only be one KJV
   word, so it anchors the quote. The BSB gives each word of a phrase the same number ("serve as
   lights"), so a phrase counts once. Common words ("the", "and", "him") are used only when a quote
   has no anchor.
2. **Find the opening** by walking back to where the speech begins. The KJV marks that with a capital
   letter after a comma or colon ("said unto him, Lovest thou me?"). The walk never crosses a word the
   BSB leaves outside its quotes, such as "he answered".
3. **Find the end** by running on to the end of the sentence or verse. The run never goes into the
   next quote or past a speech verb like "said" or "saith". It also stops at a colon or semicolon
   followed by "and": "Let there be light: and there was light".
   Where that left a quote ending mid-sentence ("thou hast well” said."), it runs on to the full stop,
   and on past a question that carries on in small letters ("shall we do after his saying? if not;
   speak thou."). A quote that ran into the narrator's next tag ("till Shelah my son be grown: for he”
   said, Lest…") ends before the tag. A quote may end on a comma before its speaker's tag ("…unto me,”
   saith the Lord.") when the tag ends the sentence or the quote takes up again after it. None of this
   applies where the BSB's quote runs on into a later verse: there the speech isn't over.
4. **Rejoin split speeches.** The BSB splits some speeches with a narrator tag that the KJV doesn't
   have ("“You will not surely die,” the serpent told her. “For God knows…”"). Those pieces become one
   quote again.
5. **Names and terms.** A word the BSB quotes inside the narrator's sentence ("God called the light
   “day”") is carried over word for word: *God called the light “Day,”*. No walking back.
6. **Check the words of Jesus.** In the Gospels the KJV marks Jesus's words itself, so a quote of Jesus
   must start and stop where that marking does.

## Tiers, easiest first

| Tier | What | File |
|---|---|---|
| 1 | One verse, nothing nested, both edges confirmed by KJV clues | [review/tier-1.md](review/tier-1.md) |
| 2 | Several verses, nothing nested, both edges confirmed | [review/tier-2.md](review/tier-2.md) |
| 3 | Quotes inside quotes | [review/tier-3.md](review/tier-3.md) |
| 4 | An edge not confirmed; each says why | [review/tier-4.md](review/tier-4.md) |
| 5 | Couldn't be carried over from the BSB | [review/tier-5.md](review/tier-5.md) |

The current counts are in `kjv-quotes.json` under `tiers`. "Confirmed" means the automatic checks
passed, not that a person has read it. A hand-checked sample of tier 1 was about 85% right. The usual
faults are an ending that runs a few words too far ("Master, master; and kissed him") and a second
speaker swallowed into the first. Each region has `status: draft` until it is reviewed.

## The data

`kjv-quotes.json` has one entry per region:

- `start` / `end`: `chapter.verse:word` positions in the KJV package (`word` is the word number in
  the verse).
- `start_word` / `end_word`: the words at those positions. If the KJV package is ever re-divided into
  words, a mismatch shows the region needs re-checking.
- `level`: 1 for a quote, 2 for a quote inside it, and so on.
- `bsb`: the BSB region it came from.
- `checks`: any check that failed.
- `joined`: how many BSB pieces were rejoined.
- `woj`: true when it's Jesus speaking.

To rebuild (it only reads the app's package files; ~25 s), run `python3 tools/build_quotes.py`.

`python3 tools/check_quote_edges.py` checks the shipped quotes against the BSB's: it lists every quote
whose first or last words are, in the Hebrew or Greek, words the BSB leaves outside its quotes ("I am
of Apollos; are ye not carnal?"). Most of what it lists is only different wording; the rest is fixed
in `reviewed.csv`. Hand edits were also read beside the NIV, ESV, NASB and CSB.

## Capital "That"

In 67 places the KJV writes "That" with a capital after a comma: "But I say unto you, That Elias is come
already" (Matthew 17:12). Two thirds of them (45 of 67) translate the Greek ὅτι.

Greek can use ὅτι like a colon or an opening quotation mark: it says "the words that follow are what
was said". The 1611 translators kept ὅτι as the word "that", and set the next word with a capital, as
they did for any speech. So the capital marks the start of the saying, not the subject. It does the
job that quotation marks do now.

How the KJVm handles it (`tools/compose_profile.py`, decisions in [`reviewed.csv`](reviewed.csv)):

- **Saying-"that"** (ὅτι, כִּי, אֲשֶׁר after a comma, colon or semicolon: 47 places): lowercase
  "that", and **no quotation marks**, whether the words after it read as direct or indirect speech.
  *He said, that John the Baptist was risen from the dead* (Mark 6:14); *Verily I say unto thee, that
  this night… thou shalt deny me thrice* (Matthew 26:34). Marks after a "that" would read
  `said, that “…”`, and the red letters still show where Jesus speaks. 21 regions are dropped this way.
- **"That" meaning "what"** ("That thou doest, do quickly", John 13:27; "That which cometh out of the
  man", Mark 7:20): a quote like any other, shipped.

Every word stays either way. Genesis 42:14 opens on "That" too, but holds a quote within the quote; it
waits for the nested ones.

## Words of Jesus

The KJV marks Jesus' words itself (red letters), so `tools/build_quotes.py` fits each quote of His to
them: one unbroken red stretch is one quote, from its first red word to its last. Where the narrator
breaks in ("(he saith to the sick of the palsy,)"), each red stretch gets its own quote.

## Quotes within quotes

A quote with quotes inside it (tier 3) ships as one group, the outer quote and every quote inside it,
when all of them pass their checks and each inner quote opens on a speech verb with a comma or colon
("saying, ‘…", "it is written, ‘…") and ends on punctuation. These carry `nested: true` in
`kjv-quotes.json`. An inner quote ends at the end of its own clause, not the sentence. A quote within a
quote is never shown without its outer quote.

Where the BSB reports a saying that the KJV gives word for word ("for he said, To day shall the house
of Israel restore me…"), the BSB has no inner quote to carry over. The KJV's own tag then places it: a
speech verb inside a quote, with a comma or colon and a capital after it, opens a quote one level
deeper (`tagged: true`). A message ("Thus saith the Lord; …", "tell him, saying, …") runs to the end of
its outer quote or to the next message; any other saying stops at its sentence, or at a colon or
semicolon followed by "and", "that" or "so". Quotes already inside the new one move one level deeper.

A quote that runs over several paragraphs is one region. Some Bibles print a fresh opening mark at
each new paragraph of a long quote, without closing the last; whether to do that is left to the app
that draws the marks. The regions only say where each quote starts and stops, and how deep it is.

## Reviewed regions

[`reviewed.csv`](reviewed.csv) records a decision per region (`book`, `start`, `end`): `ship` puts a
region in the KJVm whatever its tier; `drop` keeps it out; `fix` moves its edges to `fix_start`/`fix_end`
and ships it (a quote within a quote waits for the nested review); `add` puts in a quote the matching
never found (at `level` 2 or 3 when it sits inside another quote). On the other
decisions, a `level` limits the row to the quote at that level, where an outer and inner quote share edges (the BSB's words too far from the KJV's: "Why are you staring at one another?" for "Why
do ye look one upon another?"). The categories are reviewed smallest first,
nested quotes last.
