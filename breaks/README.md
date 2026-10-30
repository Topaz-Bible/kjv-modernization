# Paragraphs and poetry

The KJV as first printed sets every verse as its own paragraph. Its ¶ marks are sparse and stop partway
through Acts, and it sets poetry as prose.

## The traditional KJV: Cambridge Paragraph Bible breaks

[`cambridge/breaks.json`](cambridge/breaks.json) holds the paragraphs, poetry lines and stanza breaks of
**The Cambridge Paragraph Bible**, edited by F. H. A. Scrivener (Cambridge, 1873). The source is eBible.org's
public-domain USFM edition, [KJV Cambridge Paragraph Bible](https://ebible.org/find/details.php?id=engkjvcpb)
(`engkjvcpb`), kept in `keyway-data/sources/kjv-cambridge-paragraph-ebible`.

| | Count |
|---|---:|
| Paragraph breaks (besides chapter starts) | 2,344 |
| Poetry lines | 22,746 |
| Stanza breaks | 657 |
| Poetry sections | 503 |

Each break sits before a word of the Topaz KJV package (`position` = the word's number in its verse),
in the package's own marker format. Scrivener's text differs from the 1769 KJV in a few words ("You
are not ashamed" for "ye are not ashamed"); a break goes right after the last word the two share, so
it still opens the same line.

Scrivener sets every Psalm line at one level. In the Psalms each line takes its level from the BSB:
level 2 (the second line of a pair, set a step in) or level 1, by the BSB line its Hebrew words
(Strong's numbers) fall in. The first word that points into a single BSB line decides; a line with no
such word goes by a vote of its words, and the 15 lines with no matched word at all go by their place
in the verse (first line 1, later lines 2). The breaks themselves stay where Scrivener put them, so
where he joins two of the BSB's lines into one, the joined line takes the level of the first.

The Additions to Esther are placed by the chapter and verse numbers the KJV prints (`\cp`, `\vp`).

`tools/build_cambridge_breaks.py --apply` writes these breaks into the KJV package, in place of its
1611 ¶ paragraphs. Headings are untouched.

## The KJVo (planned)

The KJVo will take its paragraphs, poetry lines and lists from the BSB, as it does its quotation marks.
