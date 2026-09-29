# CMU Pronouncing Dictionary (ARPABET) -> Stemsyl sound letters, and reading a keyboard's own word list.
import re, json, collections
CMAP={'P':'p','B':'b','T':'t','D':'d','K':'k','G':'g','F':'f','V':'v','TH':'T','DH':'D','S':'s','Z':'z','SH':'S','ZH':'Z',
      'HH':'h','CH':'C','JH':'J','M':'m','N':'n','NG':'N','L':'l','R':'r','W':'w','Y':'y'}
VMAP={'AA':'A','AE':'a','AH':'@','AO':'O','AW':'W','AY':'Y','EH':'e','ER':'@r','EY':'E','IH':'i','IY':'I','OW':'G','OY':'B','UH':'u','UW':'U'}
def load_cmu(path='src/cmudict/cmudict.dict'):
    words=collections.OrderedDict()
    for line in open(path,encoding='utf-8'):
        line=line.split('#')[0].strip()
        if not line: continue
        w,*ph=line.split()
        base=re.sub(r'\(\d+\)$','',w)
        words.setdefault(base,[]).append(ph)
    return words
def conv(ph):
    out=''
    for p in ph:
        b=re.sub(r'\d','',p)
        out+= CMAP[b] if b in CMAP else VMAP[b]
    return out
def load_kb(fn):
    """the word list a keyboard file carries on its SS_WORDS line: [[spelling (a leading ! keeps it out of the
       longer-word suggestions), pronunciation, ...], ...]"""
    text=open(fn,encoding='utf-8').read()
    line=next(l for l in text.split('\n') if l.startswith('var SS_WORDS='))
    s=json.loads(line[len('var SS_WORDS='):].rstrip().rstrip(';'))
    return [l.split('\t') for l in s.split('\n') if l]
