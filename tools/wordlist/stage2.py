# Final pronunciations (the 3 x 3 file's convention; make_tsv.py converts them) and ranking for every new word; cache to stage2.json
import json, collections, re, time
from common import *
from derive import Deriver
t0 = time.time()
st = json.load(open('stage1.json')); G = st['G']; tier = st['tier']; vocab = st['vocab']
known = cmu_known(); rank, count = fw_rank(); sc = scowl_lists()
existing = [r[0].lstrip('!') for r in load_kb(KEYBOARD_3X3)]
low80 = set(sc[80][0])
real = low80 | {w for w in existing if w in low80 or rank.get(w, 9e9) < 30000}
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
# predictor fallback: eSpeak first, the neural guess as a second reading when it is close
g2p = {}
for w, (e, n) in G.items():
    out = []
    if e: out.append(e)
    if n and n not in out and (not e or lev(e, n) <= 1): out.append(n)
    if out: g2p[w] = out
names = set(sc[80][1]) - low80
D = Deriver(known, real, rank, g2p=g2p, superl=json.load(open('superlatives.json')), names=names)
final = {}; method = collections.Counter(); how = {}
for w in vocab:
    if w in known:
        final[w] = known[w][:3]; method['cmu'] += 1; how[w] = 'cmu'; continue
    p = D.pron(w)
    if not p: method['none'] += 1; continue
    m = D.method.get(w, 'g2p')
    out = list(p[:2])
    # a rule built on parts: add eSpeak's reading as an alternative when it differs by one sound
    e = G.get(w, [None])[0]
    if m != 'g2p' and e and e not in out and lev(e, out[0]) <= 1: out.append(e)
    final[w] = out[:3]; k = m.split(':')[0]; method[k] += 1; how[w] = k
print(method, round(time.time() - t0), flush=True)
# ranking: subtitle frequency first; then words with no count by list size (60 < 70 < 80 < CMU-only), alphabetically
def key(w):
    c = count.get(w, 0)
    return (0, -c, w) if c > 0 else (1, tier.get(w, 99), w)
order = sorted(final, key=key)
json.dump({'order': order, 'final': final, 'how': how}, open('stage2.json', 'w'))
print('saved', len(order), round(time.time() - t0), flush=True)
