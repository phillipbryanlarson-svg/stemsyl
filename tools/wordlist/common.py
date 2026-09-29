# Shared by the word-list steps: the vocabulary's sources (run these scripts from tools/wordlist, with the downloaded
# sources in tools/wordlist/src; see README.md) and the 30,000 words the keyboards already carried.
import re, json, os
from conv import load_cmu, conv, load_kb
HERE = os.path.dirname(os.path.abspath(__file__))
KEYBOARD_3X3 = os.path.join(HERE, '..', 'sources', 'keyboard-3x3.html')     # its words: the 3 x 3 file's convention (NORTH = aw+r)
KEYBOARD_KEYS = os.path.join(HERE, '..', 'sources', 'keyboard-keys.html')   # its words: the keys file's convention (NORTH = oh+r)
OKW = re.compile(r"[a-z]+(?:'[a-z]+)*")
def ok(w): return bool(OKW.fullmatch(w)) and (len(w) > 1 or w in ('a', 'i'))
def cmu_known(cmu=None):
    cmu = cmu or load_cmu(); known = {}
    for w, prs in cmu.items():
        if not ok(w): continue
        s = []
        for ph in prs:
            x = conv(ph)
            if x not in s: s.append(x)
        known[w] = s
    return known
def fw_rank():
    rank = {}; count = {}
    for i, line in enumerate(open('src/fw/content/2018/en/en_full.txt', encoding='utf-8')):
        p = line.rstrip('\n').split(' ')
        if len(p) == 2 and p[0] not in rank: rank[p[0]] = i; count[p[0]] = int(p[1])
    return rank, count
def scowl_lists():
    """size -> (lowercase words, capitalized names lowercased) for the American list, variant level 1, no possessives"""
    out = {}
    for sz in (60, 70, 80):
        low, cap = [], []
        for w in open(f'src/scowl/wl{sz}.txt', encoding='utf-8'):
            w = w.rstrip('\n')
            if w.endswith("'s") or w.endswith("'"): continue
            if OKW.fullmatch(w): low.append(w)
            elif re.fullmatch(r"[A-Z][a-zA-Z]*(?:'[a-zA-Z]+)*", w) and not re.fullmatch(r"[A-Z]+", w) and len(w) > 1:
                cap.append(w.lower())
        out[sz] = (low, cap)
    return out
