# The Stemsyl word list

`stemsyl-words.tsv` is a pronouncing list of 271,173 English words, most common first. Each word is written in Stemsyl sound letters and in IPA, in General American English. The Stemsyl keyboards carry exactly this list: they use it to suggest words, to show the English under each written word, and to turn typed or pasted English into Stemsyl.

It is licensed under [CC BY-SA 4.0](../LICENSES/CC-BY-SA-4.0.txt). Its sources and their notices are in [NOTICE.md](../NOTICE.md), and section 6 of the [specification](../SPECIFICATION.md#6-the-word-list) says how it was made.

## Format

The file is UTF-8 text with tabs between columns. The first line names the columns, and each line after it is one word:

```
rank	word	sounds	ipa	source	dictionary	offensive
1	you	yU	ju	cmu	1	0
3	the	D@ DI	ðə ði	cmu	1	0
4	to	tU ti t@	tu tɪ tə	cmu	1	0
```

| Column | Content |
|---|---|
| `rank` | 1 for the commonest word. Rows are in rank order. |
| `word` | The spelling, in lowercase. It is letters only, or letters with an apostrophe inside, as in *don't*. No spelling appears twice. |
| `sounds` | One to three pronunciations, separated by spaces, the usual one first. They use the sound letters below. |
| `ipa` | The same pronunciations in IPA, in the same order. |
| `source` | Where the first pronunciation came from:<br>`cmu`: the CMU Pronouncing Dictionary<br>`suffix`, `prefix`, `compound`: built by rule from CMU words<br>`g2p`: predicted by eSpeak NG, with a second reading from the g2p model where the two differ by one sound |
| `dictionary` | 1 if the word is on the English Speller Database's American list at size 60, the everyday dictionary words. |
| `offensive` | 1 if the keyboards keep the word out of their longer-word suggestions. |

## Sound letters

There is one character for each sound.

| Letter | Sound | Letter | Sound | Letter | Sound | Letter | Sound |
|---|---|---|---|---|---|---|---|
| `p` | /p/ *pie* | `b` | /b/ *buy* | `t` | /t/ *tie* | `d` | /d/ *die* |
| `k` | /k/ *kite* | `g` | /ɡ/ *guy* | `f` | /f/ *fee* | `v` | /v/ *vee* |
| `T` | /θ/ *thigh* | `D` | /ð/ *thy* | `s` | /s/ *sue* | `z` | /z/ *zoo* |
| `S` | /ʃ/ *shoe* | `Z` | /ʒ/ *vision* | `C` | /tʃ/ *chew* | `J` | /dʒ/ *jaw* |
| `h` | /h/ *high* | `m` | /m/ *my* | `n` | /n/ *nigh* | `N` | /ŋ/ *sing* |
| `l` | /l/ *lie* | `r` | /r/ *rye* | `w` | /w/ *why* | `y` | /j/ *yes* |
| `a` | /æ/ *cat* | `A` | /ɑ/ *father*, *hot* | `e` | /ɛ/ *bed* | `i` | /ɪ/ *sit* |
| `u` | /ʊ/ *book* | `@` | /ə/ *about*, *cup* | `I` | /i/ *see* | `U` | /u/ *too* |
| `E` | /eɪ/ *day* | `Y` | /aɪ/ *my* | `B` | /ɔɪ/ *boy* | `W` | /aʊ/ *now* |
| `G` | /oʊ/ *go* | `O` | /ɔ/ *law* | | | | |

Conventions:

- R-coloured vowels are a vowel plus `r`: *bird* is `b@rd`.
- NORTH and FORCE are `Gr`, as in *north* `nGrT`, but `Ar` after w, as in *war* `wAr`.
- Stress is not marked.

## Reading it

In Python, with the reader in `tools/kbdata.py`:

```python
from kbdata import read_tsv
for word, sounds, source, dictionary, offensive in read_tsv('data/stemsyl-words.tsv'):
    ...
```

Or with any CSV reader set to tabs. The file has no quoting.
