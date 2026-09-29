# Builds the web and PDF versions of the specification from SPECIFICATION.md:
#   docs/stemsyl.html               the specification as a web page (light and dark), with its figures from docs/figures
#   docs/stemsyl-specification.pdf  the same page printed to PDF (US Letter) by Chromium, with page numbers and metadata
# Run after figures.py. Needs the Python packages markdown, playwright (with Chromium) and pypdf.
import html as H, os, re, sys
import markdown
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DOCS = os.path.join(ROOT, 'docs')
SRC = os.path.join(ROOT, 'SPECIFICATION.md')
OUT_HTML = os.path.join(DOCS, 'stemsyl.html')
OUT_PDF = os.path.join(DOCS, 'stemsyl-specification.pdf')

TITLE = 'Stemsyl: a colour-stem phonetic script for English, with keyboards for phones and watches'
AUTHOR = 'Phillip Bryan Larson'
VERSION = '1.0'
DATE = '28 September 2026'
DESCRIPTION = ('Specification of Stemsyl, a phonetic script for English in which each syllable is a stem with coloured ticks, '
               'and of its keyboards for phones and watches. Dedicated to the public domain (CC0 1.0).')
KEYWORDS = ('Stemsyl; phonetic script; writing system; English; colour; syllable; 3x3 keyboard; smartwatch keyboard; '
            'text entry; defensive publication; CC0')

# the colours, for the swatches in the colour table and the names in the sound tables: [light, dark]
COLOURS = {'ink': ['#2C2C2A', '#E8E6DD'], 'rose': ['#B65754', '#E07B77'], 'mauve': ['#A55B91', '#D487BE'],
           'indigo': ['#4848B9', '#9084FF'], 'blue': ['#238DC0', '#6FC6FC'], 'emerald': ['#229279', '#55BCA1'],
           'olive': ['#4F7103', '#BCDD73'], 'amber': ['#A19005', '#A6940E'], 'red': ['#C40027', '#C34A55'],
           'orange': ['#8F2400', '#FF7F00'], 'yellow': ['#A88600', '#FFE135'], 'green': ['#236B27', '#A1FD60'],
           'vblue': ['#002FEC', '#5081C8'], 'grey': ['#5F5F5F', '#999999'], 'violet': ['#582684', '#9826EA']}

CSS = r"""
:root{
  --paper:#ffffff; --text:#23231f; --muted:#66645c; --rule:#e4e2da; --soft:#f6f5f0; --mark:#534AB7; --link:#4a41a8;
  --serif:"Charis SIL","Liberation Serif",Georgia,"Times New Roman",serif;
  --sans:"Carlito","Calibri",-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:"DejaVu Sans Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root{ --paper:#111110; --text:#e8e6dd; --muted:#aaa89f; --rule:#34332e; --soft:#1b1b19; --mark:#AFA9EC; --link:#b9b3f2; color-scheme:dark; }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--text);font:17px/1.6 var(--serif);font-kerning:normal}
.top{font:14px/1.4 var(--sans);border-bottom:1px solid var(--rule);background:var(--paper);position:sticky;top:0;z-index:2}
.top .in{max-width:1080px;margin:0 auto;padding:10px 16px;display:flex;gap:18px;align-items:center;overflow-x:auto;white-space:nowrap;scrollbar-width:none}
.top .in::-webkit-scrollbar{display:none}
.top b{font-weight:700;letter-spacing:.02em;margin-right:auto}
.top a{color:var(--link);text-decoration:none}
.top a:hover{text-decoration:underline}
main{max-width:760px;margin:0 auto;padding:28px 16px 64px}
h1{font:700 44px/1.1 var(--sans);letter-spacing:-.01em;margin:10px 0 6px}
h1 + p{font:600 21px/1.35 var(--sans);margin:0 0 8px;color:var(--text)}
h1 + p + p{font:15px/1.5 var(--sans);color:var(--muted);margin:0 0 16px}
h1 + p + p + p{font-size:15px;background:var(--soft);border-left:3px solid var(--mark);padding:10px 14px;border-radius:0 8px 8px 0}
h2{font:700 26px/1.25 var(--sans);margin:44px 0 10px;padding-top:6px;border-top:1px solid var(--rule)}
h3{font:700 19px/1.3 var(--sans);margin:28px 0 6px}
h2,h3{scroll-margin-top:56px}
p,ul,ol{margin:0 0 14px}
li{margin:3px 0}
li > ul{margin:4px 0 6px}
a{color:var(--link)}
code{font:.84em var(--mono);background:var(--soft);border:1px solid var(--rule);border-radius:5px;padding:.08em .35em;word-break:break-word}
blockquote{margin:0 0 16px;padding:10px 16px;background:var(--soft);border-left:3px solid var(--mark);border-radius:0 8px 8px 0}
blockquote p{margin:0}
.tw{overflow-x:auto;margin:6px 0 18px}
table{border-collapse:collapse;font:14.5px/1.4 var(--sans);min-width:100%}
th,td{text-align:left;vertical-align:top;padding:6px 10px;border-bottom:1px solid var(--rule)}
th{font-weight:700;border-bottom:2px solid var(--rule);white-space:nowrap}
tbody tr:nth-child(even){background:var(--soft)}
td em{font-family:var(--serif)}
figure{margin:22px 0 26px;text-align:center}
figure img{max-width:100%;height:auto;border-radius:10px;border:1px solid var(--rule);background:#fff}
figure.wide{margin-left:calc(50% - min(540px, 50vw - 16px));margin-right:calc(50% - min(540px, 50vw - 16px))}
figcaption{font:14px/1.45 var(--sans);color:var(--muted);margin-top:8px}
p.note{font:italic 14px/1.45 var(--sans);color:var(--muted);margin-top:-8px}
.sw{display:inline-block;width:.95em;height:.95em;border-radius:3px;vertical-align:-.12em;margin-right:6px;border:1px solid rgba(0,0,0,.18)}
.c-ink{color:#2C2C2A}.c-rose{color:#B65754}.c-mauve{color:#A55B91}.c-indigo{color:#4848B9}.c-blue{color:#238DC0}.c-emerald{color:#229279}.c-olive{color:#4F7103}.c-amber{color:#A19005}
.c-red{color:#C40027}.c-orange{color:#8F2400}.c-yellow{color:#A88600}.c-green{color:#236B27}.c-vblue{color:#002FEC}.c-grey{color:#5F5F5F}.c-violet{color:#582684}
@media (prefers-color-scheme:dark){
  .c-ink{color:#E8E6DD}.c-rose{color:#E07B77}.c-mauve{color:#D487BE}.c-indigo{color:#9084FF}.c-blue{color:#6FC6FC}.c-emerald{color:#55BCA1}.c-olive{color:#BCDD73}.c-amber{color:#A6940E}
  .c-red{color:#C34A55}.c-orange{color:#FF7F00}.c-yellow{color:#FFE135}.c-green{color:#A1FD60}.c-vblue{color:#5081C8}.c-grey{color:#999999}.c-violet{color:#9826EA}
  .sw{border-color:rgba(255,255,255,.25)}
}
h2#contents + ol{columns:2;column-gap:36px;font-family:var(--sans)}
h2#contents + ol li{break-inside:avoid;margin:0 0 5px}
.foot{font:13px/1.5 var(--sans);color:var(--muted);border-top:1px solid var(--rule);margin-top:48px;padding-top:14px}
@media (max-width:600px){ .top .in{gap:14px} h2#contents + ol{columns:1} body{font-size:16px} h1{font-size:36px} h2{font-size:23px} table{font-size:13.5px} th,td{padding:5px 7px} }
@page{size:Letter;margin:17mm 17mm 19mm}
@media print{
  :root{--paper:#fff;--text:#1d1d1b;--muted:#5b5a53;--rule:#d8d6cd;--soft:#f5f4ef;--mark:#534AB7;--link:#1d1d1b;color-scheme:light}
  .c-ink{color:#2C2C2A}.c-rose{color:#B65754}.c-mauve{color:#A55B91}.c-indigo{color:#4848B9}.c-blue{color:#238DC0}.c-emerald{color:#229279}.c-olive{color:#4F7103}.c-amber{color:#A19005}
  .c-red{color:#C40027}.c-orange{color:#8F2400}.c-yellow{color:#A88600}.c-green{color:#236B27}.c-vblue{color:#002FEC}.c-grey{color:#5F5F5F}.c-violet{color:#582684}
  .top,.foot .web{display:none}
  body{font-size:10.6pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  main{max-width:none;padding:0}
  h1{font-size:30pt;margin-top:0} h1 + p{font-size:15pt} h1 + p + p, h1 + p + p + p{font-size:10pt}
  h2{font-size:16pt;margin:22pt 0 6pt;break-after:avoid}
  h3{font-size:12.5pt;margin:14pt 0 4pt;break-after:avoid}
  h2#1-about-this-document, h2#11-appendix-tables{break-before:page;border-top:0;padding-top:0}
  p,li{orphans:3;widows:3}
  table{font-size:9pt}
  th,td{padding:3.5pt 6pt}
  tr,figure,blockquote{break-inside:avoid}
  .tw{overflow:visible}
  figure{margin:12pt 0 14pt}
  figure.wide{margin-left:0;margin-right:0}
  figure img{border-radius:6px}
  figcaption{font-size:9pt}
  a{text-decoration:none}
  code{font-size:.82em}
}
"""

LINKS_JS = r"""<script>
/* links to the rest of the repository: on GitHub Pages they point at the repository on GitHub; elsewhere, at the files
   beside this folder */
(function(){
  var h=location.hostname, parts=location.pathname.split('/').filter(Boolean), base='../';
  if(/\.github\.io$/.test(h) && parts.length) base='https://github.com/'+h.split('.')[0]+'/'+parts[0]+'/blob/main/';
  [].forEach.call(document.querySelectorAll('a[data-repo]'),function(a){
    var p=a.getAttribute('data-repo'); a.href=(p||base.indexOf('github.com')<0)?base+p:base.replace('/blob/main/','');
  });
})();
</script>"""

def build_html():
    text = open(SRC, encoding='utf-8').read()
    md = markdown.Markdown(extensions=['tables', 'toc', 'attr_list', 'sane_lists'])
    body = md.convert(text)
    # figures: an image on its own line, then its italic caption
    def fig(m):
        img, cap = m.group(1), m.group(2)          # the caption keeps its own emphasis
        src = re.search(r'src="([^"]+)"', img).group(1)
        wide = ' class="wide"' if re.search(r'fig-(watch|phone)\.png', src) else ''
        img = img.replace('<img ', '<img loading="lazy" ')
        return '<figure%s>%s<figcaption>%s</figcaption></figure>' % (wide, img, cap)
    body = re.sub(r'<p>(<img [^>]+>)</p>\s*<p>(<em>Figure \d+\..*?)</p>', fig, body, flags=re.S)
    body = body.replace('src="docs/figures/', 'src="figures/')
    # a caption line under a table (an italic paragraph starting with a bracket or "Square")
    body = re.sub(r'<p><em>(Square brackets.*?)</em></p>', r'<p class="note">\1</p>', body, flags=re.S)
    # links out of the docs folder
    body = body.replace('href="LICENSES/CC0-1.0.txt"', 'href="https://creativecommons.org/publicdomain/zero/1.0/"')
    # tables scroll sideways on narrow screens
    body = body.replace('<table>', '<div class="tw"><table>').replace('</table>', '</table></div>')
    # colour names in the sound tables, and swatches beside the colour codes
    def colname(m):
        name = m.group(1)
        return '<td><strong class="c-%s">%s</strong></td>' % (name, name)
    body = re.sub(r'<td><strong>(ink|rose|mauve|indigo|blue|emerald|olive|amber|red|orange|yellow|green|grey|violet)</strong></td>', colname, body)
    body = body.replace('<td><strong class="c-blue">blue</strong></td>\n<td>u /ʊ/', '<td><strong class="c-vblue">blue</strong></td>\n<td>u /ʊ/')
    body = re.sub(r'<td>(#[0-9A-Fa-f]{6})</td>', lambda m: '<td><span class="sw" style="background:%s"></span>%s</td>' % (m.group(1), m.group(1)), body)
    # the apps named in the text link to them
    for f in ('stemsyl-keyboard.html', 'stemsyl-keyboard-watch.html', 'stemsyl-trainer.html'):
        body = body.replace('<code>docs/%s</code>' % f, '<a href="%s"><code>docs/%s</code></a>' % (f, f))
    body = body.replace('<code>data/stemsyl-words.tsv</code>', '<a data-repo="data/stemsyl-words.tsv" href="../data/stemsyl-words.tsv"><code>data/stemsyl-words.tsv</code></a>')
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>Stemsyl — specification %s</title>\n' % VERSION +
            '<meta name="description" content="%s">\n' % H.escape(DESCRIPTION) +
            '<meta name="author" content="%s">\n' % AUTHOR +
            '<link rel="license" href="https://creativecommons.org/publicdomain/zero/1.0/">\n'
            '<!-- Generated from SPECIFICATION.md by tools/spec.py. This text is dedicated to the public domain under CC0 1.0. -->\n'
            '<style>%s</style>\n</head>\n<body>\n' % CSS +
            '<nav class="top" aria-label="Stemsyl"><div class="in"><b>Stemsyl</b>'
            '<a href="index.html">Home</a><a href="stemsyl-keyboard.html">Keyboard</a><a href="stemsyl-keyboard-watch.html">Watch</a>'
            '<a href="stemsyl-trainer.html">Trainer</a><a href="stemsyl-specification.pdf">PDF</a>'
            '<a data-repo="" href="../">Source</a></div></nav>\n'
            '<main>\n' + body + '\n'
            '<div class="foot">Stemsyl specification %s, %s. Written by %s. Dedicated to the public domain under CC0 1.0. '
            '<span class="web">Also as a <a href="stemsyl-specification.pdf">PDF</a>.</span></div>\n' % (VERSION, DATE, AUTHOR) +
            '</main>\n' + LINKS_JS + '\n</body>\n</html>\n')
    open(OUT_HTML, 'w', encoding='utf-8').write(page)
    return page

FOOTER = ('<div style="font:8px Carlito,Arial,sans-serif;color:#77756d;width:100%;padding:0 17mm;display:flex;justify-content:space-between">'
          '<span>Stemsyl specification ' + VERSION + ' · ' + DATE + ' · CC0 1.0</span>'
          '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')

def build_pdf():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto('file://' + OUT_HTML); pg.wait_for_load_state('networkidle')
        pg.evaluate("()=>Promise.all([].map.call(document.images,function(i){ i.loading='eager'; return i.complete?1:new Promise(function(r){ i.onload=i.onerror=r; }); }))")
        pg.emulate_media(media='print')
        pg.pdf(path=OUT_PDF + '.tmp', format='Letter', print_background=True, prefer_css_page_size=True,
               display_header_footer=True, header_template='<span></span>', footer_template=FOOTER,
               margin={'top': '17mm', 'bottom': '19mm', 'left': '17mm', 'right': '17mm'}, outline=True, tagged=True)
        b.close()
    r = PdfReader(OUT_PDF + '.tmp'); w = PdfWriter(clone_from=r)
    w.add_metadata({'/Title': TITLE + ' — Specification ' + VERSION, '/Author': AUTHOR, '/Subject': DESCRIPTION,
                    '/Keywords': KEYWORDS, '/Creator': 'tools/spec.py (Chromium)', '/Producer': 'pypdf'})
    with open(OUT_PDF, 'wb') as f: w.write(f)
    os.remove(OUT_PDF + '.tmp')
    return len(r.pages)

if __name__ == '__main__':
    build_html()
    n = build_pdf()
    print('written', os.path.relpath(OUT_HTML, ROOT), 'and', os.path.relpath(OUT_PDF, ROOT), '(%d pages)' % n)
