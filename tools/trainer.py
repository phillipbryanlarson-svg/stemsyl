# Builds docs/stemsyl-trainer.html from tools/sources/trainer.html: the Stemsyl trainer, brought in line with the
# keyboards: the vowels' colours as the keyboards have them (re-tuned after the trainer was made), the centred tick
# running the full height across the stem, and the keyboards' word conventions (the LOT vowel written as ah, the
# NORTH/FORCE vowel as oh + r). Plus the licence notice.
import json, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fullconv import to_full
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
src = open(os.path.join(ROOT, 'tools', 'sources', 'trainer.html'), encoding='utf-8').read()
s = src

def swap(s, old, new, count=1):
    assert s.count(old) == count, (old[:80], s.count(old))
    return s.replace(old, new)

# ---- colours: the keyboards' vowel colours, for both themes
LIGHT = "--vred:#c40027; --vorange:#8f2400; --vyellow:#d4a900; --vgreen:#236b27; --vvblue:#002fec; --vgrey:#5f5f5f; --vviolet:#582684;"
DARK = "--vred:#c34a55; --vorange:#ff7f00; --vyellow:#ffe135; --vgreen:#a1fd60; --vvblue:#5081c8; --vgrey:#999999; --vviolet:#9826ea;"
s = swap(s, "--olive:#4F7103; --amber:#A19005;\n", "--olive:#4F7103; --amber:#A19005;\n  /* the seven vowel colours, as the keyboards have them */\n  " + LIGHT + "\n")
s = swap(s, "--olive:#BCDD73; --amber:#A6940E;\n", "--olive:#BCDD73; --amber:#A6940E;\n    " + DARK + "\n", count=2)
s = swap(s, ".t-ink,.t-rose,.t-mauve,.t-indigo,.t-blue,.t-emerald,.t-olive,.t-amber{font-weight:600}",
         ".t-ink,.t-rose,.t-mauve,.t-indigo,.t-blue,.t-emerald,.t-olive,.t-amber,\n"
         ".t-red,.t-orange,.t-yellow,.t-green,.t-vblue,.t-grey,.t-violet{font-weight:600}")
s = swap(s, ".numdot{fill:var(--mark);stroke:none}",
         ".f-red{stroke:var(--vred)} .f-orange{stroke:var(--vorange)} .f-yellow{stroke:var(--vyellow)} .f-green{stroke:var(--vgreen)}\n"
         ".f-vblue{stroke:var(--vvblue)} .f-grey{stroke:var(--vgrey)} .f-violet{stroke:var(--vviolet)}\n"
         ".t-red{color:var(--vred)} .t-orange{color:var(--vorange)} .t-yellow{color:var(--vyellow)} .t-green{color:var(--vgreen)}\n"
         ".t-vblue{color:var(--vvblue)} .t-grey{color:var(--vgrey)} .t-violet{color:var(--vviolet)}\n"
         ".numdot{fill:var(--mark);stroke:none}")

# ---- geometry: the centred tick crosses the stem, the full tick length up and down (as the keyboards draw it)
s = swap(s, "var TICKY={u:[CY-TL,CY],c:[CY-TL/2,CY+TL/2],d:[CY,CY+TL]};",
         "var TICKY={u:[CY-TL,CY],c:[CY-TL,CY+TL],d:[CY,CY+TL]};   /* centred: across the stem, the full length up and down */")
s = swap(s, """   Vowels: the colour is the vowel, and each colour's name starts with its sound:
   amber a, emerald e, indigo i, olive o (hot), blue oo; ink is schwa.
       centred the plain vowel · up glides to i · down glides to u
   so ee (i going to i) is indigo up and oo (u going to u) is blue down. Ink down is aw. */""",
"""   Vowels: the colour is the vowel, two vowels a colour: red a · eye, orange ah · ow, yellow e · ay, green i · ee,
   blue u · oo, grey uh · aw, violet oh · oy.
       centred the plain vowel · up glides to i · down glides to u
   so ee (i going to i) is green up and oo (u going to u) is blue down. Grey down is aw. */""")
s = swap(s, """var VTICK={'|@':['ink','c'],'o|o':['ink','d'],
  'a|':['amber','c'],'a|i':['amber','u'],'a|u':['amber','d'],
  'e|':['emerald','c'],'e|i':['emerald','u'],
  'i|':['indigo','c'],'i|i':['indigo','u'],
  'a|a':['olive','c'],'o|i':['olive','u'],'o|u':['olive','d'],
  'u|':['blue','c'],'u|u':['blue','d']};""",
"""var VTICK={'a|':['red','c'],'a|i':['red','u'],'a|a':['orange','c'],'a|u':['orange','d'],
  'e|':['yellow','c'],'e|i':['yellow','u'],'i|':['green','c'],'i|i':['green','u'],
  'u|':['vblue','c'],'u|u':['vblue','d'],'|@':['grey','c'],'o|o':['grey','d'],
  'o|u':['violet','d'],'o|i':['violet','u']};""")
s = swap(s, "(h, y and w never close a syllable). Every other consonant stands alone as three dots. */",
         "(h, y and w never close a syllable). Every other consonant stands alone on a stub of its own. */")
# descriptions name the colours; the keyboards call their blue simply blue
s = swap(s, "function cname(f){ return '<span class=\"t-'+f+'\">'+f+'</span>'; }",
         "function cname(f){ return '<span class=\"t-'+f+'\">'+(f==='vblue'?'blue':f)+'</span>'; }")
s = swap(s, "if(k==='|@') return w+'schwa, the plain ink vowel';", "if(k==='|@') return w+'schwa, the plain vowel';")

# ---- the page's own description, and the licence
s = swap(s, 'content="Practise reading Stemsyl, the seven-dot phonetic script for English:',
         'content="Practise reading Stemsyl, the colour-stem phonetic script for English:')
s = swap(s, "<!doctype html>\n", """<!doctype html>
<!--
  Stemsyl trainer. Copyright (C) 2026 the Stemsyl authors (see AUTHORS).

  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
  License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
  version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
  details. You should have received a copy of the GNU General Public License along with this program. If not, see
  <https://www.gnu.org/licenses/>.

  The Stemsyl writing system itself is dedicated to the public domain under CC0 1.0. The spoken sounds were made
  with eSpeak NG (GPL-3.0); the words and sentences come from the keyboards' word list (see NOTICE).
-->
""")
s = swap(s, "voice: eSpeak NG</nav>", "voice: eSpeak NG &nbsp;·&nbsp; free software (GPL-3.0)</nav>")

# ---- the words: the keyboards' conventions (LOT is written ah; NORTH/FORCE oh + r; unstressed for- as fer-)
a = s.index('var TD=') + len('var TD=')
b = s.index(';\n', a)
TD = json.loads(s[a:b])
changed = []
def conv(word, p):
    q = to_full([p.replace('o', 'A')], word)[0]
    if q != p: changed.append((word, p, q))
    return q
for key in ('short', 'long'):
    for r in TD[key]:
        r[1] = conv(r[0], r[1])
for sent in TD['sentences']:
    for t in sent:
        if t[0] == '#': continue
        if t[0] == '*': t[2] = conv(t[1], t[2])
        else: t[1] = conv(t[0], t[1])
s = s[:a] + json.dumps(TD, ensure_ascii=False, separators=(',', ':')) + s[b:]
print(len(changed), 'pronunciations rewritten, e.g.', changed[:4])
OUT = os.path.join(ROOT, 'docs', 'stemsyl-trainer.html')
open(OUT, 'w', encoding='utf-8').write(s)
print('written', os.path.normpath(OUT), len(s.encode('utf-8')), 'bytes')
