"""Flag KJVm quote edges that hold words the BSB leaves outside its quotes.

A KJV word and a BSB word in the same verse with the same Strong's number are the same Hebrew or
Greek word. If the words at the very start or end of a KJVm quote match only BSB words outside every
BSB quote, the edge may have taken in the narrator ("I am of Apollos; are ye not carnal?").
Quotes the BSB words wholly as reported speech are skipped. Many flags are only wording differences;
each is read by hand, and fixes go in quotes/reviewed.csv.

Run: python3 tools/check_quote_edges.py  (prints one line per flagged edge)
"""
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_quotes as B  # noqa: E402

MOD = Path(__file__).parent.parent.parent / 'topaz' / 'packages' / 'eng.bible.kjv' / 'eng.bible.kjv.mod.json'


def main():
    regions = json.loads(MOD.read_text())['quote_regions']
    for bk in B.BOOKS:
        bsb = B.read(B.bsb_zip, f'{bk}.json')
        bch, K = B.bsb_chapters(bsb), B.kjv_chapters(bk)
        quoted = collections.defaultdict(set)
        for q in bsb.get('quotes', []):
            start, end = B.parse(q['start']), B.parse(q['end'])
            for c in range(start[0], end[0] + 1):
                quoted[c].update((w.v, w.n) for w in bch.get(c, []) if start <= (c, w.v, w.n) <= end)
        for q in regions.get(bk, []):
            if q['level'] != 1:
                continue
            seq = []  # (outside the BSB's quotes?, chapter, word) for each matched word, in order
            for c in range(int(q['start'][:3]), int(q['end'][:3]) + 1):
                for w in K.get(c, []):
                    if not (q['start'] <= w.key(c) <= q['end']) or not w.S:
                        continue
                    same = [x for x in bch.get(c, []) if x.v == w.v and x.S & w.S]
                    if same:
                        seq.append((all((x.v, x.n) not in quoted[c] for x in same), c, w))
            if not seq or all(o for o, _, _ in seq):
                continue
            for edge, words in (('start', seq), ('end', seq[::-1])):
                run = []
                for outside, c, w in words:
                    if not outside:
                        break
                    run.append(w.t)
                if run:
                    at = q[edge]
                    print(f"{bk} {int(at[:3])}:{int(at[4:7])} {edge}: {' '.join(run if edge == 'start' else run[::-1])}")


if __name__ == '__main__':
    main()
