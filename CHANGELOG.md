# Changelog

## Unreleased

- **Words now written as two.** 60 words the KJV prints as one are split the way they're written
  today, in 166 places: *stumblingblock* → *stumbling block*, *dwellingplace* → *dwelling place*,
  *threshingfloor* → *threshing floor*, the *fellow-* words (*fellowservant* → *fellow servant*), and
  hyphens where today's spelling has one (*twoedged* → *two-edged*, *wellbeloved* → *well-beloved*).
  The list is `words/splits.csv`; `tools/compose_profile.py` writes it into the profile as word rules.
- **Quotes checked verse by verse against the NIV and ESV.** Of about 26,000 verses in chapters with
  quotes, 24,600 agree with both; 93 verses where the two agreed with each other and not with the KJVm
  were read by hand. Fixed about 30 places: quotes that opened a verse late or closed a verse early
  (Genesis 37:6, Exodus 18:17, Deuteronomy 18:17, 2 Kings 3:15, Numbers 27:17, Lamentations 3:43–47),
  quotes that ran on past the speaker (John 3:31–36 is the evangelist, not John the Baptist; Amos 4:13
  and 5:6–15; Isaiah 8:9–10; Jeremiah 17:9 and 17:11; the Leviticus summaries "This is the law…"),
  Isaiah 40:1–2 no longer quoted (the voice's words open at "Prepare ye the way"), and four sayings
  added (Luke 5:26, Psalm 132:7, Isaiah 66:10–11, Revelation 18:20). Kept: places where the NIV
  rewords direct speech as reported (Matthew 2:23), omits the KJV's words (Luke 20:23), or wraps a long
  oracle in one outer quote (Jeremiah 32, 51).
- **Pronouns for God are lowercase again.** The capitals layer is switched off: most modern Bibles
  don't capitalize them, and it followed the BSB into interpretation (who "he" is). The three "That"
  lowerings set by hand move to `quotes/that-by-hand.csv`.
- **The last 200 quotes the matching couldn't place, read by hand.** Most were already right: the BSB
  splits a saying around "he said" where the KJV keeps it whole. 27 sayings the KJV has but wasn't
  quoting are now quoted ("Is he well?" Genesis 29:6, "Here am I; send me." Isaiah 6:8, "Who art
  thou?" 2 Samuel 1:8), and Jacob's answer in Genesis 31:31 now opens at "Because", with his thought
  inside it. Left out: sayings the KJV doesn't have (Genesis 4:8), tune names in Psalm titles, "yea"
  and "nay" used as words, and a lament that would need a third level of marks (Jeremiah 34:5).
- **Jeremiah 29:10–14 quoted**, opening after a lowercased "that", with "saith the Lord" inside as in
  29:8–9.
- **Psalm lines set in a step.** Scrivener sets every Psalm line at one level; each now takes its level
  from the BSB line its Hebrew words fall in, so the second line of a pair can sit a step in. The
  line positions stay Scrivener's. 5,347 of 5,362 Psalm lines matched; the other 15 go by their place
  in the verse.
- **Quote edges checked against the BSB.** A new check, `tools/check_quote_edges.py`, finds quotes whose
  first or last words the BSB leaves outside its quotes. Fixed: "“I am of Apollos;” are ye not carnal?"
  (1 Corinthians 3:4), Jesus's words in Matthew 26:50 no longer run into "Then came they", Mark 4:35
  opens at "Let us pass over", "“Rabbi, which is to say, being interpreted, Master,) where dwellest thou?”"
  (John 1:38) is one quote, ""For," said Hushai, "thou knowest…"" (2 Samuel 17:8). The writer's own "For",
  "And therefore", "Even as" now stay outside the Scripture he quotes ("For “the earth is the Lord's…”",
  1 Corinthians 10:26). News the KJV reports with "that" loses its marks (1 Samuel 13:4, 1 Kings 2:29,
  Jude 1:18).
- **Sayings after "that".** Where the KJV writes "said, That…", the "that" is lowercase and the quote
  opens after it, wherever that still reads as what was said: "Others said, that “it is Elijah.”" (Mark
  6:15), Luke 7:16, 2 Samuel 1:4, Daniel 6:13, Galatians 1:23, Psalm 118:2–4. Where the KJV has shifted
  the words into reported speech ("that he was worthy for whom he should do this", Luke 7:4), they stay
  unmarked.
- **Deuteronomy 1 and Isaiah 14 follow the NIV.** No quote opens over Moses's whole speech or the whole
  taunt song; only the sayings inside them are marked ("Dread not" now opens at 1:29).
- **Quotes checked against modern Bibles.** Every place the KJV says "saying," with no quote after it,
  and every quote that opens with no speech verb near it, was read beside the NIV, ESV, NASB and CSB.
  60 places gain or change quotes: "it was told the Gazites, saying, “Samson is come hither.”" (Judges
  16:2), Reuben's whole answer with his old warning inside it (Genesis 42:22), the prophet's "“Thus saith
  the Lord…" now inside the quote where the word came "saying," (Jeremiah 26:2), and four parties with
  four sayings in 1 Corinthians 1:12 ("“I am of Paul;” and “I of Apollos;” and…"). Seven come out: the
  writer's own words (Romans 2:6, Hebrews 12:29, Revelation 13:10) and a psalm handed to Asaph (1
  Chronicles 16:8–36, whose sayings keep their marks). See [unchanged.md](unchanged.md).
- **Quotes in the Apocrypha, a first few.** 30 of the plainest: one speech tag, the speech filling the
  rest of its verse, the next verse narrative again ("But Tobias said, “No; but let me go to my
  father.”", Tobit 10:9).
- **Red letters without quotes.** Where the words of Jesus stood outside any quote, the quote now
  follows the red letters: Luke 6:5 opens after the lowered "that" ("he said unto them, that “the Son
  of man is Lord also of the sabbath.”"), Luke 9:55–56 (words the BSB's Greek text lacks), Revelation
  1:11 ("“I am Alpha and Omega, the first and the last:” and, “What thou seest…”"). Acts 1:4 turns
  direct at "which", as the Greek does: "wait for the promise of the Father, “which,” saith he, “ye
  have heard of me.”"
- **More capitals for God.** 1,146 pronouns in verses the pairing had left for review: where
  the KJV and BSB count their pronouns differently, they now pair through the Hebrew or Greek word
  ("walked in My law, nor in My statutes", Jeremiah 44:10). A pronoun the BSB adds of its own ("His
  covenant" for "the covenant") no longer holds a verse back. A verse is settled whole or left whole;
  1,064 remain, most of them *he*.
- **Capitals for God by hand.** [`capitals/by-hand.csv`](capitals/by-hand.csv) settles verses the
  pairing leaves for review: "Rejoice, ye Gentiles, with His people" (Romans 15:10).
- **Tablets, not tables.** The tables of stone become tablets, as do the other tables written on: "the
  tablet of your heart" (Proverbs 3:3), "a writing tablet" (Luke 1:63), "tablets of brass" (1 Maccabees).
  46 places, chosen by the Hebrew and Greek word (לוּחַ, πλάξ, πινακίδιον); every table to eat at stays.
- **Names in their modern spelling.** Every name, in both Testaments, takes the BSB's spelling where it
  is only a spelling: 864 words, 380 names. Phebe → Phoebe, Cesar → Caesar, Tyrus → Tyre, Zidon → Sidon,
  Timotheus → Timothy, Pharez → Perez, Maachah → Maacah. Where the KJV spells one name two ways and the
  BSB evens them out, so does the KJVm (Nebuchadrezzar → Nebuchadnezzar). Rebekah stays, and Beelzebub, for familiarity. The BSB's other
  names for the same place or person (Syria → Aram, Ahasuerus → Xerxes, Diana → Artemis) are
  translating, and stay out: see [unchanged.md](unchanged.md). The survey that found them is
  [`names/spelling-survey.md`](names/spelling-survey.md).
- **Red letters stop at reported speech.** Acts 1:4 was red from "wait for the promise of the Father";
  the KJV never colours reported speech red elsewhere (Mark 8:30, Luke 9:21), and the Greek turns
  direct at "which". The red now starts there too.
- **The last unplaced quotes read by hand.** 152 quotes that failed a check and had never shipped,
  with the quotes inside them; nothing the matching found is left unreviewed. 72 are left unmarked,
  because the KJV has no speech there: it reports what was said ("he asked him if he saw ought", "told
  the disciples that she had seen the Lord") or the words are the narrator's or prophet's own ("Peniel:
  for I have seen God face to face"). 80 ship, most with edges set by hand: the saying stops where the
  speaker does ("thou shalt say, ‘I will eat flesh,’ because thy soul longeth…"), and a tag in the
  middle splits it ("for ‘the God of my father,’ said he, ‘was mine help…’", "for ‘who,’ say they, ‘doth
  hear?’"). Where the Lord's words go on after "saith the Lord", the words before the tag are quoted
  too ("‘Shall I not visit for these things?’ saith the Lord: ‘and shall not my soul be avenged…’").
  Stephen's speech now runs to its end (Acts 7:2–53), with the eleven sayings inside it. Never marked
  before: Michal's answer (1 Samuel 19:17), "What way went he?" (1 Kings 13:12), "Go, search the land:"
  (Judges 18:2). Today, forever and the other joined words are now joined where a quote opens before
  the pair or closes after it (84 more); only a mark between the two words keeps them apart.
- **Inner quotes from the KJV's own speech tags.** 163 quotes held a speech verb with no quote after it
  ("he abideth at Jerusalem: for he said, To day shall the house of Israel restore me…"). Where the BSB had turned the KJV's direct speech into
  reported speech, there was nothing to carry over; now a tag inside a quote ("saying,", "said unto
  him,", "say,") followed by a capital opens a quote one level deeper. A message ("Thus saith the Lord;
  …", "Go, tell him, saying, …") runs to the end of the speech or the next message; any other saying
  stops at its sentence, or at a colon or semicolon followed by "and", "that" or "so". Quotes already
  inside the new one move one level deeper. Example: "Go into the city to such a man, and say unto him,
  ‘The Master saith, “My time is at hand…”’". Kept fixed by hand: messages that are really two
  (Ezekiel 36:1–5, Jeremiah 21:8–14), sayings that end mid-sentence ("The Lord is God of the hills, but he
  is not God of the valleys,” therefore will I deliver…"), and the eastern tribes' answer (Joshua 22),
  now with its quotes three deep. Four levels deep is now possible (Exodus 3:17, Jeremiah 21:13).
- **Quotes within quotes, the held groups.** The last 53 groups the rules couldn't settle were read by
  hand. Where the outer and inner quote opened on the same word, the inner one now opens after its own
  tag ("It is written, ‘My house shall be called the house of prayer;’ but ye have made it a den of
  thieves."), or the outer one opens back at its speaker ("Ye are idle, ye are idle: therefore ye say,
  ‘Let us go…’"). A narrator's tag inside a quote splits it ("“All this,” said David, “the Lord made me
  understand…”", "“…north,” saith the Lord: “for I have spread you abroad…”"). Three deep, by hand:
  Absalom's message (2 Samuel 14:32) and Zedekiah's question (Jeremiah 32:3–5). Deborah's song ships
  with its inner calls. A `reviewed.csv` row with a `level` now applies only to the quote at that
  level, since an outer and inner quote can share edges.
- **Quotes within quotes, third batch.** 119 more speeches ship with their inner quotes (226 single, 5
  double), among them the Sermon on the Mount, Elihu, and the Lord's sayings in Jeremiah and Ezekiel.
  A speech that opened on its inner quote's first word now opens with its speaker ("And he said unto the
  woman, “Yea, hath God said, ‘Ye shall not eat of every tree of the garden?’”"). The rest were read by
  hand: an inner quote stops at its own saying ("If they say thus unto us, ‘Tarry until we come to
  you;’ then…", "to the mountains, ‘Fall on us;’ and to the hills, ‘Cover us.’"), and a speaker's own
  words are not quoted inside his speech ("Therefore speak I to them in parables", "He that believeth on
  me, as the scripture hath said"). A quote is never its own inner quote (Hebrews 4:3 had ““…””). An
  `add` row replaces a generated quote with the same edges. Deborah's song and Jeremiah 3:12 wait for
  the three-level pass.
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
