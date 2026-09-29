# Build the vocabulary and the eSpeak / neural predictions for every word CMU lacks; cache to stage1.json
import json, subprocess, time
from common import *
from g2pmodel import predict_batch
from ipa2ss import espeak_to_ss
from conv import conv
t0=time.time()
known = cmu_known(); rank, count = fw_rank(); sc = scowl_lists()
existing = [r[0].lstrip('!') for r in load_kb(KEYBOARD_3X3)]; EX = set(existing)
low80, cap80 = sc[80]
S60 = set(sc[60][0]) | set(sc[60][1]); S70 = set(sc[70][0]) | set(sc[70][1]); S80 = set(low80) | set(cap80)
vocab = []; seen = set(EX)
def add(w):
    if w not in seen and ok(w) and not w.endswith("'s"): seen.add(w); vocab.append(w)
for w in known: add(w)
for w in low80: add(w)
for w in cap80: add(w)
missing = [w for w in vocab if w not in known]
print('vocab', len(vocab), 'missing', len(missing), round(time.time()-t0), flush=True)
esp = subprocess.run(['./espk', 'src/espeak-ng/build'], input='\n'.join(w.replace("'", '') for w in missing) + '\n', capture_output=True, text=True).stdout.split('\n')
print('espeak done', round(time.time()-t0), flush=True)
neu = predict_batch([w.replace("'", '') for w in missing])
print('neural done', round(time.time()-t0), flush=True)
G = {}
for w, e, n in zip(missing, esp, neu):
    try: x = espeak_to_ss(e, w)
    except KeyError: x = None
    G[w] = [x, conv(n) if n else None]
tier = {w: (60 if w in S60 else 70 if w in S70 else 80 if w in S80 else 99) for w in vocab}
json.dump({'vocab': vocab, 'missing': missing, 'G': G, 'tier': tier}, open('stage1.json', 'w'))
print('saved', round(time.time()-t0), flush=True)
