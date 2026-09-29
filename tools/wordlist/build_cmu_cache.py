# For the checks only: eSpeak NG's IPA for every CMU word, cached to espeak_cmu.json (used by eval_g2p.py and espcorr.py).
import subprocess, json, re
from conv import load_cmu, conv
cmu=load_cmu()
ok=lambda w: re.fullmatch(r"[a-z]+(?:'[a-z]+)*",w) and (len(w)>1 or w in ('a','i'))
words=[w for w in cmu if ok(w)]
p=subprocess.run(['./espk','src/espeak-ng/build'],input='\n'.join(words)+'\n',capture_output=True,text=True)
lines=p.stdout.split('\n')[:len(words)]
json.dump(dict(zip(words,lines)),open('espeak_cmu.json','w'),ensure_ascii=False)
print(len(words),len(lines))
