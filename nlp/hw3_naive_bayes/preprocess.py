
from math import log
import os
import re
from nltk.stem.snowball import RussianStemmer
from pymorphy.contrib import tokenizers

def to_seq(input):
    words = list()
    for word in tokenizers.extract_words(input):
        words.append(word)
    stemmed = [RussianStemmer().stem(word) for word in words]
    return " ".join(stemmed)

def file_to_seq(fr, to):
    for f in os.listdir(fr):
        wrf = open(to + "/" + f, "w+")
        wrf.write(to_seq(open(fr + "/" + f, "r+").read().decode("utf-8")).encode("utf-8"))
        wrf.close()

file_to_seq("learn/internet", "learn_preprocessed/internet")
file_to_seq("learn/nointernet", "learn_preprocessed/nointernet")
file_to_seq("test/internet",  "test_preprocessed/internet")
file_to_seq("test/nointernet",  "test_preprocessed/nointernet")

