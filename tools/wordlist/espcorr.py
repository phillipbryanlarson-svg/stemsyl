# An experiment, not a step: learn, from CMU words, how CMU writes the sounds eSpeak gives, in context, and apply it to
# eSpeak output for other words. It was measured and left out of the list. Needs espeak_cmu.json from build_cmu_cache.py.
import json, random, collections, difflib, re
from ipa2ss import ph2ss, espeak_to_ss
VOW = set('@aAYWiIuUeEOGB')
def units(ipa, spelling):
    """eSpeak IPA -> list of (stemsyl letters, stressed?) per phoneme token, flaps resolved as espeak_to_ss does"""
    toks = [x for x in re.split(r'[_ ]', ipa) if x]
    out = []
    for t in toks:
        st = ('ˈ' in t) or ('ˌ' in t)
        out.append([ph2ss(t), st])
    ss = espeak_to_ss(ipa, spelling)
    # re-derive flap choices from the final string: walk and copy letters
    flat = ''.join(u[0] for u in out)
    if '?' in flat:
        k = 0; res = []
        for u in out:
            s = ''
            for ch in u[0]:
                s += ss[k] if ch == '?' else ch; k += 1
            res.append([s, u[1]])
        out = res
    return out
def letters_with_stress(us):
    L, S = [], []
    for s, st in us:
        for ch in s: L.append(ch); S.append(st if ch in VOW else None)
    return L, S
def ctx_keys(L, S, i):
    p = L[i-1] if i > 0 else '^'; n = L[i+1] if i + 1 < len(L) else '$'
    n2 = L[i+2] if i + 2 < len(L) else '$'
    st = 'S' if S[i] else 'u'
    c = L[i]
    return [(c, st, p, n, n2), (c, st, p, n), (c, st, n, n2), (c, st, n), (c, st, p), (c, st)]
class Corrector:
    def __init__(self): self.tab = collections.defaultdict(collections.Counter)
    def train(self, pairs):
        for ipa, sp, cmu in pairs:
            try: us = units(ipa, sp)
            except KeyError: continue
            L, S = letters_with_stress(us)
            e = ''.join(L)
            sm = difflib.SequenceMatcher(None, e, cmu, autojunk=False)
            amap = {}
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == 'equal':
                    for k in range(i2 - i1): amap[i1 + k] = cmu[j1 + k]
                elif op == 'replace' and i2 - i1 == j2 - j1:
                    for k in range(i2 - i1): amap[i1 + k] = cmu[j1 + k]
                elif op == 'replace':
                    for k in range(i1, i2): amap[k] = None     # unaligned: skip
                elif op == 'delete':
                    for k in range(i1, i2): amap[k] = ''
            for i, ch in enumerate(L):
                if ch not in VOW or S[i]: continue          # only unstressed vowels are corrected
                tgt = amap.get(i)
                if tgt is None: continue
                for key in ctx_keys(L, S, i): self.tab[key][tgt] += 1
    def fix(self, ipa, sp, minn=8, minp=0.55):
        us = units(ipa, sp); L, S = letters_with_stress(us); out = []
        for i, ch in enumerate(L):
            if ch in VOW and not S[i]:
                for key in ctx_keys(L, S, i):
                    c = self.tab.get(key)
                    if c and sum(c.values()) >= minn:
                        tgt, n = c.most_common(1)[0]
                        if n / sum(c.values()) >= minp: ch = tgt
                        break
            out.append(ch)
        s = ''.join(out)
        return s.replace('@r@r', '@r')
if __name__ == '__main__':
    from common import cmu_known
    known = cmu_known(); esp = json.load(open('espeak_cmu.json'))
    rank = {}
    for i, line in enumerate(open('src/fw/content/2018/en/en_full.txt', encoding='utf-8')):
        p = line.split(' ')
        if len(p) == 2 and p[0] not in rank: rank[p[0]] = i
    words = [w for w in esp if "'" not in w]
    random.seed(7); random.shuffle(words)
    test = words[:15000]; train = words[15000:]
    C = Corrector(); C.train([(esp[w], w, known[w][0]) for w in train])
    for name, sel in [('all', test), ('common (rank<100k)', [w for w in test if rank.get(w, 9e9) < 100000]), ('rare/names', [w for w in test if rank.get(w, 9e9) >= 100000])]:
        b = a = 0
        for w in sel:
            try:
                raw = espeak_to_ss(esp[w], w); cor = C.fix(esp[w], w)
            except KeyError: continue
            b += raw in known[w]; a += cor in known[w]
        print(f'{name:22s} n={len(sel)}  raw eSpeak {b/len(sel):.1%}  corrected {a/len(sel):.1%}')
    import pickle; pickle.dump(dict(C.tab), open('espcorr.pkl', 'wb'))
