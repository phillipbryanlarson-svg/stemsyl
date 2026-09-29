# A check, not a step: hides 40,000 CMU words from derive.py's rules and rebuilds them, reporting how often each rule
# gets the CMU pronunciation right. Run from tools/wordlist with the sources in src/.
import random, collections
from common import *
from derive import Deriver
known = cmu_known(); rank, count = fw_rank(); sc = scowl_lists()
real = set(sc[80][0])
import json; D = Deriver(known, real, rank, superl=json.load(open("superlatives.json")))
test = [w for w in known if rank.get(w, 9e9) < 150000 and w in real]
random.seed(3); test = random.sample(test, min(40000, len(test)))
stat = collections.defaultdict(lambda: [0, 0]); bad = collections.defaultdict(list)
for w in test:
    r = D.derive(w, 3, exclude=w)
    if not r: continue
    prons, how = r
    good = prons[0] in known[w]
    stat[how][0] += good; stat[how][1] += 1
    if not good and len(bad[how]) < 8: bad[how].append((w, prons[0], known[w][:2]))
tot = [0, 0]
for m, (g, n) in sorted(stat.items(), key=lambda x: -x[1][1]):
    tot[0] += g; tot[1] += n
    if n >= 8: print(f'{m:16s} {g}/{n} = {g/n:.1%}   e.g. {bad[m][:4]}')
print('overall', tot, round(tot[0] / tot[1], 3), 'coverage', round(tot[1] / len(test), 3))
