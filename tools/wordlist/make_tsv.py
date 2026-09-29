# The last word-list step: writes data/stemsyl-words.tsv, the word list every app is built from.
#   rows 1-30,000: the keyboards' own list (the CMU words they started with, commonest first), as the keys file writes them
#   then every other word of the CMU dictionary and of the English Speller Database's American list at size 80, with the
#   pronunciations stage2.py found (CMU, built by rule from CMU words, or predicted), in the keys file's convention, ordered:
#   words counted in the subtitle frequencies by their count, the rest alphabetically, the commoner speller lists first.
# Each word is flagged when it is an everyday dictionary word (the speller's size-60 list: only these count as homophones
# of a word written without the name mark) and when it is offensive (kept out of the longer-word suggestions).
# Run from tools/wordlist after stage1.py and stage2.py.
import json, re, sys, os, collections
from common import *
sys.path.insert(0, os.path.join(HERE, '..'))
from fullconv import to_full
from kbdata import write_tsv
OUT = os.path.join(HERE, '..', '..', 'data', 'stemsyl-words.tsv')

s2 = json.load(open('stage2.json')); st = json.load(open('stage1.json'))
order, final = s2['order'], s2['final']; tier = st['tier']
rank, count = fw_rank()

# ---------- which new words stay out of the completions ----------
# The lists' own 77 blocked words stay as they are. New words are blocked when they are profanity, slurs or explicit terms,
# or built on one (motherfucking, shitheads) — without catching ordinary words that happen to contain the letters
# (snigger, niggardly, mishit, Matsushita, spicier, crapes, pricking, retarding, cocker).
def ex_rows(fn): return load_kb(fn)
PROPAGATE = {'fuck','shit','cunt','nigger','nigga','faggot','motherfucker','bitch','whore','slut','asshole','arsehole','dickhead',
             'bullshit','twat','wanker','jackass','dumbass','goddamn','bastard','blowjob','handjob','dyke','gook','honky','kike',
             'wetback','jigaboo','porn','titty','pussy','milf','nympho','tranny','paki','darkie','pikey','shite','poontang',
             'bukkake','gangbang','anilingus','cunnilingus','fellatio','bunghole','butthole','clit','sodomize','chickenshit',
             'horseshit','dipshit','apeshit','fistfuck','mindfuck','boob','horny','negro','cum','sluttish','whoremonger'}
STRONG_RE = re.compile(r"fuck|(?<!s)cunt|(?<!s)nigger|nigga(?!rd)|faggot|motherf|bitch|whore|slut(?!sk|zk)|asshole|dickhead|cocksuck"
                       r"|jizz|blowjob|handjob|bullshit|dumbass|jackass|(?<![a-z])wank"
                       r"|(?:^|bull|chicken|horse|ape|rat|dip|en|bat|dog|gob|holy|jack)shit(?!tah|tim|ake|a$|z)")
ALLOW = {'retarding','retarder','retarders','cockers','cocker','dicker','dickers','pricking','pricker','prickers','prickings','crapes',
         'craped','craping','spicing','spicier','spiciest','chinking','chinked','boobies','cumings','bustier','shrimping','snowballing',
         'scissoring','pegging','swinger','swingers','undressing','twinkies','wankel','wanke','wanko','cummer','cummers'}
def blocked(w, vocab=None):
    if w in ALLOW: return False
    if STRONG_RE.search(w): return True
    for s in ['', 's', 'es', 'ed', 'd', 'ing', 'er', 'ers', 'y', 'ies', 'ier', 'iest', 'ied', 'ily', 'iness', 'ings', 'head', 'heads',
              'hole', 'holes', 'face', 'faces', 'ish', 'ness']:
        if s and not w.endswith(s): continue
        b = w[:len(w) - len(s)] if s else w
        if not b: continue
        if s.startswith('i') and s != 'ing' and s != 'ings' and s != 'ish':
            cands = [b + 'y']                                      # titties <- titty, hornier <- horny
        elif s == 'es':
            cands = [b] if b.endswith(('s','x','z','sh','ch')) else []
        else:
            cands = [b]
            if s in ('ing','ed','er','ers','ings') and len(b) >= 3 and b[-1] == b[-2]: cands.append(b[:-1])   # cumming <- cum
        if any(c in PROPAGATE for c in cands): return True
    return False
# ---------- order: common new words by subtitle count; the rest alphabetically, commoner lists first ----------
def band(w):
    c = count.get(w, 0)
    if c >= 100: return 0
    if c >= 30: return 1
    if c >= 10: return 2
    if c >= 3: return 3
    if c >= 1: return 4
    return {60: 5, 70: 6, 80: 7}.get(tier.get(w, 99), 8)
bands = collections.defaultdict(list)
for w in order: bands[band(w)].append(w)
ORDERED = []
for b in sorted(bands):
    ws = bands[b]
    ORDERED += (sorted(ws, key=lambda w: (-count.get(w, 0), w)) if b <= 1 else sorted(ws))



# ---------- the rows ----------
head = load_kb(KEYBOARD_KEYS)
assert len(head) == 30000
OKW = re.compile(r"[a-z]+(?:'[a-z]+)*")
dict60 = {w.rstrip('\n') for w in open('src/scowl/wl60.txt', encoding='utf-8')
          if OKW.fullmatch(w.rstrip('\n')) and not w.rstrip('\n').endswith("'s")}
how = s2['how']
rows = []
for r in head:
    w = r[0].lstrip('!')
    rows.append((w, r[1:], 'cmu', w in dict60, r[0].startswith('!')))
for w in ORDERED:
    rows.append((w, to_full(final[w], w)[:3], how[w], w in dict60, blocked(w)))
write_tsv(OUT, rows)
c = collections.Counter(r[2] for r in rows)
print(len(rows), 'words ->', os.path.normpath(OUT), dict(c), '| dictionary:', sum(r[3] for r in rows), '| offensive:', sum(r[4] for r in rows))
