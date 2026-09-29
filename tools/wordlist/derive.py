# Derive Stemsyl pronunciations (in the 3 x 3 file's convention, NORTH/FORCE as aw + r) for words the CMU dictionary lacks, from words it has:
# inflections, stress-neutral suffixes, transparent prefixes and compounds of common words.
# Every rule here was checked by hiding CMU words and rebuilding them (validate_derive.py).
import re
CONS = set('pbtdkgfvTDszSZhCJmnNlrwy')
SIB = set('szSZCJ')
VOICELESS = set('ptkfTsSC')

def pl_s(p):                      # -s / -es
    last = p[-1]
    if last in SIB: return p + 'iz'
    if last in 'ptkfT': return p + 's'
    return p + 'z'
def pl_ed(p):                     # -ed
    last = p[-1]
    if last in 'td': return p + 'id'
    if last in VOICELESS: return p + 't'
    return p + 'd'
def unsyl(p, b):                  # tickle -> tickl- before a vowel suffix
    return p[:-2] + 'l' if b.endswith('le') and p.endswith('@l') else p

def base_candidates(word, sfx):
    """(base spelling, how) pairs: the base as it may have been spelled before `sfx` was added."""
    if not word.endswith(sfx) or len(word) - len(sfx) < 2: return []
    stem = word[:-len(sfx)]
    out = [(stem, '')]
    if sfx[0] in 'aeiouy':
        out.append((stem + 'e', 'e'))                             # abase -> abasing
        if len(stem) >= 3 and stem[-1] == stem[-2] and stem[-1] not in 'aeiouwxyhs':
            out.append((stem[:-1], 'dbl'))                         # abhor -> abhorring
        if sfx.startswith('ing') and stem.endswith('y'):
            out.append((stem[:-1] + 'ie', 'ie'))                   # die -> dying
        if len(stem) >= 2 and stem.endswith('ck') and sfx[0] in 'eiy':
            out.append((stem[:-1], 'ck'))                          # panic -> panicking
    if stem.endswith('i') and not sfx.startswith('i'):
        out.append((stem[:-1] + 'y', 'y'))                         # happy -> happier, happiness
    if sfx == 'ly' and len(stem) >= 2:
        out.append((stem + 'le', 'le'))                            # simple -> simply, unshakable -> unshakably
    return out

def ly(p, b, h):
    if h == 'le': return p[:-2] + 'lI' if p.endswith('@l') else None       # simple -> simply
    if h == 'y': return p[:-1] + '@lI' if p.endswith('I') else None        # happy -> happily
    if b.endswith('le') and p.endswith('@l'): return p[:-2] + 'lI'         # able -> ably
    if b.endswith('ical') and p.endswith('@l'): return p[:-2] + 'lI'       # musical -> musically
    if b.endswith('l') and p.endswith('l'): return p + 'I'                 # full -> fully, habitual -> habitually
    return p + 'lI'

# suffix -> rule(base_pron, base_spelling, how)
RULES = {
    's':      lambda p,b,h: pl_s(p) if not b.endswith(('s','x','z','sh','ch')) else None,
    'es':     lambda p,b,h: pl_s(p) if b.endswith(('s','x','z','sh','ch','o')) or h=='y' else None,
    'ed':     lambda p,b,h: pl_ed(p),
    'd':      lambda p,b,h: pl_ed(p) if b.endswith('e') else None,
    'ing':    lambda p,b,h: unsyl(p,b) + 'iN',
    'er':     lambda p,b,h: unsyl(p,b) + '@r',
    'ers':    lambda p,b,h: unsyl(p,b) + '@rz',
    'est':    lambda p,b,h: unsyl(p,b) + '@st',
    'ly':     ly,
    'ally':   lambda p,b,h: p + 'lI' if b.endswith('ic') else None,
    'ness':   lambda p,b,h: p + 'n@s',
    'nesses': lambda p,b,h: p + 'n@siz',
    'less':   lambda p,b,h: p + 'l@s',
    'lessly': lambda p,b,h: p + 'l@slI',
    'lessness':lambda p,b,h: p + 'l@sn@s',
    'ment':   lambda p,b,h: p + 'm@nt',
    'ments':  lambda p,b,h: p + 'm@nts',
    'ful':    lambda p,b,h: (p[:-1] + 'if@l') if h=='y' else p + 'f@l',
    'fully':  lambda p,b,h: (p[:-1] + 'if@lI') if h=='y' else p + 'f@lI',
    'fulness':lambda p,b,h: p + 'f@ln@s',
    'able':   lambda p,b,h: p + '@b@l',
    'ably':   lambda p,b,h: p + '@blI',
    'ism':    lambda p,b,h: p + 'iz@m',
    'isms':   lambda p,b,h: p + 'iz@mz',
    'ship':   lambda p,b,h: p + 'Sip',
    'ships':  lambda p,b,h: p + 'Sips',
    'hood':   lambda p,b,h: p + 'hud',
    'hoods':  lambda p,b,h: p + 'hudz',
    'dom':    lambda p,b,h: p + 'd@m',
    'like':   lambda p,b,h: p + 'lYk',
    'wise':   lambda p,b,h: p + 'wYz',
    'ation':  lambda p,b,h: p[:-2] + 'ES@n' if p.endswith('Et') and h=='e' else None,
    'ations': lambda p,b,h: p[:-2] + 'ES@nz' if p.endswith('Et') and h=='e' else None,
    'ator':   lambda p,b,h: p[:-2] + 'Et@r' if p.endswith('Et') and h=='e' else None,
    'ators':  lambda p,b,h: p[:-2] + 'Et@rz' if p.endswith('Et') and h=='e' else None,
    'ization':lambda p,b,h: p[:-2] + '@zES@n' if p.endswith('Yz') and h=='e' else None,
    'izations':lambda p,b,h: p[:-2] + '@zES@nz' if p.endswith('Yz') and h=='e' else None,
    'ingly':  lambda p,b,h: unsyl(p,b) + 'iNlI',
    'edly':   lambda p,b,h: p + 'idlI' if p[-1] in 'td' else p + '@dlI',
}
SPECIAL_FIRST = {'edly'}                     # -edly: the syllabic -ed, rather than -ly on the -ed form

# transparent prefixes only (validated >= 80% on CMU words): prefix -> sounds
PREFIXES = {'un':'@n','non':'nAn','over':'Gv@r','under':'@nd@r','out':'Wt','sub':'s@b','super':'sUp@r','inter':'int@r',
            'counter':'kWnt@r','mid':'mid','up':'@p','down':'dWn','back':'bak','anti':'antI','multi':'m@ltI','dis':'dis',
            'mis':'mis','ultra':'@ltr@','mega':'meg@','extra':'ekstr@','self':'self','well':'wel','semi':'semI','fore':'fOr',
            're':'rI','pre':'prI','de':'dI','co':'kG'}
# prefixes that reduce their vowel in old words (reference, decay, coupon): only for new formations on a common base
LOOSE_PREFIXES = {'re','pre','de','co','fore','dis','mis','semi'}
# second parts that reduce their vowel in compounds (craftsman, England)
REDUCING = {'man':'m@n','men':'m@n','woman':'wum@n','women':'wim@n','land':'l@nd','ton':'t@n','ham':'@m','ford':'f@rd',
            'mouth':'m@T','borough':'b@rG','shire':'S@r'}

# strings that are words but act as endings or beginnings inside longer words (protect+ion, tact+ician)
NOT_SECOND = {'ion','ions','ian','ate','ates','age','ages','ant','ants','ent','ents','ity','ive','ous','ism','ist','ise','ize','ish',
              'ure','ery','ory','ance','ence','able','ible','ship','ness','less','ful','ling','lings','ward','wards','ten','tens','tic','tics',
              'nation','ration','ration','sion','tion','ter','ters','ted','ting','tial','ual','ally','ily','ology','ologist','one','ones',
              'era','eras','ere','ore','ores','ate','ant','ally','ear','ears','ion','ions','our','ours','ice','ices','ace','aces','ide','ides',
              'ism','isms','end','ends','and','ands','ever','hen','hens','ore','row','rows','ran','red','reds','sin','sins','sis','tan','tans',
              'ant','ants','cess','lion','lions','man','men'}
NOT_FIRST = {'con','com','pro','per','pre','dis','mis','sub','sur','ant','ante','inter','para','peri','epi','hyper','hypo','tele',
             'mono','poly','auto','bio','geo','neo','tri','uni','ex','de','re','co'}

class Deriver:
    def __init__(self, known, real, rank, g2p=None, superl=(), names=()):
        """known: word -> [prons], trusted (CMU).  real: words that may serve as a base (real English words).
           rank: word -> int (lower = commoner).  g2p: word -> [prons] for vocabulary words nothing else covers."""
        self.known, self.real, self.rank, self.g2p = known, real, rank, (g2p or {})
        self.memo, self.method = {}, {}
        self.superl = set(superl); self.names = set(names)
    def r(self, w): return self.rank.get(w, 10**7)
    def pron(self, w, depth=3, exclude=None):
        if w == exclude: return None
        if w in self.known: return self.known[w]
        if exclude is None and w in self.memo: return self.memo[w]
        if depth <= 0: return None
        res = self.derive(w, depth, exclude)
        if res is None and exclude is None and w in self.g2p: res = (self.g2p[w], 'g2p')
        if exclude is None:
            self.memo[w] = res[0] if res else None
            if res: self.method[w] = res[1]
        return res[0] if res else None
    def derive(self, w, depth=3, exclude=None):
        if w in self.names: return self.compound(w, exclude)
        # 1. suffixes: every analysis whose base is a real word with a pronunciation; best = trusted, common, long base
        cands = []
        for sfx, rule in RULES.items():
            if sfx == 'est' and w not in self.superl: continue
            for b, how in base_candidates(w, sfx):
                if b == exclude or len(b) < 2 or b not in self.real: continue
                if b in self.known: bp, trusted = self.known[b], 0
                else:
                    bp, trusted = self.pron(b, depth - 1, exclude), 1
                if not bp: continue
                out = []
                for p in bp[:2]:
                    q = rule(p, b, how)
                    if q and q not in out: out.append(q)
                if out:
                    special = 0 if sfx in SPECIAL_FIRST else 1
                    cands.append(((special, trusted, min(self.r(b), 10**6) // 20000, -len(b)), out, 'suffix:' + sfx))
        if cands:
            cands.sort(key=lambda c: c[0])
            return (cands[0][1], cands[0][2])
        # 2. transparent prefixes
        for pre in sorted(PREFIXES, key=len, reverse=True):
            if not w.startswith(pre): continue
            b = w[len(pre):]
            if len(b) < 3 or b == exclude or b not in self.real: continue
            if pre in LOOSE_PREFIXES and (len(b) < 4 or self.r(b) > 60000 or b not in self.known): continue
            bp = self.known.get(b) or self.pron(b, depth - 1, exclude)
            if bp: return ([PREFIXES[pre] + p for p in bp[:2]], 'prefix:' + pre)
        return self.compound(w, exclude)
    def compound(self, w, exclude=None):
        # 3. compounds of two common words
        cands = []
        for i in range(3, len(w) - 2):
            a, b = w[:i], w[i:]
            if a == exclude or b == exclude: continue
            if a in self.known and a in self.real and self.r(a) < 40000 and a not in NOT_FIRST:
                if b in REDUCING: pb = REDUCING[b]
                elif b in self.known and b in self.real and self.r(b) < 40000 and b not in NOT_SECOND: pb = self.known[b][0]
                else: continue
                cands.append((max(self.r(a), self.r(b) if b in self.rank else 0), a, pb))
        if cands:
            cands.sort()
            _, a, pb = cands[0]
            return ([self.known[a][0] + pb], 'compound')
        return None
