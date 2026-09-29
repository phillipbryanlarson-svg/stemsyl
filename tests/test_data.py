# The word list: data/stemsyl-words.tsv is well formed, and it is exactly the list inside both keyboards.
import base64, collections, re
from helpers import *
from kbdata import read_tsv, read_text, ipa, COLUMNS

C = Checks('word list')
PATH = os.path.join(ROOT, 'data', 'stemsyl-words.tsv')
rows = read_tsv(PATH)                                  # checks every row's shape, rank, source and sound letters
C.ok('it holds over 250,000 words', len(rows) > 250000, len(rows))
OKW = re.compile(r"[a-z]+(?:'[a-z]+)*")
C.eq('every spelling is lowercase letters, with apostrophes only inside', [r[0] for r in rows if not OKW.fullmatch(r[0])][:5], [])
dup = [w for w, n in collections.Counter(r[0] for r in rows).items() if n > 1]
C.eq('no spelling appears twice', dup[:5], [])
C.eq('every word has one to three different pronunciations', [r[0] for r in rows if not 1 <= len(r[1]) <= 3 or len(set(r[1])) != len(r[1])][:5], [])
with open(PATH, encoding='utf-8') as f:
    f.readline()
    bad = [l.split('\t')[1] for l in f if ' '.join(ipa(p) for p in l.split('\t')[2].split(' ')) != l.split('\t')[3]]
C.eq('the ipa column is the sounds column in IPA', bad[:5], [])
n = collections.Counter(r[2] for r in rows)
C.ok('words from every source', all(n[s] > 1000 for s in ('cmu', 'suffix', 'prefix', 'compound', 'g2p')), dict(n))
top = [r for r in rows if "'" not in r[0]][:100]          # (contractions are not flagged: the speller's list has no it's, and writes I'm)
C.ok('the commonest words are everyday dictionary words', sum(r[3] for r in top) >= 98, [r[0] for r in top if not r[3]])
C.ok('some words are flagged offensive, none of the commonest hundred', 0 < sum(r[4] for r in rows) < 1000 and not any(r[4] for r in rows[:100]))
for w, want in [('the', ['D@', 'DI']), ('cat', ['kat']), ('north', ['nGrT']), ('war', ['wAr']), ('forget', ['f@rget']), ('hot', ['hAt'])]:
    got = next((r[1] for r in rows if r[0] == w), None)
    C.eq('%s is %s' % (w, ' or '.join(want)), got, want)

# the same list inside both keyboards: the words, their pronunciations, the offensive and the dictionary flags
want = [(w, ps, off) for w, ps, src, dic, off in rows]
for name in ('stemsyl-keyboard.html', 'stemsyl-keyboard-watch.html'):
    h = open(os.path.join(DOCS, name), encoding='utf-8').read()
    got = read_text(h)
    C.ok('%s carries exactly the data file\'s words' % name, got == want,
         'first difference at row %s' % next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), min(len(got), len(want))))
    bits = base64.b64decode(re.search(r'id="ssDict">([^<]*)<', h).group(1))
    flags = [bool((bits[i >> 3] >> (i & 7)) & 1) for i in range(len(rows))]
    C.ok('%s flags the same dictionary words' % name, flags == [r[3] for r in rows])
C.report()
