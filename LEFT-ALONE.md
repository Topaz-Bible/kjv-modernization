# What we left alone

**The choices not to modernize, and why.** Every rule here has a point past which it would stop being
*form* and start being *translation*. This page lists where we stopped, with examples, so readers can
see what the KJVm keeps on purpose, and developers reusing these lists can see where the traps lie.

The test throughout: a change may alter how a word is spelled or set, never which word it is or what
it means. When a change would need us to choose a meaning, the KJV's word stays.

## Words

**Words whose meaning has shifted.** Swapping in today's word would mean choosing a translation.

| KJV word | It meant | Example |
|---|---|---|
| let | hinder | "only he who now letteth will let" (2 Thessalonians 2:7). *letteth* becomes *lets* (the ending), but the word stays |
| prevent | go before | "we… shall not prevent them which are asleep" (1 Thessalonians 4:15) |
| conversation | way of life | "Only let your conversation be as it becometh the gospel" (Philippians 1:27) |
| charity | love | "and have not charity" (1 Corinthians 13:1) |
| suffer | allow | "Suffer little children… to come unto me" (Mark 10:14) |
| quick | alive | "to judge the quick and the dead" (2 Timothy 4:1) |
| meat | food | "to you it shall be for meat" (Genesis 1:29) |
| corn | grain | "plenty of corn and wine" (Genesis 27:28) |
| carriage | baggage | "the carriage before them" (Judges 18:21) |

**Old words that are their own words, not old forms of ours.** There's no one modern word to put in their place.

| KJV word | What it is | Why not swap it | Example |
|---|---|---|---|
| wist | past of the old verb *wit*, "to know" | "knew" is close but not the same word: *wit* survives in "to wit" and "unwittingly" | "Wist ye not that I must be about my Father's business?" (Luke 2:49) |
| wot | present of *wit* | same reason | "I wot not who hath done this thing" (Genesis 21:26) |
| trow | think, suppose | | "I trow not" (Luke 17:9) |
| sith | since | | "sith thou hast not hated blood" (Ezekiel 35:6) |
| betwixt, peradventure, howbeit, haply, twain, kine, wroth, asunder, nigh, ere | | still read clearly, and each would need a synonym chosen | "Peradventure there be fifty righteous" (Genesis 18:24) |

**Words still in use, kept as the KJV's voice:** unto, behold, lo, verily, brethren, begat, thereof,
wherefore, wherewith. Changing them would be style, not form.

**Yea and nay.** "Yea" becomes "yes" only where the Greek is ναί, *yes* (23 places). Everywhere else
it means "indeed", "even" or "rather", and stays:
- "yea, the deep things of God" (1 Corinthians 2:10)
- **The Old Testament keeps every yea and nay.** Hebrew has no word for *yes*. "Yea, though I walk through
  the valley of the shadow of death" (Psalm 23:4) is "even though", not "yes".

**Bare.** "Bare" becomes "bore" (she bare a son → she bore a son), except in 14 verses where it means
*naked*: "The Lord hath made bare his holy arm" (Isaiah 52:10).

**Lookalikes.** Words ending in -eth or -est that aren't old verb forms stay as they are:
- nouns: priest, harvest
- superlatives: greatest, eldest
- ordinals: twentieth
- names: Nazareth, Japheth

## Two words that are one today

The KJVm writes *to day* → *today*, *for ever* → *forever* and 15 more ([`words/joins.csv`](words/joins.csv)).
These pairs stay two words, because often they aren't the compound:

| KJV | Why not join it | Example |
|---|---|---|
| every one | often "each one", not "everyone" | "every one that findeth me shall slay me" (Genesis 4:14) |
| any more | often "any longer" | "neither shall all flesh be cut off any more" (Genesis 9:11) |
| in ward | "in custody", not "inward" | "put them in ward" (Genesis 40:3) |
| head stone | the top stone of a building; a *headstone* is now a grave marker | "the head stone of the corner" (Psalm 118:22) |
| high way, up on, near by | don't consistently mean the one-word form | |

None is joined where punctuation, a line break or a quotation mark falls between the two words.

## Names

Old Testament names take their Old Testament spelling in the New (Elias → Elijah) only for the same
person. **1,011 shared names are left alone** because the BSB names someone else there. Example: "Simon,
son of Jonas" (John 21:15) keeps *Jonas*; only the prophet becomes Jonah. Every case is in
[`names/changes.md`](names/changes.md).

**Renames.** Names take the BSB's spelling (Phebe → Phoebe, Zidon → Sidon), but not the BSB's choice of
another name for the same person or place. That is translating: deciding what to call it, not how to
spell it.

| KJV | BSB | Why it stays |
|---|---|---|
| Syria | Aram | the BSB uses the Hebrew name; *Syria* is the Greek and Latin one |
| Ahasuerus | Xerxes | the BSB gives the Greek name for the Persian king |
| Ethiopia | Cush | *Ethiopia* is the Greek translators' word for Cush |
| Diana | Artemis | the Latin goddess for the Greek one |
| Jupiter, Mercurius | Zeus, Hermes | the same |
| Noph | Memphis | the Greek name for the Egyptian city |
| Chittim | Cyprus | the BSB reads the people as their island |
| Shushan | Susa | the Greek name for the Persian city |
| Idumea | Edom | the Greek form of the land against the Hebrew |
| Hiddekel | Tigris | the Hebrew name against the Greek |
| Jewry | Judea | an old English name for the land |
| Babel, Olivet | Babylon, Mount of Olives | the KJV's own name for the place |

Also left alone: where the BSB writes the people for the land or the reverse (*Philistines* →
*Philistia*), a plural for one (*Assyrian* → *Assyrians*), and where it reads another word in the
manuscripts (*Heleb* → *Heled*). Those are listed in `tools/build_names.py`.

## Capitals for God

He, Him, Thou, Thy… are capitalized only where they can be paired one to one with the BSB's, by
order or through the Hebrew or Greek word. **1,823 verses are left lowercase** because a guess could
capitalize the wrong person; 1,417 of them are *he, him, his*, where a verse often has God and a person
both as "he". See [`capitals/review.md`](capitals/review.md).

## Quotation marks

- **A saying introduced by "that" gets no marks.** "And he said, that John the Baptist was risen from the
  dead" (Mark 6:14) is reported speech in the KJV's grammar; `said, that “…”` would read wrong.
- **Psalm tune names.** The BSB quotes them ("To the tune of “Lilies”"); the KJV leaves them untranslated
  ("upon Shoshannim"), so there's nothing to quote.
- **Speech the KJV reports.** "He asked him if he saw ought" (Mark 8:23), "told the disciples that she had
  seen the Lord" (John 20:18). The BSB turns these into quotes; the KJV's words are the narrator's.
- **Where the KJV has no speech.** "Let us go out to the field" (Genesis 4:8) is in the BSB, but the KJV
  says only "Cain talked with Abel his brother".
- **Terms the KJV words differently.** The BSB quotes "Yes" and "No" in James 5:12; the KJV's "let your
  yea be yea" has no quoted term.

## Layout

Every paragraph, poetry line and stanza break of the Cambridge Paragraph Bible stays in the package.
The app's drop-cap view sets a chapter's first verse as running text beside the cap; the margin-number
view draws every break.

## Not touched at all

- word order and grammar, beyond the verb endings
- the italics (the words the translators supplied) in the traditional KJV
- verse divisions
- the underlying text: every change happens on screen as the page is drawn

---

Dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
