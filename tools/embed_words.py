# Puts the word list (data/stemsyl-words.tsv) into a keyboard file: the commonest 30,000 words on its SS_WORDS line, read
# as the page opens; the rest in a block of text the browser doesn't run (id "ssMore"), read a moment later in small
# slices; and the word-list code that reads both. Also the credits for the list's sources.
import json, collections
HEAD = 30000          # words on the SS_WORDS line; the rest go in the ssMore block

KC = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def pre(a, b):
    n = 0
    while n < len(a) and n < len(b) and a[n] == b[n] and n < 61: n += 1
    return n
def encode(rows):
    """rows: (word, blocked, prons). One line per word: [!] K spelling-rest (TAB K sounds-rest)+ ;
       K says how many characters to keep from the previous word (spelling) / previous first reading / this first reading"""
    out = []; pw = pp = ''
    for w, blk, ps in rows:
        k = pre(pw, w); line = ('!' if blk else '') + KC[k] + w[k:]
        k2 = pre(pp, ps[0]); line += '\t' + KC[k2] + ps[0][k2:]
        for q in ps[1:]:
            k3 = pre(ps[0], q); line += '\t' + KC[k3] + q[k3:]
        out.append(line); pw, pp = w, ps[0]
    return '\n'.join(out)

WORDS_JS_OLD_START = "var WORDS=(function(){"
WORDS_JS_NEW = r"""var WORDS=(function(){
  'use strict';
  /* SP spelling · PR its pronunciations · BLK kept out of the longer-word suggestions · FLAT word and pronunciation pairs,
     commonest first · B2 where each pronunciation starts, filed by its first two sounds (B1: one-sound words) · BYS spelling -> word */
  var SP=[], PR=[], BLK=[], FLAT=[], B1=Object.create(null), B2=Object.create(null), BYS=Object.create(null), bysUpTo=0;
  var headDone=false, moreText=null, morePos=0, pw='', pp='', moreDone=false, timer=0, listeners=[];
  function addWord(w,blk,prons){
    var n=SP.length, j, p, k, B; SP.push(w); BLK.push(blk?1:0); PR.push(prons);
    for(j=0;j<prons.length;j++){
      p=prons[j]; if(p.length>=2){ k=p.slice(0,2); B=B2; } else { k=p; B=B1; }
      (B[k]||(B[k]=[])).push(FLAT.length); FLAT.push(n,p);
    }
  }
  function indexSpellings(){ for(var n=bysUpTo;n<SP.length;n++) if(BYS[SP[n]]===undefined) BYS[SP[n]]=n; bysUpTo=SP.length; }
  var KC='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', KV=Object.create(null);
  for(var q=0;q<KC.length;q++) KV[KC.charAt(q)]=q;
  /* The rest of the list, one word a line: an optional ! (kept out of the longer-word suggestions), then one character
     saying how much of the previous word's spelling to keep, and the rest of this one; then its pronunciations the same
     way, the first against the previous word's first and the others against this word's first. */
  function loadSome(budgetMs){
    var txt=moreText, i=morePos, t0=Date.now(), c=0, e, L, f, w, p0, prons, j, blk;
    while(i<txt.length){
      e=txt.indexOf('\n',i); if(e<0) e=txt.length;
      L=txt.slice(i,e); i=e+1;
      if(L){
        blk=L.charCodeAt(0)===33; if(blk) L=L.slice(1);
        f=L.split('\t');
        if(f.length>=2){
          w=pw.slice(0,KV[f[0].charAt(0)])+f[0].slice(1);
          p0=pp.slice(0,KV[f[1].charAt(0)])+f[1].slice(1); prons=[p0];
          for(j=2;j<f.length;j++) prons.push(p0.slice(0,KV[f[j].charAt(0)])+f[j].slice(1));
          addWord(w,blk,prons); pw=w; pp=p0;
        }
      }
      if(++c===400){ c=0; if(Date.now()-t0>=budgetMs) break; }
    }
    morePos=i;
    if(i>=txt.length){
      moreDone=true; moreText=null;
      for(j=0;j<listeners.length;j++){ try{ listeners[j](); }catch(err){} }
    }
  }
  function step(){ timer=0; loadSome(12); if(!moreDone) timer=setTimeout(step,0); }
  /* the common words now; the rest a little at a time once the page is showing, so it opens as fast as before */
  function load(){
    if(headDone) return; headDone=true;
    var lines=SS_WORDS.split('\n'), i, f, w;
    for(i=0;i<lines.length;i++){
      f=lines[i].split('\t'); if(f.length<2) continue;
      w=f[0]; var blk=w.charAt(0)==='!'; if(blk) w=w.slice(1);
      addWord(w,blk,f.slice(1));
    }
    SS_WORDS=''; indexSpellings();
    var more=document.getElementById('ssMore');
    if(more&&more.textContent.length>1){ moreText=more.textContent; more.textContent=''; timer=setTimeout(step,60); }
    else moreDone=true;
  }
  function loadAll(){ load(); if(!moreDone){ clearTimeout(timer); timer=0; loadSome(1e9); } }
  /* words that sound exactly like pron, then commoner words that begin with those sounds.
     The commonest exact words lead; when many words share the sounds, the rarer ones follow the longer words. */
  var LEAD=5;
  function candidates(pron,limitMore){
    load();
    var ex=[], more=[], seen=Object.create(null), i, at, n, p, b;
    function exact(at){ var n=FLAT[at]; if(!seen[SP[n]]){ seen[SP[n]]=1; ex.push({w:SP[n],p:pron,exact:true}); } }
    function longer(at){ var n=FLAT[at], p=FLAT[at+1];
      if(BLK[n]||seen[SP[n]]||p.length<=pron.length||p.lastIndexOf(pron,0)!==0) return;
      seen[SP[n]]=1; more.push({w:SP[n],p:p,exact:false}); }
    if(pron.length>=2){
      b=B2[pron.slice(0,2)]||[];
      for(i=0;i<b.length;i++) if(FLAT[b[i]+1]===pron) exact(b[i]);
      for(i=0;i<b.length&&more.length<limitMore;i++) longer(b[i]);
    } else if(pron.length===1){
      b=B1[pron]||[];
      for(i=0;i<b.length;i++) exact(b[i]);
      for(i=0;i<FLAT.length&&more.length<limitMore;i+=2) longer(i);
    }
    return ex.slice(0,LEAD).concat(more,ex.slice(LEAD));
  }
  /* a spelling: the common words are indexed at once; the first word they don't hold waits for the rest of the list */
  function lookup(spelling){
    load(); var n=BYS[spelling];
    if(n===undefined&&(!moreDone||bysUpTo<SP.length)){ loadAll(); indexSpellings(); n=BYS[spelling]; }
    return n===undefined?null:{w:SP[n],p:PR[n][0]};
  }
  return {load:load,candidates:candidates,lookup:lookup,loadAll:loadAll,
    ready:function(){ return moreDone; }, onMore:function(fn){ if(moreDone) fn(); else listeners.push(fn); },
    size:function(){ loadAll(); return SP.length; }};
})();"""

CREDITS_OLD = "<p>Pronunciations: the CMU Pronouncing Dictionary (General American), written in Stemsyl sounds. Word order: Hermit Dave’s FrequencyWords, counted from OpenSubtitles 2018 and licensed CC BY-SA 4.0; this keyboard uses its ranking of the 30,000 commonest words that the dictionary knows.</p>"

def credits(stats):
    return ("<p>Words: every word of the CMU Pronouncing Dictionary and of the English Speller Database’s American list at size 80 "
            f"— {stats['total']:,} in all. Pronunciations (General American, written in Stemsyl sounds): {stats['cmu']:,} from the CMU dictionary; "
            f"{stats['rule']:,} built from those by regular endings, prefixes and compounds (abjured from abjure, aboveground from above and ground); "
            f"and {stats['g2p']:,} rarer words and names predicted by eSpeak NG (GPL-3.0), with a second guess from Kyubyong Park and Jongseok Kim’s g2p model (Apache-2.0) where the two nearly agree. "
            "Predicted pronunciations are usually right or one sound off.</p>"
            "<p>Word order: Hermit Dave’s FrequencyWords, counted from OpenSubtitles 2018 and licensed CC BY-SA 4.0. Words it never counted follow, "
            "the commoner speller lists first. Offensive words are kept out of the longer-word suggestions, partly using the LDNOOBW list (CC BY 4.0); "
            "they can still be written by their sounds.</p>")
ESDB_NOTICE = """<pre style="white-space:pre-wrap;font-size:11px;line-height:1.45;max-height:160px;overflow:auto;background:var(--key-2);padding:8px;border-radius:8px">English Speller Database (ESDB, previously SCOWL)
Copyright 2000-2026 by Kevin Atkinson

Permission to use, copy, modify, distribute, and sell any part of the English
Speller Database (ESDB, previously known as SCOWLv2), or word lists
created from it, is hereby granted without fee, provided that the above
copyright notice appears in all copies and that both the above copyright
notice and this notice appear in supporting documentation.  Kevin Atkinson
makes no representations about the suitability of this database for any
purpose.  It is provided "as is" without express or implied warranty.</pre>"""


def ss_words_line(rows):
    """the SS_WORDS line: one word a line, a leading ! for an offensive word, its pronunciations after tabs"""
    return 'var SS_WORDS=' + json.dumps('\n'.join(('!' if off else '') + w + '\t' + '\t'.join(ps) for w, ps, src, dic, off in rows)) + ';'

def embed(html, rows):
    """html: a keyboard file (tools/sources/keyboard-keys.html); rows: read_tsv('data/stemsyl-words.tsv')"""
    # 1. the commonest words, on the SS_WORDS line
    lines = html.split('\n')
    at = [i for i, l in enumerate(lines) if l.startswith('var SS_WORDS=')]
    assert len(at) == 1
    lines[at[0]] = ss_words_line(rows[:HEAD])
    html = '\n'.join(lines)
    # 2. the word-list code
    a = html.index(WORDS_JS_OLD_START); b = html.index('})();', a) + len('})();')
    html = html[:a] + WORDS_JS_NEW + html[b:]
    # 3. the rest of the words, as text the browser never runs, placed before the keyboard's own script
    blob = encode([(w, off, ps) for w, ps, src, dic, off in rows[HEAD:]])
    assert '</script' not in blob and '<!--' not in blob
    marker = html.index('<script>', html.index(WORDS_JS_NEW) + len(WORDS_JS_NEW))
    html = html[:marker] + '<script type="text/plain" id="ssMore">\n' + blob + '\n</script>\n\n' + html[marker:]
    # 4. what the word list is and where it comes from
    n = collections.Counter(src for w, ps, src, dic, off in rows)
    stats = {'total': len(rows), 'cmu': n['cmu'], 'rule': n['suffix'] + n['prefix'] + n['compound'], 'g2p': n['g2p']}
    assert html.count(CREDITS_OLD) == 1
    html = html.replace(CREDITS_OLD, credits(stats))
    i = html.index('</details>', html.index(credits(stats)))
    html = html[:i] + ESDB_NOTICE + '\n  ' + html[i:]
    START = "WORDS.load();\nload();"
    assert html.count(START) == 1
    html = html.replace(START, "WORDS.load();\n/* the rest of the word list arrives a moment after the page opens: offer its words too */\n"
                        "WORDS.onMore(function(){ candKey=null; renderStatus(); });\nload();")
    return html
