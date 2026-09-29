# Builds docs/stemsyl-keyboard.html: one file, both keyboards (the key grid, with a key for every sound, and the 3 × 3
# keyboard), with a switch between them.
#   in:  tools/sources/keyboard-keys.html   the key-grid keyboard (the base; its words write the NORTH vowel as oh+r)
#        tools/sources/keyboard-3x3.html    the 3 × 3 keyboard: its styles, state and tables, its builder and its hold /
#                                           swipe / tap handlers are taken unchanged, except that each only acts while
#                                           its layout is showing
#        data/stemsyl-words.tsv             the word list
# Each change is an exact-text replacement that must match exactly once (swap), so a change to a source that moves a
# replaced piece stops the build with that piece named, rather than building something else.
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kbdata import read_tsv
from embed_words import embed
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ROWS = read_tsv(os.path.join(ROOT, 'data', 'stemsyl-words.tsv'))
base = embed(open(os.path.join(ROOT, 'tools', 'sources', 'keyboard-keys.html'), encoding='utf-8').read(), ROWS)
fix = open(os.path.join(ROOT, 'tools', 'sources', 'keyboard-3x3.html'), encoding='utf-8').read()

def cut(s, a, b, incl_b=False):
    i = s.index(a); j = s.index(b, i) + (len(b) if incl_b else 0)
    return s[i:j]
def swap(s, old, new, count=1):
    assert s.count(old) == count, (old[:70], s.count(old))
    return s.replace(old, new)

# ---------- styles ----------
css3 = cut(fix, "/* --- 3x3 clean - hold center, diagonal 9/0, swipe --- */", "\n</style>")
css3 = swap(css3, ".kb{\n  display:block !important;", ".kb.l3{\n  display:block !important;")
css3 = css3.replace("/* --- 3x3 clean - hold center, diagonal 9/0, swipe --- */",
                    "/* ---------- the 3 × 3 keyboard (layout 'grid3'): hold the centre for numbers, punctuation and cursor keys; swipe to move ---------- */")
css_switch = """
/* ---------- the layout switch, at the top of either keyboard ---------- */
.layrow{grid-column:1/-1;display:flex;justify-content:center;align-items:center;min-width:0}
.kb:not(.l3){grid-template-rows:28px}
.kb.l3 .layrow{margin:0 0 2px}
.lay{display:inline-flex;border:1px solid var(--key-line);border-radius:9px;overflow:hidden;background:var(--key)}
.lay button{border:0;background:none;color:var(--muted);height:28px;padding:0 12px;display:inline-flex;align-items:center;gap:6px;
  font-size:12px;font-weight:600;cursor:pointer;white-space:nowrap}
.lay button+button{border-left:1px solid var(--key-line)}
.lay button[aria-pressed="true"]{background:var(--mark);color:var(--mark-ink)}
.lay svg{width:16px;height:12px;flex:none;overflow:visible}
.lay .ico{fill:none;stroke:currentColor;stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round}
.lay .sq{fill:currentColor;stroke:none}
/* on a small screen the note gives way (it scrolls), so the word strip is never pushed under the keyboard */
.doc{min-height:min(calc(var(--u)*48px*10),calc(100vh - var(--kbh,380px) - 104px));min-height:min(calc(var(--u)*48px*10),calc(100dvh - var(--kbh,380px) - 104px))}
.strip{flex:none}
"""
base = swap(base, "\n</style>", "\n\n" + css3 + css_switch + "\n</style>")
# the page keeps exactly the keyboard's height free below the note, whichever keyboard is showing (set from its measured height)
base = swap(base, ".app{padding-bottom:calc(var(--kh)*6 + 43px + env(safe-area-inset-bottom,0px));}",
            ".app{padding-bottom:var(--kbh,calc(var(--kh)*6 + 76px + env(safe-area-inset-bottom,0px)));}")
base = swap(base, "bottom:calc(var(--kh)*6 + 84px);", "bottom:calc(var(--kbh,calc(var(--kh)*6 + 76px)) + 41px);")

# ---------- state: the layout is a preference, kept with the others ----------
base = swap(base, "var S={notes:[],cur:null,prefs:{gs:56,aid:'off',view:'stemsyl'}};",
            "var S={notes:[],cur:null,prefs:{gs:56,aid:'off',view:'stemsyl',layout:'keys'}};")
base = swap(base, "          S.prefs.view=VIEWS.indexOf(o.prefs.view)>=0?o.prefs.view:'stemsyl'; }",
            "          S.prefs.view=VIEWS.indexOf(o.prefs.view)>=0?o.prefs.view:'stemsyl';\n"
            "          S.prefs.layout=LAYOUTS.indexOf(o.prefs.layout)>=0?o.prefs.layout:'keys'; }")
# settings another Stemsyl keyboard keeps in the same place (the watch keyboard's glyph size) are kept as they are
base = swap(base, "        if(o.prefs){ S.prefs.gs=clampGs(+o.prefs.gs||56);",
            "        if(o.prefs){\n"
            "          /* settings another Stemsyl keyboard keeps in the same place (the watch keyboard's glyph size): kept as they are */\n"
            "          for(var pk in o.prefs){ var pv=o.prefs[pk];\n"
            "            if(pk!=='__proto__'&&Object.prototype.hasOwnProperty.call(o.prefs,pk)&&!(pk in S.prefs)&&/^(string|number|boolean)$/.test(typeof pv)) S.prefs[pk]=pv; }\n"
            "          S.prefs.gs=clampGs(+o.prefs.gs||56);")

# picking a word from the strip: the 3 × 3 keyboard goes back to choosing a tick position, as it did on its own
base = swap(base, "  candKey=null; edited();\n}\n$('cands')",
            "  candKey=null; edited();\n  if(S.prefs.layout==='grid3'){ selectedPos=null; buildKb(); }\n}\n$('cands')")

# ---------- the two keyboards ----------
state3 = cut(fix, "var selectedPos = null;", "function buildKb(){")
build3 = cut(fix, "function buildKb(){", "  $('kb').innerHTML=h;\n}", incl_b=True)
build3 = swap(build3, "function buildKb(){", "/* the 3 × 3 keyboard: a tick position, then its colour */\nfunction grid3Html(){")
build3 = swap(build3, "  $('kb').innerHTML=h;\n}", "  return h;\n}")
handlers3 = cut(fix, "$('kb').addEventListener('pointerdown',function(e){", "/* hold delete")
# each 3 × 3 handler acts only while the 3 × 3 keyboard is showing
handlers3 = swap(handlers3, "$('kb').addEventListener('pointerdown',function(e){\n",
                 "$('kb').addEventListener('pointerdown',function(e){\n  if(S.prefs.layout!=='grid3') return;\n")
handlers3 = swap(handlers3, "$('kb').addEventListener('pointermove',function(e){\n  if(!swipeSX) return;",
                 "$('kb').addEventListener('pointermove',function(e){\n  if(S.prefs.layout!=='grid3'||!swipeSX) return;")
handlers3 = swap(handlers3, "  $('kb').addEventListener(ev,function(e){\n    clearTimeout(centerHoldTimer);",
                 "  $('kb').addEventListener(ev,function(e){\n    if(S.prefs.layout!=='grid3') return;\n    clearTimeout(centerHoldTimer);")
handlers3 = swap(handlers3, "$('kb').addEventListener('click',function(e){\n  if(centerHoldFired)",
                 "$('kb').addEventListener('click',function(e){\n  if(S.prefs.layout!=='grid3') return;\n  if(centerHoldFired)")
# a swipe or a hold swallows only the tap its own lift may produce: every new touch clears it. (Before, only the next click
# cleared it, and a moved finger produces no click, so the first tap after every swipe was ignored.)
handlers3 = swap(handlers3, "  swipeSX = e.clientX; swipeSY = e.clientY; swipeST = Date.now(); swipeMoved=false;\n",
                 "  centerHoldFired=false;   /* a new touch: what the last swipe or hold was waiting to swallow is over */\n"
                 "  swipeSX = e.clientX; swipeSY = e.clientY; swipeST = Date.now(); swipeMoved=false;\n")
# picking a coloured tick writes its sound and goes straight back to the tick positions (✕ still cancels without writing)
handlers3 = swap(handlers3, "    if(cell.dataset.cons){ insert(['s',cell.dataset.cons]); return; }\n    if(cell.dataset.vow){ insert(['s',cell.dataset.vow]); return; }",
                 "    if(cell.dataset.cons||cell.dataset.vow){ selectedPos=null; insert(['s',cell.dataset.cons||cell.dataset.vow]); buildKb(); return; }")
handlers3 = "/* ---------- the 3 × 3 keyboard's hold, swipe and taps ---------- */\n" + handlers3

# the key grid's builder becomes keysHtml(); buildKb() draws whichever layout is chosen, with the switch on top
base = swap(base, "function buildKb(){\n  var h='';\n  (layer?NUMS:MAIN).forEach(function(k){",
            "/* the full keyboard: a key for every sound */\nfunction keysHtml(){\n  var h='';\n  (layer?NUMS:MAIN).forEach(function(k){")
base = swap(base, "    h+='<button type=\"button\" class=\"key '+cls+'\" data-k=\"'+k+'\" aria-label=\"'+esc(aria)+'\" title=\"'+esc(aria)+'\">'+inner+'</button>';\n  });\n  $('kb').innerHTML=h;\n}",
            "    h+='<button type=\"button\" class=\"key '+cls+'\" data-k=\"'+k+'\" aria-label=\"'+esc(aria)+'\" title=\"'+esc(aria)+'\">'+inner+'</button>';\n  });\n  return h;\n}")
layout_js = r"""
/* ---------- two layouts in one: the full keyboard and the 3 × 3 keyboard ---------- */
var LAYOUTS=['keys','grid3'];
ICON.keys='<svg viewBox="0 0 20 14" aria-hidden="true"><rect class="ico" x="0.7" y="0.7" width="18.6" height="12.6" rx="2.6"/><path class="ico" d="M4 4.6h1.2M7.6 4.6h1.2M11.2 4.6h1.2M14.8 4.6h1.2M4 7.6h1.2M7.6 7.6h1.2M11.2 7.6h1.2M14.8 7.6h1.2M6 10.4h8"/></svg>';
ICON.grid3='<svg viewBox="0 0 14 14" aria-hidden="true">'+[0,5,10].map(function(y){ return [0,5,10].map(function(x){
  return '<rect class="sq" x="'+x+'" y="'+y+'" width="4" height="4" rx="0.8"/>'; }).join(''); }).join('')+'</svg>';
function layoutSwitch(){
  var L=S.prefs.layout;
  return '<div class="layrow"><div class="lay" role="group" aria-label="Keyboard layout">'
    +'<button type="button" data-layout="keys" aria-pressed="'+(L==='keys')+'" title="Full keyboard: a key for every sound">'+ICON.keys+'Keys</button>'
    +'<button type="button" data-layout="grid3" aria-pressed="'+(L==='grid3')+'" title="3 × 3 keyboard: pick a tick position, then its colour">'+ICON.grid3+'3 × 3</button>'
    +'</div></div>';
}
/* the page keeps the keyboard's own height free below the note, so the word strip always sits just above the keys */
function fitKb(){ var h=$('kb').offsetHeight; if(h) document.documentElement.style.setProperty('--kbh',h+'px'); }
function buildKb(){
  var three=S.prefs.layout==='grid3', kb=$('kb');
  kb.classList.toggle('l3',three);
  kb.setAttribute('aria-label',three?'Stemsyl keyboard, 3 × 3 layout':'Stemsyl keyboard');
  kb.innerHTML=layoutSwitch()+(three?grid3Html():keysHtml());
  fitKb();
}
function setLayout(L){
  if(LAYOUTS.indexOf(L)<0||L===S.prefs.layout) return;
  flushTyping(); S.prefs.layout=L; layer=0; kbMode='sounds'; selectedPos=null;
  buildKb(); scheduleSave();
}
window.addEventListener('resize',fitKb);
if(window.ResizeObserver){ try{ new ResizeObserver(fitKb).observe($('kb')); }catch(e){} }
"""
anchor = "function flushTyping(){ return P.buf?commitBuf():null; }"
base = swap(base, anchor, state3 + build3 + "\n" + layout_js + "\n" + anchor)
# the switch is a tap anywhere on it; then the full keyboard's own handler (it acts only on its keys), then the 3 × 3 handlers
base = swap(base, "$('kb').addEventListener('mousedown',function(e){ e.preventDefault(); });   /* keep focus where it is */\n",
            "$('kb').addEventListener('mousedown',function(e){ e.preventDefault(); });   /* keep focus where it is */\n"
            "$('kb').addEventListener('click',function(e){ var b=e.target.closest('[data-layout]'); if(b) setLayout(b.dataset.layout); });\n")
base = swap(base, "/* hold delete to repeat */", handlers3 + "\n/* hold delete to repeat */")

# ---------- the guide ----------
base = swap(base, "  <div class=\"lbl\">Typing on a physical keyboard</div>",
            "  <p class=\"fine\">There are two layouts, switched at the top of the keyboard. <b>Keys</b> has a key for every sound. "
            "<b>3 × 3</b> asks for a tick position first, then its colour; hold its centre for numbers, punctuation and cursor keys, "
            "and swipe sideways across it to move the cursor.</p>\n  <div class=\"lbl\">Typing on a physical keyboard</div>")

# ---------- a word written only by its sounds shows its English when exactly one word has those sounds ----------
# Homophones (see, sea) keep their sounds, shown as IPA, until one is picked from the strip. Only everyday dictionary words
# (the standard American spell-check list, size 60) count as homophones of an unmarked word, so surnames and rare entries
# (Boye, Catt, qat) don't block boy or cat; after the name mark, names count too (Jon, John).
import base64
_bits = bytearray((len(ROWS) + 7) // 8)
for _i, (_w, _ps, _src, _dict, _off) in enumerate(ROWS):
    if _dict: _bits[_i >> 3] |= 1 << (_i & 7)
_dict_block = '<script type="text/plain" id="ssDict">' + base64.b64encode(bytes(_bits)).decode() + '</script>\n'
base = swap(base, '<script type="text/plain" id="ssMore">', _dict_block + '<script type="text/plain" id="ssMore">')
print('dictionary words flagged:', sum(bin(x).count('1') for x in _bits), 'of', len(ROWS))

base = swap(base, "  function loadAll(){ load(); if(!moreDone){ clearTimeout(timer); timer=0; loadSome(1e9); } }",
            "  function loadAll(){ load(); if(!moreDone){ clearTimeout(timer); timer=0; loadSome(1e9); } }\n"
            "  /* which words are everyday dictionary words (the standard American spell-check list): only these can be homophones\n"
            "     of an unmarked word, so surnames and rare entries don't count */\n"
            "  var DICT=null;\n"
            "  function isDict(n){\n"
            "    if(DICT===null){ var el=document.getElementById('ssDict'), s=el?atob(el.textContent.trim()):''; DICT=new Uint8Array(s.length);\n"
            "      for(var i=0;i<s.length;i++) DICT[i]=s.charCodeAt(i); }\n"
            "    return (DICT[n>>3]>>(n&7))&1;\n"
            "  }\n"
            "  /* the English spelling of a word written only by its sounds: the one word whose pronunciation is exactly these sounds,\n"
            "     or null when none or several are (homophones stay as sounds). After the name mark, names count as well. */\n"
            "  var EXM=Object.create(null);\n"
            "  /* two sounds that always mean one word, although others share them: eye alone is I, uh alone is a */\n"
            "  var FIXED={'Y':'i','@':'a'};\n"
            "  function exact(pron,named){\n"
            "    load(); if(!pron) return null;\n"
            "    if(FIXED[pron]) return FIXED[pron];\n"
            "    var key=(named?'N':'')+pron, hit=EXM[key]; if(hit!==undefined) return hit;\n"
            "    var b=pron.length>=2?B2[pron.slice(0,2)]:B1[pron], i, n, all=[], dict=[], seen=Object.create(null);\n"
            "    if(b) for(i=0;i<b.length;i++){ if(FLAT[b[i]+1]!==pron) continue; n=FLAT[b[i]];\n"
            "      if(seen[SP[n]]) continue; seen[SP[n]]=1; all.push(n); if(isDict(n)) dict.push(n); }\n"
            "    if(named) hit=all.length===1?SP[all[0]]:null;\n"
            "    else hit=dict.length===1?SP[dict[0]]:(dict.length===0&&all.length===1?SP[all[0]]:null);\n"
            "    if(moreDone) EXM[key]=hit;             /* remembered once the whole list is in */\n"
            "    return hit;\n"
            "  }")
base = swap(base, "  return {load:load,candidates:candidates,lookup:lookup,loadAll:loadAll,",
            "  return {load:load,candidates:candidates,lookup:lookup,exact:exact,loadAll:loadAll,")
# the English under the glyphs, the English view and Copy English
base = swap(base, "        var w;\n        if(sp){ w=sp; if(/^i($|')/.test(w)) w='I'+w.slice(1); if(start||capNext) w=capFirst(w); }\n        else w='/'+ipaOf(pron)+'/';",
            "        /* a spelling picked from the strip or typed on a keyboard; otherwise the one word that has exactly these sounds.\n"
            "           Homophones, and sounds that make no word, stay as their sounds between slashes. */\n"
            "        var w=sp||WORDS.exact(pron,capNext);\n"
            "        if(w){ if(/^i($|')/.test(w)) w='I'+w.slice(1); if(start||capNext) w=capFirst(w); }\n"
            "        else w='/'+ipaOf(pron)+'/';")
# when the rest of the word list arrives, the English under the glyphs is worked out again against all of it
base = swap(base, "WORDS.onMore(function(){ candKey=null; renderStatus(); });",
            "WORDS.onMore(function(){ candKey=null; if(S.prefs.view!=='stemsyl'||capsOn()) renderDoc(); else renderStatus(); });")
base = swap(base, "English uses the spelling of each word you finished from the strip or typed on a keyboard. A word spelled only by sound comes out as its sounds between slashes.",
            "English uses the spelling you picked from the strip or typed on a keyboard. A word written only by its sounds shows its English when exactly one word has those sounds; "
            "a word that shares its sounds with another (see, sea), or sounds that make no word, come out as sounds between slashes.")
base = swap(base, "Tapping one finishes the word and keeps its spelling for <b>Copy English</b>; the note itself shows only the sounds.",
            "When exactly one English word has the sounds you wrote, its spelling goes under the glyphs and into <b>Copy English</b> by itself. "
            "Words that share their sounds with another (see, sea; to, two, too) stay as sounds until you tap one — except eye alone, which is always I, "
            "and uh alone, which is always a. After the ◆ name mark, names count too, "
            "so Jon and John wait for your choice. Tapping a longer word finishes the word; the note itself shows only the sounds.")

# ---------- test hook ----------
base = swap(base, "window.__ss={parseText:parseText,", "window.__ss={setLayout:setLayout,get layout(){return S.prefs.layout;},parseText:parseText,")

# ---------- licences: the app is free software (GPL-3.0-or-later); its word list is CC BY-SA 4.0; the script is CC0 ----------
LICENCE_HEADER = """<!--
  Stemsyl keyboard. Copyright (C) 2026 the Stemsyl authors (see AUTHORS).

  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
  License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
  version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
  details. You should have received a copy of the GNU General Public License along with this program. If not, see
  <https://www.gnu.org/licenses/>.

  The word list inside (the SS_WORDS, ssDict and ssMore blocks) is also available on its own under CC BY-SA 4.0, and
  the Stemsyl writing system itself is dedicated to the public domain under CC0 1.0. The third-party sources of the
  word list and their licences are listed in the app, under "Word data and licences".
-->
"""
base = swap(base, '<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + LICENCE_HEADER)
# the geometry notes: the vowels' colours as they are now (they were re-tuned after the notes were written)
base = swap(base, "   Vowels: the colour is the vowel: amber a, emerald e, indigo i, olive o (hot), blue oo; ink is schwa.\n",
            "   Vowels: the colour is the vowel, two vowels a colour: red a · eye, orange ah · ow, yellow e · ay, green i · ee,\n"
            "   blue u · oo, grey uh · aw, violet oh · oy.\n")
base = swap(base, '<summary>Word data and licences</summary>\n',
            '<summary>Word data and licences</summary>\n'
            '    <p>This app is free software: you can share and change it under the GNU General Public License, version 3 or later, '
            'and it comes with no warranty. Its word list is also offered on its own under CC BY-SA 4.0, and the Stemsyl writing system '
            'itself is dedicated to the public domain (CC0 1.0), so anyone may use, teach and build on it.</p>')

assert 'function buildKb(){' in base and base.count('function buildKb(){') == 1
OUT = os.path.join(ROOT, 'docs', 'stemsyl-keyboard.html')
open(OUT, 'w', encoding='utf-8').write(base)
print('written', os.path.normpath(OUT), len(base.encode('utf-8')), 'bytes')
