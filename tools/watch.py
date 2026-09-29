# Builds docs/stemsyl-keyboard-watch.html: the 3 × 3 keyboard on its own, the size of an Apple Watch screen.
# Base: the two-layout file (docs/stemsyl-keyboard.html, built by keyboard.py), so the 3 × 3 keys, the word list, the English under the glyphs
# and everything else work exactly as its 3 × 3 layout does. Changes:
#   - only the 3 × 3 keys (no full keyboard, no layout switch)
#   - the whole app, panels and messages included, fits the 46 mm Apple Watch Series 12 screen: 208 × 248 points
#     (416 × 496 pixels), shrinking to fit anything smaller (the 42 mm is 187 × 223 points)
#   - the note is a one-line strip at the top, then the word strip (or, as chosen in the menu, below the keys), then the
#     3 × 3 keys. Holding the note shows all of it over the watch face; there a tap puts the cursor where it lands and brings
#     up delete, space and new line, and a hold goes back to the keys
#   - the top bar's buttons (notes, title, view, menu, share) become a set of option keys. Held, the middle key of each
#     edge brings up numbers, punctuation, the options or cursor keys, and the centre key brings back the tick positions
# Like keyboard.py, each change is an exact-text replacement that must match exactly once.
import re, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
src = open(os.path.join(ROOT, 'docs', 'stemsyl-keyboard.html'), encoding='utf-8').read()
s = src

def swap(s, old, new, count=1):
    assert s.count(old) == count, (old[:80], s.count(old))
    return s.replace(old, new)
def between(s, a, b, new, keep_b=True):
    """replace from marker a (inclusive) to marker b (b kept unless keep_b is False)"""
    i = s.index(a); j = s.index(b, i)
    assert s.count(a) == 1, a[:60]
    return s[:i] + new + (s[j:] if keep_b else s[j + len(b):])
def grab(s, a, b):
    i = s.index(a); j = s.index(b, i); return s[i:j]

# ---------------------------------------------------------------- head
s = swap(s, '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
         '<meta name="disabled-adaptations" content="watch">')
s = swap(s, '<meta name="description" content="Write English in Stemsyl, the colour-stem phonetic script: one key per sound, syllables group themselves.">',
         '<meta name="description" content="Write English in Stemsyl, the colour-stem phonetic script, on a 3 × 3 keyboard the size of an Apple Watch screen.">')
s = swap(s, '<title>Stemsyl Keyboard</title>', '<title>Stemsyl Watch Keyboard</title>')

# ---------------------------------------------------------------- styles
s = swap(s, "  --kh:clamp(46px,7.6vh,62px);--kh:clamp(46px,7.6dvh,62px);\n  --u:.875;",
         "  --u:.625;\n"
         "  /* the watch screen: its corner, the corner of what sits inside it, and the watch body around it */\n"
         "  --r:32px; --ri:28px; --page:#1e1e1c;")
s = swap(s, "@media (max-width:600px){\n  :root{ --kh:clamp(41px,5.5vh,50px);--kh:clamp(41px,5.5dvh,50px); }\n}\n", "")
glyph_css = grab(s, "/* the glyphs: a stem and fat coloured ticks */", "\n/* ---------- status line and word strip ---------- */")

CSS = r"""html{height:100%;box-sizing:border-box;background:var(--page);-webkit-text-size-adjust:100%;text-size-adjust:100%}
[hidden]{display:none!important}
*,*::before,*::after{box-sizing:inherit;-webkit-tap-highlight-color:transparent}
html,body{overscroll-behavior:none}
body{height:100%;margin:0;display:flex;align-items:center;justify-content:center;background:var(--page);color:var(--text);overflow:hidden;
  font:13px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
button,input,textarea{font:inherit;color:inherit}
.ipa{font-family:"Charis SIL","Doulos SIL","Gentium Plus","Noto Serif","DejaVu Serif","Times New Roman",serif}

/* ---------- the watch screen: the whole app, panels and messages included, stays inside the screen of the 46 mm
   Apple Watch Series 12 — 208 × 248 points, 416 × 496 pixels — and shrinks to fit a smaller one (42 mm: 187 × 223) ---------- */
.app{position:relative;flex:none;width:min(208px,100vw);height:min(248px,100vh);height:min(248px,100dvh);
  display:flex;flex-direction:column;gap:3px;padding:4px;overflow:hidden;isolation:isolate;
  border-radius:var(--r);background:var(--paper);box-shadow:inset 0 0 0 1px var(--rule)}

/* ---------- the note: one line of glyphs along the top, scrolled sideways to keep the cursor in sight ---------- */
.doc{flex:none;margin-bottom:2px;overflow-x:auto;overflow-y:hidden;background:var(--sheet);border:1px solid var(--rule);
  border-radius:var(--ri) var(--ri) 8px 8px;padding:3px 12px;cursor:zoom-in;scrollbar-width:none;overscroll-behavior:contain;
  -webkit-overflow-scrolling:touch}
.doc::-webkit-scrollbar{display:none}
.sheet{display:flex;flex-wrap:nowrap;align-items:flex-start;width:max-content;min-width:100%;padding-right:4px}
.w{flex:none;display:inline-flex;flex-direction:column;align-items:flex-start}
.w .gl{display:flex;flex-wrap:nowrap}
.w .rd{font-size:10px;line-height:12px;color:var(--muted);white-space:nowrap;padding-left:1px}
.g{position:relative;flex:none;height:calc(var(--u) * 48px);display:flex;align-items:center}
.g svg{display:block;height:100%;width:100%;overflow:visible}
.g.t{font-size:calc(var(--u) * 25px);line-height:1;white-space:pre;color:var(--text);padding:0 1px}
.g.t.pu{color:var(--mark)}
.g.t.un{color:var(--muted);font-style:italic}
.sp{position:relative;flex:none;width:calc(var(--u) * 16px);height:calc(var(--u) * 48px)}
/* a one-line strip has no next row to start: a new line shows as a return sign */
.nl{position:relative;flex:none;width:calc(var(--u) * 26px);height:calc(var(--u) * 48px);display:flex;align-items:center;justify-content:center}
.nl::before{content:"\21B5";color:var(--muted);opacity:.75;font-size:calc(var(--u) * 24px);line-height:1}
.end{position:relative;flex:none;width:0;height:calc(var(--u) * 48px)}
.car{position:absolute;top:calc(var(--u) * 48px * .12);height:calc(var(--u) * 48px * .76);width:2px;margin-left:-1px;border-radius:1px;
  background:var(--mark);animation:blink 1.1s steps(1) infinite;pointer-events:none}
@keyframes blink{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.car{animation:none}}
.w.lab .gl{min-height:calc(var(--u) * 48px)}
.sheet.lab .sp,.sheet.lab .end{height:calc(var(--u) * 48px + 12px)}
/* the whole note: holding the strip spreads it over the watch face, many lines at once, with the keys put away.
   A tap there puts the cursor where it lands and brings up a bar with delete, space and new line; a hold goes back. */
.app.reading .kb,.app.reading .strip{display:none}
.app.reading .doc{flex:1 1 auto;margin-bottom:0;overflow-x:hidden;overflow-y:auto;border-radius:var(--ri);padding:8px 12px 12px;cursor:zoom-out}
.app.reading .sheet{flex-wrap:wrap;width:auto;min-width:0;row-gap:4px;align-content:flex-start;padding-right:0}
.app.reading .w{max-width:100%}
.app.reading .w .gl{flex-wrap:wrap;max-width:100%}
.app.reading .nl{flex-basis:100%;width:auto;height:0}
.app.reading .nl::before{content:none}
.app.reading .nl.blank{height:calc(var(--u) * 48px)}
.editbar{display:none;order:4;flex:none;gap:4px;height:36px;padding:0 10px 2px}
.app.reading.editing .editbar{display:flex}
.editbar button{flex:1;min-width:0;border:1.5px solid var(--key-line);border-radius:10px;background:var(--key);color:var(--key-ink);
  font-size:17px;line-height:1;cursor:pointer;padding:0;touch-action:manipulation}
.editbar button:active{transform:scale(.96)}
.editbar button:first-child{border-bottom-left-radius:20px}
.editbar button:last-child{border-bottom-right-radius:20px}

""" + glyph_css + r"""
/* ---------- the word strip: English words for the sounds before the cursor, or the status. Above the keys, or (menu)
   below them, where its ends keep clear of the screen's rounded bottom corners ---------- */
.strip{position:relative;flex:none;display:flex;align-items:center;height:28px;min-width:0}
.app.words-below .strip{order:3;padding:0 6px}
.status{flex:1;min-width:0;display:flex;align-items:center;gap:5px;padding:0 6px;font-size:10.5px;color:var(--muted);white-space:nowrap;overflow:hidden}
.status b{color:var(--text);font-weight:600}
.status .sp2{flex:1}
.status .kbd{font:500 11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--mark-soft);color:var(--text);padding:3px 5px;border-radius:4px}
.status .pv{display:flex;align-items:center;height:20px}
.status .pv svg{height:20px;width:auto;overflow:visible}
.cands{flex:1;min-width:0;display:flex;align-items:center;gap:4px;overflow-x:auto;padding:1px;scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
.cands::-webkit-scrollbar{display:none}
.cand{flex:none;height:26px;padding:0 9px;border-radius:9px;border:1px solid var(--key-line);background:var(--key);color:var(--text);cursor:pointer;font-size:12.5px;white-space:nowrap}
.cand.ex{font-weight:700}
.cand.cur{border-color:var(--mark);box-shadow:0 0 0 1px var(--mark) inset;background:var(--mark-soft)}
.cand.top{border-color:var(--mark)}
.cand .more{color:var(--muted);font-weight:400}

/* ---------- the 3 × 3 keys: a tick position, then its colour; hold the centre for the other keys; swipe to move ----------
   Sizes follow the keys' own height (cqh: a hundredth of the 3 × 3 block), which changes with the watch and the note strip. */
.kb{flex:1 1 0;min-height:0;display:flex;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none;touch-action:none}
.grid3-wrap{flex:1;min-width:0;display:flex}
.grid3{flex:1;min-width:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(3,minmax(0,1fr));gap:4px;container-type:size}
.grid3 .cell{min-width:0;min-height:0;border-radius:10px;border:1.5px solid var(--key-line);background:var(--key);color:var(--key-ink);cursor:pointer;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;padding:2px;position:relative;overflow:hidden;
  touch-action:none;user-select:none;-webkit-user-select:none}
.grid3 .cell:active{transform:scale(.96)}
/* when the keys reach the foot of the screen (the word strip above them), their bottom corners follow its curve */
.app:not(.words-below) .grid3>:nth-child(7){border-bottom-left-radius:var(--ri)}
.app:not(.words-below) .grid3>:nth-child(9){border-bottom-right-radius:var(--ri)}
/* in a key's corner: the keys holding it brings up (filled in: the keys showing now, where holding it just types) */
.grid3 .cell .hold-to{position:absolute;top:2px;right:3px;display:flex;align-items:center;font-size:8px;font-size:clamp(7px,5cqh,8.5px);line-height:1;
  font-weight:700;color:var(--mark);white-space:nowrap;pointer-events:none}
.grid3 .cell .hold-to.on{top:1px;right:2px;padding:1px 2px;border-radius:3px;background:var(--mark);color:var(--mark-ink)}
.grid3 .cell .hold-to svg{display:block;width:10px;height:8px;overflow:visible}
.grid3 .cell .hold-to svg.lr{width:13px;height:9px}
.grid3 .cell.pos.mid{background:var(--key-2)}
.grid3 .cell .pos-icon{display:flex}
.grid3 .cell .pos-icon svg{height:20px;height:clamp(14px,12.5cqh,24px);width:auto}
.grid3 .cell .pos-lb{font-size:10px;font-size:clamp(8.5px,6.2cqh,11px);font-weight:700;line-height:1.1;white-space:nowrap}
.grid3 .cell .pos-lb.big{font-size:17px;font-size:clamp(14px,10.5cqh,19px)}
.grid3 .cell .pos-lb.small{font-size:8px;font-size:clamp(7.5px,5cqh,9px);font-weight:600;opacity:.72}
.grid3 .cell.sel{background:var(--mark);color:var(--mark-ink);border-color:var(--mark)}
.grid3 .cell.sel .sel-x{font-size:16px;line-height:1}
.grid3 .cell.colopt .col-glyph{display:flex}
.grid3 .cell.colopt .col-glyph svg{height:24px;height:clamp(17px,15cqh,28px);width:auto}
.grid3 .cell.colopt .col-lb{font-size:10px;font-size:clamp(8.5px,6.2cqh,11px);font-weight:700;line-height:1}
.grid3 .cell.empty{background:transparent;border:1px dashed var(--rule);opacity:.25}
.grid3 .cell.pos.num svg.numdice{height:22px;height:clamp(16px,14cqh,26px);width:auto;flex:none}
.cell.split-diag{padding:0!important}
.cell.split-diag .tri{position:absolute;inset:0;width:100%;height:100%;border:none;background:transparent;cursor:pointer;display:flex;flex-direction:column;gap:1px;
  font-weight:700;font-size:14px;color:var(--key-ink);padding:0;z-index:1}
.cell.split-diag .tri:active{background:var(--mark-soft)}
.cell.split-diag .tri-9{clip-path:polygon(0 0,100% 0,0 100%);justify-content:flex-start;align-items:flex-start;padding:4px 0 0 7px}
.cell.split-diag .tri-0{clip-path:polygon(100% 0,100% 100%,0 100%);justify-content:flex-end;align-items:flex-end;padding:0 10px 6px 0}
.cell.split-diag .tri svg.numdice{width:16px;height:16px;width:clamp(13px,10cqh,20px);height:clamp(13px,10cqh,20px);flex:none}
.cell.split-diag .tri .pos-lb{font-size:9px;font-weight:700;line-height:1}
.cell.split-diag .diag-line{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:0;
  background:linear-gradient(135deg,transparent calc(50% - 0.75px),var(--key-line) calc(50% - 0.75px),var(--key-line) calc(50% + 0.75px),transparent calc(50% + 0.75px))}
/* the app keys: what a bigger screen keeps along the top */
.grid3 .cell.appk svg.ai{width:19px;height:19px;width:clamp(15px,12cqh,22px);height:clamp(15px,12cqh,22px);flex:none;
  stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.grid3 .cell.appk .nc{position:absolute;top:4px;left:6px;font-size:8.5px;font-weight:700;color:var(--muted);font-variant-numeric:tabular-nums}
.grid3 .cell.appk .vg{height:19px;height:clamp(15px,12cqh,22px);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;line-height:1}
.grid3 .cell.appk .vg svg{height:100%;width:auto;overflow:visible}
.grid3 .cell.appk .vg.sm{height:13px;height:clamp(11px,8.5cqh,16px)}
.grid3 .cell.appk .uc{font-size:8.5px;line-height:9px;height:9px;color:var(--muted);font-weight:600}
.cell.split-diag .tri .az{font-size:14px;line-height:1}
.cell.split-diag .tri-9 .az{font-size:11px}

/* ---------- panels and messages, inside the watch screen ---------- */
.scrim{position:absolute;inset:0;background:var(--scrim);z-index:10}
.panel{position:absolute;inset:0;z-index:11;overflow-y:auto;overflow-x:hidden;background:var(--sheet);color:var(--text);border-radius:var(--r);
  padding:0 12px 20px;font-size:12px;scrollbar-width:none;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
.panel::-webkit-scrollbar{display:none}
.panel h2{font-size:14px;margin:0;font-weight:700}
.ph{position:sticky;top:0;z-index:2;display:flex;align-items:center;gap:6px;margin:0 -12px 4px;padding:10px 12px 6px 16px;background:var(--sheet)}
.ph .sp2{flex:1}
.x{flex:none;width:28px;height:28px;border-radius:14px;border:1px solid var(--key-line);background:var(--key);cursor:pointer;display:grid;place-items:center;padding:0}
.x svg{width:12px;height:12px;stroke:currentColor;stroke-width:1.8;fill:none;stroke-linecap:round}
.btn{height:30px;padding:0 10px;border-radius:9px;border:1px solid var(--key-line);background:var(--key);cursor:pointer;font-size:12px;white-space:nowrap}
.btn.primary{background:var(--mark);border-color:var(--mark);color:var(--mark-ink);font-weight:600}
.btn.danger{color:var(--warn);border-color:var(--warn)}
.btn[disabled]{opacity:.4;cursor:default}
.row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.lbl{font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:12px 0 5px;font-weight:700}
.fine{font-size:11px;color:var(--muted);line-height:1.45;margin:6px 0 0}
.fine b{color:var(--text)}
.seg{display:inline-flex;border:1px solid var(--key-line);border-radius:9px;overflow:hidden}
.seg button{border:0;background:var(--key);padding:6px 9px;cursor:pointer;font-size:12px}
.seg button+button{border-left:1px solid var(--key-line)}
.seg button[aria-pressed="true"]{background:var(--mark);color:var(--mark-ink);font-weight:600}
/* text fields at 16px: smaller makes an iPhone zoom the page when one is focused */
textarea{width:100%;min-height:52px;border:1px solid var(--key-line);border-radius:9px;background:var(--key);padding:6px 8px;resize:vertical;font-size:16px}
.title{width:100%;height:36px;border:1px solid var(--key-line);border-radius:9px;background:var(--key);padding:0 9px;font-size:16px;font-weight:700;text-overflow:ellipsis}
.title:focus{outline:none;border-color:var(--mark)}
:focus-visible{outline:2px solid var(--mark);outline-offset:2px}
.notes{display:flex;flex-direction:column;gap:6px}
.note{display:flex;flex-wrap:wrap;align-items:center;gap:4px;border:1px solid var(--key-line);border-radius:10px;background:var(--key);padding:5px 4px 5px 8px}
.note.cur{border-color:var(--mark);box-shadow:0 0 0 1px var(--mark) inset}
.note .open{flex:1;min-width:0;text-align:left;background:none;border:0;cursor:pointer;padding:0}
.note .t{font-weight:700;font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.note .m{font-size:9.5px;color:var(--muted)}
.note .pv{display:flex;margin-top:2px;height:18px;overflow:hidden}
.note .pv svg{height:18px;width:auto;flex:none}
.note .del{flex:none;width:28px;height:28px;border-radius:8px;border:1px solid transparent;background:none;cursor:pointer;color:var(--muted);display:grid;place-items:center;padding:0}
.note .del svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.confirm{display:flex;gap:4px;align-items:center;font-size:11px;margin-left:auto}
.confirm .btn{height:26px;padding:0 8px;font-size:11px}
.shot{display:block;max-width:100%;max-height:84px;margin:0 auto;border:1px solid var(--rule);border-radius:8px;background:#fff;
  -webkit-touch-callout:default;user-select:auto}
.check{display:inline-flex;align-items:center;gap:6px;font-size:12px;cursor:pointer}
.check input{width:16px;height:16px;accent-color:var(--mark)}
.legend{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:2px 1px;text-align:center}
.legend div{display:flex;flex-direction:column;align-items:center;font-size:9.5px;font-weight:700;line-height:1.1;padding-bottom:3px;min-width:0}
.legend svg{height:22px;width:auto;overflow:visible;margin-bottom:2px}
.legend .h{font-weight:500;font-size:7.5px;color:var(--muted);padding:0;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel details summary{cursor:pointer}
.panel pre{font-size:9.5px!important}
/* a message sits over the word strip, wherever it is (placed by hint()), or at the foot of the screen */
.toast{position:absolute;left:16px;right:16px;bottom:6px;z-index:20;min-height:28px;display:flex;align-items:center;justify-content:center;text-align:center;
  background:var(--text);color:var(--sheet);padding:4px 10px;border-radius:9px;font-size:11.5px;line-height:1.3;box-shadow:0 4px 14px rgba(0,0,0,.25);pointer-events:none}
.warnline{color:var(--warn)}
"""
s = between(s, "html{height:100%;box-sizing:border-box}", "\n</style>", CSS)

# ---------------------------------------------------------------- the page: note strip, word strip, keys; panels inside the screen
s = between(s, '<div class="app" id="app">', '<div class="scrim" id="scrim" hidden></div>',
"""<div class="app" id="app">
  <main class="doc" id="doc" aria-label="Note: hold to see all of it" aria-expanded="false"
    title="Hold to see the whole note; there, tap to put the cursor and hold to go back to the keys"><div class="sheet" id="sheet"></div></main>
  <div class="strip">
    <div class="status" id="status" aria-live="polite"></div>
    <div class="cands" id="cands" hidden role="group" aria-label="English words for the sounds before the cursor"></div>
  </div>
  <div class="kb" id="kb" role="group" aria-label="Stemsyl keys, 3 × 3: hold the middle key of an edge for numbers, punctuation, options or cursor keys, and the centre key for the tick positions"></div>
  <div class="editbar" id="editbar" role="group" aria-label="Edit at the cursor">
    <button type="button" data-ed="bs" aria-label="Delete" title="Delete">⌫</button>
    <button type="button" data-ed="sp" aria-label="Space" title="Space">␣</button>
    <button type="button" data-ed="nl" aria-label="New line" title="New line">⏎</button>
  </div>
  <div class="toast" id="toast" hidden role="status"></div>

""")
s = swap(s, '<div class="seg" id="aidSeg"><button data-v="off">Nothing</button><button data-v="en">English</button><button data-v="ipa">IPA</button></div>',
         '<div class="seg" id="aidSeg"><button data-v="off">Nothing</button><button data-v="en">English</button><button data-v="ipa">IPA</button></div>\n'
         '  <div class="lbl">Word strip</div>\n'
         '  <div class="seg" id="stripSeg"><button data-v="above">Above keys</button><button data-v="below">Below keys</button></div>')
s = swap(s, '<button class="btn primary" id="newNote">New note</button>', '<button class="btn primary" id="newNote">New</button>')
s = swap(s, '<button class="btn" id="backupBtn">Save a backup file</button>', '<button class="btn" id="backupBtn">Save backup</button>')
s = swap(s, '>Restore from a backup</label>', '>Restore</label>')
s = swap(s, '\n<div class="toast" id="toast" hidden role="status"></div>\n', '\n</div>\n')

# the guide, for these keys
s = swap(s, """  <div class="lbl">How the keys work</div>
  <p class="fine" style="margin-top:0">Every key is one sound. The note groups the sounds of a word into syllables by itself: each vowel takes the consonant just before it on its left and the one just after it on its right. Any other consonant stands on a short stub of its own.</p>""",
"""  <div class="lbl">How the keys work</div>
  <p class="fine" style="margin-top:0">Each sound is one tick: pick where it goes, then its colour. The top row of keys is a consonant’s tick — up, centred or down — and the middle row a vowel’s. Tapping one shows its colours; picking a colour writes that sound and brings the tick positions back (✕ goes back without writing). The bottom row deletes, adds a space and starts a new line.</p>
  <p class="fine">Hold the middle key of an edge to bring up other keys: the top one for numbers (123), the left one for punctuation (?!), the right one for the options (opt) and the bottom one for cursor keys (↔). A key’s corner shows what holding it brings up; the keys showing now have their label filled in. Hold the centre key to come back to the tick positions, from any other keys or from a colour you’ve changed your mind about. The options are the buttons a bigger screen keeps along the top: <b>Notes</b>, <b>Title</b>, <b>Share</b>, <b>View</b> (the note in Stemsyl, English or IPA), <b>Menu</b> (this page), <b>Under</b> (English, IPA or nothing under each word), <b>Undo</b>, <b>New</b> note, and smaller or larger glyphs (A− · A+).</p>
  <p class="fine">Swipe sideways across the keys to move the cursor. The note is one line along the top that follows the cursor (a new line shows as ↵); swipe it sideways to read back. Hold it to see the whole note over the watch face, many lines at once. There, tap a spot to put the cursor there — a bar with delete, space and new line comes up for small fixes — and hold anywhere on the note to go back to the keys.</p>
  <p class="fine">The note groups the sounds of a word into syllables by itself: each vowel takes the consonant just before it on its left and the one just after it on its right. Any other consonant stands on a short stub of its own.</p>""")
s = swap(s, "After the sounds of a word, the strip above the keys offers", "After the sounds of a word, the word strip (above the keys, or below them: Menu › Word strip) offers")
s = swap(s, """  <p class="fine">The ◆ key is the name mark: it goes before a name, where English uses a capital letter. Numerals are dice on a 3 × 3 grid — count the lit squares.</p>
  <p class="fine">There are two layouts, switched at the top of the keyboard. <b>Keys</b> has a key for every sound. <b>3 × 3</b> asks for a tick position first, then its colour; hold its centre for numbers, punctuation and cursor keys, and swipe sideways across it to move the cursor.</p>""",
"""  <p class="fine">The ◆ name mark goes before a name, where English uses a capital letter; pasting English, or typing it on a physical keyboard, adds it. Numerals are dice on a 3 × 3 grid — count the lit squares.</p>
  <p class="fine">The whole app fits the screen of the 46 mm Apple Watch Series 12, 208 × 248 points (416 × 496 pixels), and shrinks to fit a smaller one, such as the 42 mm’s 187 × 223.</p>""")

# ---------------------------------------------------------------- script
# settings: the watch keeps its own glyph size (the phone keyboards keep theirs, under the same storage, untouched)
s = swap(s, "var S={notes:[],cur:null,prefs:{gs:56,aid:'off',view:'stemsyl',layout:'keys'}};",
         "var S={notes:[],cur:null,prefs:{wgs:40,aid:'off',view:'stemsyl',wstrip:'above'}};")
s = swap(s, "function clampGs(g){ return Math.max(32,Math.min(112,Math.round(g/8)*8)); }",
         "function clampGs(g){ return Math.max(24,Math.min(56,Math.round(g/8)*8)); }")
s = swap(s, """          /* settings another Stemsyl keyboard keeps in the same place (the watch keyboard's glyph size): kept as they are */""",
         """          /* settings the other Stemsyl keyboards keep in the same place (their glyph size, their layout): kept as they are */""")
s = swap(s, """          S.prefs.gs=clampGs(+o.prefs.gs||56); S.prefs.aid=['off','en','ipa'].indexOf(o.prefs.aid)>=0?o.prefs.aid:'off';
          S.prefs.view=VIEWS.indexOf(o.prefs.view)>=0?o.prefs.view:'stemsyl';
          S.prefs.layout=LAYOUTS.indexOf(o.prefs.layout)>=0?o.prefs.layout:'keys'; }""",
"""          S.prefs.wgs=clampGs(+o.prefs.wgs||40); S.prefs.aid=['off','en','ipa'].indexOf(o.prefs.aid)>=0?o.prefs.aid:'off';
          S.prefs.view=VIEWS.indexOf(o.prefs.view)>=0?o.prefs.view:'stemsyl';
          S.prefs.wstrip=o.prefs.wstrip==='below'?'below':'above'; }""")
s = swap(s, "S.prefs.gs", "S.prefs.wgs", count=s.count("S.prefs.gs"))
s = swap(s, "  $('noteCount').textContent=S.notes.length;\n", "  showNoteCount();\n", count=2)

# the cursor: the note strip scrolls sideways (only the strip) to keep it in sight
s = swap(s, "  if(car.scrollIntoView) car.scrollIntoView({block:'nearest'});\n}",
"""  showCaret(car);
}
/* keep the cursor in sight, with a little room around it: sideways in the one-line strip, up and down in the whole note */
function showCaret(car){
  var d=$('doc'), r=car.getBoundingClientRect(), dr=d.getBoundingClientRect(), room;
  if(reading){
    room=Math.min(24,dr.height/4);
    if(r.top<dr.top+room) d.scrollTop-=dr.top+room-r.top;
    else if(r.bottom>dr.bottom-room) d.scrollTop+=r.bottom-(dr.bottom-room);
    return;
  }
  room=Math.min(28,dr.width/4);
  if(r.left<dr.left+room) d.scrollLeft-=dr.left+room-r.left;
  else if(r.right>dr.right-room) d.scrollLeft+=r.right-(dr.right-room);
}""")

# the note: a hold shows all of it; there a tap puts the cursor and a hold goes back to the keys
s = between(s, "$('sheet').addEventListener('click',function(e){", "/* ---------- status line ---------- */", r"""/* ---------- the note ----------
   Hold the one-line strip to see the whole note over the watch face (a tap on the strip only says so, so a stray tap
   changes nothing). In the whole note a tap puts the cursor where it lands and brings up a bar with delete, space and
   new line for small fixes; a hold anywhere on the note goes back to the keys. */
var reading=false, noteHold=0, noteHoldFired=false, noteX=0, noteY=0, readHints=0, stripHints=0;
function setReading(on){
  reading=!!on; var app=$('app');
  app.classList.toggle('reading',reading); app.classList.remove('editing');
  $('doc').setAttribute('aria-expanded',String(reading));
  $('doc').setAttribute('aria-label',reading?'The whole note: tap to put the cursor, hold to go back to the keys':'Note: hold to see all of it');
  $('doc').scrollTop=0; $('doc').scrollLeft=0;
  renderDoc();
  if(reading&&readHints<1){ readHints++; hint('Tap to put the cursor · hold to go back to the keys',2600); }
}
/* the cursor to the point (x, y) on the note */
function caretToPoint(x,y){
  if(document.activeElement===$('title')) $('title').blur();
  flushTyping();
  var hit=document.elementFromPoint(x,y), el=hit&&hit.closest?hit.closest('#sheet [data-a]'):null;
  if(el){
    if(el.classList.contains('nl')||el.classList.contains('end')) return moveCaret(+el.dataset.a);
    return moveCaret(caretFromPoint(el,x));
  }
  /* empty space: the end of the row that was tapped, or the end of the note */
  var cells=[].slice.call($('sheet').querySelectorAll('.g,.sp,.nl')), best=null;
  cells.forEach(function(c){ var r=c.getBoundingClientRect();
    if(y>=r.top-4&&y<r.bottom+4&&r.left<=x+1) if(!best||r.right>best.r) best={i:c.classList.contains('nl')?+c.dataset.a:+c.dataset.b,r:r.right}; });
  moveCaret(best?best.i:doc.length);
}
$('doc').addEventListener('pointerdown',function(e){
  noteHoldFired=false; noteX=e.clientX; noteY=e.clientY; clearTimeout(noteHold);
  noteHold=setTimeout(function(){
    noteHoldFired=true; if(navigator.vibrate) navigator.vibrate(30);
    setReading(!reading);
  },420);
});
/* moving is scrolling the note, not holding it */
$('doc').addEventListener('pointermove',function(e){ if(Math.abs(e.clientX-noteX)>10||Math.abs(e.clientY-noteY)>10) clearTimeout(noteHold); });
['pointerup','pointercancel','pointerleave'].forEach(function(ev){ $('doc').addEventListener(ev,function(){ clearTimeout(noteHold); }); });
$('doc').addEventListener('click',function(e){
  if(noteHoldFired){ noteHoldFired=false; e.preventDefault(); return; }
  if(!reading){ if(stripHints<2){ stripHints++; hint('Hold the note to see all of it',1500); } return; }
  caretToPoint(e.clientX,e.clientY);
  if(!$('app').classList.contains('editing')){
    $('app').classList.add('editing'); $('toast').hidden=true;   /* the how-to message has done its job */
    var car=document.querySelector('#sheet .car'); if(car) showCaret(car);   /* the bar took some room: keep the cursor in sight */
  }
});
/* the bar for small fixes in the whole note: delete, space and new line at the cursor */
$('editbar').addEventListener('mousedown',function(e){ e.preventDefault(); });
$('editbar').addEventListener('click',function(e){
  var bt=e.target.closest('[data-ed]'); if(!bt) return;
  flushTyping();
  if(bt.dataset.ed==='bs') backspace();
  else if(bt.dataset.ed==='sp') insert(['sp']);
  else if(bt.dataset.ed==='nl') insert(['nl']);
});

""")
s = swap(s, "  if(e.key==='Escape'&&overlayOpen()){ closeAll(); return; }\n",
         "  if(e.key==='Escape'&&overlayOpen()){ closeAll(); return; }\n  if(e.key==='Escape'&&reading){ setReading(false); return; }\n")
# a short message for a swipe; the others stay up as long as before
s = swap(s, "function hint(msg){ var t=$('toast'); t.textContent=msg; t.hidden=false; clearTimeout(toastT); toastT=setTimeout(function(){ t.hidden=true; },3000); }",
         """function hint(msg,ms){
  var t=$('toast'), st=document.querySelector('.strip'), app=$('app');
  t.textContent=msg; t.hidden=false;
  /* over the word strip, wherever it is; when it's put away, at the foot of the screen (above the edit bar) */
  if(st&&st.offsetParent!==null){
    t.style.left=t.style.right=(S.prefs.wstrip==='below'?16:4)+'px';
    if(S.prefs.wstrip==='below'){ t.style.top='auto'; t.style.bottom=(app.clientHeight-st.offsetTop-st.offsetHeight)+'px'; }
    else { t.style.bottom='auto'; t.style.top=st.offsetTop+'px'; }
  } else { t.style.left=t.style.right='16px'; t.style.top='auto'; t.style.bottom=(app.classList.contains('editing')?44:6)+'px'; }
  clearTimeout(toastT); toastT=setTimeout(function(){ t.hidden=true; },ms||3000);
}""")

# the status fits the watch
s = swap(s, """h='<span class="ipa" style="font-size:15px;color:var(--text)">/'+esc(ipaOf(run.pron))+'/</span><span>no English word sounds like this</span>';""",
         """h='<span class="ipa" style="font-size:12px;color:var(--text)">/'+esc(ipaOf(run.pron))+'/</span><span>no English word</span>';""")
s = swap(s, """(S.prefs.view!=='stemsyl'?' · showing <b>'+VIEWNAME[S.prefs.view]+'</b>':'')""",
         """(S.prefs.view!=='stemsyl'?' · <b>'+VIEWNAME[S.prefs.view]+'</b>':'')""")
s = swap(s, """'<span class="warnline">Not saved in this browser — back up from Notes</span>'""",
         """'<span class="warnline" title="Not saved in this browser — back up from Notes">Not saved</span>'""")

# picking a word goes back to the tick positions (as the 3 × 3 layout does)
s = swap(s, "  if(S.prefs.layout==='grid3'){ selectedPos=null; buildKb(); }\n", "  selectedPos=null; buildKb();\n")

# only the 3 × 3 keys: the full keyboard's key lists and builder go
s = between(s, "var MAIN=[].concat(", "var PNAME=", "")
s = between(s, "/* the full keyboard: a key for every sound */\nfunction keysHtml(){", "var selectedPos = null;", "")
s = swap(s, "var kbMode = 'sounds'; // sounds | nums | punct | nav", "var kbMode = 'sounds'; // sounds | nums | punct | nav | options")
s = swap(s, "var centerHoldTimer = null;\nvar centerHoldFired = false;",
         "var holdTimer = null;\nvar holdFired = false;   // a hold or a swipe just happened: the tap its lift may produce does nothing")

GRID = r"""/* ---------- the 3 × 3 keys ----------
   The tick positions: the top row is a consonant's tick (up, centred, down), the middle row a vowel's; pick one, then its colour.
   Held, the middle key of each edge brings up other keys: top numbers, left punctuation, right the options (the buttons a
   bigger screen keeps along the top), bottom cursor keys. Held, the centre key brings back the tick positions.
   The same four keys and the centre do this on every page of keys, a colour page too; the 9 · 0 key never does. */
var MODES=['sounds','nums','punct','nav','options'];
var HOLD_AT={1:'nums',3:'punct',5:'options',7:'nav'};
var MODE_TAG={nums:'123',punct:'?!',options:'opt',
  nav:'<svg class="lr" viewBox="0 0 14 10" aria-hidden="true"><path d="M1.8 5h10.4M4.6 2.2L1.8 5l2.8 2.8M9.4 2.2L12.2 5 9.4 7.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'};
var MODE_NAME={sounds:'the tick positions',nums:'numbers',punct:'punctuation',options:'options',nav:'cursor keys'};
var TICK_TAG='<svg viewBox="0 0 12 10" aria-hidden="true"><path d="M1.5 6.5h9" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
  +'<path d="M6 1.5v5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>';
/* what holding the key at position i brings up (null: nothing, as its keys are already showing, and a long press just types) */
function holdTarget(i){
  if(i===4) return kbMode!=='sounds'||selectedPos!==null?'sounds':null;
  var m=HOLD_AT[i]; return m&&m!==kbMode?m:null;
}
function holdMark(i){
  var t=holdTarget(i);
  if(t) return '<span class="hold-to" aria-hidden="true">'+(t==='sounds'?TICK_TAG:MODE_TAG[t])+'</span>';
  if(HOLD_AT[i]&&HOLD_AT[i]===kbMode) return '<span class="hold-to on" aria-hidden="true">'+MODE_TAG[kbMode]+'</span>';
  return '';
}
/* one key at grid position i: c = {cls, attrs, inner, title, aria, div} */
function cellHtml(c,i){
  var t=holdTarget(i), hold=t?'hold for '+MODE_NAME[t]:'', tg=c.div?'div':'button';
  var title=[c.title,hold].filter(Boolean).join(' — '), aria=[c.aria||c.title,hold].filter(Boolean).join(' — ');
  return '<'+tg+(c.div?'':' type="button"')+' class="cell '+c.cls+'"'+(c.attrs||'')+(t?' data-hold="'+t+'"':'')
    +(title?' title="'+esc(title)+'"':'')+(aria?' aria-label="'+esc(aria)+'"':'')+'>'+(c.inner||'')+holdMark(i)+'</'+tg+'>';
}
var TICKWORD={u:'up',c:'mid',d:'down'};
var NAVWORD={home:'Home',up:'Up',end:'End',left:'Left',enter:'Enter',right:'Right',bs:'Backspace',down:'Down',space:'Space'};
function tickIcon(pos){
  return '<svg viewBox="-3 13 24 38" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'+stem(9-5,9+5).replace('class="stem"','class="stem" style="stroke-width:2.6"')+tick(9,['ink',pos])+'</svg>';
}
function appIcon(d){ return '<svg class="ai" viewBox="0 0 24 24" aria-hidden="true">'+d+'</svg>'; }
var APP_ICON={
  notes:appIcon('<path d="M5 4h11l3 3v13H5z"/><path d="M8 10h8M8 14h8M8 18h5"/>'),
  title:appIcon('<path d="M4 20h16"/><path d="M14.5 5.5l3 3L9 17H6v-3z"/>'),
  share:appIcon('<path d="M12 3v12"/><path d="M8 7l4-4 4 4"/><path d="M6 11v9h12v-9"/>'),
  menu:appIcon('<path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/>'),
  undo:appIcon('<path d="M9 14L4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 010 11H11"/>'),
  add:appIcon('<path d="M6 3h8l4 4v14H6z"/><path d="M12 10v7M8.5 13.5h7"/>')
};
var AIDS=['off','en','ipa'], AIDNAME={off:'nothing',en:'English',ipa:'IPA'};
/* the options: what a bigger screen keeps along the top, and a few more */
function optionKeys(){
  var v=S.prefs.view, nv=VIEWS[(VIEWS.indexOf(v)+1)%VIEWS.length], a=S.prefs.aid, na=AIDS[(AIDS.indexOf(a)+1)%AIDS.length];
  var cat='<svg viewBox="3 12 36 40" aria-hidden="true">'+syllableInner('k',VCHAR.a,'t')+'</svg>';
  function opt(act,inner,label,title){ return {cls:'appk',attrs:' data-app="'+act+'"',title:title,inner:inner+'<span class="pos-lb small">'+esc(label)+'</span>'}; }
  return [
    opt('notes',APP_ICON.notes+'<span class="nc" id="noteCount">'+S.notes.length+'</span>','Notes','Your notes: open, add, delete, back up'),
    opt('title',APP_ICON.title,'Title','Rename this note'),
    opt('share',APP_ICON.share,'Share','Share the note as an image, English or IPA'),
    opt('view','<span class="vg">'+viewGlyph(v)+'</span>',VIEWNAME[v],'The note is showing '+VIEWNAME[v]+'; tap to show '+VIEWNAME[nv]),
    opt('menu',APP_ICON.menu,'Menu','View, paste and guide'),
    opt('aid','<span class="vg sm">'+cat+'</span><span class="uc'+(a==='ipa'?' ipa':'')+'">'+(a==='en'?'cat':a==='ipa'?'kæt':'·')+'</span>','Under',
        'Under each word: '+AIDNAME[a]+'; tap for '+AIDNAME[na]),
    opt('undo',APP_ICON.undo,'Undo','Undo'),
    opt('new',APP_ICON.add,'New','New note'),
    {div:true,cls:'appk split-diag',attrs:' role="group"',aria:'Glyph size',inner:
      '<button type="button" class="tri tri-9" data-app="smaller" aria-label="Smaller glyphs" title="Smaller glyphs"><span class="az">A−</span></button>'
     +'<button type="button" class="tri tri-0" data-app="larger" aria-label="Larger glyphs" title="Larger glyphs"><span class="az">A+</span></button>'
     +'<span class="diag-line"></span>'}
  ];
}
function grid3Html(){
  var cells=[], i;
  if(kbMode==='sounds'&&selectedPos===null){
    /* top row: a consonant's tick; middle row: a vowel's; bottom row: edit */
    [0,3,6,1,4,7].forEach(function(pi){
      var p=POSITIONS[pi], cons=p.type==='cons';
      cells.push({cls:'pos '+(cons?'side':'mid')+' row-'+p.pos,attrs:' data-pos="'+pi+'"',title:(cons?'Consonant ':'Vowel ')+TICKWORD[p.pos]+' tick',
        inner:'<span class="pos-icon">'+tickIcon(p.pos)+'</span><span class="pos-lb">'+(cons?'C ':'V ')+TICKWORD[p.pos]+'</span>'});
    });
    cells.push({cls:'pos nav',attrs:' data-nav="bs"',title:'Backspace',inner:'<span class="pos-lb big">⌫</span><span class="pos-lb small">backspace</span>'});
    cells.push({cls:'pos nav',attrs:' data-nav="space"',title:'Space',inner:'<span class="pos-lb big">␣</span><span class="pos-lb small">space</span>'});
    cells.push({cls:'pos nav',attrs:' data-nav="enter"',title:'Newline',inner:'<span class="pos-lb big">⏎</span><span class="pos-lb small">newline</span>'});
  } else if(kbMode==='sounds'){
    /* the chosen position's colours; the first key goes back without writing */
    var sel=POSITIONS[selectedPos], cmap=CONS_BY_POS[sel.pos];
    var opts=sel.type==='vow'?Object.entries(VOW_BY_POS[sel.pos]).map(function(e){ return e[1]; }):Object.keys(cmap).map(function(k){ return cmap[k]; });
    cells.push({cls:'sel',attrs:' data-unselect="1"',title:'Back to the tick positions',inner:'<span class="sel-x">✕</span><span class="pos-lb">'+sel.label+'</span>'});
    for(i=1;i<9;i++){
      var L=opts[i-1];
      if(L===undefined){ cells.push({div:true,cls:'empty'}); continue; }
      if(sel.type==='vow'){ var vt=vowelTick(VCHAR[L]);
        cells.push({cls:'colopt vow t-'+vt[0],attrs:' data-vow="'+L+'"',title:VNAME[L]?VNAME[L][0]+' as in '+VNAME[L][1]:L,
          inner:'<span class="col-glyph">'+keyGlyph(vt,10.5)+'</span><span class="col-lb">'+(VNAME[L]?VNAME[L][0]:L)+'</span>'}); }
      else cells.push({cls:'colopt cons t-'+CODE[L][0],attrs:' data-cons="'+L+'"',title:CONS_NAME[L]+' as in '+CONS_EX[L],
          inner:'<span class="col-glyph">'+consGlyph(L)+'</span><span class="col-lb">'+CONS_NAME[L]+'</span>'});
    }
  } else if(kbMode==='nums'){
    for(i=0;i<8;i++){ var ng=NUM_GRID[i];
      cells.push({cls:'pos num',attrs:' data-k="'+ng.k+'"',aria:'Numeral '+ng.label,
        inner:'<svg class="numdice" viewBox="4 6 40 52" aria-hidden="true">'+numeralInner(+ng.label)+'</svg><span class="pos-lb">'+ng.label+'</span>'}); }
    /* 9 and 0 share the last key, split corner to corner; holding it does nothing */
    cells.push({div:true,cls:'pos num split-diag',attrs:' role="group"',aria:'9 and 0',inner:
      '<button type="button" class="tri tri-9" data-k="d:9" aria-label="Numeral 9"><svg class="numdice" viewBox="4 6 40 52" aria-hidden="true">'+numeralInner(9)+'</svg><span class="pos-lb">9</span></button>'
     +'<button type="button" class="tri tri-0" data-k="d:0" aria-label="Numeral 0"><svg class="numdice" viewBox="4 6 40 52" aria-hidden="true">'+numeralInner(0)+'</svg><span class="pos-lb">0</span></button>'
     +'<span class="diag-line"></span>'});
  } else if(kbMode==='punct'){
    PUNCT_GRID.forEach(function(pg){ var pn=PNAME[pg.k.slice(2)];
      cells.push({cls:'pos punct',attrs:' data-k="'+pg.k+'"',title:pn||'',inner:'<span class="pos-lb big">'+pg.label+'</span>'}); });
  } else if(kbMode==='nav'){
    NAV_GRID.forEach(function(nv){
      cells.push({cls:'pos nav',attrs:' data-nav="'+nv.act+'"',title:NAVWORD[nv.act],inner:'<span class="pos-lb big">'+nv.icon+'</span><span class="pos-lb small">'+nv.label+'</span>'}); });
  } else cells=optionKeys();
  return '<div class="grid3-wrap"><div class="grid3">'+cells.map(cellHtml).join('')+'</div></div>';
}
function buildKb(){ $('kb').innerHTML=grid3Html(); }
/* the option keys show the note count, the view and what goes under each word: redraw them when those change */
function refreshAppKeys(){ if(kbMode==='options') buildKb(); }
function showNoteCount(){ var c=$('noteCount'); if(c) c.textContent=S.notes.length; }
function appAction(a){
  flushTyping();
  if(a==='notes') openNotes();
  else if(a==='title') openTitle();
  else if(a==='share') openShare();
  else if(a==='view') cycleView();
  else if(a==='menu') openMenu();
  else if(a==='aid'){
    S.prefs.aid=AIDS[(AIDS.indexOf(S.prefs.aid)+1)%AIDS.length]; syncMenu(); renderDoc(); scheduleSave(); refreshAppKeys();
    var m=S.prefs.aid==='off'?'Nothing under each word':AIDNAME[S.prefs.aid]+' under each word';
    if(S.prefs.aid!=='off'&&!capsOn()) m+=' (not while the note shows '+VIEWNAME[S.prefs.view]+')';
    hint(m);
  }
  else if(a==='undo'){ P.buf=''; if(undoStack.length) undo(); else hint('Nothing to undo'); }
  else if(a==='new'){ var n=newNote(); open(n); save(); closeAll(); hint('New note'); }
  else if(a==='smaller'||a==='larger'){
    var g=clampGs(S.prefs.wgs+(a==='larger'?8:-8));
    if(g===S.prefs.wgs){ hint(a==='larger'?'These are the largest glyphs':'These are the smallest glyphs'); return; }
    S.prefs.wgs=g; setSize(); renderDoc(); scheduleSave(); hint('Glyph size '+Math.round(g/64*100)+'%');
  }
}

"""
s = between(s, "/* the 3 × 3 keyboard: a tick position, then its colour */\nfunction grid3Html(){", "function flushTyping(){", GRID)

# the full keyboard's tap handler, the layout switch and its hold-to-repeat delete go, and the 3 × 3 keys get their own
# holds: the middle key of each edge for a set of keys, the centre for the tick positions
HANDLERS = r"""/* ---------- the 3 × 3 keys: holds, swipes and taps ----------
   Held for a moment, a key with a corner label brings up those keys (see holdTarget). A quick sideways swipe moves the cursor. */
$('kb').addEventListener('pointerdown',function(e){
  holdFired=false;   /* a new touch: what the last swipe or hold was waiting to swallow is over */
  swipeSX=e.clientX; swipeSY=e.clientY; swipeST=Date.now(); swipeMoved=false;
  clearTimeout(holdTimer);
  var cell=e.target.closest('.cell[data-hold]');
  if(!cell) return;
  var to=cell.dataset.hold;
  holdTimer=setTimeout(function(){
    holdFired=true; kbMode=to; selectedPos=null; buildKb();
    if(navigator.vibrate) navigator.vibrate(30);
  },420);
});
$('kb').addEventListener('pointermove',function(e){
  if(!swipeSX) return;
  var dx=e.clientX-swipeSX, dy=e.clientY-swipeSY;
  if(Math.abs(dx)>12||Math.abs(dy)>12) swipeMoved=true;
  if(Math.abs(dx)>18||Math.abs(dy)>18) clearTimeout(holdTimer);   /* moving is a swipe, not a hold */
});
function endTouch(e,lifted){
  clearTimeout(holdTimer);
  if(lifted&&swipeSX){
    var dx=e.clientX-swipeSX, dy=e.clientY-swipeSY, dt=Date.now()-swipeST, absX=Math.abs(dx), absY=Math.abs(dy), s;
    /* a quick sideways swipe: the cursor moves one sound for every 36 pixels */
    if(absX>40&&absX>absY*1.2&&dt<600){
      var steps=Math.max(1,Math.floor(absX/36));
      flushTyping();
      if(dx<0){ for(s=0;s<steps;s++) moveCaret(caret-1); hint('← '+steps,1200); }
      else { for(s=0;s<steps;s++) moveCaret(caret+1); hint(steps+' →',1200); }
      e.preventDefault();
      holdFired=true;   /* the tap this lift may still produce does nothing */
    }
  }
  swipeSX=0; swipeSY=0; swipeST=0;
  setTimeout(function(){ swipeMoved=false; },50);
}
$('kb').addEventListener('pointerup',function(e){ endTouch(e,true); });
$('kb').addEventListener('pointercancel',function(e){ endTouch(e,false); });
/* leaving the keys ends a hold or a swipe; moving about inside them does not */
$('kb').addEventListener('pointerleave',function(e){ endTouch(e,false); });

$('kb').addEventListener('click',function(e){
  if(holdFired){ holdFired=false; e.preventDefault(); return; }
  if(swipeMoved){ e.preventDefault(); return; }
  var ap=e.target.closest('[data-app]');
  if(ap){ appAction(ap.dataset.app); return; }
  var tri=e.target.closest('.tri');
  if(tri&&tri.dataset.k){
    var k=tri.dataset.k, ty=k.charAt(0), v=k.slice(2);
    flushTyping();
    if(ty==='d') insert(['d',+v]);
    else if(ty==='p') insert(['p',v]);
    return;
  }
  var cell=e.target.closest('.cell');
  if(!cell) return;
  if(cell.dataset.pos!==undefined){ var idx=+cell.dataset.pos; selectedPos=(selectedPos===idx?null:idx); buildKb(); return; }
  if(cell.dataset.unselect!==undefined){ selectedPos=null; buildKb(); return; }
  if(cell.dataset.cons||cell.dataset.vow){ selectedPos=null; insert(['s',cell.dataset.cons||cell.dataset.vow]); buildKb(); return; }
  if(cell.dataset.k){
    var k2=cell.dataset.k, ty2=k2.charAt(0), v2=k2.slice(2);
    flushTyping();
    if(ty2==='p') insert(['p',v2]);
    else if(ty2==='d') insert(['d',+v2]);
    else if(ty2==='c'||ty2==='v') insert(['s',v2]);
    return;
  }
  if(cell.dataset.nav){
    var act=cell.dataset.nav;
    flushTyping();
    if(act==='left') moveCaret(caret-1);
    else if(act==='right') moveCaret(caret+1);
    else if(act==='up'||act==='home') moveCaret(0);
    else if(act==='down'||act==='end') moveCaret(doc.length);
    else if(act==='bs') backspace();
    else if(act==='space') insert(['sp']);
    else if(act==='enter') insert(['nl']);
  }
});

"""
s = between(s, "$('kb').addEventListener('click',function(e){ var b=e.target.closest('[data-layout]');",
            "/* ---------- physical keyboard: English words ---------- */", HANDLERS)
s = swap(s, "closest('.key,.tb,.btn,.cand')", "closest('.cell,.tri,.btn,.cand,.x')")

# panels: opened from the app keys; the title has a panel of its own
s = swap(s, "function openPanel(id){ closeAll(); $('scrim').hidden=false; $(id).hidden=false; if(id==='menuPanel'){ var p=$('pasteIn'); if(p) setTimeout(function(){ p.focus(); },50); } }\n"
            "function closeAll(){ ['notesPanel','sharePanel','menuPanel'].forEach(function(p){ $(p).hidden=true; }); $('scrim').hidden=true; }",
         "function openPanel(id){ closeAll(); $('scrim').hidden=false; var p=$(id); p.hidden=false; p.scrollTop=0; }\n"
         "function closeAll(){ ['notesPanel','titlePanel','sharePanel','menuPanel'].forEach(function(p){ $(p).hidden=true; }); $('scrim').hidden=true; }")
s = swap(s, "$('notesBtn').addEventListener('click',function(){ renderNotes(); refreshSaveAvail(); openPanel('notesPanel'); });",
         "function openNotes(){ renderNotes(); refreshSaveAvail(); openPanel('notesPanel'); }")
s = swap(s, "hint('New note — tap its title to rename it');", "hint('New note');")
s = swap(s, "$('title').addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); this.blur(); } });",
         "$('title').addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); this.blur(); closeAll(); } });\n"
         "function openTitle(){ var t=$('title'); t.value=note.title; openPanel('titlePanel'); setTimeout(function(){ try{ t.focus(); t.select(); }catch(e){} },60); }\n"
         "$('titleDone').addEventListener('click',closeAll);")
s = swap(s, "$('menuBtn').addEventListener('click',function(){ syncMenu(); openPanel('menuPanel'); });",
         "function openMenu(){ syncMenu(); openPanel('menuPanel'); }")
s = swap(s, "  $('sizeVal').textContent=Math.round(S.prefs.wgs/64*100)+'%';\n}",
         "  [].forEach.call($('stripSeg').querySelectorAll('button'),function(b){ b.setAttribute('aria-pressed',b.dataset.v===S.prefs.wstrip?'true':'false'); });\n"
         "  $('sizeVal').textContent=Math.round(S.prefs.wgs/64*100)+'%';\n}\n"
         "/* the word strip above the keys, or below them */\n"
         "function applyWordStrip(){ $('app').classList.toggle('words-below',S.prefs.wstrip==='below'); }\n"
         "$('stripSeg').addEventListener('click',function(e){ var b=e.target.closest('button'); if(!b) return; S.prefs.wstrip=b.dataset.v; applyWordStrip(); syncMenu(); scheduleSave(); });")
s = swap(s, "setSize(); renderViewBtn(); buildKb(); renderDoc();", "setSize(); renderViewBtn(); applyWordStrip(); buildKb(); renderDoc();")
s = swap(s, "S.prefs.aid=b.dataset.v; syncMenu(); renderDoc(); scheduleSave(); });",
         "S.prefs.aid=b.dataset.v; syncMenu(); renderDoc(); scheduleSave(); refreshAppKeys(); });")
s = between(s, "function renderViewBtn(){", "/* ---------- export: one SVG of the whole note, then a PNG from it ---------- */",
"""function viewGlyph(v){
  if(v==='stemsyl') return '<svg viewBox="3 12 36 40" aria-hidden="true">'+syllableInner('k',VCHAR.a,'t')+'</svg>';
  return v==='en'?'Ab':'<span class="ipa">/ə/</span>';
}
/* the View key (with the app keys) shows what the note is showing; tapping it moves on to the next */
function renderViewBtn(){ refreshAppKeys(); }
function cycleView(){
  S.prefs.view=VIEWS[(VIEWS.indexOf(S.prefs.view)+1)%VIEWS.length];
  renderViewBtn(); renderDoc(); scheduleSave();
}

""")
s = swap(s, "$('shareBtn').addEventListener('click',function(){ flushTyping(); openPanel('sharePanel'); refreshShare(); });",
         "function openShare(){ flushTyping(); openPanel('sharePanel'); refreshShare(); }")

# the layout is gone from the fit-to-keyboard code and the test hook
s = swap(s, "window.__ss={setLayout:setLayout,get layout(){return S.prefs.layout;},parseText:parseText,",
         "window.__ss={get mode(){return kbMode;},setMode:function(m){ if(MODES.indexOf(m)>=0){ kbMode=m; selectedPos=null; buildKb(); } },app:appAction,\n"
         "  get prefs(){return S.prefs;},get reading(){return reading;},setReading:function(on){ setReading(on); },\n"
         "  setWordStrip:function(v){ S.prefs.wstrip=v; applyWordStrip(); syncMenu(); },parseText:parseText,")

# ================================================================ the Latin keys, and a text box they type into
# Held on the tick positions, the centre key brings up the Latin letters (and held there, the tick positions again); from
# the other keys it brings back whichever letters were in use. A group of letters, then the letter, as a tick position,
# then its colour. In the note, the letters make an English word that is written in Stemsyl (from the word list) when
# it is finished with space, a new line, punctuation or a word from the strip. The note's title and the menu's English
# box take the same keys, in a text box at the top of the screen, so no other keyboard is needed.
LATIN_CSS = r"""
/* ---------- the Latin keys: a group of letters, then the letter ---------- */
.grid3 .cell .lat-lb{font-size:13px;font-size:clamp(11px,8.5cqh,15px);font-weight:700;letter-spacing:.05em;line-height:1.1;white-space:nowrap}
.grid3 .cell .lat-lb .lat-sh{margin-left:3px;color:var(--mark)}
.grid3 .cell.lat.shifted .lat-lb .lat-sh{background:var(--mark);color:var(--mark-ink);border-radius:3px;padding:0 2px}
.grid3 .cell .lat-big{font-size:20px;font-size:clamp(15px,13cqh,24px);font-weight:700;line-height:1}
.grid3 .cell.lat-opt.shift.on{background:var(--mark);color:var(--mark-ink);border-color:var(--mark)}
/* the letters typed so far, at the head of the word strip */
.typed{flex:none;font:600 12.5px/1 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--mark-soft);color:var(--text);padding:6px 7px;border-radius:7px;white-space:nowrap}
/* ---------- a text box with the Latin keys under it: the note's title, or English to write in Stemsyl ---------- */
.field{flex:none;display:flex;flex-direction:column;gap:3px;margin-bottom:2px;padding:3px 10px 5px;background:var(--sheet);border:1px solid var(--rule);
  border-radius:var(--ri) var(--ri) 8px 8px}
.app.fielding .doc,.app.fielding .strip{display:none}
.fhead{display:flex;align-items:center;gap:6px;padding-left:12px;min-height:26px}
.fhead .sp2{flex:1}
.flabel{font-size:9.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.fhead .x{width:26px;height:26px;border-radius:13px}
.frow{display:flex;gap:5px;align-items:flex-end}
.field .title{flex:1;min-width:0;width:auto;height:34px}
.field textarea{flex:1;min-width:0;width:auto;min-height:0;height:46px;resize:none;padding:4px 7px;line-height:1.2}
.field .btn{flex:none;height:34px;padding:0 9px}
"""
s = swap(s, "\n/* ---------- panels and messages, inside the watch screen ---------- */", LATIN_CSS + "\n/* ---------- panels and messages, inside the watch screen ---------- */")

# the text box, at the top of the screen (shown only while it is in use); the title and the English box move into it
s = swap(s, '<div class="app" id="app">\n  <main class="doc"',
'''<div class="app" id="app">
  <div class="field" id="field" hidden>
    <div class="fhead"><span class="flabel" id="fieldLabel">Title</span><span class="sp2"></span>
      <button type="button" class="x" id="fieldX" aria-label="Cancel" title="Cancel"><svg viewBox="0 0 16 16"><path d="M3 3l10 10M13 3L3 13"/></svg></button></div>
    <div class="frow">
      <input class="title" id="title" maxlength="80" autocomplete="off" spellcheck="false" aria-label="Note title" inputmode="none" enterkeyhint="done">
      <textarea id="pasteIn" rows="2" placeholder="Practice makes perfect." aria-label="English to write in Stemsyl" inputmode="none" spellcheck="false" autocomplete="off"></textarea>
      <button type="button" class="btn primary" id="fieldGo">Done</button>
    </div>
  </div>
  <main class="doc"''')
s = between(s, '<div class="lbl">Paste English</div>', '\n\n  <div class="lbl">Consonants',
'''<div class="lbl">Write English</div>
  <div class="row"><button class="btn primary" id="writeEn">Write English…</button></div>
  <p class="fine">A box with the Latin keys under it: type (or paste) English, and <b>Insert</b> writes each word in Stemsyl at the cursor. A word that isn’t in the word list is skipped, and you can spell it with the sound keys. You can also type English straight into the note with the Latin keys, or paste it onto the page.</p>''')

# the guide
s = swap(s, "Hold the centre key to come back to the tick positions, from any other keys or from a colour you’ve changed your mind about.",
         "Hold the centre key to come back to your letters (the tick positions, or the Latin letters if that’s what you were typing), from any other keys or from a colour or group you’ve changed your mind about. On the letters themselves, holding the centre switches between the tick positions and the Latin letters.")
s = swap(s, """  <p class="fine">Swipe sideways across the keys to move the cursor.""",
"""  <p class="fine"><b>Latin letters.</b> Tap a group of letters, then the letter. ⇧ makes the next letter a capital (a capital in the middle of a sentence marks a name), and ' goes inside a word, as in don’t. As you type, the word strip offers words that begin with your letters; tapping one, or space, a new line or punctuation, writes the word in Stemsyl. A word that isn’t in the word list stays typed, for you to fix. The same keys type the note’s <b>Title</b> and the English you <b>Write</b> from the menu, in a box at the top of the screen.</p>
  <p class="fine">Swipe sideways across the keys to move the cursor.""")

# ---- the word list: spellings that begin with the letters typed so far
s = swap(s, "  return {load:load,candidates:candidates,lookup:lookup,exact:exact,loadAll:loadAll,",
"""  /* longer spellings that begin with the letters typed so far, commonest first: everyday dictionary words, then the rest */
  function prefix(p,n){
    load(); var dict=[], rest=[], seen=Object.create(null), i, w;
    for(i=0;i<SP.length&&dict.length<n;i++){
      w=SP[i]; if(BLK[i]||seen[w]||w.length<=p.length||w.lastIndexOf(p,0)!==0) continue;
      seen[w]=1; if(isDict(i)) dict.push(w); else if(rest.length<n) rest.push(w);
    }
    return dict.concat(rest).slice(0,n);
  }
  return {load:load,candidates:candidates,lookup:lookup,exact:exact,prefix:prefix,loadAll:loadAll,""")

# ---- a word typed in Latin letters that isn't in the word list stays typed when it's finished with space, a new line or
# punctuation (the letters can be fixed); moving the cursor elsewhere still lets it go, as before
s = swap(s, """function commitBuf(){
  var w=P.buf; P.buf='';
  if(!w) return;
  var toks=wordTokens(w,sentenceStart(doc,caret)&&!(caret>0&&doc[caret-1][0]==='nm'));
  if(toks){ if(caret>0&&doc[caret-1][0]==='nm'&&toks[0][0]==='nm') toks.shift(); insertMany(toks); return true; }
  hint('“'+w+'” isn’t in the word list — spell it with the sound keys.'); renderStatus(); return false;
}""", """function commitBuf(keep){
  var w=P.buf;
  if(!w) return;
  var toks=wordTokens(w,sentenceStart(doc,caret)&&!(caret>0&&doc[caret-1][0]==='nm'));
  if(toks){ P.buf=''; if(caret>0&&doc[caret-1][0]==='nm'&&toks[0][0]==='nm') toks.shift(); insertMany(toks); return true; }
  if(!keep) P.buf='';
  hint('“'+w+'” isn’t in the word list — '+(keep?'fix it, or spell it with the sound keys':'spell it with the sound keys.')); renderStatus(); return false;
}""")
s = swap(s, "  else if(k==='Enter'){ e.preventDefault(); flushTyping(); insert(['nl']); }",
            "  else if(k==='Enter'){ e.preventDefault(); if(P.buf&&commitBuf(true)===false) return; insert(['nl']); }")
s = swap(s, "  else if(k===' '){ e.preventDefault(); if(flushTyping()===false&&caret>0&&doc[caret-1][0]==='sp') return; insert(['sp']); }",
            "  else if(k===' '){ e.preventDefault(); if(P.buf&&commitBuf(true)===false) return; insert(['sp']); }")
s = swap(s, "  else if(k.length===1&&PIN[k]){ e.preventDefault(); flushTyping(); insert(['p',PIN[k]]); }",
            "  else if(k.length===1&&PIN[k]){ e.preventDefault(); if(P.buf&&commitBuf(true)===false) return; insert(['p',PIN[k]]); }")
s = swap(s, "  if(e.key==='Escape'&&overlayOpen()){ closeAll(); return; }\n  if(e.key==='Escape'&&reading){ setReading(false); return; }\n",
            "  if(e.key==='Escape'&&fieldEl){ e.preventDefault(); closeField(false); return; }\n"
            "  if(e.key==='Escape'&&overlayOpen()){ closeAll(); return; }\n  if(e.key==='Escape'&&reading){ setReading(false); return; }\n")

# ---- the word strip: while a word is being typed in Latin letters, the letters so far and longer words that begin with them
s = between(s, "function renderCands(run){", "function pickCand(c){", r"""function renderCands(run){
  var key=P.buf?'P|'+P.buf:(run?run.a+'|'+run.pron+'|'+run.spelled:'');
  if(key!==candKey){
    candKey=key; CAND_RUN=run;
    try {
      if(P.buf){
        var low=P.buf.toLowerCase().replace(/’/g,"'"), cap=/^[A-Z]/.test(P.buf);
        CANDS=WORDS.prefix(low,10).map(function(w){ return {w:cap?capFirst(w):w,typed:true}; });
      } else CANDS=run?WORDS.candidates(run.pron,14):[];
    } catch(e) {
      CANDS=[];
      /* visible error so silent failures are diagnosable */
      $('status').innerHTML='<span style="color:#ff6b6b">lookup error: '+esc(e.message)+'</span>';
    }
    var h=P.buf?'<span class="typed" aria-label="Typed so far">'+esc(P.buf)+'</span>':'';
    CANDS.forEach(function(c,k){
      if(c.typed){ h+='<button type="button" class="cand'+(k===0?' top':'')+'" data-c="'+k+'" aria-label="'+esc(c.w)+'">'+esc(c.w)+'</button>'; return; }
      var cur=run.spelled&&c.exact&&c.w.toLowerCase()===run.spelled.toLowerCase();
      h+='<button type="button" class="cand'+(c.exact?' ex':'')+(cur?' cur':'')+(k===0&&!cur&&!run.spelled?' top':'')+'" data-c="'+k+'" aria-label="'+esc(c.w)+(c.exact?'':' — adds its other sounds')+'">'
        +esc(c.w)+(c.exact?'':'<span class="more">…</span>')+'</button>';
    });
    $('cands').innerHTML=h; $('cands').scrollLeft=0;
  }
  var show=P.buf?CANDS.length>0:CANDS.length>0&&!(run&&run.spelled&&CANDS.length===1&&CANDS[0].exact);
  $('cands').hidden=!show; $('status').hidden=show;
}
""")
s = swap(s, "function pickCand(c){\n  var run=CAND_RUN; if(!c||!run) return;", "function pickCand(c){\n  if(c&&c.typed) return pickTyped(c);\n  var run=CAND_RUN; if(!c||!run) return;")
s = swap(s, "$('cands').addEventListener('mousedown',function(e){ e.preventDefault(); });",
"""/* a word from the strip while typing in Latin letters: written in Stemsyl, with a space after it */
function pickTyped(c){
  P.buf=c.w;
  if(commitBuf(true)===false) return;
  if(caret>=doc.length||doc[caret][0]!=='sp'&&doc[caret][0]!=='nl'){ doc.splice(caret,0,['sp']); autoSp=caret; caret++; }
  else { caret++; autoSp=-1; }
  candKey=null; edited(); latinSel=null; buildKb();
}
$('cands').addEventListener('mousedown',function(e){ e.preventDefault(); });""")

# ---- the 3 × 3 keys: the Latin letters, and the centre key's letters
s = swap(s, "var MODES=['sounds','nums','punct','nav','options'];",
         "var MODES=['sounds','latin','nums','punct','nav','options'];\n"
         "var LATIN=['abcde','fghij','klmno','pqrst','uvwxy',\"z'⇧\"];\n"
         "var latinSel=null, shiftOn=false, lastLetters='sounds';          /* the Latin keys: the group chosen, shift, the letters last in use */\n"
         "var fieldEl=null, fieldKind='', fieldPrev=null, fieldOrig='';    /* the text box the keys type into, when one is open */")
s = swap(s, "var MODE_TAG={nums:'123',punct:'?!',options:'opt',", "var MODE_TAG={latin:'abc',nums:'123',punct:'?!',options:'opt',")
s = swap(s, "var MODE_NAME={sounds:'the tick positions',", "var MODE_NAME={sounds:'the tick positions',latin:'the Latin letters',")
s = swap(s, """function holdTarget(i){
  if(i===4) return kbMode!=='sounds'||selectedPos!==null?'sounds':null;
  var m=HOLD_AT[i]; return m&&m!==kbMode?m:null;
}""", """function holdTarget(i){
  if(i===4){
    if(fieldEl) return kbMode!=='latin'||latinSel!==null?'latin':null;       /* a text box takes Latin letters only */
    if(kbMode==='sounds') return selectedPos!==null?'sounds':'latin';        /* on the letters: switch alphabet */
    if(kbMode==='latin') return latinSel!==null?'latin':'sounds';
    return lastLetters;                                                      /* elsewhere: back to the letters in use */
  }
  var m=HOLD_AT[i];
  return m&&m!==kbMode&&!(fieldEl&&m==='options')?m:null;
}""")
s = swap(s, "  } else if(kbMode==='nums'){\n    for(i=0;i<8;i++){", r"""  } else if(kbMode==='latin'&&latinSel===null){
    /* groups of letters (the last: z, the apostrophe and shift); then delete, space and new line */
    LATIN.forEach(function(g,gi){
      var shown=g.replace('⇧','').split('').map(function(ch){ return shiftOn&&ch!=="'"?ch.toUpperCase():ch; }).join('');
      cells.push({cls:'pos lat'+(gi===5&&shiftOn?' shifted':''),attrs:' data-lg="'+gi+'"',title:'Letters '+g.replace('⇧','').split('').join(' ')+(gi===5?' and shift':''),
        inner:'<span class="lat-lb">'+esc(shown)+(gi===5?'<span class="lat-sh">⇧</span>':'')+'</span>'});
    });
    cells.push({cls:'pos nav',attrs:' data-nav="bs"',title:'Backspace',inner:'<span class="pos-lb big">⌫</span><span class="pos-lb small">backspace</span>'});
    cells.push({cls:'pos nav',attrs:' data-nav="space"',title:'Space',inner:'<span class="pos-lb big">␣</span><span class="pos-lb small">space</span>'});
    cells.push({cls:'pos nav',attrs:' data-nav="enter"',title:'Newline',inner:'<span class="pos-lb big">⏎</span><span class="pos-lb small">newline</span>'});
  } else if(kbMode==='latin'){
    /* the group's letters; the first key goes back without typing */
    var grp=LATIN[latinSel].split('');
    cells.push({cls:'sel',attrs:' data-lunselect="1"',title:'Back to the letter groups',inner:'<span class="sel-x">✕</span><span class="pos-lb">'+esc(LATIN[latinSel].replace('⇧',''))+'</span>'});
    for(i=1;i<9;i++){
      var lc=grp[i-1];
      if(lc===undefined){ cells.push({div:true,cls:'empty'}); continue; }
      if(lc==='⇧'){ cells.push({cls:'lat-opt shift'+(shiftOn?' on':''),attrs:' data-lat="shift"',title:shiftOn?'Shift is on: tap to turn it off':'Shift: the next letter is a capital',
        inner:'<span class="lat-big">⇧</span>'}); continue; }
      var sc=shiftOn&&lc!=="'"?lc.toUpperCase():lc;
      cells.push({cls:'lat-opt',attrs:' data-lat="'+lc+'"',title:lc==="'"?'Apostrophe':'Letter '+sc,inner:'<span class="lat-big">'+esc(sc)+'</span>'});
    }
  } else if(kbMode==='nums'){
    for(i=0;i<8;i++){""")

# ---- holds, swipes and taps: the centre's letters; the Latin keys; the text box
s = swap(s, "    holdFired=true; kbMode=to; selectedPos=null; buildKb();",
            "    holdFired=true; if(!fieldEl&&(to==='sounds'||to==='latin')) lastLetters=to; kbMode=to; selectedPos=null; latinSel=null; buildKb();")
s = swap(s, """      flushTyping();
      if(dx<0){ for(s=0;s<steps;s++) moveCaret(caret-1); hint('← '+steps,1200); }
      else { for(s=0;s<steps;s++) moveCaret(caret+1); hint(steps+' →',1200); }""",
"""      if(fieldEl) fieldMove(dx<0?fieldEl.selectionStart-steps:fieldEl.selectionEnd+steps);
      else { flushTyping(); for(s=0;s<steps;s++) moveCaret(dx<0?caret-1:caret+1); }
      hint(dx<0?'← '+steps:steps+' →',1200);""")
s = between(s, "  var tri=e.target.closest('.tri');\n  if(tri&&tri.dataset.k){\n    var k=tri.dataset.k, ty=k.charAt(0), v=k.slice(2);",
            "/* ---------- physical keyboard: English words ---------- */", r"""  var tri=e.target.closest('.tri');
  if(tri&&tri.dataset.k){ keyK(tri.dataset.k); return; }
  var cell=e.target.closest('.cell');
  if(!cell) return;
  if(cell.dataset.pos!==undefined){ var idx=+cell.dataset.pos; selectedPos=(selectedPos===idx?null:idx); buildKb(); return; }
  if(cell.dataset.unselect!==undefined){ selectedPos=null; buildKb(); return; }
  if(cell.dataset.cons||cell.dataset.vow){ selectedPos=null; flushTyping(); insert(['s',cell.dataset.cons||cell.dataset.vow]); buildKb(); return; }
  if(cell.dataset.lg!==undefined){ var gi=+cell.dataset.lg; latinSel=(latinSel===gi?null:gi); buildKb(); return; }
  if(cell.dataset.lunselect!==undefined){ latinSel=null; buildKb(); return; }
  if(cell.dataset.lat){ typeLatin(cell.dataset.lat); latinSel=null; buildKb(); return; }
  if(cell.dataset.k){ keyK(cell.dataset.k); return; }
  if(cell.dataset.nav) navAct(cell.dataset.nav);
});
/* a numeral, punctuation or sound key: into the text box when one is open; else into the note, after writing any word
   being typed in Latin letters (one that isn't in the word list stays, to be fixed) */
function keyK(k){
  var ty=k.charAt(0), v=k.slice(2);
  if(fieldEl){ fieldType(v); return; }
  if(P.buf&&commitBuf(true)===false) return;
  if(ty==='d') insert(['d',+v]);
  else if(ty==='p') insert(['p',v]);
  else if(ty==='c'||ty==='v') insert(['s',v]);
}
/* delete, space, new line and the cursor keys */
function navAct(act){
  if(fieldEl){ fieldNav(act); return; }
  if(act==='bs'){ backspace(); return; }
  if(act==='space'||act==='enter'){ if(P.buf&&commitBuf(true)===false) return; insert(act==='space'?['sp']:['nl']); return; }
  flushTyping();
  if(act==='left') moveCaret(caret-1);
  else if(act==='right') moveCaret(caret+1);
  else if(act==='up'||act==='home') moveCaret(0);
  else if(act==='down'||act==='end') moveCaret(doc.length);
}
/* a Latin letter: into the text box when one is open, else onto the word being typed */
function typeLatin(ch){
  if(ch==='shift'){ shiftOn=!shiftOn; return; }
  if(shiftOn&&ch!=="'"){ ch=ch.toUpperCase(); shiftOn=false; }
  if(fieldEl){ fieldType(ch); return; }
  if(ch==="'"&&!P.buf){ hint('An apostrophe goes inside a word, as in don’t',1600); return; }
  autoSp=-1; P.buf+=ch; renderStatus();
}

/* ---------- a text box at the top of the screen with the Latin keys under it: the note's title, or English to write
   in Stemsyl. Numbers, punctuation and the cursor keys type into it too. ---------- */
function openField(kind){
  closeAll(); flushTyping(); if(reading) setReading(false);
  fieldKind=kind; fieldEl=kind==='title'?$('title'):$('pasteIn');
  fieldPrev={mode:kbMode,last:lastLetters};
  $('fieldLabel').textContent=kind==='title'?'Title':'English → Stemsyl';
  $('fieldGo').textContent=kind==='title'?'Done':'Insert';
  $('title').hidden=kind!=='title'; $('pasteIn').hidden=kind==='title';
  if(kind==='title'){ fieldOrig=note.title; $('title').value=note.title; }
  $('field').hidden=false; $('app').classList.add('fielding');
  kbMode='latin'; latinSel=null; selectedPos=null; shiftOn=false; buildKb();
  setTimeout(function(){ if(!fieldEl) return; try{ fieldEl.focus({preventScroll:true}); var n=fieldEl.value.length; fieldEl.setSelectionRange(n,n); }catch(e){} },30);
}
/* commit: keep the title (an emptied one goes back to what it was) or write the English in Stemsyl; else put things back */
function closeField(commit){
  if(!fieldEl) return;
  var kind=fieldKind, v=fieldEl.value;
  if(kind==='title'&&(!commit||!v.trim())){ note.title=fieldOrig; $('title').value=fieldOrig; note.updated=Date.now(); scheduleSave(); }
  try{ fieldEl.blur(); }catch(e){}
  fieldEl=null; fieldKind=''; $('field').hidden=true; $('app').classList.remove('fielding');
  kbMode=fieldPrev?fieldPrev.mode:'sounds'; if(fieldPrev) lastLetters=fieldPrev.last; fieldPrev=null;
  latinSel=null; selectedPos=null; shiftOn=false; buildKb(); renderDoc();
  /* English written in after a word gets a space before it */
  if(kind==='english'){ if(commit&&v.trim()) pasteInsert((caret>0&&doc[caret-1][0]!=='sp'&&doc[caret-1][0]!=='nl'&&!/^\s/.test(v)?' ':'')+v); $('pasteIn').value=''; }
}
function keepFieldFocus(){ try{ if(fieldEl&&document.activeElement!==fieldEl) fieldEl.focus({preventScroll:true}); }catch(e){} }
function fieldType(str){
  var f=fieldEl; if(!f) return;
  if(f.tagName==='INPUT') str=str.replace(/\n/g,' ');
  var a=f.selectionStart, b=f.selectionEnd; if(a==null){ a=b=f.value.length; }
  if(f.maxLength>0&&f.value.length-(b-a)+str.length>f.maxLength) return;
  f.setRangeText(str,a,b,'end'); f.dispatchEvent(new Event('input',{bubbles:true})); keepFieldFocus();
}
function fieldBack(){
  var f=fieldEl, a=f.selectionStart, b=f.selectionEnd;
  if(a===b){ if(!a) return; a--; }
  f.setRangeText('',a,b,'end'); f.dispatchEvent(new Event('input',{bubbles:true})); keepFieldFocus();
}
function fieldMove(to){ var f=fieldEl, n=Math.max(0,Math.min(f.value.length,to)); f.setSelectionRange(n,n); keepFieldFocus(); }
function fieldNav(act){
  var f=fieldEl;
  if(act==='bs') fieldBack();
  else if(act==='space') fieldType(' ');
  else if(act==='enter'){ if(fieldKind==='title') closeField(true); else fieldType('\n'); }
  else if(act==='left') fieldMove(f.selectionStart-1);
  else if(act==='right') fieldMove(f.selectionEnd+1);
  else if(act==='up'||act==='home') fieldMove(0);
  else if(act==='down'||act==='end') fieldMove(f.value.length);
}
$('fieldGo').addEventListener('click',function(){
  if(fieldKind==='english'&&!$('pasteIn').value.trim()){ hint('Type some English first',1500); keepFieldFocus(); return; }
  closeField(true);
});
$('fieldX').addEventListener('click',function(){ closeField(false); });
$('field').addEventListener('mousedown',function(e){ if(e.target.closest('button')) e.preventDefault(); });

/* ---------- physical keyboard: English words ---------- */""", keep_b=False)

# the title and the English box open as text boxes with the Latin keys
s = swap(s, "$('title').addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); this.blur(); closeAll(); } });\n"
            "function openTitle(){ var t=$('title'); t.value=note.title; openPanel('titlePanel'); setTimeout(function(){ try{ t.focus(); t.select(); }catch(e){} },60); }\n"
            "$('titleDone').addEventListener('click',closeAll);",
         "$('title').addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); closeField(true); } });\n"
         "function openTitle(){ openField('title'); }")
s = swap(s, "$('pasteGo').addEventListener('click',function(){ var t=$('pasteIn').value; if(!t.trim()){ hint('Type or paste some English first.'); return; } closeAll(); pasteInsert(t); $('pasteIn').value=''; });",
         "$('writeEn').addEventListener('click',function(){ openField('english'); });")
s = swap(s, "['notesPanel','titlePanel','sharePanel','menuPanel']", "['notesPanel','sharePanel','menuPanel']")
s = swap(s, "setMode:function(m){ if(MODES.indexOf(m)>=0){ kbMode=m; selectedPos=null; buildKb(); } },",
         "setMode:function(m){ if(MODES.indexOf(m)>=0){ if(m==='sounds'||m==='latin') lastLetters=m; kbMode=m; selectedPos=null; latinSel=null; buildKb(); } },\n"
         "  get field(){return fieldKind||null;},openField:openField,closeField:closeField,get typed(){return P.buf;},")

# ---- holding delete clears all the text: the whole note (Undo brings it back), or the text box that is open. The key
# fills with the warning colour while it is held, so a finger can still let go in time; a quick tap deletes one sound.
CLEAR_CSS = """
/* holding delete: the key fills with the warning colour until the text is cleared */
:root{--arm:#f2d4d0}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){--arm:#4d2320} }
:root[data-theme="dark"]{--arm:#4d2320}
.grid3 .cell.arming,.editbar button.arming{border-color:var(--warn);background:var(--arm);transition:background-color .6s linear,border-color .15s}
"""
s = swap(s, "\n/* ---------- panels and messages, inside the watch screen ---------- */", CLEAR_CSS + "\n/* ---------- panels and messages, inside the watch screen ---------- */")
s = swap(s, "  clearTimeout(holdTimer);\n  var cell=e.target.closest('.cell[data-hold]');\n  if(!cell) return;",
         "  clearTimeout(holdTimer); disarmClear();\n"
         "  var bs=e.target.closest('.cell[data-nav=\"bs\"]');\n"
         "  if(bs){ armClear(bs); return; }   /* delete: held, it clears all the text */\n"
         "  var cell=e.target.closest('.cell[data-hold]');\n  if(!cell) return;")
s = swap(s, "  if(Math.abs(dx)>18||Math.abs(dy)>18) clearTimeout(holdTimer);   /* moving is a swipe, not a hold */",
         "  if(Math.abs(dx)>18||Math.abs(dy)>18){ clearTimeout(holdTimer); disarmClear(); }   /* moving is a swipe, not a hold */")
s = swap(s, "function endTouch(e,lifted){\n  clearTimeout(holdTimer);", "function endTouch(e,lifted){\n  clearTimeout(holdTimer); disarmClear();")
s = swap(s, "/* a numeral, punctuation or sound key: into the text box when one is open;", r"""/* Holding delete clears all the text: the whole note, which Undo (in the options) brings back, or the text box that is
   open. The key fills with the warning colour while it is held; let go sooner and it deletes just one. */
var CLEAR_MS=700, armedKey=null, ebTimer=0, ebFired=false;
function armClear(el){
  armedKey=el; el.classList.add('arming');
  holdTimer=setTimeout(function(){ holdFired=true; disarmClear(); clearAll(); },CLEAR_MS);
}
function disarmClear(){ if(armedKey){ armedKey.classList.remove('arming'); armedKey=null; } }
function clearAll(){
  if(navigator.vibrate) navigator.vibrate(40);
  if(fieldEl){
    if(!fieldEl.value){ hint('The box is empty already',1500); return; }
    fieldEl.value=''; fieldEl.dispatchEvent(new Event('input',{bubbles:true})); keepFieldFocus(); hint('Cleared the box',1500); return;
  }
  if(!doc.length&&!P.buf){ hint('There’s nothing to clear',1500); return; }
  clearDoc(); hint('Cleared all the text · Undo, in the options, brings it back',3000);
}
/* the same on the delete key of the bar in the whole-note view */
$('editbar').addEventListener('pointerdown',function(e){
  ebFired=false; clearTimeout(ebTimer);
  var bt=e.target.closest('[data-ed="bs"]'); if(!bt) return;
  bt.classList.add('arming');
  ebTimer=setTimeout(function(){ ebFired=true; bt.classList.remove('arming'); clearAll(); },CLEAR_MS);
});
['pointerup','pointercancel','pointerleave'].forEach(function(ev){ $('editbar').addEventListener(ev,function(){
  clearTimeout(ebTimer); var a=$('editbar').querySelector('.arming'); if(a) a.classList.remove('arming'); }); });
/* a numeral, punctuation or sound key: into the text box when one is open;""")
s = swap(s, "  var bt=e.target.closest('[data-ed]'); if(!bt) return;",
         "  if(ebFired){ ebFired=false; return; }   /* a hold that cleared the note: its lift deletes nothing more */\n"
         "  var bt=e.target.closest('[data-ed]'); if(!bt) return;")
s = swap(s, "title:'Backspace',inner:'<span class=\"pos-lb big\">⌫</span>", "title:'Backspace — hold to clear all the text',inner:'<span class=\"pos-lb big\">⌫</span>", count=2)
s = swap(s, "bs:'Backspace'", "bs:'Backspace — hold to clear all the text'")
s = swap(s, 'data-ed="bs" aria-label="Delete" title="Delete"', 'data-ed="bs" aria-label="Delete — hold to clear all the text" title="Delete — hold to clear all the text"')
s = swap(s, "and hold anywhere on the note to go back to the keys.</p>",
         "and hold anywhere on the note to go back to the keys.</p>\n"
         "  <p class=\"fine\"><b>Clearing.</b> Hold delete (⌫) to clear all the text: the key fills red, and when you’ve held it for a moment "
         "the note is cleared. <b>Undo</b>, in the options, brings it back. In a text box, holding delete empties the box.</p>")

# nothing of the removed parts may be left in the code (comments may still mention them)
for gone in ['layout', 'keysHtml', 'fitKb', '--kbh', 'notesBtn', 'menuBtn', 'shareBtn', 'viewBtn', 'LAYOUTS', "'.key'", 'MAIN', 'NUMS', '--kh', 'S.prefs.gs']:
    code = re.sub(r'<script type="text/plain" id="ss(More|Dict)">.*?</script>', '', s, flags=re.S)
    code = re.sub(r'var SS_WORDS=".*?";', '', code, flags=re.S)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
    hits = [m.start() for m in re.finditer(re.escape(gone), code)]
    if hits:
        print('LEFT:', gone, [code[max(0, h - 60):h + 60] for h in hits[:3]])
OUT = os.path.join(ROOT, 'docs', 'stemsyl-keyboard-watch.html')
open(OUT, 'w', encoding='utf-8').write(s)
print('written', os.path.normpath(OUT), len(s.encode('utf-8')), 'bytes')
