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

The Additions to Esther are placed by the chapter and verse numbers the KJV prints (`\cp`, `\vp`).

`tools/build_cambridge_breaks.py --apply` writes these breaks into the KJV package, in place of its
1611 ¶ paragraphs. Headings are untouched.

## The KJVm (planned)

The KJVm will take its paragraphs, poetry lines and lists from the BSB, as it does its quotation marks.
