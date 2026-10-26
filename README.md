# KJV Modernization

**The King James Version, made easier to read without changing what it says, as open, reusable data.**

The King James text itself is never edited. Everything here is a layer laid over it when it is shown,
and each layer can be switched on or off on its own. With every layer off, the reader sees the KJV
word for word. The line we hold throughout is **form, not translation**: spelling, punctuation and
layout may change; the words and what they mean may not.

This is the same kind of work the KJV's own printers did between 1611 and 1769, when they standardized its
spelling and punctuation. Each step changed how the text looks, not what it says.

## The layers

| Layer | What it does | Status |
|---|---|---|
| [Word forms](words/) | thou → you, believeth → believes, spake → spoke, shew → show | **Released** (1.2.0) |
| [Quotation marks](quotes/) | Adds “ ” and ‘ ’ around speech, carried over from the BSB | Draft, in review |
| [Names](names/) | Old Testament names in the New Testament take the KJV's Old Testament spelling: Elias → Elijah, Esaias → Isaiah | Draft |
| [Pronouns for God](capitals/) | He, Him, His, Thou, Thy… capitalized where they refer to God, following the BSB | Draft |
| [Headings](headings/) | Section headings written for the KJV | Planned |
| [Paragraphs and poetry](breaks/) | The Cambridge Paragraph Bible's paragraphs, poetry lines and stanzas | **In the Topaz KJV** |

**[What we left alone](LEFT-ALONE.md)**: the changes we chose not to make, and why. *wist* isn't
*knew*, *every one* isn't always *everyone*, and Old Testament *yea* isn't *yes*.

[`profile.json`](profile.json) lists the layers for software: each one's folder, data file and whether
it starts switched on.

Each layer's folder explains how it was made, which calls were hard, and lists every change it makes,
so anyone can check the judgement involved. Every list is pinned to word positions in a Topaz KJV
package, with the word itself kept alongside as a check.

`tools/` rebuilds every list from the Topaz app's package files (Python 3, no dependencies).

## Versions

Each release names the Topaz KJV package it was built from. See [CHANGELOG.md](CHANGELOG.md).

## Corrections

Found something we missed, or a change that's wrong? [Open an issue](https://github.com/Topaz-Bible/kjv-modernization/issues) with the verse and the word.

## Licence

The rules and lists are dedicated to the public domain under [CC0 1.0](LICENSE). Use them in your own Bible app or project for anything, with no permission or attribution needed, though a link back to [topaz.bible](https://topaz.bible) is appreciated.

The King James Version text is in the public domain outside the United Kingdom. In the UK it is under Crown rights. This repository contains rules and word lists, not the Bible text.
