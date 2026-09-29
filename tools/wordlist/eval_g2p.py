# A check, not a step: how often eSpeak NG and the g2p model give a CMU word's pronunciation, by how common the word is.
# Needs espeak_cmu.json from build_cmu_cache.py.
import json, re, random, collections
from conv import load_cmu, conv
from ipa2ss import espeak_to_ss
from g2pmodel import predict_batch
cmu=load_cmu()
esp=json.load(open('espeak_cmu.json'))
fw={}
for i,line in enumerate(open('src/fw/content/2018/en/en_full.txt',encoding='utf-8')):
    p=line.split(' ')
    if len(p)==2 and p[0] not in fw: fw[p[0]]=i
words=list(esp)
def cmuset(w):
    s=[]
    for ph in cmu[w]:
        x=conv(ph)
        if x not in s: s.append(x)
    return s
random.seed(1)
bands={'rank<30k':[w for w in words if fw.get(w,9e9)<32000],'30k-100k':[w for w in words if 32000<=fw.get(w,9e9)<200000],
       'rank>200k':[w for w in words if 200000<=fw.get(w,9e9)<9e9],'no count':[w for w in words if w not in fw]}
sample={k:random.sample(v,min(3000,len(v))) for k,v in bands.items()}
allw=[w for v in sample.values() for w in v if "'" not in w]
neu=dict(zip(allw,[conv(p) if p else '' for p in predict_batch([w.replace("'","") for w in allw])]))
for k,v in sample.items():
    v=[w for w in v if "'" not in w]
    e_ok=0; n_ok=0; both=0; agree=0; agree_ok=0; either=0
    for w in v:
        c=cmuset(w)
        try: e=espeak_to_ss(esp[w],w)
        except KeyError as ex: e='?'
        n=neu[w]
        e_ok+= e in c; n_ok+= n in c; either+= (e in c or n in c)
        if e==n: agree+=1; agree_ok+= e in c
    N=len(v)
    print(f'{k:10s} n={N}  eSpeak {e_ok/N:.1%}  neural {n_ok/N:.1%}  either {either/N:.1%}  agree {agree/N:.1%} (correct when agree {agree_ok/max(1,agree):.1%})')
