# Notices

The Stemsyl writing system and its specification are dedicated to the public domain (CC0 1.0). The apps, tools and tests are licensed under GPL-3.0-or-later. The word list is licensed under CC BY-SA 4.0.

The word list, in `data/stemsyl-words.tsv` and inside both keyboards, is built from the works below. This file gives their credits and the notices their licences ask for. Changes were made to all of them: words were selected and merged, their pronunciations were converted to Stemsyl sound letters, derived and predicted, and the words were ranked and flagged. None of these works is included whole.

## The CMU Pronouncing Dictionary

Most pronunciations come from the CMU Pronouncing Dictionary ([github.com/cmusphinx/cmudict](https://github.com/cmusphinx/cmudict), commit 7479086, October 2025), converted to Stemsyl sound letters.

```
Copyright (C) 1993-2015 Carnegie Mellon University. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
   The contents of this file are deemed to be source code.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.

This work was supported in part by funding from the Defense Advanced
Research Projects Agency, the Office of Naval Research and the National
Science Foundation of the United States of America, and by member
companies of the Carnegie Mellon Sphinx Speech Consortium. We acknowledge
the contributions of many volunteers to the expansion and improvement of
this dictionary.

THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## The English Speller Database (ESDB, previously SCOWL)

These parts come from the English Speller Database ([github.com/en-wl/wordlist](https://github.com/en-wl/wordlist), commit 1e5b7d3, June 2026):

- the words of its American lists at sizes 60, 70 and 80, which join the vocabulary and set the dictionary flag
- the superlatives in `tools/wordlist/superlatives.json`, taken from its part-of-speech data

No list larger than size 80 was used.

```
Copyright 2000-2026 by Kevin Atkinson

Permission to use, copy, modify, distribute, and sell any part of the English
Speller Database (ESDB, previously known as SCOWLv2), or word lists
created from it, is hereby granted without fee, provided that the above
copyright notice appears in all copies and that both the above copyright
notice and this notice appear in supporting documentation.  Kevin Atkinson
makes no representations about the suitability of this database for any
purpose.  It is provided "as is" without express or implied warranty.
```

The database's part-of-speech data was first assigned with the help of WordNet, so for `superlatives.json` its notice may also apply:

```
WordNet 1.6 Copyright 1997 by Princeton University.  All rights
reserved.

THIS SOFTWARE AND DATABASE IS PROVIDED "AS IS" AND PRINCETON
UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PRINCETON
UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT-
ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE
LICENSED SOFTWARE, DATABASE OR DOCUMENTATION WILL NOT INFRINGE ANY
THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

The name of Princeton University or Princeton may not be used in
advertising or publicity pertaining to distribution of the software
and/or database.  Title to copyright in this software, database and
any associated documentation shall at all times remain with
Princeton University and LICENSEE agrees to preserve same.
```

## FrequencyWords

The word order comes from Hermit Dave's FrequencyWords English list ([github.com/hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords), commit 525f9b5, content from OpenSubtitles 2018). Its content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). That is why the word list is shared under the same licence. The word list keeps only the order, not the counts.

## eSpeak NG

The pronunciations of 50,924 rarer words and names were predicted with eSpeak NG ([github.com/espeak-ng/espeak-ng](https://github.com/espeak-ng/espeak-ng), commit ba90c8e, September 2026). The trainer's spoken sounds were also made with eSpeak NG. eSpeak NG is free software under the GNU General Public License, version 3 or later. Its program is not included here. `tools/wordlist/espk.c` is a small program of our own that calls its library.

## g2p (Kyubyong Park and Jongseok Kim)

A second reading for some predicted words comes from Kyubyong Park and Jongseok Kim's grapheme-to-phoneme model, g2p ([github.com/Kyubyong/g2p](https://github.com/Kyubyong/g2p), commit c6439c2), licensed under the Apache License 2.0.

`tools/wordlist/g2pmodel.py` is our own reimplementation of the model's inference. It reads their published model file, which is not included here.

## LDNOOBW

Offensive words are kept out of the longer-word suggestions, partly by means of the "List of Dirty, Naughty, Obscene, and Otherwise Bad Words" ([github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words), commit 5faf2ba). It is © 2012–2020 Shutterstock, Inc., licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Only the word list's flags derive from it.

## The numerals

Stemsyl's numerals are borrowed. They are the dice-like digits on a 3 × 3 grid of an "Intuitive Clock" design that the author saw shared on Reddit. Who first designed them is not known, and they are not the author's work, so the public-domain dedication of the writing system does not cover them. If you know who designed them, please say so, so that they can be credited here.

## Trademarks

Apple Watch and watchOS are trademarks of Apple Inc. This project is not affiliated with or endorsed by Apple.
