# The phone keyboard (docs/stemsyl-keyboard.html): typing by sound on both layouts, the word strip, captions, the 3 × 3
# holds and swipes, pasting and typing English, undo, and that notes and settings survive a reload.
from playwright.sync_api import sync_playwright
from helpers import *

C = Checks('phone keyboard')
def key(pg, cdp, k): tap(pg, cdp, '#kb [data-k="%s"]' % k)
def caps(pg): return pg.evaluate("()=>[].map.call(document.querySelectorAll('#sheet .w .rd'),e=>e.textContent)")
def page3(pg):
    return pg.evaluate("()=>document.querySelector('.cell.num')?'nums':document.querySelector('.cell.punct')?'punct':"
                       "document.querySelector('.cell[data-nav=home]')?'nav':document.querySelector('.cell[data-pos]')?'sounds':"
                       "document.querySelector('.cell[data-unselect]')?'colours':'?'")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg, cdp, errs = open_app(b, PHONE, 393, 852, prefs={'aid': 'en', 'view': 'stemsyl', 'layout': 'keys'})
    C.eq('opens on the Keys layout', pg.evaluate("()=>window.__ss.layout"), 'keys')
    C.eq('a key for each of the 38 sounds, and 9 more', pg.evaluate("()=>document.querySelectorAll('#kb .key').length"), 47)
    # typing by sound: k a t, the strip, a space
    for k in ['c:k', 'v:a', 'c:t']: key(pg, cdp, k)
    C.eq('three taps write k a t', sounds(pg), 'kat')
    C.eq('the strip offers cat first', cands(pg, 1), ['cat'])
    key(pg, cdp, 'u:space')
    C.eq('after a space, cat goes under the word by itself (a capital: it starts the note)', caps(pg), ['Cat'])
    # a homophone stays as sounds until one is picked
    for k in ['c:s', 'v:I']: key(pg, cdp, k)
    C.ok('see and sea are both offered', {'see', 'sea'} <= set(cands(pg, 6)), cands(pg, 6))
    key(pg, cdp, 'u:space')
    C.eq('unpicked, the homophone shows its sounds', caps(pg)[-1], '/si/')
    pg.evaluate("()=>window.__ss.moveCaret(window.__ss.caret-1)")
    k = cands(pg, 8).index('sea'); tap(pg, cdp, '.cand[data-c="%d"]' % k)
    C.eq('picking sea puts it under the word', caps(pg)[-1], 'sea')
    pg.evaluate("()=>window.__ss.moveCaret(1e9)")
    # the name mark, and the numbers page
    key(pg, cdp, 'u:name')
    for k in ['c:J', 'v:A', 'c:n']: key(pg, cdp, k)
    key(pg, cdp, 'u:space')
    C.eq('after the name mark, Jon and John stay undecided', caps(pg)[-1], '/dʒɑn/')
    key(pg, cdp, 'u:layer'); key(pg, cdp, 'd:7'); key(pg, cdp, 'p::'); key(pg, cdp, 'd:4'); key(pg, cdp, 'd:5'); key(pg, cdp, 'u:layer')
    C.eq('numbers and the time colon', english(pg).split(' ')[-1], '7:45')
    shot(pg, 'phone-keys')
    # hold delete: it repeats
    n = len(doc(pg)); x, y = centre(pg, '#kb [data-k="u:bs"]'); hold_at(pg, cdp, x, y, 1100)
    C.ok('holding delete deletes more than one', len(doc(pg)) <= n - 3, (n, len(doc(pg))))
    # undo
    m = len(doc(pg)); pg.keyboard.press('Control+z'); pg.wait_for_timeout(100)
    C.eq('Ctrl-Z undoes the last delete', len(doc(pg)), m + 1)

    # ---- 3 × 3 ----
    pg.evaluate("()=>window.__ss.moveCaret(1e9)")
    tap(pg, cdp, '[data-layout="grid3"]')
    C.eq('the switch shows the 3 × 3 keys', [pg.evaluate("()=>window.__ss.layout"), page3(pg)], ['grid3', 'sounds'])
    key(pg, cdp, 'u:space') if pg.query_selector('#kb [data-k="u:space"]') else tap(pg, cdp, '.cell[data-nav="space"]')
    n0 = len(doc(pg))
    for ch in 'hWs': sound3(pg, cdp, ch)
    C.eq('two taps a sound: h ow s', sounds(pg, n0), 'hWs')
    C.eq('the strip offers house', cands(pg, 1), ['house'])
    tap(pg, cdp, '.cand[data-c="0"]')
    C.eq('back on the tick positions after picking', page3(pg), 'sounds')
    got = []
    for _ in range(4):
        hold(pg, cdp, '.cell[data-pos="4"]' if page3(pg) == 'sounds' else KEY_AT(4)); got.append(page3(pg))
    C.eq('holding the centre steps through the pages', got, ['nums', 'punct', 'nav', 'sounds'])
    kb = pg.query_selector('#kb').bounding_box(); y = kb['y'] + kb['height'] * 0.6
    c0 = pg.evaluate("()=>window.__ss.caret"); swipe(pg, cdp, kb['x'] + kb['width'] * 0.75, kb['x'] + kb['width'] * 0.75 - 110, y)
    C.eq('a 110-point swipe left moves the cursor 3 sounds back', pg.evaluate("()=>window.__ss.caret"), c0 - 3)
    tap(pg, cdp, '.cell[data-pos="0"]')
    C.eq('a tap right after a swipe still counts', page3(pg), 'colours')
    tap(pg, cdp, '.cell[data-unselect]')
    shot(pg, 'phone-3x3')
    C.eq('nothing wider than the screen', pg.evaluate("()=>document.documentElement.scrollWidth<=innerWidth"), True)

    # ---- typing and pasting English ----
    pg.evaluate("()=>window.__ss.moveCaret(1e9)")
    pg.keyboard.type(' Hello world. '); pg.wait_for_timeout(150)
    C.ok('typed English becomes its sounds', english(pg).rstrip().endswith('Hello world.'), english(pg)[-30:])
    tap(pg, cdp, '#menuBtn'); pg.wait_for_timeout(200)
    pg.fill('#pasteIn', 'The quick brown fox.'); pg.click('#pasteGo'); pg.wait_for_timeout(300)
    C.ok('pasted English is inserted as Stemsyl', 'The quick brown fox.' in english(pg), english(pg)[-40:])
    # the English view
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    pg.click('#viewBtn'); pg.wait_for_timeout(100)
    C.ok('the English view shows the note as text', 'fox' in pg.evaluate("()=>[].map.call(document.querySelectorAll('#sheet .g.t'),e=>e.textContent).join('')"))
    pg.click('#viewBtn'); pg.click('#viewBtn'); pg.wait_for_timeout(100)
    C.eq('three taps on the view button come back to Stemsyl', pg.evaluate("()=>document.querySelectorAll('#sheet .g.t').length"), 0)
    C.eq('no page errors', errs, [])
    # saved: coming back to the app finds the note and the layout
    before = english(pg); pg, cdp, errs = reopen(pg, PHONE)
    C.eq('coming back finds the note', english(pg), before)
    C.eq('and the layout', pg.evaluate("()=>window.__ss.layout"), 'grid3')

    # ---- dark theme, and a small phone ----
    for dark, w, h in [(True, 393, 852), (False, 320, 568)]:
        pg2, cdp2, errs2 = open_app(b, PHONE, w, h, prefs={'layout': 'keys'}, dark=dark)
        C.ok('%s at %d × %d: loads, nothing wider than the screen' % ('dark theme' if dark else 'light theme', w, h),
             not errs2 and pg2.evaluate("()=>document.documentElement.scrollWidth<=innerWidth"), errs2)
        shot(pg2, 'phone-%s-%dx%d' % ('dark' if dark else 'light', w, h))
    b.close()
C.report()
