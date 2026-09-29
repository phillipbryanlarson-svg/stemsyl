# Tests

The tests open the apps in `docs/` in a headless Chromium browser and use them as a person would: they tap, hold and swipe with touch events, at phone and watch sizes. Each test serves `docs/` from its own local web server, as a website would, so the apps can keep notes between visits. The tests also check that the specification, the word list and the apps agree.

```sh
pip install -r tools/requirements.txt && python -m playwright install chromium    # once
python3 tests/run.py            # every test, about three minutes
python3 tests/run.py watch      # only the tests whose file name contains "watch"
python3 tests/test_phone.py     # one test on its own
```

Each test prints `ok` or `FAIL` for every check, then a count. `run.py` exits with 1 if any test failed. Screenshots are saved in `tests/out/` for a person to look at; they are not checked in.

| Test | What it checks |
|---|---|
| `test_data.py` | The word list is well formed: one to three pronunciations per word, the IPA matching the sounds, no repeated spellings. It is also exactly the list inside both keyboards, with the same flags. |
| `test_script.py` | The apps' sound tables, colours in both themes, glyph measurements, numerals and punctuation are those in `SPECIFICATION.md`. The syllable rule groups the specification's worked examples as shown, and the caption rule behaves as written. |
| `test_phone.py` | The phone keyboard, on both layouts: typing by sound, the word strip, captions and homophones, the name mark, numbers, hold-to-delete and undo, the 3 × 3 centre hold and swipes, typing and pasting English, the English view, saved notes, the dark theme and a small screen. |
| `test_watch.py` | The watch keyboard at 208 × 248 and 187 × 223:<br>- every page of keys and every panel fits the screen with nothing cut off<br>- each held key brings up its page, and the 9 · 0 key never holds<br>- display mode and its edit bar<br>- holding delete to clear the note or a text box, with Undo<br>- the word strip above or below the keys<br>- Latin letters in the note, the title box and Write English<br>- the option keys |
| `test_parity.py` | The same 45 steps on the phone's 3 × 3 layout and on the watch give the same note, cursor, English and suggestions at every step. |
| `test_trainer.py` | The trainer draws the script exactly as the keyboards do, its practice words use the keyboards' sounds, and every kind of card shows and reveals. |

`helpers.py` holds what the tests share: the checks, the touch gestures, and opening an app with a given note and settings.
