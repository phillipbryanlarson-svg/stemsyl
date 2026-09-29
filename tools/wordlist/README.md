# Making the word list

These scripts made `data/stemsyl-words.tsv` from public sources. You only need them to rebuild the list from scratch, for example with a newer CMU dictionary. The apps are built from the finished list (see `../README.md`).

Run everything from this folder (`tools/wordlist`). The scripts expect their sources in `src/` here, and they write their caches here too. Both are left out of the repository by `.gitignore`.

## 1. Get the sources

These are the versions the published list was made from:

```sh
mkdir -p src && cd src
git clone https://github.com/cmusphinx/cmudict.git              # commit 7479086
git clone https://github.com/en-wl/wordlist.git scowl           # commit 1e5b7d3
git clone https://github.com/hermitdave/FrequencyWords.git fw   # commit 525f9b5
git clone https://github.com/espeak-ng/espeak-ng.git            # commit ba90c8e
git clone https://github.com/Kyubyong/g2p.git kyu               # commit c6439c2
git clone https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words.git ldnoobw   # commit 5faf2ba
cd ..
```

To match the published list exactly, check out the commits named above. Newer versions will give a slightly different list.

The g2p model file, `src/kyu/g2p_en/checkpoint20.npz`, comes with its repository.

## 2. Build the tools they need

**The speller lists.** These are American spelling, variant level 1, with accents removed:

```sh
cd src/scowl && make && for n in 60 70 80; do ./scowl word-list $n A 1 --deaccent > wl$n.txt; done; cd ../..
```

**eSpeak NG, and a small program that asks it for phonemes.** The eSpeak NG build is a static, release build with no audio:

```sh
cmake -S src/espeak-ng -B src/espeak-ng/build -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF \
      -DUSE_ASYNC=OFF -DUSE_LIBPCAUDIO=OFF -DUSE_LIBSONIC=OFF -DUSE_MBROLA=OFF
cmake --build src/espeak-ng/build -j
B=src/espeak-ng/build/src
gcc -O2 espk.c -I src/espeak-ng/src/include $B/libespeak-ng/libespeak-ng.a $B/ucd-tools/libucd.a \
    $B/speechPlayer/libspeechPlayer.a -lstdc++ -lm -o espk
echo hello | ./espk src/espeak-ng/build          # prints h_ə_l_ˈoʊ
```

**Python.** You need Python 3.9 or later and `numpy`.

## 3. Run the steps

```sh
python3 stage1.py     # the vocabulary; eSpeak NG and g2p readings for every word the CMU dictionary lacks -> stage1.json (about a minute)
python3 stage2.py     # the final pronunciations and their sources -> stage2.json
python3 make_tsv.py   # order, flags, the keys file's conventions -> ../../data/stemsyl-words.tsv
```

`make_tsv.py` overwrites `data/stemsyl-words.tsv`, so hand edits made there are lost. Then rebuild the apps with `python3 ../rebuild.py`.

## What each file does

| File | Purpose |
|---|---|
| `conv.py` | Converts the CMU dictionary's ARPABET to Stemsyl sound letters, and reads a keyboard's own 30,000-word list. |
| `common.py` | Where the sources and the keyboards' own lists are; the vocabulary's word shape; the frequency ranks; the speller lists. |
| `derive.py` | Builds pronunciations for words the CMU dictionary lacks from words it has: regular endings, stress-neutral suffixes, transparent prefixes and compounds. |
| `superlatives.json` | The adjective and adverb superlatives in the English Speller Database, without look-alikes such as *honest* and *priest*. `derive.py` only takes *-est* off these. |
| `ipa2ss.py` | Converts eSpeak NG's IPA to Stemsyl sound letters. |
| `g2pmodel.py` | Batched inference for Kyubyong Park and Jongseok Kim's g2p model, in numpy only. |
| `espk.c` | Reads words, one per line, and prints eSpeak NG's IPA for each. |
| `stage1.py`, `stage2.py`, `make_tsv.py` | The three steps above. |

**Checks, not needed to make the list:**

- `validate_derive.py` rebuilds hidden CMU words with `derive.py`'s rules, to measure them.
- `build_cmu_cache.py` and `eval_g2p.py` measure eSpeak NG and the g2p model against the CMU dictionary.
- `espcorr.py` tried learning corrections to eSpeak NG's output. It was measured, and not used.
- `eval_subs.py` and `eval_target.py` compare the methods on the words the list needed.

## The conventions

The CMU dictionary is converted sound for sound (`conv.py`), with these conventions:

- The keys file writes NORTH and FORCE as *oh* + r (`Gr`), and as *ah* + r (`Ar`) after w.
- Unstressed *for-* in *forget*, *forgive* and similar words is written *uh* + r.

Section 2.3 of the specification lists all the conventions.
