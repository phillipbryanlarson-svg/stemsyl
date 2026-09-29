# A check, not a step: where derive.py's rules and eSpeak NG disagree on the words the CMU dictionary lacks, which
# sounds they disagree on most often. Needs stage1.json.
import json, collections, difflib
from common import *
from derive import Deriver
st = json.load(open('stage1.json')); G = st['G']
known = cmu_known(); rank, count = fw_rank(); sc = scowl_lists()
existing = [r[0].lstrip('!') for r in load_kb(KEYBOARD_3X3)]
real = set(sc[80][0]) | {w for w in existing if w in set(sc[80][0]) or rank.get(w, 9e9) < 30000}
D = Deriver(known, real, rank, superl=json.load(open('superlatives.json')))
subs = collections.Counter(); ex = collections.defaultdict(list); n=0
for w in st['missing']:
    p = D.pron(w)
    if not p: continue
    e = G[w][0]
    if not e or e in p: continue
    n+=1
    sm = difflib.SequenceMatcher(None, p[0], e, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        key = (p[0][max(0,i1-1):i2+1], e[max(0,j1-1):j2+1])
        subs[key] += 1
        if len(ex[key]) < 3: ex[key].append((w, p[0], e))
print('mismatches', n)
for k, v in subs.most_common(70): print(v, k, ex[k])
