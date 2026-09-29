# Converts pronunciations from the 3 x 3 keyboard's convention to the keys keyboard's, which the apps and the word list use.
import re
FER = re.compile(r"^(un)?for(get|giv|gav|got|sak|sook|go|bad|bid|bear|bore|swear|swore|sworn|lorn)")
def to_full(prons, word=''):
    """the 3 x 3 file's sounds -> the keys file's sounds (the convention the apps and data/stemsyl-words.tsv use): the
       NORTH/FORCE vowel is written oh+r, and ah+r after w; the unstressed for- of forget/forgive/forsake/forgo... is fer-,
       as the keys file's own list writes it"""
    out = []
    for p in prons:
        q = re.sub(r'(?<=w)Or', 'Ar', p)
        if FER.match(word):
            q = re.sub(r'^(@n)?fOr', lambda m: (m.group(1) or '') + 'f@r', q)
        q = q.replace('Or', 'Gr')
        out.append(q)
    fer = {q for q in out if 'f@r' in q}
    out = [q for q in out if not ('fGr' in q and q.replace('fGr', 'f@r', 1) in fer)]
    res = []
    for q in out:
        if q not in res: res.append(q)
    return res[:3]
