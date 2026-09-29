# Tools

These scripts build everything in `docs/` from the sources, and made the word list. The builds are reproducible. Given the same inputs, the apps come out the same byte for byte, and the figures and PDF differ only in details such as the PDF's creation date.

```sh
pip install -r tools/requirements.txt && python -m playwright install chromium    # once
python3 tools/rebuild.py              # the apps, figures, web page and PDF (about 30 seconds)
python3 tools/rebuild.py --test       # then every test
python3 tools/rebuild.py --docs-only  # only the figures, web page and PDF
python3 tools/rebuild.py --apps-only  # only the three apps
```

## What is built from what

| Script | Reads | Writes |
|---|---|---|
| `keyboard.py` | `sources/keyboard-keys.html`, `sources/keyboard-3x3.html`, `../data/stemsyl-words.tsv` | `docs/stemsyl-keyboard.html` |
| `watch.py` | `docs/stemsyl-keyboard.html` | `docs/stemsyl-keyboard-watch.html` |
| `trainer.py` | `sources/trainer.html` | `docs/stemsyl-trainer.html` |
| `figures.py` | the two keyboards in `docs/` | `docs/figures/` |
| `spec.py` | `../SPECIFICATION.md`, `docs/figures/` | `docs/stemsyl.html`, `docs/stemsyl-specification.pdf` |
| `rebuild.py` | runs all of the above, in that order | |

Helpers:

- `embed_words.py` puts the word list into a keyboard file.
- `kbdata.py` reads and writes the word list, and reads it back out of a built keyboard.
- `fullconv.py` converts pronunciations between the two keyboards' conventions for the NORTH vowel.

### The sources

`sources/` holds the three hand-written apps the build starts from:

- `keyboard-keys.html`: the key-grid keyboard
- `keyboard-3x3.html`: the 3 × 3 keyboard
- `trainer.html`: the trainer

Each is a complete app in one file of HTML, CSS and JavaScript.

### How the apps are made from them

The build scripts change the sources by **exact-text replacement**. Each change names a piece of the source and what replaces it, and the piece must be found exactly once. If a source changes so that a piece is missing or appears twice, the build stops and prints that piece, rather than quietly building something else.

**`keyboard.py`** takes the key-grid keyboard as its base. It embeds the word list (with `embed_words.py`), then brings in the 3 × 3 keyboard's styles, tables, key builder and touch handlers, and adds:

- the layout switch
- the English captions and the rule that chooses them
- the licence notices

**`watch.py`** takes the finished phone keyboard and turns it into the watch keyboard:

- the 208 × 248 layout, with the note strip, the word strip and the keys
- the hold-to-switch edge keys
- display mode and the edit bar
- the Latin letters
- the text boxes
- the option keys

**`trainer.py`** brings the trainer in line with the keyboards' colours, geometry and spelling conventions.

## Changing the apps

There are two ways to change an app:

1. **Change the build.** Edit a source in `sources/`, or add a replacement to `keyboard.py`, `watch.py` or `trainer.py`. Then run `python3 tools/rebuild.py --test`. A change made this way reaches every app built from that source: a change to the phone keyboard also reaches the watch keyboard. This is how the apps have been developed so far.
2. **Edit a built app directly.** Every file in `docs/` is a complete app, and you can edit it by hand. But the next full rebuild would overwrite your change. After editing by hand, run only `python3 tools/rebuild.py --docs-only`, which rebuilds the figures and the PDF from the apps as they are. From then on, treat the edited app as the source.

Whichever way you choose, run the tests (`python3 tests/run.py`) afterwards. If the change adds something new, describe it in `SPECIFICATION.md` and publish a new version, as `PUBLISHING.md` explains.

## The word list

`data/stemsyl-words.tsv` is an input to the build, not an output. The scripts in [`wordlist/`](wordlist/README.md) made it from the CMU Pronouncing Dictionary, the English Speller Database, FrequencyWords, eSpeak NG and the g2p model. They need those sources, about 400 MB, downloaded first.

To change a pronunciation or a flag by hand, edit the data file, then run `python3 tools/rebuild.py`. Keep the columns as `data/README.md` describes them; `kbdata.read_tsv` checks every row.
