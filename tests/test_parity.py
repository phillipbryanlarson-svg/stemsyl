# The same taps on the phone keyboard's 3 × 3 layout and on the watch keyboard must give the same note, the same English
# and the same word strip after every step: the watch is the phone's 3 × 3 keyboard, rearranged for a small screen.
from playwright.sync_api import sync_playwright
from helpers import *

C = Checks('phone 3 × 3 and watch agree')
# sounds by position and colour, the edit keys, numbers and punctuation, picks from the strip, cursor keys and swipes
SCRIPT = [('s', 'kat'), ('nav', 'space'), ('s', 'sI'), ('nav', 'space'), ('s', 'Y'), ('nav', 'space'), ('s', '@'), ('nav', 'space'),
          ('s', 'bB'), ('pick', 0), ('s', 'tU'), ('nav', 'space'), ('s', 'Der'), ('nav', 'bs'), ('nav', 'bs'), ('s', 'r'), ('nav', 'space'),
          ('page', 'nums'), ('k', 'd:7'), ('k', 'd:4'), ('tri', 'd:9'), ('tri', 'd:0'), ('page', 'punct'), ('k', 'p:.'), ('k', 'p:?'), ('k', 'p:“'),
          ('page', 'nav'), ('nav', 'left'), ('nav', 'left'), ('nav', 'home'), ('nav', 'end'), ('nav', 'enter'), ('page', 'sounds'),
          ('s', 'hapI'), ('pick', 1), ('s', 'wAtr'), ('nav', 'space'), ('s', 'JAn'), ('nav', 'space'), ('s', 'wOk'), ('swipe', 'left'),
          ('s', 'n'), ('swipe', 'right'), ('s', 'Dis'), ('nav', 'enter')]
WATCH_HOLD = {'nums': 1, 'punct': 3, 'options': 5, 'nav': 7, 'sounds': 4}

def run(b, url, w, h, watch):
    pg, cdp, errs = open_app(b, url, w, h, prefs={'gs': 56, 'wgs': 40, 'aid': 'en', 'view': 'stemsyl', 'layout': 'grid3'})
    page, out = 'sounds', []
    for act, arg in SCRIPT:
        if act == 's':
            for ch in arg: sound3(pg, cdp, ch)
        elif act == 'nav': tap(pg, cdp, '.cell[data-nav="%s"]' % arg)
        elif act == 'k': tap(pg, cdp, '.cell[data-k="%s"]' % arg)
        elif act == 'tri':
            bb = pg.query_selector('.tri[data-k="%s"]' % arg).bounding_box(); f = 0.25 if arg == 'd:9' else 0.75
            tap_at(pg, cdp, bb['x'] + bb['width'] * f, bb['y'] + bb['height'] * f)
        elif act == 'pick': tap(pg, cdp, '.cand[data-c="%d"]' % arg)
        elif act == 'page':
            if watch: hold(pg, cdp, KEY_AT(WATCH_HOLD[arg]))
            else:          # the phone: holding the centre steps sounds → numbers → punctuation → cursor → sounds
                while page != arg:
                    hold(pg, cdp, KEY_AT(4))
                    page = pg.evaluate("()=>document.querySelector('.cell.num')?'nums':document.querySelector('.cell.punct')?'punct':"
                                       "document.querySelector('.cell[data-nav=home]')?'nav':document.querySelector('.cell[data-pos]')?'sounds':'?'")
        elif act == 'swipe':
            kb = pg.query_selector('.grid3').bounding_box(); y = kb['y'] + kb['height'] * 0.5; cx = kb['x'] + kb['width'] / 2
            d = 55 if arg == 'right' else -55
            swipe(pg, cdp, cx - d, cx + d, y)
        out.append((act, arg, pg.evaluate("()=>({doc:JSON.stringify(window.__ss.doc), caret:window.__ss.caret, en:window.__ss.toEnglish(window.__ss.doc),"
                                          " strip:window.__ss.cands().map(c=>c.w).join(',')})")))
    caps = pg.evaluate("()=>[].map.call(document.querySelectorAll('#sheet .rd'),e=>e.textContent)")
    pg.context.close()
    return out, caps, errs

with sync_playwright() as p:
    b = p.chromium.launch()
    A, capA, eA = run(b, PHONE, 412, 915, False)
    B, capB, eB = run(b, WATCH, 208, 248, True)
    diff = [(act, arg, [k for k in x if x[k] != y[k]]) for (act, arg, x), (_, _, y) in zip(A, B) if x != y]
    C.eq('all %d steps give the same note, cursor, English and word strip' % len(SCRIPT), diff[:3], [])
    C.eq('the same English under every word', capA, capB)
    C.ok('the words came out as typed', B[-1][2]['en'].startswith('Cat /si/ I a boy'), B[-1][2]['en'][:40])
    C.eq('no page errors', eA + eB, [])
    b.close()
C.report()
