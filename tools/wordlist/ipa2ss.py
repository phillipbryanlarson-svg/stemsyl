# eSpeak NG en-us IPA ('_'-separated phonemes) -> Stemsyl sound letters (the 3 x 3 file's convention: AO R -> 'Or', aw + r)
import re
VOW=[('aɪɚ','Y@r'),('aʊɚ','W@r'),('ɔːɹ','Or'),('ɔɹ','Or'),('oːɹ','Or'),('oɹ','Or'),('ɑːɹ','Ar'),('ɑɹ','Ar'),('ɛɹ','er'),('eɹ','er'),('ɪɹ','ir'),('iɹ','ir'),('ʊɹ','ur'),('uɹ','ur'),('ɜːɹ','@r'),('ɜɹ','@r'),('əɹ','@r'),
     ('aɪ','Y'),('aʊ','W'),('oʊ','G'),('ɔɪ','B'),('eɪ','E'),('iə','I@'),('ɜː','@r'),('ɜ','@r'),('ɚ','@r'),('əl','@l'),
     ('ɑː','A'),('ɑ','A'),('ɒ','A'),('ɔː','O'),('ɔ','O'),('iː','I'),('i','I'),('uː','U'),('u','U'),('æ','a'),('ɛ','e'),('e','e'),('ɪ','i'),('ᵻ','i'),('ʊ','u'),('ə','@'),('ɐ','@'),('ʌ','@'),('a','a'),('o','G')]
CON={'p':'p','b':'b','t':'t','d':'d','k':'k','ɡ':'g','g':'g','f':'f','v':'v','θ':'T','ð':'D','s':'s','z':'z','ʃ':'S','ʒ':'Z','h':'h','tʃ':'C','dʒ':'J',
     'm':'m','n':'n','ŋ':'N','l':'l','ɹ':'r','r':'r','w':'w','j':'y','ʔ':'t','x':'k','ç':'h','ʍ':'w','n̩':'@n','l̩':'@l','m̩':'@m','ɬ':'l','ɾ':'?'}
def ph2ss(tok):
    t=tok.replace('ˈ','').replace('ˌ','').replace('‍','').replace('ː','ː')
    if not t: return ''
    if t in CON: return CON[t]
    for a,b in VOW:
        if t==a: return b
    # fallbacks: long marks / unknown combos
    for a,b in VOW:
        if t.startswith(a): return b+ph2ss(t[len(a):])
    raise KeyError(tok)
def espeak_to_ss(ipa, spelling):
    toks=[x for x in re.split(r'[_ ]',ipa) if x]
    out=[ph2ss(t) for t in toks]
    # flaps: t or d by the letters still unaccounted for
    if '?' in out:
        nt=len(re.findall(r't+',spelling)); nd=len(re.findall(r'd+',spelling))
        ht=sum(1 for x in out if x=='t'); hd=sum(1 for x in out if x=='d')
        for i,x in enumerate(out):
            if x=='?':
                if nt-ht>0: out[i]='t'; ht+=1
                elif nd-hd>0: out[i]='d'; hd+=1
                else: out[i]='t'; ht+=1
    s=''.join(out)
    s=s.replace('@r@r','@r').replace('rr','r')
    return s
