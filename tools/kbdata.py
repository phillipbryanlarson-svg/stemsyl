# The word list: the data file every app is built from (data/stemsyl-words.tsv), and reading the list back out of a
# built keyboard. A word is a row (spelling, [pronunciations], source, dictionary word?, offensive?).
import json

# the sound letters as IPA: the apps' own table (a vowel letter by where it starts and ends, a consonant one to one)
IPA = {'p': 'p', 'b': 'b', 't': 't', 'd': 'd', 'k': 'k', 'g': 'ɡ', 'f': 'f', 'v': 'v', 'T': 'θ', 'D': 'ð', 's': 's', 'z': 'z',
       'S': 'ʃ', 'Z': 'ʒ', 'h': 'h', 'C': 'tʃ', 'J': 'dʒ', 'm': 'm', 'n': 'n', 'N': 'ŋ', 'l': 'l', 'r': 'r', 'w': 'w', 'y': 'j',
       '@': 'ə', 'a': 'æ', 'A': 'ɑ', 'Y': 'aɪ', 'W': 'aʊ', 'i': 'ɪ', 'I': 'i', 'u': 'ʊ', 'U': 'u', 'e': 'ɛ', 'E': 'eɪ',
       'O': 'ɔ', 'G': 'oʊ', 'B': 'ɔɪ'}
def ipa(pron):
    return ''.join(IPA[c] for c in pron)

# ---------- the data file ----------
COLUMNS = ['rank', 'word', 'sounds', 'ipa', 'source', 'dictionary', 'offensive']
SOURCES = ('cmu', 'suffix', 'prefix', 'compound', 'g2p')

def write_tsv(path, rows):
    """rows: (spelling, [pronunciations], source, dictionary, offensive), commonest first"""
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(COLUMNS) + '\n')
        for i, (w, ps, src, dic, off) in enumerate(rows, 1):
            assert w and not any(c in w for c in '\t\n '), repr(w)
            assert src in SOURCES and ps and all(ps) and all(c in IPA for p in ps for c in p), (w, ps, src)
            f.write('%d\t%s\t%s\t%s\t%s\t%d\t%d\n' % (i, w, ' '.join(ps), ' '.join(ipa(p) for p in ps), src, dic, off))

def read_tsv(path):
    """the rows of data/stemsyl-words.tsv, in order: (spelling, [pronunciations], source, dictionary, offensive)"""
    rows = []
    with open(path, encoding='utf-8') as f:
        head = f.readline().rstrip('\n').split('\t')
        assert head == COLUMNS, 'unexpected columns: %r' % head
        for n, line in enumerate(f, 1):
            r = line.rstrip('\n').split('\t')
            assert len(r) == len(COLUMNS) and r[0] == str(n), 'row %d is malformed: %r' % (n, line[:80])
            ps = r[2].split(' ')
            assert r[4] in SOURCES and all(c in IPA for p in ps for c in p), 'row %d: %r' % (n, line[:80])
            rows.append((r[1], ps, r[4], r[5] == '1', r[6] == '1'))
    return rows

# ---------- a built keyboard ----------
KC = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def read(path):
    """the word list inside a built keyboard: [(spelling, [pronunciations], offensive)] in file order"""
    return read_text(open(path, encoding='utf-8').read())

def read_text(h):
    line = [l for l in h.split('\n') if l.startswith('var SS_WORDS=')][0]
    rows = []
    for l in json.loads(line[len('var SS_WORDS='):].rstrip().rstrip(';')).split('\n'):
        f = l.split('\t')
        if len(f) < 2: continue
        w = f[0]; bl = w.startswith('!'); rows.append((w.lstrip('!'), f[1:], bl))
    a = h.index('<script type="text/plain" id="ssMore">\n') + len('<script type="text/plain" id="ssMore">\n'); b = h.index('\n</script>', a)
    pw = pp = ''
    for L in h[a:b].split('\n'):
        bl = L[0] == '!'; L = L[1:] if bl else L
        f = L.split('\t'); w = pw[:KC.index(f[0][0])] + f[0][1:]; p0 = pp[:KC.index(f[1][0])] + f[1][1:]
        rows.append((w, [p0] + [p0[:KC.index(x[0])] + x[1:] for x in f[2:]], bl)); pw, pp = w, p0
    return rows
