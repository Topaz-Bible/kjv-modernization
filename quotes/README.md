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
   word, so it anchors the quote. Common words ("the", "and", "him") are used only when a quote has
   no anchor.
2. **Find the opening** by walking back to where the speech begins. The KJV marks that with a capital
   letter after a comma or colon ("said unto him, Lovest thou me?"). The walk never crosses a word the
   BSB leaves outside its quotes, such as "he answered".
3. **Find the end** by running on to the end of the sentence or verse. The run never goes into the
   next quote or past a speech verb like "said" or "saith".
4. **Rejoin split speeches.** The BSB splits some speeches with a narrator tag that the KJV doesn't
   have ("“You will not surely die,” the serpent told her. “For God knows…”"). Those pieces become one
   quote again.
5. **Check the words of Jesus.** In the Gospels the KJV marks Jesus's words itself, so a quote of Jesus
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

## Capital "That" (open question)

In 67 places the KJV writes "That" with a capital after a comma: "But I say unto you, That Elias is come
already" (Matthew 17:12). Two thirds of them (45 of 67) translate the Greek ὅτι.

Greek can use ὅτι like a colon or an opening quotation mark: it says "the words that follow are what
was said". The 1611 translators kept ὅτι as the word "that", and set the next word with a capital, as
they did for any speech. So the capital marks the start of the saying, not the subject. It does the
job that quotation marks do now.

Planned handling, verse by verse:

- **Indirect speech** ("saying, That it was needful to circumcise them", Acts 15:5): lowercase
  "that", no marks.
- **Direct speech** ("Of whom it was said, That in Isaac shall thy seed be called", Hebrews 11:18):
  lowercase "that", and open the quote after it: *it was said, that "in Isaac shall thy seed be
  called."*

Either way every word stays. These regions are flagged `opens with a capital "That"` in tier 4.
