# coding: utf8

import os
import nltk
from nltk.corpus import stopwords
import string

words = {}

def low(s):
    return s.decode("utf-8").lower().encode("utf-8")

for f in os.listdir("./learn_set"):
    if f.count("auto") == 1:
        with open(f, "r+") as inp:
            for line in inp:
                splitted = nltk.word_tokenize(line)
                for word in [s for s in splitted if not s in string.punctuation]:
                    if not low(word) in words:
                        words[low(word)] = 0
                    words[low(word)] += 1


for key in words:
    if len(list(key)) > 3 and not key in stopwords.words('russian') and not key in ['это', 'об', "на", "также"]:
        print key + "\t" + str(words[key])
