# Paragraphs and poetry (planned)

The KJV prints every verse as its own paragraph. Its ¶ marks are sparse and stop partway through Acts.
It sets poetry as prose too.

This layer will add:
- **paragraph breaks**
- **line and stanza breaks for poetry**, so a refrain like "for his mercy endureth for ever" in Psalm 136
  stands on its own line
- **list layout** for genealogies and other lists

The BSB is the starting point:

| | KJV (Topaz package) | BSB |
|---|---:|---:|
| Paragraph breaks | 2,970 | 13,442 |
| Line breaks | 0 | 24,444 |
| Stanza breaks | 0 | 2,388 |
| List items | 0 | 1,537 |
| Poetry sections | 0 | 1,050 |

Breaks between verses carry over directly. Breaks inside a verse will be matched word by word, the same
way as the quotation marks.
