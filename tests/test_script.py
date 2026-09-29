# The script as the apps draw it, checked against SPECIFICATION.md: the sound tables, the colours, the glyph geometry, the
# syllable rule's worked examples, the numerals and the caption rule. If the apps or the specification change, this is
# where they must still agree.
import re
from playwright.sync_api import sync_playwright
from helpers import *

C = Checks('the script')
SPEC = open(os.path.join(ROOT, 'SPECIFICATION.md'), encoding='utf-8').read()

def md_table(after, n=0):
    """the rows of the n-th Markdown table after the line that starts with `after`"""
    i = SPEC.index(after)
    rows, seen = [], 0
    for line in SPEC[i:].split('\n')[1:]:
        if line.startswith('|'):
            rows.append([c.strip() for c in line.strip('|').split('|')])
        elif rows:
            if seen == n: return [r for r in rows[2:]]
            seen += 1; rows = []
    return rows[2:]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg, cdp, errs = open_app(b, PHONE, 412, 915, touch=False, seed=False)
    app = pg.evaluate("""()=>({CODE:CODE, NAME:CONS_NAME, CIPA:CONS_IPA, EX:CONS_EX, VNAME:VNAME, VCHAR:VCHAR,
        VT:Object.fromEntries(Object.keys(VCHAR).map(function(k){ return [k, vowelTick(VCHAR[k])]; })),
        VIPA:Object.fromEntries(Object.keys(VCHAR).map(function(k){ return [k, soundIPA(k)]; })),
        geo:{SYL_W:SYL_W, LONE_W:LONE_W, GH:GH, CY:CY, TX:TX, LONE_X:LONE_X, STEM:STEM, LONE_STEM:LONE_STEM, TL:TL, TICKY:TICKY,
             NUM_W:NUM_W, NUM_U:NUM_U, NUM_G:NUM_G, PUNCT_W:PUNCT_W, NAME_W:NAME_W},
        mask:NUMMASK, punct:Object.keys(PUNCT)})""")
    POSW = {'u': 'up', 'c': 'centred', 'd': 'down'}

    # ---- the sound tables (appendix 11.1) ----
    cons = md_table('Consonants:')
    C.eq('24 consonants in the specification and in the app', (len(cons), len(app['CODE'])), (24, 24))
    bad = [r[0] for r in cons if app['CODE'].get(r[0]) != [r[5], {'up': 'u', 'centred': 'c', 'down': 'd'}[r[6]]]
           or app['NAME'][r[0]] != r[1] or app['CIPA'][r[0]] != r[2] or app['EX'][r[0]] != r[3]]
    C.eq('every consonant has the colour, position, name, IPA and example the specification gives', bad, [])
    vows = md_table('Vowels:')
    C.eq('14 vowels in the specification and in the app', (len(vows), len(app['VCHAR'])), (14, 14))
    vcol = lambda c: 'blue' if c == 'vblue' else c
    bad = [r[0] for r in vows if [vcol(app['VT'][r[0]][0]), POSW[app['VT'][r[0]][1]]] != [r[5], r[6]]
           or app['VNAME'][r[0]] != [r[1], r[3]] or app['VIPA'][r[0]] != r[2]]
    C.eq('every vowel has the colour, position, name, IPA and example the specification gives', bad, [])
    # section 2.1's family table agrees with the appendix
    fam = md_table('The families are loosely ordered')
    got = [[r[0].strip('*')] + [c.split(' ')[0] for c in r[1:]] for r in fam]
    want = [[f] + [app['NAME'][k] for k in sorted([k for k in app['CODE'] if app['CODE'][k][0] == f], key=lambda k: 'ucd'.index(app['CODE'][k][1]))]
            for f in ['ink', 'rose', 'mauve', 'indigo', 'blue', 'emerald', 'olive', 'amber']]
    C.eq('the consonant families table (2.1) matches the app', got, want)

    # ---- geometry (appendix 11.2 and section 3) ----
    g = app['geo']
    C.eq('glyph 64 tall, stem line at 32, syllable 42 wide, lone consonant 18', [g['GH'], g['CY'], g['SYL_W'], g['LONE_W']], [64, 32, 42, 18])
    C.eq('stem from 5 to 37; tick slots at 9, 21, 33; stub 4 to 14 with its tick at 9', [g['STEM'], g['TX'], g['LONE_STEM'], g['LONE_X']], [[5, 37], [9, 21, 33], [4, 14], 9])
    C.eq('tick length 14: up 18-32, centred 18-46, down 32-46', [g['TL'], g['TICKY']], [14, {'u': [18, 32], 'c': [18, 46], 'd': [32, 46]}])
    C.eq('numeral 48 wide, dots 10.4 with gaps 2.08; punctuation 30 wide; name mark 22', [g['NUM_W'], g['NUM_U'], g['NUM_G'], g['PUNCT_W'], g['NAME_W']], [48, 10.4, 2.08, 30, 22])
    C.ok('the specification states the same measures', all(x in SPEC for x in ['x = 5 to x = 37', 'x = 9 for the **onset**', 'x = 21 for the **vowel**',
         'x = 33 for the **coda**', 'L = 14', 'from x = 4 to x = 14', '10.4-unit squares', '2.08 units apart', 'A numeral is 48 units wide', 'Each is 30 units wide', 'It is 22 units wide']))
    # ---- numerals: a digit lights as many dots as its value, like dice ----
    ones = [bin(m).count('1') for m in app['mask']]
    C.eq('each digit lights as many dots as its value', ones, list(range(10)))
    C.eq('1 is the centre, 4 the corners, 8 the ring, 9 all', [app['mask'][1], app['mask'][4], app['mask'][8], app['mask'][9]], [16, 1 + 4 + 64 + 256, 511 - 16, 511])
    C.eq('twelve punctuation marks', sorted(app['punct']), sorted(['.', ',', '?', '!', ':', ';', '“', '”', '(', ')', '–', '/']))

    # ---- colours (3.9): the app's style sheet has the specification's values, light and dark ----
    css = open(os.path.join(DOCS, 'stemsyl-keyboard.html'), encoding='utf-8').read()
    light = css[css.index(':root{'):css.index('}', css.index(':root{'))]
    dark = css[css.index('@media (prefers-color-scheme:dark)'):]; dark = dark[:dark.index('}\n}')]
    var = {'ink': 'ink', 'rose': 'rose', 'mauve': 'mauve', 'indigo': 'indigo', 'blue (consonant)': 'blue', 'emerald': 'emerald', 'olive': 'olive',
           'amber': 'amber', 'red': 'vred', 'orange': 'vorange', 'yellow': 'vyellow', 'green': 'vgreen', 'blue (vowel)': 'vvblue', 'grey': 'vgrey',
           'violet': 'vviolet', 'mark': 'mark'}
    bad = []
    for r in md_table('### 3.9 Colour'):
        v = var[r[0]]
        for block, want in ((light, r[1]), (dark, r[2])):
            m = re.search(r'--%s:(#[0-9A-Fa-f]{6})' % v, block)
            if not m or m.group(1).lower() != want.lower(): bad.append((r[0], want, m and m.group(1)))
    C.eq('every colour in the table is the app\'s, in both themes', bad, [])

    # ---- the syllable rule's worked examples (3.4) ----
    by_name = {v: k for k, v in app['NAME'].items()}; by_name.update({v[0]: k for k, v in app['VNAME'].items()})
    rows = md_table('4. The glyphs follow in the order of their sounds')
    bad = []
    for word, snd, glyphs in rows:
        pron = ''.join(by_name[x] for x in snd.split(' '))
        got = pg.evaluate("""p=>syllabify(phonemes(p)).map(function(u){
            function nm(c){ return CONS_NAME[c]; }
            if(u.k!=='S') return nm(u.c);
            var v=Object.keys(VCHAR).filter(function(k){ return VCHAR[k][0]===u.v[0]&&VCHAR[k][1]===u.v[1]; })[0];
            return '['+[u.on?nm(u.on):null, VNAME[v][0], u.co?nm(u.co):null].filter(Boolean).join('·')+']'; }).join(' ')""", pron)
        if got != glyphs: bad.append((word, got, glyphs))
    C.ok('the %d worked examples group as the specification shows' % len(rows), not bad and len(rows) >= 8, bad)

    # ---- the caption rule (3.10) ----
    r = pg.evaluate("""()=>{ var W=window.__ss.words; return {boy:W.exact('bB',false), cat:W.exact('kat',false), see:W.exact('sI',false),
        eye:W.exact('Y',false), uh:W.exact('@',false), jon:W.exact('JAn',true), to:W.exact('tU',false), nonword:W.exact('zNkr',false)}; }""")
    C.eq('one word with these sounds: its spelling', [r['boy'], r['cat']], ['boy', 'cat'])
    C.eq('homophones and non-words: no spelling', [r['see'], r['to'], r['nonword']], [None, None, None])
    C.eq('eye alone is I, uh alone is a', [r['eye'], r['uh']], ['i', 'a'])
    C.eq('after the name mark, names count too (Jon, John)', r['jon'], None)
    t = 'Practice makes perfect.\nWe met Jon in London at 7:45 on Monday.'
    back = pg.evaluate("t=>{ var p=window.__ss.parseText(t); return [window.__ss.toEnglish(p.tokens), p.skipped, p.tokens.filter(x=>x[0]==='nm').length]; }", t)
    C.eq('English written into Stemsyl comes back out unchanged, with names marked', back, [t, [], 3])
    C.eq('no page errors', errs, [])
    b.close()
C.report()
