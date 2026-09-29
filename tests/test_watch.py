# The watch keyboard (docs/stemsyl-keyboard-watch.html) at the 46 mm and 42 mm Apple Watch sizes: every page of keys and
# every panel fits the screen with nothing cut off; the held keys bring up their pages; holding delete to clear the text;
# display mode and its edit bar; the word strip above or below the keys; the Latin letters, in the note and in the text
# boxes; and the option keys.
from playwright.sync_api import sync_playwright
from helpers import *

C = Checks('watch keyboard')
SIZES = [(208, 248), (187, 223)]
EXAMPLE = 'Practice makes perfect.\nWe met Jon in London at 7:45 on Monday.'
PREFS = {'wgs': 40, 'aid': 'en', 'view': 'stemsyl'}
POS = {'nums': 1, 'punct': 3, 'options': 5, 'nav': 7}
def mode(pg): return pg.evaluate("()=>window.__ss.mode")
def page(pg):
    return pg.evaluate("()=>[window.__ss.mode, !!document.querySelector('.cell[data-unselect],.cell[data-lunselect]')]")
def fits(pg, what, size):
    bad, cut = outside(pg), cut_keys(pg)
    C.ok('%s: fits the %d × %d screen, nothing cut off' % (what, size[0], size[1]), not bad and not cut, (bad[:3], cut[:3]))
def panel_open(pg, pid): return pg.evaluate("id=>!document.getElementById(id).hidden", pid)

with sync_playwright() as p:
    b = p.chromium.launch()
    # the example note, as tokens
    pg, cdp, errs = open_app(b, WATCH, 208, 248)
    toks = pg.evaluate("t=>window.__ss.parseText(t).tokens", EXAMPLE)
    pg.context.close()

    # ---------- every page and panel fits, at both sizes ----------
    for size in SIZES:
        pg, cdp, errs = open_app(b, WATCH, size[0], size[1], doc=toks, prefs=PREFS)
        app = pg.evaluate("()=>{ var r=document.getElementById('app').getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }")
        C.eq('the app is exactly the screen (%d × %d)' % size, app, list(size))
        fits(pg, 'tick positions', size)
        for pos in ['0', '3', '6', '1', '4', '7']:
            tap(pg, cdp, '.cell[data-pos="%s"]' % pos); fits(pg, 'colour page %s' % pos, size); tap(pg, cdp, '.cell[data-unselect]')
        for m in ['nums', 'punct', 'nav', 'options']:
            hold(pg, cdp, KEY_AT(POS[m])); fits(pg, m, size)
        hold(pg, cdp, KEY_AT(4)); hold(pg, cdp, KEY_AT(4))
        C.eq('holding the centre twice: tick positions, then Latin letters', page(pg), ['latin', False])
        fits(pg, 'Latin groups', size)
        for g in range(6):
            tap(pg, cdp, '.cell[data-lg="%d"]' % g); fits(pg, 'Latin group %d' % g, size); tap(pg, cdp, '.cell[data-lunselect]')
        hold(pg, cdp, KEY_AT(4))
        for key, pid in [('notes', 'notesPanel'), ('share', 'sharePanel'), ('menu', 'menuPanel')]:
            hold(pg, cdp, KEY_AT(5)); tap(pg, cdp, '[data-app="%s"]' % key); pg.wait_for_timeout(250)
            C.ok('%s panel opens' % key, panel_open(pg, pid)); fits(pg, key + ' panel', size)
            pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
        hold(pg, cdp, KEY_AT(5)); tap(pg, cdp, '[data-app="title"]'); pg.wait_for_timeout(150)
        C.eq('the title opens as a text box', pg.evaluate("()=>window.__ss.field"), 'title'); fits(pg, 'title box', size)
        tap(pg, cdp, '#fieldX'); pg.wait_for_timeout(300)
        pg.evaluate("()=>window.__ss.setReading(true)"); pg.wait_for_timeout(200); fits(pg, 'display mode', size)
        pg.evaluate("()=>window.__ss.setReading(false)"); pg.evaluate("()=>window.__ss.setWordStrip('below')"); pg.wait_for_timeout(100)
        fits(pg, 'word strip below the keys', size)
        C.eq('no page errors at %d × %d' % size, errs, [])
        pg.context.close()

    # ---------- holds ----------
    pg, cdp, errs = open_app(b, WATCH, 208, 248, doc=toks, prefs=PREFS)
    C.eq('opens on the tick positions', page(pg), ['sounds', False])
    tags = pg.evaluate("()=>[1,3,5,7,4].map(i=>{ var t=document.querySelector('.grid3 > :nth-child('+(i+1)+') .hold-to'); return t?(t.querySelector('svg')?'icon':t.textContent):''; })")
    C.eq('the edge keys and the centre carry tags: 123, ?!, opt, the cursor arrow, abc', tags, ['123', '?!', 'opt', 'icon', 'abc'])
    for m in ['nums', 'punct', 'options', 'nav']:
        hold(pg, cdp, KEY_AT(POS[m])); C.eq('hold the %s key: %s' % ({1: 'top', 3: 'left', 5: 'right', 7: 'bottom'}[POS[m]], m), mode(pg), m)
    for m in ['punct', 'nums', 'nav', 'options']:
        hold(pg, cdp, KEY_AT(POS[m])); C.eq('and straight to %s from any page' % m, mode(pg), m)
    C.ok('on its own page, the key\'s tag is highlighted and it holds nothing',
         pg.evaluate("()=>{ var c=document.querySelector('.grid3 > :nth-child(6)'); return !c.dataset.hold && !!c.querySelector('.hold-to.on'); }"))
    hold(pg, cdp, KEY_AT(4))
    C.ok('the centre brings back the letters last in use, without opening the menu', page(pg) == ['sounds', False] and not panel_open(pg, 'menuPanel'), page(pg))
    hold(pg, cdp, KEY_AT(1)); n0 = len(doc(pg))
    bb = pg.query_selector('.tri[data-k="d:9"]').bounding_box(); hold_at(pg, cdp, bb['x'] + bb['width'] * .25, bb['y'] + bb['height'] * .25, 800)
    C.ok('the 9 · 0 key never holds: a long press types 9', mode(pg) == 'nums' and doc(pg)[n0:] == [['d', 9]], doc(pg)[n0:])
    hold(pg, cdp, KEY_AT(1), 800)
    C.eq('holding the key of the page on show types, as a tap does', doc(pg)[-1], ['d', 2])
    n1 = len(doc(pg)); hold(pg, cdp, KEY_AT(4))
    C.ok('holding 5 goes back to the letters without typing 5', mode(pg) == 'sounds' and len(doc(pg)) == n1)
    tap(pg, cdp, '.cell[data-pos="4"]'); n2 = len(doc(pg)); hold(pg, cdp, KEY_AT(4))
    C.ok('on a colour page, the centre goes back to the tick positions without writing', page(pg) == ['sounds', False] and len(doc(pg)) == n2, page(pg))
    tap(pg, cdp, '.cell[data-pos="0"]'); hold(pg, cdp, KEY_AT(7))
    C.eq('on a colour page, the bottom key brings up the cursor keys', mode(pg), 'nav')
    hold(pg, cdp, KEY_AT(4))
    n3 = len(doc(pg))
    tap(pg, cdp, KEY_AT(1)); tap(pg, cdp, '.cell[data-cons="r"]'); tap(pg, cdp, KEY_AT(4)); tap(pg, cdp, '.cell[data-vow="e"]')
    C.eq('quick taps on the held keys still type (C mid, r; V mid, e)', sounds(pg, n3), 're')
    kb = pg.query_selector('.grid3').bounding_box(); cx = kb['x'] + kb['width'] / 2; y = kb['y'] + kb['height'] / 2
    c0 = pg.evaluate("()=>window.__ss.caret"); swipe(pg, cdp, cx + 55, cx - 55, y)
    C.eq('a swipe left of 110 points moves the cursor 3 sounds', pg.evaluate("()=>window.__ss.caret"), c0 - 3)
    tap(pg, cdp, '.cell[data-pos="0"]')
    C.eq('and a tap right after it counts', page(pg), ['sounds', True])
    tap(pg, cdp, '.cell[data-unselect]')
    C.eq('no page errors while holding and swiping', errs, [])
    pg.context.close()

    # ---------- display mode and the edit bar ----------
    pg, cdp, errs = open_app(b, WATCH, 208, 248, doc=toks, prefs=PREFS)
    def st(pg): return pg.evaluate("()=>[window.__ss.reading, document.getElementById('app').classList.contains('editing')]")
    s0 = st(pg); tap(pg, cdp, '#doc')
    C.ok('a tap on the note strip only says how to open display mode', st(pg) == s0 and not pg.evaluate("()=>document.getElementById('toast').hidden"))
    pg.wait_for_timeout(1600)
    x, y = centre(pg, '#doc'); hold_at(pg, cdp, x, y)
    C.eq('holding the note strip opens display mode', st(pg), [True, False])
    C.ok('display mode hides the keys and the word strip', pg.evaluate("()=>!document.getElementById('kb').getClientRects().length"))
    gl = [e for e in pg.query_selector_all('#sheet .g') if e.bounding_box()['y'] > 30][3]; gb = gl.bounding_box(); a = int(gl.get_attribute('data-a'))
    tap_at(pg, cdp, gb['x'] + 2, gb['y'] + gb['height'] / 2, 200)
    if a > 0 and doc(pg)[a - 1][0] == 'w': a -= 1          # the cursor stands before a word's silent spelling
    C.eq('a tap puts the cursor where it lands and brings up the edit bar', [st(pg), pg.evaluate("()=>window.__ss.caret")], [[True, True], a])
    n = len(doc(pg)); tap(pg, cdp, '#editbar [data-ed="sp"]'); C.eq('the bar\'s space key', len(doc(pg)), n + 1)
    tap(pg, cdp, '#editbar [data-ed="bs"]'); C.eq('its delete key', len(doc(pg)), n)
    tap(pg, cdp, '#editbar [data-ed="nl"]'); C.eq('its new-line key', doc(pg)[pg.evaluate("()=>window.__ss.caret") - 1], ['nl'])
    tap(pg, cdp, '#editbar [data-ed="bs"]')
    c = pg.evaluate("()=>window.__ss.caret"); x, y = centre(pg, '#doc'); hold_at(pg, cdp, x, y)
    C.ok('holding the note goes back to the keys, the cursor where it was put', st(pg) == [False, False] and pg.evaluate("()=>window.__ss.caret") == c)
    C.eq('no page errors in display mode', errs, [])

    # ---------- holding delete clears all the text ----------
    pc, cdpc, errc = open_app(b, WATCH, 208, 248, doc=toks, prefs=PREFS)
    n = len(doc(pc)); tap(pc, cdpc, '.cell[data-nav="bs"]')
    C.eq('a tap on delete deletes one', len(doc(pc)), n - 1)
    x, y = centre(pc, '.cell[data-nav="bs"]'); touch(cdpc, 'touchStart', [(x, y)]); pc.wait_for_timeout(350)
    C.ok('while it is held, the delete key fills with the warning colour', pc.evaluate("()=>!!document.querySelector('.cell.arming')"))
    pc.wait_for_timeout(500); touch(cdpc, 'touchEnd', []); pc.wait_for_timeout(300)
    C.ok('held, it clears all the text, and says Undo brings it back',
         doc(pc) == [] and 'Undo' in pc.evaluate("()=>document.getElementById('toast').textContent"), (len(doc(pc)), pc.evaluate("()=>document.getElementById('toast').textContent")))
    hold(pc, cdpc, KEY_AT(5)); tap(pc, cdpc, '[data-app="undo"]')
    C.eq('Undo brings the note back', len(doc(pc)), n - 1)
    hold(pc, cdpc, KEY_AT(4)); m = len(doc(pc))
    x, y = centre(pc, '.cell[data-nav="bs"]'); touch(cdpc, 'touchStart', [(x, y)])
    for i in range(1, 7): touch(cdpc, 'touchMove', [(x + 20 * i, y)]); pc.wait_for_timeout(30)
    pc.wait_for_timeout(800); touch(cdpc, 'touchEnd', []); pc.wait_for_timeout(300)
    C.eq('a finger that slides off delete clears nothing', len(doc(pc)), m)
    hold(pc, cdpc, KEY_AT(7)); hold(pc, cdpc, '.cell[data-nav="bs"]', 900)
    C.eq('delete on the cursor page clears too', doc(pc), [])
    hold(pc, cdpc, KEY_AT(5)); tap(pc, cdpc, '[data-app="undo"]'); hold(pc, cdpc, KEY_AT(4))
    hold(pc, cdpc, KEY_AT(5)); tap(pc, cdpc, '[data-app="title"]'); pc.wait_for_timeout(150)
    before = pc.evaluate("()=>document.getElementById('title').value")
    hold(pc, cdpc, '.cell[data-nav="bs"]', 900)
    C.eq('in a text box, holding delete empties the box', pc.evaluate("()=>document.getElementById('title').value"), '')
    C.eq('and the note is untouched', len(doc(pc)), m)
    tap(pc, cdpc, '#fieldX'); pc.wait_for_timeout(300)
    C.eq('✕ puts the title back', pc.evaluate("()=>document.getElementById('title').value"), before)
    pc.evaluate("()=>window.__ss.setReading(true)"); pc.wait_for_timeout(200)
    gl = [e for e in pc.query_selector_all('#sheet .g') if e.bounding_box()['y'] > 30][1].bounding_box()
    tap_at(pc, cdpc, gl['x'] + 2, gl['y'] + gl['height'] / 2, 200)
    hold(pc, cdpc, '#editbar [data-ed="bs"]', 900)
    C.eq('in the whole-note view, holding the bar\'s delete clears the note', doc(pc), [])
    hold(pc, cdpc, '#editbar [data-ed="bs"]', 900)
    C.ok('with nothing left, it says so', 'nothing' in pc.evaluate("()=>document.getElementById('toast').textContent"))
    C.eq('no page errors while clearing', errc, [])
    pc.context.close()

    # ---------- the word strip below the keys ----------
    pg.evaluate("()=>window.__ss.moveCaret(1e9)")
    hold(pg, cdp, KEY_AT(5)); tap(pg, cdp, '[data-app="menu"]'); pg.wait_for_timeout(250)
    tap(pg, cdp, '#stripSeg [data-v="below"]'); pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
    hold(pg, cdp, KEY_AT(4))
    for ch in 'sI': sound3(pg, cdp, ch)
    order = pg.evaluate("()=>{ var s=document.querySelector('.strip').getBoundingClientRect(), k=document.getElementById('kb').getBoundingClientRect(); return s.top>=k.bottom-1; }")
    C.ok('the menu can put the word strip below the keys', order and 'see' in cands(pg, 6), cands(pg, 6))
    pg, cdp, errs = reopen(pg, WATCH)
    C.eq('the choice is kept', pg.evaluate("()=>window.__ss.prefs.wstrip"), 'below')

    # ---------- Latin letters: in the note, and in the text boxes ----------
    pg.evaluate("()=>{ window.__ss.setWordStrip('above'); window.__ss.moveCaret(1e9); }")
    tap(pg, cdp, '.cell[data-nav="enter"]')
    hold(pg, cdp, KEY_AT(4)); C.eq('holding the centre brings up the Latin letters', mode(pg), 'latin')
    for ch in 'we me': letter(pg, cdp, ch)
    C.ok('typing "me" offers words that begin with it', any(w.startswith('me') for w in cands(pg, 6)), cands(pg, 6))
    for ch in 't ': letter(pg, cdp, ch)
    C.ok('words typed in English are written in Stemsyl', english(pg).rstrip().endswith('We met'), english(pg)[-20:])
    hold(pg, cdp, KEY_AT(5)); tap(pg, cdp, '[data-app="title"]'); pg.wait_for_timeout(150)
    for _ in range(12): tap(pg, cdp, '.cell[data-nav="bs"]', 40)
    for ch in 'Walk': letter(pg, cdp, ch)
    tap(pg, cdp, '#fieldGo'); pg.wait_for_timeout(700)
    C.eq('the title box renames the note', pg.evaluate("()=>JSON.parse(localStorage.getItem('%s')).notes[0].title" % KEY), 'Walk')
    hold(pg, cdp, KEY_AT(5)); tap(pg, cdp, '[data-app="menu"]'); pg.wait_for_timeout(250)
    pg.evaluate("()=>document.getElementById('writeEn').scrollIntoView({block:'center'})"); pg.wait_for_timeout(100); tap(pg, cdp, '#writeEn')
    C.eq('Write English opens a text box', pg.evaluate("()=>window.__ss.field"), 'english')
    for ch in 'good day': letter(pg, cdp, ch)
    pg.wait_for_timeout(400); tap(pg, cdp, '#fieldGo'); pg.wait_for_timeout(300)
    C.ok('Insert writes it into the note in Stemsyl', english(pg).rstrip().endswith('good day'), english(pg)[-20:])

    # ---------- option keys ----------
    hold(pg, cdp, KEY_AT(5))
    g0 = pg.evaluate("()=>window.__ss.prefs.wgs"); tap(pg, cdp, '[data-app="larger"]')
    C.eq('A+ makes the glyphs larger', pg.evaluate("()=>window.__ss.prefs.wgs"), min(56, g0 + 8))
    a0 = pg.evaluate("()=>window.__ss.prefs.aid"); tap(pg, cdp, '[data-app="aid"]')
    C.ok('Under switches what goes under each word', pg.evaluate("()=>window.__ss.prefs.aid") != a0)
    v0 = pg.evaluate("()=>window.__ss.prefs.view"); tap(pg, cdp, '[data-app="view"]')
    C.ok('View switches the note to English or IPA', pg.evaluate("()=>window.__ss.prefs.view") != v0)
    n = pg.evaluate("()=>JSON.parse(localStorage.getItem('%s')).notes.length" % KEY); tap(pg, cdp, '[data-app="new"]'); pg.wait_for_timeout(700)
    C.eq('New starts a new note', pg.evaluate("()=>JSON.parse(localStorage.getItem('%s')).notes.length" % KEY), n + 1)
    C.eq('no page errors', errs, [])
    shot(pg, 'watch-options', '#app')
    pg.context.close()

    # ---------- dark theme ----------
    pg, cdp, errs = open_app(b, WATCH, 208, 248, doc=toks, prefs=PREFS, dark=True)
    bg = pg.evaluate("()=>getComputedStyle(document.querySelector('.cell[data-pos=\"0\"]')).backgroundColor")
    C.ok('the dark theme draws dark keys', bg in ('rgb(0, 0, 0)', 'rgba(0, 0, 0, 0)') or bg.startswith('rgb(1') or bg.startswith('rgb(2') or bg.startswith('rgb(3'), bg)
    C.eq('no page errors in the dark theme', errs, [])
    b.close()
C.report()
