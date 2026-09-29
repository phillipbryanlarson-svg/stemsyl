# Standalone numpy inference for Kyubyong Park & Jongseok Kim's g2p_en model (Apache-2.0, github.com/Kyubyong/g2p),
# batched greedy decoding; no nltk needed.
import numpy as np, os
PH=["<pad>","<unk>","<s>","</s>"]+['AA0','AA1','AA2','AE0','AE1','AE2','AH0','AH1','AH2','AO0','AO1','AO2','AW0','AW1','AW2','AY0','AY1','AY2','B','CH','D','DH',
 'EH0','EH1','EH2','ER0','ER1','ER2','EY0','EY1','EY2','F','G','HH','IH0','IH1','IH2','IY0','IY1','IY2','JH','K','L','M','N','NG','OW0','OW1','OW2','OY0','OY1','OY2',
 'P','R','S','SH','T','TH','UH0','UH1','UH2','UW','UW0','UW1','UW2','V','W','Y','Z','ZH']
GR=["<pad>","<unk>","</s>"]+list("abcdefghijklmnopqrstuvwxyz")
G2I={g:i for i,g in enumerate(GR)}
V=np.load(os.path.join(os.path.dirname(__file__),'src/kyu/g2p_en/checkpoint20.npz'))
W={k:V[k].astype(np.float64) for k in V.files}
def sig(x): return 1/(1+np.exp(-x))
def cell(x,h,wih,whh,bih,bhh):
    a=x@wih.T+bih; b=h@whh.T+bhh; k=a.shape[-1]*2//3
    rz=sig(a[:,:k]+b[:,:k]); r,z=np.split(rz,2,-1)
    n=np.tanh(a[:,k:]+r*b[:,k:]); return (1-z)*n+z*h
def predict_batch(words, maxlen=24):
    """words: list of lowercase a-z strings. Returns list of phoneme lists."""
    out=[None]*len(words)
    # group by length so each batch has identical encoder steps (no padding effects)
    by=len and {}
    for i,w in enumerate(words): by.setdefault(len(w),[]).append(i)
    for L,idx in by.items():
        for s in range(0,len(idx),512):
            ii=idx[s:s+512]
            X=np.array([[G2I.get(c,1) for c in words[i]]+[2] for i in ii])
            E=W['enc_emb'][X]                       # (b, L+1, 64)
            h=np.zeros((len(ii),W['enc_w_hh'].shape[1]))
            for t in range(L+1): h=cell(E[:,t,:],h,W['enc_w_ih'],W['enc_w_hh'],W['enc_b_ih'],W['enc_b_hh'])
            dec=np.repeat(W['dec_emb'][[2]],len(ii),0); done=np.zeros(len(ii),bool); preds=[[] for _ in ii]
            for step in range(maxlen):
                h=cell(dec,h,W['dec_w_ih'],W['dec_w_hh'],W['dec_b_ih'],W['dec_b_hh'])
                p=(h@W['fc_w'].T+W['fc_b']).argmax(1)
                for j,pp in enumerate(p):
                    if done[j]: continue
                    if pp==3: done[j]=True
                    else: preds[j].append(PH[pp])
                if done.all(): break
                dec=W['dec_emb'][p]
            for j,i in enumerate(ii): out[i]=preds[j]
    return out
if __name__=='__main__':
    ws=['activationist','abjure','abjured','abashedly','aboveground','abscissa','selfie','emoji','blockchain','covid','doomscrolling','ghosting','abrupter','aeschylus','agrippina']
    for w,p in zip(ws,predict_batch(ws)): print(w,' '.join(p))
