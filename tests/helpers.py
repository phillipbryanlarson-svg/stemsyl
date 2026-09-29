# Shared by the tests: where the apps are, a small pass/fail record, and touch gestures for the browser.
import functools, http.server, json, os, sys, threading
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DOCS = os.path.join(ROOT, 'docs')
sys.path.insert(0, os.path.join(ROOT, 'tools'))

# The apps are served over http from a local web server, as a website serves them: a browser keeps what a page stores
# for its web address, which it does not reliably do for files opened from disk.
class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
def _serve(folder):
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(_Quiet, directory=folder))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return 'http://127.0.0.1:%d/' % srv.server_address[1]
SITE = _serve(DOCS)
PHONE = SITE + 'stemsyl-keyboard.html'
WATCH = SITE + 'stemsyl-keyboard-watch.html'
TRAINER = SITE + 'stemsyl-trainer.html'
OUT = os.path.join(ROOT, 'tests', 'out')          # screenshots, for a person to look at; not checked in
KEY = 'stemsyl_keyboard_v1'

class Checks:
    """records each check; report() prints a summary and exits non-zero if any failed"""
    def __init__(self, name):
        self.name, self.failed, self.n = name, [], 0
        print('#', name)
    def ok(self, what, cond, detail=''):
        self.n += 1
        if cond: print('  ok   ', what)
        else:
            self.failed.append(what); print('  FAIL ', what, '--', detail)
        return cond
    def eq(self, what, got, want):
        return self.ok(what, got == want, 'got %r, want %r' % (got, want))
    def report(self):
        print('%s: %d checks, %d failed' % (self.name, self.n, len(self.failed)))
        sys.exit(1 if self.failed else 0)

# ---------- pages ----------
def seed_script(doc=(), prefs=None, title='Test'):
    """an init script that starts the app with one note (these tokens) and these settings, unless it has saved its own"""
    state = {'notes': [{'id': 'n1', 'title': title, 'doc': list(doc), 'caret': len(doc), 'updated': 1}], 'cur': 'n1', 'prefs': prefs or {}}
    return "if(!localStorage.getItem('%s')) localStorage.setItem('%s', %s)" % (KEY, KEY, json.dumps(json.dumps(state)))

def open_app(b, url, w, h, doc=(), prefs=None, dark=False, touch=True, seed=True):
    """a new page of the app at this size, with its word list fully loaded; returns (page, cdp session, errors)"""
    ctx = b.new_context(viewport={'width': w, 'height': h}, has_touch=touch, is_mobile=touch, device_scale_factor=2,
                        color_scheme='dark' if dark else 'light')
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    if seed: pg.add_init_script(seed_script(doc, prefs))
    pg.goto(url)
    pg.evaluate("()=>new Promise(r=>window.__ss.words.onMore(r))"); pg.wait_for_timeout(120)
    return pg, cdp, errs

def reopen(pg, url):
    """open the app again in a new tab of the same browser profile and close the old one, as a person coming back to it
       would; first a pause, as the app saves 450 ms after a change"""
    ctx = pg.context; pg.wait_for_timeout(1000)
    new = ctx.new_page(); cdp = ctx.new_cdp_session(new); errs = []
    new.on('pageerror', lambda e: errs.append(str(e)))
    new.goto(url); new.evaluate("()=>new Promise(r=>window.__ss.words.onMore(r))"); new.wait_for_timeout(120)
    pg.close()
    return new, cdp, errs

def shot(pg, name, sel=None):
    os.makedirs(OUT, exist_ok=True)
    (pg.query_selector(sel) if sel else pg).screenshot(path=os.path.join(OUT, name + '.png'))

# ---------- gestures (touch events, as a finger makes them) ----------
def touch(cdp, typ, pts):
    cdp.send('Input.dispatchTouchEvent', {'type': typ, 'touchPoints': [{'x': x, 'y': y} for x, y in pts]})
def centre(pg, sel):
    bb = pg.query_selector(sel).bounding_box(); return bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
def tap_at(pg, cdp, x, y, wait=90):
    touch(cdp, 'touchStart', [(x, y)]); touch(cdp, 'touchEnd', []); pg.wait_for_timeout(wait)
def tap(pg, cdp, sel, wait=90):
    x, y = centre(pg, sel); tap_at(pg, cdp, x, y, wait)
def hold_at(pg, cdp, x, y, ms=650):
    touch(cdp, 'touchStart', [(x, y)]); pg.wait_for_timeout(ms); touch(cdp, 'touchEnd', []); pg.wait_for_timeout(450)
def hold(pg, cdp, sel, ms=650):
    x, y = centre(pg, sel); hold_at(pg, cdp, x, y, ms)
def swipe(pg, cdp, x0, x1, y):
    """a quick sideways swipe; the wait after it lets the next tap count (a browser drops a tap made right after one)"""
    touch(cdp, 'touchStart', [(x0, y)])
    for i in range(1, 7): touch(cdp, 'touchMove', [(x0 + (x1 - x0) * i / 6, y)]); pg.wait_for_timeout(20)
    touch(cdp, 'touchEnd', []); pg.wait_for_timeout(450)

# ---------- the 3 x 3 keys ----------
KEY_AT = lambda i: '.grid3 > :nth-child(%d)' % (i + 1)
CPOS = {'u': '0', 'c': '3', 'd': '6'}; VPOS = {'u': '1', 'c': '4', 'd': '7'}
CONS_AT = {'t': 'u', 'n': 'c', 'd': 'd', 'p': 'u', 'm': 'c', 'b': 'd', 'f': 'u', 'w': 'c', 'v': 'd', 'T': 'u', 'h': 'c', 'D': 'd',
           's': 'u', 'l': 'c', 'z': 'd', 'S': 'u', 'r': 'c', 'Z': 'd', 'C': 'u', 'y': 'c', 'J': 'd', 'k': 'u', 'N': 'c', 'g': 'd'}
VOW_AT = {'Y': 'u', 'E': 'u', 'I': 'u', 'B': 'u', 'a': 'c', 'A': 'c', 'e': 'c', 'i': 'c', 'u': 'c', '@': 'c', 'W': 'd', 'O': 'd', 'G': 'd', 'U': 'd'}
def sound3(pg, cdp, ch):
    """one sound: its tick position, then its colour"""
    if ch in CONS_AT: tap(pg, cdp, '.cell[data-pos="%s"]' % CPOS[CONS_AT[ch]]); tap(pg, cdp, '.cell[data-cons="%s"]' % ch)
    else: tap(pg, cdp, '.cell[data-pos="%s"]' % VPOS[VOW_AT[ch]]); tap(pg, cdp, '.cell[data-vow="%s"]' % ch)
LATIN = ['abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy', "z'"]
def letter(pg, cdp, ch):
    """one Latin letter on the watch: its group, then the letter (a space is the space key)"""
    if ch == ' ': tap(pg, cdp, '.cell[data-nav="space"]'); return
    if ch.isupper(): tap(pg, cdp, '.cell[data-lg="5"]'); tap(pg, cdp, '.cell[data-lat="shift"]')
    tap(pg, cdp, '.cell[data-lg="%d"]' % next(i for i, g in enumerate(LATIN) if ch.lower() in g))
    tap(pg, cdp, '.cell[data-lat="%s"]' % ch.lower() if ch != "'" else ".cell[data-lat=\"'\"]")

# ---------- state ----------
def doc(pg): return pg.evaluate("()=>window.__ss.doc")
def sounds(pg, frm=0): return ''.join(t[1] for t in doc(pg)[frm:] if t[0] == 's')
def english(pg): return pg.evaluate("()=>window.__ss.toEnglish(window.__ss.doc)")
def cands(pg, n=8): return pg.evaluate("n=>window.__ss.cands().slice(0,n).map(c=>c.w)", n)
def outside(pg, frame='#app'):
    """visible elements that poke out of the frame (what a scroller clips counts only where it shows)"""
    return pg.evaluate("""f=>{ var a=document.querySelector(f).getBoundingClientRect(), bad=[];
      document.querySelectorAll(f+' *').forEach(function(e){ if(!e.getClientRects().length) return; if(getComputedStyle(e).visibility==='hidden') return;
        var r=e.getBoundingClientRect(); if(!r.width||!r.height) return; r={left:r.left,top:r.top,right:r.right,bottom:r.bottom};
        var p=e.parentElement; while(p&&p!==document.querySelector(f)){ var ps=getComputedStyle(p); if(ps.overflowX!=='visible'||ps.overflowY!=='visible'){ var q=p.getBoundingClientRect();
            r.left=Math.max(r.left,q.left); r.top=Math.max(r.top,q.top); r.right=Math.min(r.right,q.right); r.bottom=Math.min(r.bottom,q.bottom); } p=p.parentElement; }
        if(r.right<=r.left||r.bottom<=r.top) return;
        if(r.left<a.left-0.5||r.top<a.top-0.5||r.right>a.right+0.5||r.bottom>a.bottom+0.5) bad.push((e.id||e.className||e.tagName)+' '+[r.left,r.top,r.right,r.bottom].map(Math.round)); });
      return bad; }""", frame)
def cut_keys(pg):
    """keys whose content is cut off"""
    return pg.evaluate("""()=>[].filter.call(document.querySelectorAll('.grid3 .cell'),c=>c.scrollHeight>c.clientHeight+1||c.scrollWidth>c.clientWidth+1)
        .map(c=>(c.dataset.pos||c.dataset.app||c.dataset.k||c.dataset.nav||c.className)+' '+c.scrollWidth+'x'+c.scrollHeight+'>'+c.clientWidth+'x'+c.clientHeight)""")
