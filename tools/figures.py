# Figures for the specification, written to docs/figures:
#   fig-consonants, fig-vowels, fig-numerals, fig-punctuation, fig-anatomy (.svg and .png): charts drawn by the apps' own
#     glyph code, so they are exactly the glyphs the apps draw
#   fig-example (.svg and .png): a note as the apps export it, with the English under each word
#   fig-phone.png, fig-watch.png: screenshots of the phone keyboard's two layouts and of every page of the watch keyboard
#   app-phone.png, app-watch.png, app-watch-colours.png, app-trainer.png: single screenshots for the front page (docs/index.html)
# Run after the apps are built (rebuild.py does both). Needs Playwright for Python with Chromium.
import base64, json, os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DOCS = os.path.join(ROOT, 'docs')
OUT = os.path.join(DOCS, 'figures')
PHONE = 'file://' + os.path.join(DOCS, 'stemsyl-keyboard.html')
WATCH = 'file://' + os.path.join(DOCS, 'stemsyl-keyboard-watch.html')
TRAINER = 'file://' + os.path.join(DOCS, 'stemsyl-trainer.html')
KEY = 'stemsyl_keyboard_v1'                    # where the apps keep their notes (localStorage)
EXAMPLE = 'Practice makes perfect.\nWe met Jon in London at 7:45 on Monday.'

# ---------- the charts ----------
CSS = """.stem{stroke:#2C2C2A;stroke-width:2;fill:none;stroke-linecap:round}.tk{stroke-width:7.5;fill:none;stroke-linecap:round}
.f-ink{stroke:#2C2C2A}.f-rose{stroke:#B65754}.f-mauve{stroke:#A55B91}.f-indigo{stroke:#4848B9}.f-blue{stroke:#238DC0}.f-emerald{stroke:#229279}.f-olive{stroke:#4F7103}.f-amber{stroke:#A19005}
.f-red{stroke:#c40027}.f-orange{stroke:#8f2400}.f-yellow{stroke:#d4a900}.f-green{stroke:#236b27}.f-vblue{stroke:#002fec}.f-grey{stroke:#5f5f5f}.f-violet{stroke:#582684}
.numdot,.namemk,.numon{fill:#534AB7;stroke:none}.numoff{fill:#9c9a92;opacity:.22}.pn{stroke:#534AB7;stroke-width:3.6;fill:none;stroke-linecap:round}
text{font-family:-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;fill:#2C2C2A}
.lb{font-size:11px;font-weight:700;text-anchor:middle}.sm{font-size:8.5px;fill:#6f6d66;text-anchor:middle}.ip{font-size:10px;text-anchor:middle;font-family:"Charis SIL","Doulos SIL","Noto Serif","DejaVu Serif",serif}
.hd{font-size:10px;font-weight:700;text-anchor:middle;letter-spacing:.04em}.rl{font-size:10px;font-weight:700;text-anchor:end;fill:#6f6d66}
.an{font-size:9.5px;fill:#2C2C2A}.ln{stroke:#9c9a92;stroke-width:.8;fill:none}
.t-ink{fill:#2C2C2A}.t-rose{fill:#B65754}.t-mauve{fill:#A55B91}.t-indigo{fill:#4848B9}.t-blue{fill:#238DC0}.t-emerald{fill:#229279}.t-olive{fill:#4F7103}.t-amber{fill:#A19005}
.t-red{fill:#c40027}.t-orange{fill:#8f2400}.t-yellow{fill:#a88600}.t-green{fill:#236b27}.t-vblue{fill:#002fec}.t-grey{fill:#5f5f5f}.t-violet{fill:#582684}"""

def svg(w, h, body, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="%s">'
            '<title>%s</title><style>%s</style><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>') % (w * 2, h * 2, w, h, title, title, CSS, w, h, body)

# runs in the phone app: its own glyph functions draw every glyph
JS_FIGS = r"""()=>{
  var out={};
  var FAM=['ink','rose','mauve','indigo','blue','emerald','olive','amber'], POS=['u','c','d'], PW={u:'up',c:'centred',d:'down'};
  var BYFP={}; Object.keys(CODE).forEach(function(k){ BYFP[CODE[k][0]+CODE[k][1]]=k; });
  /* consonants: families across, positions down; each with its name, its IPA and a word */
  var cw=58, ch=88, x0=62, y0=26, g='';
  FAM.forEach(function(f,i){ g+='<text class="hd t-'+f+'" x="'+(x0+i*cw+cw/2)+'" y="16">'+f+'</text>'; });
  POS.forEach(function(p,r){ g+='<text class="rl" x="'+(x0-8)+'" y="'+(y0+r*ch+26)+'">'+PW[p]+'</text>';
    FAM.forEach(function(f,i){ var c=BYFP[f+p], cx=x0+i*cw+cw/2, cy=y0+r*ch;
      g+='<g transform="translate('+(cx-9)+' '+(cy-10)+')">'+loneInner(c)+'</g>';
      g+='<text class="lb t-'+f+'" x="'+cx+'" y="'+(cy+52)+'">'+CONS_NAME[c]+'</text>';
      g+='<text class="ip" x="'+cx+'" y="'+(cy+63)+'">/'+CONS_IPA[c]+'/</text>';
      g+='<text class="sm" x="'+cx+'" y="'+(cy+74)+'">'+CONS_EX[c]+'</text>'; }); });
  out.cons={w:x0+8*cw+10,h:y0+3*ch-6,g:g};
  /* vowels: colours across, positions down */
  var COL=['red','orange','yellow','green','vblue','grey','violet'], vw=64, vh=88, vx0=62, vy0=26, V={};
  Object.keys(VCHAR).forEach(function(k){ var t=vowelTick(VCHAR[k]); if(t) V[t[0]+t[1]]=k; });
  g='';
  COL.forEach(function(c,i){ g+='<text class="hd t-'+c+'" x="'+(vx0+i*vw+vw/2)+'" y="16">'+(c==='vblue'?'blue':c)+'</text>'; });
  ['u','c','d'].forEach(function(p,r){ g+='<text class="rl" x="'+(vx0-8)+'" y="'+(vy0+r*vh+26)+'">'+PW[p]+'</text>';
    COL.forEach(function(c,i){ var v=V[c+p], cx=vx0+i*vw+vw/2, cy=vy0+r*vh;
      if(!v){ g+='<text class="sm" x="'+cx+'" y="'+(cy+26)+'">—</text>'; return; }
      g+='<g transform="translate('+(cx-21)+' '+(cy-10)+')">'+syllableInner(null,VCHAR[v],null)+'</g>';
      g+='<text class="lb t-'+c+'" x="'+cx+'" y="'+(cy+52)+'">'+VNAME[v][0]+'</text>';
      g+='<text class="ip" x="'+cx+'" y="'+(cy+63)+'">/'+soundIPA(v)+'/</text>';
      g+='<text class="sm" x="'+cx+'" y="'+(cy+74)+'">'+VNAME[v][1]+'</text>'; }); });
  out.vow={w:vx0+7*vw+10,h:vy0+3*vh-6,g:g};
  /* anatomy: "cats" = k a t + s */
  var units=syllabify(phonemes('kats')), gg='', x=0;
  units.forEach(function(u){ gg+='<g transform="translate('+x+' 0)">'+unitInner(u)+'</g>'; x+=unitW(u); });
  out.anat={g:gg,w:x};
  /* numerals 0-9 */
  g='';
  for(var d=0;d<=9;d++){ g+='<g transform="translate('+(d*54+3)+' -4)">'+numeralInner(d)+'</g><text class="lb" x="'+(d*54+27)+'" y="72">'+d+'</text>'; }
  out.nums={w:10*54+6,h:80,g:g};
  /* punctuation and the name mark */
  var P=[['.','full stop'],[',','comma'],['?','question'],['!','exclamation'],[':','colon'],[';','semicolon'],['“','open quote'],['”','close quote'],['(','open bracket'],[')','close bracket'],['–','dash'],['/','slash']], s=64;
  g=''; P.forEach(function(p,i){ g+='<g transform="translate('+(i*s+(s-PUNCT_W)/2)+' 0)">'+PUNCT[p[0]]+'</g><text class="sm" x="'+(i*s+s/2)+'" y="72">'+p[1]+'</text>'; });
  g+='<g transform="translate('+(12*s+s/2-10)+' 20)">'+nameMarkInner()+'</g><text class="sm" x="'+(12*s+s/2)+'" y="72">name mark</text>';
  out.punct={w:13*s,h:80,g:g};
  return out;
}"""

def anatomy(inner):
    """the glyphs of "cats" at three times their size, with a label on each part"""
    S, gx, gy = 3.0, 196, 34
    T = lambda u: gx + u * S
    Y = lambda v: gy + (v - 8) * S
    body = '<g transform="translate(%g %g) scale(%g)">%s</g>' % (gx, gy - 8 * S, S, inner)
    def lab(x1, y1, x2, y2, txt, anchor='start'):
        return ('<path class="ln" d="M %g %g L %g %g"/><text class="an" x="%g" y="%g" text-anchor="%s">%s</text>'
                % (x1, y1, x2, y2, x2 + (4 if anchor == 'start' else -4), y2 + 3, anchor, txt))
    body += lab(T(9), Y(19), T(9) - 34, Y(3), 'onset: k — amber, up', 'end')
    body += lab(T(21), Y(45), T(21) - 34, Y(62), 'vowel: a — red, centred (across the stem)', 'end')
    body += lab(T(33), Y(19), T(33) + 34, Y(3), 'coda: t — ink, up')
    body += lab(T(27), Y(32.5), T(27) + 10, Y(64), 'stem')
    body += lab(T(51), Y(22), T(51) + 30, Y(22), 'lone consonant: s — blue, up')
    body += lab(T(55.5), Y(32.5), T(55.5) + 24, Y(46), 'stub')
    return svg(560, int(Y(70)), body, 'Anatomy of the Stemsyl word cats')

def seed(notes_doc, prefs, title='Example'):
    """an init script that gives the app one note (its tokens) and these settings"""
    state = {'notes': [{'id': 'n1', 'title': title, 'doc': notes_doc, 'caret': len(notes_doc), 'updated': 1}], 'cur': 'n1', 'prefs': prefs}
    return "localStorage.setItem('%s', %s)" % (KEY, json.dumps(json.dumps(state)))

def ready(pg):
    pg.evaluate("()=>new Promise(r=>window.__ss.words.onMore(r))"); pg.wait_for_timeout(150)

def charts(b):
    pg = b.new_page(viewport={'width': 412, 'height': 915}, device_scale_factor=2)
    pg.goto(PHONE); ready(pg)
    F = pg.evaluate(JS_FIGS)
    toks = pg.evaluate("t=>window.__ss.parseText(t).tokens", EXAMPLE)
    pg.close()
    figs = {
        'fig-consonants.svg': svg(F['cons']['w'], F['cons']['h'], F['cons']['g'], 'Stemsyl consonants: eight colour families, three positions'),
        'fig-vowels.svg': svg(F['vow']['w'], F['vow']['h'], F['vow']['g'], 'Stemsyl vowels: seven colours, three positions'),
        'fig-numerals.svg': svg(F['nums']['w'], F['nums']['h'], F['nums']['g'], 'Stemsyl numerals 0 to 9'),
        'fig-punctuation.svg': svg(F['punct']['w'], F['punct']['h'], F['punct']['g'], 'Stemsyl punctuation and the name mark'),
        'fig-anatomy.svg': anatomy(F['anat']['g']),
    }
    for name, text in figs.items():
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(text)
        p2 = b.new_page(device_scale_factor=2)
        p2.set_content('<html><body style="margin:0;background:#fff">' + text + '</body></html>')
        p2.query_selector('svg').screenshot(path=os.path.join(OUT, name.replace('.svg', '.png'))); p2.close()
    # the example, as the Share panel exports it
    ctx = b.new_context(viewport={'width': 412, 'height': 915}, device_scale_factor=2)
    pe = ctx.new_page()
    pe.add_init_script(seed(toks, {'gs': 56, 'aid': 'en', 'view': 'stemsyl', 'layout': 'keys'}))
    pe.goto(PHONE); ready(pe)
    ex = pe.evaluate("()=>window.__ss.exportSVG({aid:true})")
    open(os.path.join(OUT, 'fig-example.svg'), 'w', encoding='utf-8').write(ex)
    pe.set_content('<html><body style="margin:0;background:#fff">' + ex + '</body></html>')
    pe.query_selector('svg').screenshot(path=os.path.join(OUT, 'fig-example.png'))
    ctx.close()
    return toks

# ---------- screenshots ----------
def touch(cdp, typ, pts):
    cdp.send('Input.dispatchTouchEvent', {'type': typ, 'touchPoints': [{'x': x, 'y': y} for x, y in pts]})
def centre(pg, sel):
    bb = pg.query_selector(sel).bounding_box(); return bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
def tap(pg, cdp, sel):
    x, y = centre(pg, sel); touch(cdp, 'touchStart', [(x, y)]); touch(cdp, 'touchEnd', []); pg.wait_for_timeout(80)
def hold(pg, cdp, sel, ms=650):
    x, y = centre(pg, sel); touch(cdp, 'touchStart', [(x, y)]); pg.wait_for_timeout(ms); touch(cdp, 'touchEnd', []); pg.wait_for_timeout(450)
CPOS = {'u': '0', 'c': '3', 'd': '6'}; VPOS = {'u': '1', 'c': '4', 'd': '7'}
CONS_AT = {'t': 'u', 'n': 'c', 'd': 'd', 'p': 'u', 'm': 'c', 'b': 'd', 'f': 'u', 'w': 'c', 'v': 'd', 'T': 'u', 'h': 'c', 'D': 'd',
           's': 'u', 'l': 'c', 'z': 'd', 'S': 'u', 'r': 'c', 'Z': 'd', 'C': 'u', 'y': 'c', 'J': 'd', 'k': 'u', 'N': 'c', 'g': 'd'}
VOW_AT = {'Y': 'u', 'E': 'u', 'I': 'u', 'B': 'u', 'a': 'c', 'A': 'c', 'e': 'c', 'i': 'c', 'u': 'c', '@': 'c', 'W': 'd', 'O': 'd', 'G': 'd', 'U': 'd'}
def sound3(pg, cdp, ch):
    """one sound on the 3 x 3 keys: its tick position, then its colour"""
    if ch in CONS_AT: tap(pg, cdp, '.cell[data-pos="%s"]' % CPOS[CONS_AT[ch]]); tap(pg, cdp, '.cell[data-cons="%s"]' % ch)
    else: tap(pg, cdp, '.cell[data-pos="%s"]' % VPOS[VOW_AT[ch]]); tap(pg, cdp, '.cell[data-vow="%s"]' % ch)
LATIN = ['abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy', "z'"]
def letter(pg, cdp, ch):
    if ch == ' ': tap(pg, cdp, '.cell[data-nav="space"]'); return
    tap(pg, cdp, '.cell[data-lg="%d"]' % next(i for i, g in enumerate(LATIN) if ch in g))
    tap(pg, cdp, '.cell[data-lat="%s"]' % ch)
def png(pg, sel=None):
    return (pg.query_selector(sel).screenshot() if sel else pg.screenshot())

def phone_screens(b, toks):
    ctx = b.new_context(viewport={'width': 393, 'height': 852}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.add_init_script(seed(toks, {'aid': 'en', 'view': 'stemsyl', 'layout': 'keys'}))
    pg.goto(PHONE); ready(pg)
    shots = []
    for k in ['u:nl', 'c:g', 'c:r', 'v:E', 'c:t']: tap(pg, cdp, '#kb [data-k="%s"]' % k)
    shots.append((png(pg), 'Keys: a key for every sound, and the words that sound like it'))
    pg.evaluate("()=>window.__ss.setLayout('grid3')"); pg.wait_for_timeout(200)
    shots.append((png(pg), '3 × 3: first a tick position'))
    tap(pg, cdp, '.cell[data-pos="4"]')
    shots.append((png(pg), '3 × 3: then its colour'))
    ctx.close()
    return shots

def watch_screens(b, toks, dark=False):
    ctx = b.new_context(viewport={'width': 208, 'height': 248}, device_scale_factor=2, has_touch=True, is_mobile=True,
                        color_scheme='dark' if dark else 'light')
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.add_init_script(seed(toks, {'wgs': 40, 'aid': 'en', 'view': 'stemsyl'}))
    pg.goto(WATCH); ready(pg)
    APP = '#app'
    tap(pg, cdp, '.cell[data-nav="enter"]')
    for ch in 'grEt': sound3(pg, cdp, ch)
    if dark:
        shot = png(pg, APP); ctx.close(); return [(shot, 'Dark theme')]
    shots = [(png(pg, APP), 'The tick positions, and the words that sound like it')]
    tap(pg, cdp, '.cell[data-pos="0"]'); shots.append((png(pg, APP), 'Consonant, up: its eight colours')); tap(pg, cdp, '.cell[data-unselect]')
    tap(pg, cdp, '.cell[data-pos="4"]'); shots.append((png(pg, APP), 'Vowel, centred: its six colours')); tap(pg, cdp, '.cell[data-unselect]')
    tap(pg, cdp, '.cand[data-c="0"]'); pg.wait_for_timeout(100)
    for pos, name in [(1, 'Hold the top key: numbers'), (3, 'Hold the left key: punctuation'), (7, 'Hold the bottom key: the cursor'),
                      (5, 'Hold the right key: the options')]:
        hold(pg, cdp, '.grid3 > :nth-child(%d)' % (pos + 1)); shots.append((png(pg, APP), name))
    hold(pg, cdp, '.grid3 > :nth-child(5)')                     # the centre: back to the tick positions
    hold(pg, cdp, '.grid3 > :nth-child(5)')                     # and again: the Latin letters
    shots.append((png(pg, APP), 'Hold the centre: Latin letters'))
    tap(pg, cdp, '.cell[data-lg="0"]'); shots.append((png(pg, APP), 'A group, then its letter')); tap(pg, cdp, '.cell[data-lunselect]')
    hold(pg, cdp, '.grid3 > :nth-child(5)')                     # back to the tick positions
    hold(pg, cdp, '.grid3 > :nth-child(6)'); tap(pg, cdp, '[data-app="menu"]'); pg.wait_for_timeout(300)
    shots.append((png(pg, APP), 'The menu'))
    pg.evaluate("()=>document.getElementById('writeEn').scrollIntoView({block:'center'})"); pg.wait_for_timeout(100); tap(pg, cdp, '#writeEn')
    for ch in 'we met': letter(pg, cdp, ch)
    shots.append((png(pg, APP), 'Write English: typed, then turned into Stemsyl'))
    tap(pg, cdp, '#fieldX'); pg.wait_for_timeout(400)
    pg.evaluate("()=>window.__ss.setReading(true)"); pg.wait_for_timeout(300)
    shots.append((png(pg, APP), 'Hold the note: all of it'))
    gl = [e for e in pg.query_selector_all('#sheet .g') if e.bounding_box()['y'] > 40][2].bounding_box()
    touch(cdp, 'touchStart', [(gl['x'] + 2, gl['y'] + gl['height'] / 2)]); touch(cdp, 'touchEnd', []); pg.wait_for_timeout(300)
    shots.append((png(pg, APP), 'Tap in it: the cursor, and delete · space · new line'))
    pg.evaluate("()=>window.__ss.setReading(false)"); pg.wait_for_timeout(200)
    pg.evaluate("()=>{ window.__ss.setWordStrip('below'); window.__ss.setMode('sounds'); window.__ss.moveCaret(1e9); }"); pg.wait_for_timeout(100)
    for ch in 'sI': sound3(pg, cdp, ch)
    shots.append((png(pg, APP), 'The words below the keys (a menu choice)'))
    ctx.close()
    return shots

def trainer_shot(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 700}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.add_init_script("(function(){ var s=7; Math.random=function(){ s=s*16807%2147483647; return (s-1)/2147483646; }; })()")   # the same card each time
    pg.goto(TRAINER); pg.wait_for_timeout(500)
    shot = pg.screenshot(); ctx.close()
    return shot

def sheet(b, shots, cols, width, radius, name, pad=10):
    """the screenshots in a grid, each in a dark frame with its caption, as one PNG"""
    cells = ''.join('<figure><div class="fr"><img src="data:image/png;base64,%s"></div><figcaption><b>%d</b> %s</figcaption></figure>'
                    % (base64.b64encode(s).decode(), i + 1, c) for i, (s, c) in enumerate(shots))
    html = ('<html><head><style>body{margin:0;background:#fff;font:13px/1.35 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#2C2C2A}'
            '.sh{display:grid;grid-template-columns:repeat(%d,%dpx);gap:22px 18px;padding:18px;width:max-content;align-items:start}'
            'figure{margin:0}.fr{background:#161615;padding:%dpx;border-radius:%dpx}'
            'img{display:block;width:%dpx;border-radius:%dpx}figcaption{margin-top:8px;font-size:12.5px;color:#4a4944;text-align:center;padding:0 4px}'
            'figcaption b{color:#534AB7;margin-right:3px}</style></head><body><div class="sh">%s</div></body></html>'
            % (cols, width + 2 * pad, pad, radius + pad, width, radius, cells))
    pg = b.new_page(device_scale_factor=2); pg.set_content(html); pg.wait_for_timeout(200)
    pg.query_selector('.sh').screenshot(path=os.path.join(OUT, name)); pg.close()

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        toks = charts(b)
        phone, watch = phone_screens(b, toks), watch_screens(b, toks)
        sheet(b, phone, 3, 262, 30, 'fig-phone.png', pad=9)
        sheet(b, watch + watch_screens(b, toks, dark=True), 5, 208, 32, 'fig-watch.png', pad=7)
        for name, png_bytes in [('app-phone.png', phone[0][0]), ('app-watch.png', watch[0][0]), ('app-watch-colours.png', watch[2][0]),
                                ('app-trainer.png', trainer_shot(b))]:
            open(os.path.join(OUT, name), 'wb').write(png_bytes)
        b.close()
    print('figures written to', os.path.relpath(OUT, ROOT))
