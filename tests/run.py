# Runs every test in this folder, one after another, and says which passed. Exits with 1 if any failed.
#   python3 tests/run.py            all of them (about four minutes)
#   python3 tests/run.py watch      only those whose file name contains "watch"
import glob, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ['test_data.py', 'test_script.py', 'test_phone.py', 'test_watch.py', 'test_parity.py', 'test_trainer.py']
tests = [t for t in ORDER if os.path.exists(os.path.join(HERE, t))]
tests += sorted(os.path.basename(t) for t in glob.glob(os.path.join(HERE, 'test_*.py')) if os.path.basename(t) not in ORDER)
if len(sys.argv) > 1: tests = [t for t in tests if any(a in t for a in sys.argv[1:])]
results = []
for t in tests:
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.join(HERE, t)], cwd=HERE)
    results.append((t, r.returncode == 0, time.time() - t0))
print()
for t, ok, s in results: print('%-18s %s  (%.0f s)' % (t, 'passed' if ok else 'FAILED', s))
failed = [t for t, ok, s in results if not ok]
print('all %d passed' % len(results) if not failed else '%d of %d failed' % (len(failed), len(results)))
sys.exit(1 if failed else 0)
