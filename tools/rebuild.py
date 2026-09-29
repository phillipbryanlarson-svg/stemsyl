# Rebuilds everything that is made from the sources, in order, and stops at the first step that fails:
#   1. keyboard.py  docs/stemsyl-keyboard.html        from tools/sources/keyboard-keys.html, keyboard-3x3.html and data/stemsyl-words.tsv
#   2. watch.py     docs/stemsyl-keyboard-watch.html  from 1
#   3. trainer.py   docs/stemsyl-trainer.html         from tools/sources/trainer.html
#   4. figures.py   docs/figures/                     drawn by 1 and 2
#   5. spec.py      docs/stemsyl.html and docs/stemsyl-specification.pdf, from SPECIFICATION.md and 4
#   6. (with --test) tests/run.py
#
#   python3 tools/rebuild.py              steps 1 to 5
#   python3 tools/rebuild.py --test       steps 1 to 5, then all the tests
#   python3 tools/rebuild.py --docs-only  steps 4 and 5 only: after editing the apps in docs/ by hand, or SPECIFICATION.md
#   python3 tools/rebuild.py --apps-only  steps 1 to 3 only
#
# The word list, data/stemsyl-words.tsv, is an input here; tools/wordlist makes it from its sources (see its README).
import os, subprocess, sys, time
TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
APPS = ['keyboard.py', 'watch.py', 'trainer.py']
DOCS = ['figures.py', 'spec.py']
args = set(sys.argv[1:])
unknown = args - {'--test', '--docs-only', '--apps-only'}
if unknown or {'--docs-only', '--apps-only'} <= args:
    print(__doc__ or open(__file__).read().split('\nimport')[0]); sys.exit(2)
steps = (DOCS if '--docs-only' in args else APPS if '--apps-only' in args else APPS + DOCS)
t00 = time.time()
for s in steps:
    t0 = time.time(); print('==> %s' % s, flush=True)
    r = subprocess.run([sys.executable, os.path.join(TOOLS, s)], cwd=ROOT)
    if r.returncode:
        print('\n%s failed (exit %d); nothing after it was rebuilt.' % (s, r.returncode)); sys.exit(r.returncode)
    print('    done in %.0f s' % (time.time() - t0), flush=True)
if '--test' in args:
    print('==> tests', flush=True)
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tests', 'run.py')], cwd=ROOT)
    if r.returncode: sys.exit(r.returncode)
print('rebuilt in %.0f s' % (time.time() - t00))
