# A check, not a step: for the words the CMU dictionary lacks, how often eSpeak NG and the g2p model agree with the
# pronunciations derive.py builds, by kind of rule. Needs stage1.json.
import json, collections, random
from common import *
from derive import Deriver
st = json.load(open('stage1.json')); G = st['G']; tier = st['tier']
known = cmu_known(); rank, count = fw_rank(); sc = scowl_lists()
existing = [r[0].lstrip('!') for r in load_kb(KEYBOARD_3X3)]
real = set(sc[80][0]) | {w for w in existing if w in set(sc[80][0]) or rank.get(w, 9e9) < 30000}
D = Deriver(known, real, rank, superl=json.load(open('superlatives.json')))
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
res = collections.defaultdict(lambda: collections.Counter())
for w in st['missing']:
    p = D.pron(w)
    if not p: continue
    m = D.method.get(w, '')
    kind = 'inflection' if m.split(':')[-1] in ('s','es','ed','d','ing','er','ers','est') else m.split(':')[0]
    e, n = G[w]
    c = res[kind]; c['n'] += 1
    c['esp'] += e in p; c['neu'] += n in p; c['either'] += (e in p or n in p); c['agree'] += (e == n); c['agree_ok'] += (e == n and e in p)
    c['esp_near'] += (e is not None and lev(e, p[0]) <= 1); c['neu_near'] += (n is not None and lev(n, p[0]) <= 1)
for k, c in res.items():
    N = c['n']
    print(f"{k:11s} n={N:6d} eSpeak {c['esp']/N:.1%} (±1 {c['esp_near']/N:.1%})  neural {c['neu']/N:.1%} (±1 {c['neu_near']/N:.1%})  either {c['either']/N:.1%}  agree {c['agree']/N:.1%} → right {c['agree_ok']/max(1,c['agree']):.1%}")
