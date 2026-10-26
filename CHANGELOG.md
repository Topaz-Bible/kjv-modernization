# Changelog

## Unreleased

- **Quotes of Jesus follow the red letters.** One unbroken stretch of the KJV's words of Jesus is one
  speech and gets one quote, first red word to last: *“Verily I say unto you, Except ye be converted…”*,
  not *Verily I say unto you, “Except…”*. Halves left by the BSB match are joined. Red-letter
  disagreements fall from 82 to 4 (narrator asides inside His words, left for later); 46 more quotes ship.
- **Words now written as one** ([`words/joins.csv`](words/joins.csv)): *to day* → *today*, *for ever*
  → *forever* and 15 more pairs, 912 places, as `join` token edits that close up the space.
  "Jesus Christ the same yesterday, and today, and forever" (Hebrews 13:8).
- **Capital "That" quotes reviewed** ([`quotes/reviewed.csv`](quotes/reviewed.csv)): a saying-"that"
  gets no quotation marks (21 dropped); "That thou doest, do quickly" and Mark 7:20 ship.
- **The KJVm.** The Topaz app now has two editions: the KJV as printed, and the KJVm with every layer
  on (word forms, quotation marks, capitals for God, Old Testament names, the saying-"That"
  lowercased). `tools/compose_profile.py` writes the layers into the app's modernization profile as
  `token_edits` and `quote_regions`. Only quote tiers 1 and 2 ship so far.
- **Quotes:** names and terms the BSB quotes ("God called the light “day”") are carried over word for
  word; a quote stops at "…: and it was so"; a phrase the BSB tags word by word counts once when
  matching. Genesis 1 now reads right.
- **Quote or capital, not both.** A term set in quotation marks is lowercased where the BSB has it
  lowercase: God called the light "day," and the darkness He called "night." Terms the KJV words
  differently from the BSB ("Yet once more" for "Once more") are no longer quoted by halves.
- **Capitals for God after a semicolon** now follow the BSB too: "He makes me lie down in green
  pastures; He leads me." 154 more.
- **Cambridge paragraphs for the traditional KJV** ([breaks/](breaks/)): Scrivener's 1873 paragraphs,
  poetry lines and stanza breaks, from eBible.org's public-domain edition.

## 1.3.0 — 2026-10-26

Word lists built from Topaz KJV package `1.4-primary.20261025.139.1` with the 1.3.0 rules applied. The Topaz app picks the rules up with its next KJV package.

- **Here, there and where** (474 more words change):
  - hither → here, thither → there, whither → where, everywhere
  - after "from" only: from thence → from there, from whence → from where, from hence → from here
  - whithersoever → wherever
  - Left as written: hence, thence and whence on their own (they'd need two words), hitherto and thitherward.
- **One folder per layer.** The word lists moved from `data/` and `docs/` into [`words/`](words/). Draft layers for quotation marks, Old Testament names and pronouns for God sit beside them, unreleased.

## 1.2.0 — 2026-10-24

Built from Topaz KJV package `1.4-primary.20261023.120.3`.

- **84 new spelling and verb-form rules** (462 more words change):
  - Spellings: intreat → entreat, brasen → brazen, stedfast → steadfast, recompence → recompense, bason → basin, jubile → jubilee, subtil → subtle, morter → mortar, inclose → enclose, lothe → loathe, carcase → carcass, plaister → plaster, sycomore → sycamore, and about 40 more.
  - Old verb forms, matching spake → spoke: digged → dug, astonied → astonished, forgat → forgot, trode → trod, forbad → forbade, lien → lain, chode → chided, shaked → shook, strawed → strewed.
- **Removed wist → knew.** "Wist" is the past tense of a different verb (*wit*), so replacing it was a word change, not a spelling update. It now stays, like "wot".
- **Left on purpose:**
  - "begat"
  - British spellings (honour, defence)
  - "neesings" (Job 41:18), an old word for sneezing
- 1,161 word rules and 61 single-verse exceptions; 40,626 words change.

## 1.1.0 — 2026-10-24

Built from Topaz KJV package `1.4-primary.20261023.120.2`.

- graff → graft and graffed → grafted (Romans 11, 6 words). "Graff" is the older spelling of the same word.
- 1,078 word rules and 61 single-verse exceptions; 40,164 words change.

## 1.0.0 — 2026-10-21

First public release, built from Topaz KJV package `1.4-primary.20261021.101.1`.

- 1,076 word rules and 61 single-verse exceptions; 40,158 of the KJV's 931,532 words change.
- Includes 205 -eth/-est forms added in this round (believeth, mightest…).
- yea → yes and nay → no only where the Greek is ναί or οὐ/οὐχί (39 New Testament verses).
- bare → bore everywhere except 14 verses where "bare" means naked.
