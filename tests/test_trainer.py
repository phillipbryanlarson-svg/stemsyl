# The trainer (docs/stemsyl-trainer.html): it draws the script exactly as the keyboards do (the same tables, geometry and
# colours), its practice words use the keyboards' sounds, and every kind of practice card shows and reveals.
import re
from playwright.sync_api import sync_playwright
from helpers import *

C = Checks('trainer')
TABLES = "()=>({CODE:CODE, VCHAR:VCHAR, TICKY:TICKY, VT:Object.fromEntries(Object.keys(VCHAR).map(function(k){ return [k, vowelTick(VCHAR[k])]; }))})"
def css_vars(path):
    h = open(path, encoding='utf-8').read()
    return dict(re.findall(r'--(v?(?:red|orange|yellow|green|vblue|grey|violet)|ink|rose|mauve|indigo|blue|emerald|olive|amber|mark):(#[0-9A-Fa-f]{6})', h[:h.index('</style>')])[:23])

with sync_playwright() as p:
    b = p.chromium.launch()
    kb, _, _ = open_app(b, PHONE, 412, 915, touch=False, seed=False)
    want = kb.evaluate(TABLES); kb.context.close()
    ctx = b.new_context(viewport={'width': 1100, 'height': 900}); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(TRAINER); pg.wait_for_timeout(600)
    got = pg.evaluate(TABLES)
    for t in ('VCHAR', 'VT'): got[t].pop('o', None)      # the trainer keeps o, its old letter for the LOT vowel, as another name for ah
    C.eq('the same sound tables, tick positions and vowel colours as the keyboards', got, want)
    tv, kv = css_vars(os.path.join(DOCS, 'stemsyl-trainer.html')), css_vars(os.path.join(DOCS, 'stemsyl-keyboard.html'))
    C.eq('the same colours (light theme) as the keyboards', {k: v.lower() for k, v in tv.items()}, {k: v.lower() for k, v in kv.items()})
    letters = set('pbtdkgfvTDszSZhCJmnNlrwy@aAYWiIuUeEOBG')
    bad = pg.evaluate("""()=>{ var out=[]; ['short','long'].forEach(function(k){ TD[k].forEach(function(r){ out.push(r[1]); }); });
        TD.sentences.forEach(function(s){ s.forEach(function(t){ if(t[0]==='#') return; out.push(t[0]==='*'?t[2]:t[1]); }); }); return out; }""")
    C.eq('every practice word is written with the keyboards\' sound letters', [x for x in bad if not set(x) <= letters][:5], [])
    for chip in ['Vowels', 'Consonants', 'One-glyph words', 'Longer words', 'Sentences', 'Numbers', 'Punctuation']:
        pg.click('button:has-text("%s")' % chip); pg.wait_for_timeout(150)
        drawn = pg.evaluate("()=>{ var g=document.getElementById('glyph'); return !!g && g.querySelectorAll('path,rect,circle').length>0; }")
        pg.click('#card'); pg.wait_for_timeout(150)
        shown = pg.evaluate("()=>{ var a=document.getElementById('answer'); return !!a && a.textContent.trim().length>0; }")
        C.ok('%s: a card is drawn, and a tap reveals its answer' % chip, drawn and shown, (drawn, shown))
    shot(pg, 'trainer')
    links = pg.evaluate("()=>[].map.call(document.querySelectorAll('nav.links a'),a=>a.getAttribute('href'))")
    C.ok('its links to the specification and the keyboard lead to files that exist', links and all(os.path.exists(os.path.join(DOCS, h)) for h in links), links)
    C.eq('no page errors', errs, [])
    b.close()
C.report()
