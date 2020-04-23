#!/usr/bin/env python3


import sys

from multiset import Multiset


voc = filter(len, map(lambda line: line.lower().strip(), open(sys.argv[1])))

word = sys.argv[2].lower()
word_letters = Multiset(word)
for word_check in voc:
    if word_check != word and not Multiset(word_check) - word_letters:
        print(word_check)
