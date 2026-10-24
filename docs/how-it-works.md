# How the rules work

## The idea in one paragraph

The KJV text is never edited. The rules are a display layer: as each word is drawn, the reader looks it up in the rule list and, if a rule applies, shows the replacement instead. Turn the option off and the original word is shown. Because the replacement is per word (per *token*), punctuation, italics, verse numbers and every link from a word to its Greek or Hebrew stay exactly where they were.

## How a word is matched

1. **Unit.** One token: a single word as the KJV prints it, without its surrounding punctuation. `"thee,"` is the token `thee` with `,` after it; only `thee` is replaced.
2. **Order.**
   1. Single-verse overrides (`location_overrides`) are checked first.
   2. Then rules in file order.
   3. The first match wins.
3. **Case.** Matching ignores case. The replacement copies the original's casing:

   | Original | Replacement |
   |---|---|
   | thee | you |
   | Thee | You |
   | THEE | YOU |

   Mixed casing falls back to the replacement as written.
4. **Conditions (`when`).** Optional. All listed conditions must hold:

   | Condition | Meaning |
   |---|---|
   | `previous_text_in` / `next_text_in` | The neighbouring token is one of these words (case-insensitive) |
   | `after_punctuation_present` | Punctuation follows the token (used for `thine` → `yours` at the end of a phrase) |
   | `book_id_in` | Only in these books (USFM ids) |
   | `flags_include` | The token carries these package flags |
   | `strongs_in` | The token's Strong's number is one of these (supported by the engine, but no rule in this set uses it) |

5. **Overrides.**
   - An override names one exact token: book, chapter, verse, and the token's position in the verse (1-based).
   - It applies only if that token's text still matches `match.text`, so a stale override does nothing rather than replacing the wrong word.

A minimal implementation:

```js
function modernize(tokens, place, profile) {
  return tokens.map((token, i) => {
    const override = profile.overrides.get(`${place.book}:${place.chapter}:${place.verse}:${token.n}`);
    if (override && override.match === token.t.toLowerCase()) return keepCase(token.t, override.replace);
    for (const rule of profile.rules.get(token.t.toLowerCase()) ?? []) {
      if (conditionsHold(rule.when, tokens, i, place)) return keepCase(token.t, rule.replace);
    }
    return token.t;
  });
}
```

## How the rules were made

- **Pronouns and helping verbs.** Written by hand: thou → you, hath → has, shalt → shall, and so on.
- **Verb endings.** Every token ending in *-eth* or *-est* was checked against an English dictionary. A hand pass then removed words that only look like verb forms:
  - nouns (priest, harvest)
  - superlatives (greatest, eldest)
  - ordinals (twentieth)
  - names (Nazareth, Japheth)

  The surviving forms map like this:

  | KJV form | Becomes | Example |
  |---|---|---|
  | *-eth* | the modern *-s* form | believeth → believes, carrieth → carries |
  | *-est* (the form used with "thou") | the bare verb | knowest → know |
  | *-est*, past tense | the past tense | camest → came |

- **Ambiguous words.** Words that are a verb in one place and something else in another get a condition. For example, *meanest* becomes *mean* only next to "thou"; "the meanest" stays.
- **Yea and nay.** These are decided by the Greek word underneath, verse by verse:

  | KJV | Becomes | Only where the Greek is |
  |---|---|---|
  | yea | yes | ναί (G3483) |
  | nay | no | οὐ (G3756), οὐχί (G3780) |

  Every other *yea* and *nay* keeps its sense of "indeed", "even" or "rather", and the Old Testament is left alone. Each of these changes is stored as an override, generated from the Greek.

## Scope

- **Changed:** forms of words.
- **Not changed:** words whose meaning has shifted ("let" = hinder, "prevent" = go before, "conversation" = conduct). Replacing those is translation, which this layer deliberately does not attempt.

## Do you need Greek or Hebrew to use this?

**No.** Every rule matches English text alone. Two sets of changes were *decided* by looking at the Greek and Hebrew, but both ship as plain English instructions:

- **Yea/nay.** "Yea" becomes "yes" in 23 places and "nay" becomes "no" in 16, all in the New Testament. Each is a location override: "in Matthew 5:37, word 6, change *yea* to *yes*." The Greek was used to *choose* those places. An English-only reader just applies the list.
- **Bare/bore.** "Bare" becomes "bore" everywhere except 14 listed verses where it means "naked" ("made bare his holy arm").

For the simplest possible integration, skip the rule engine and use `data/every-change.csv`. For each row, find the verse, find the word by its position, check that it is the `kjv` word, and show `modernized` instead.

A word's position is its number among the verse's words, counting from 1, with punctuation not counted as a word. If your text splits words differently, use the `kjv` column to find the right one.

## Caveats for reuse

- **Tokenization.** Overrides are keyed to Topaz's tokenization of the KJV, meaning token positions within a verse. Rules keyed only on word text work on any KJV text that splits words the same way. Overrides need the same tokenization or a remapping.
- **Regenerating.** `tools/build_lists.py` rebuilds every list from the KJV package and reports any rule that never fires (there are none in 1.4-primary.20261023.120.2).
- **Base text.** The KJV is in the public domain outside the United Kingdom. Inside the UK it is under Crown rights, administered by the Queen's (King's) Printer under letters patent.
- **Licence.** These files are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Use them for anything, with no attribution required, though a link back to topaz.bible is appreciated.
