# Changelog

## Unreleased

- **Quotes within quotes, second batch.** 56 more speeches ship with their inner quotes (154 single, 2
  double): messengers' words ("go, tell thy lord, ‘Behold, Elijah is here.’"), "Thus saith the Lord"
  inside a prophet's speech, the parables of the trees (Judges 9) and the virgins and talents
  (Matthew 25). An inner quote that opened inside its own sentence now opens with it ("a voice saying
  unto me, ‘Saul, Saul, why persecutest thou me?’"), but never back past its outer quote's opening or
  onto the speaker's own "O Lord God,". By hand: the curses at Ebal (Deuteronomy 27) are each their own
  quote, as is each "Amen."; Psalm 75:4 and Jeremiah 3:4 end the inner saying at its clause; Isaiah
  45:24 ("Surely, shall one say, in the Lord…") stays unmarked. `reviewed.csv` gains a `level` column for
  added quotes within quotes.
- **Quotes within quotes, first batch.** 473 speeches that quote someone else ("as it is written, ‘He
  gave them bread from heaven to eat.’", "say unto Ahab, ‘Prepare thy chariot…’") ship with their
  inner quotes: 706 single-quoted, 8 double again inside those. A group ships whole only when every
  quote in it passes its checks and each inner quote opens on a speech verb ("saying, ‘…") and ends on
  punctuation. An inner quote stops at the end of its clause ("yet they say, ‘Sword and famine shall not
  be in this land;’ By sword and famine…"). A quote within a quote never ships without its outer one: 9
  lone ‘…’ are gone until their speech is marked.
- **Held-back starts and ends read by hand.** 77 quotes that end on a colon, semicolon or comma where the
  narrator or writer takes over ("“It is manna:” for they wist not what it was", "If a man say, “I love
  God,” and hateth his brother") ship, as do 20 whose speech tag stands far back or isn't there ("Then
  said Pilate to the chief priests and to the people, “I find no fault in this man.”"). 13 more open or
  end a few words off and are fixed. Left unmarked on purpose: reported "that" sayings, oracles with no
  speaker named, and quotes within quotes (the nested review comes last).
- **Where a quote opens, round two.** The speech tag may stand a few words back ("And Abram said to the
  king of Sodom, I have lift up mine hand") or end the verse before ("saying, | And I, behold, I
  establish my covenant"). A quote that opened on a name or "O" inside its own sentence ("What doest
  thou here, “Elijah?") opens with the sentence. Two quotes touching in one verse are one (“How went the
  matter? I pray thee, tell me.”). 41 more quotes ship; hand fixes in `quotes/reviewed.csv` (Genesis
  19:7–8 one speech, Isaiah 30:10 two sayings; the Book of Jasher citation in Joshua 10:13 is the
  narrator's).
- **Overlapping quotes joined.** Where the BSB splits a speech around its tag (“Please come near,” said
  Joseph, “I am Joseph…”) and the KJV puts the tag first, the two pieces overlapped; they are now one
  quote. A quote within a quote that ran past its outer quote stretches it. A verse that opens on the
  narrator's tag ("Then said they unto him, Tell us…") opens the quote after it. 24 questions whose
  speech goes on in small letters ("whence camest thou? and whither wilt thou go?") run on, by hand.
- **Where a quote ends.** Quotes the BSB match left ending mid-sentence run on to the full stop
  ("“Master, thou hast well said.”"), or end before the narrator's next tag ("“…till Shelah my son be
  grown:” for he said, “Lest…”"). A quote may end on a comma before "saith the Lord" when the tag ends
  the sentence or the quote takes up again after it. Not where the BSB's speech runs on into a later
  verse. 40 more quotes ship, each read. Six verses where a quote opened on the narrator ("Therefore
  said they unto him, How…") fixed by hand.
- **Where a quote opens.** A quote taken up again after its speaker is named opens on a small letter and
  is right ("“Vanity of vanities,” saith the Preacher, “vanity of vanities;”"); so is Scripture quoted
  after "it is written," or "what saith the scripture?". A quote that opened on a tag ("lest, “said he,
  …") opens after it. One that opened a few words into a speech joins the quote just before it, or
  moves back to the speech tag ("“Behold now, I am old, I know not the day of my death:"). Hand fixes in
  `quotes/reviewed.csv`; "say, that his mercy endureth for ever" (Psalm 118) is a saying-"that", unmarked.
- **The 200 quotes the BSB match couldn't place:** 162 are halves of a quote the KJV already has (the BSB
  splits “Here,” she said, “…”); 13 are Psalm tune names the KJV leaves untranslated ("upon
  Shoshannim"); 44 short replies are found by the KJV's own speech tag ("And he said, “Here am I.”"),
  each read, 6 fixed or dropped by hand; 18 more added by hand (`add` in `quotes/reviewed.csv`). Left
  without marks: Genesis 4:8 (the KJV has no words of Cain), and BSB term quotes the KJV words
  differently ("let your yea be yea").
- **Quotes of Jesus follow the red letters.** One unbroken stretch of the KJV's words of Jesus is one
  speech and gets one quote, first red word to last: *“Verily I say unto you, Except ye be converted…”*,
  not *Verily I say unto you, “Except…”*. Halves left by the BSB match are joined. Where the
  narrator breaks in, the quote splits around the aside: “…to forgive sins,” (he saith to the sick of
  the palsy,) “I say unto thee, Arise…”. Red-letter disagreements fall from 82 to 0; 50 more quotes ship.
  An audit of the red letters themselves found no narrator words tagged red and no missed words.
- **Breaks stay in the package; the drop cap sets verse 1 flat.** Every Cambridge break is kept
  (margin-number mode draws them); the app's drop-cap view leaves out the line breaks of a chapter's
  first verse, which wraps beside the cap.
- **Remembered words of Jesus are red**, as Acts 11:16 and 20:35 already were: "Before the cock crow,
  thou shalt deny me thrice" (Matthew 26:75, Mark 14:72, Luke 22:61), "Thy son liveth" (John 4:53),
  "If I will that he tarry till I come, what is that to thee?" (John 21:23). 45 words, in the KJV package.
- **Narrator taken out of quotes:** “And they said, So do,” → And they said, “So do,”. Not where the
  speaker tells of words said to them ("and I said, ‘I will never break my covenant…’"). Two copies of
  one quote opening on the same word keep the longer.
- **Quoted terms fixed by hand** (7): “O wheel.”, “King of righteousness,” … “King of peace;”, and more;
  `quotes/reviewed.csv` gains `fix` with new edges.
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
