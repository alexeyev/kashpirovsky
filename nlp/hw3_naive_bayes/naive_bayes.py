# -*- coding: utf-8 -*-
from pymorphy.contrib import tokenizers

__author__ = 'achugr'

from math import log
import os
import re
from nltk.stem.snowball import RussianStemmer

learn_internet = "learn_internet"
learn_nointernet = "learn_nointernet"

class NaiveBayes:
    classes = set()
    docs_in_class = dict()   # количество документов в классе
    docs_number = 0          # число документов
    unique_words_set = set() # множество уникальных слов
    words_in_class = dict()  # количество слов в классе
    words_freq = dict()      # частота появления слова в классе

    def learn(self, class_name):
        self.classes.add(class_name)
        self.words_freq[class_name] = {}
        if class_name is "internet":
            dir_name = learn_internet
        else:
            dir_name = learn_nointernet

        for file_name in os.listdir(dir_name):
            text = open(dir_name + "/" + file_name, "r").read().decode("utf-8")
            words = [word.lower() for word in tokenizers.extract_words(text)]
            self.docs_number += 1
            self.unique_words_set = self.unique_words_set | set(words)
            stemmer = RussianStemmer()
            for word in words:
                stemmed = stemmer.stem(word)
                if stemmed in self.words_freq[class_name]:
                    self.words_freq[class_name][stemmed] += 1
                else:
                    self.words_freq[class_name][stemmed] = 1

            if class_name in self.words_in_class:
                self.words_in_class[class_name] += len(words)
                self.docs_in_class[class_name] += 1
            else:
                self.words_in_class[class_name] = len(words)
                self.docs_in_class[class_name] = 1

    def classify(self, input):
        words = list()
        for word in tokenizers.extract_words(input):
            words.append(word)
        stemmed = [RussianStemmer().stem(word) for word in words]

        result = dict()
        for _class in self.classes:
            prob = log(float(self.docs_in_class[_class]) / self.docs_number)
            for word in stemmed:
                if word in self.words_freq[_class]:
                    wordFreq = self.words_freq[_class][word]
                else:
                    wordFreq = 0
                prob += log(float(wordFreq + 1) / float(len(self.unique_words_set) + self.words_in_class[_class]))
            result[_class] = prob
        return result

    def test(self):
        metrics = dict()
        metrics['tp'] = 0
        metrics['fp'] = 0
        metrics['tn'] = 0
        metrics['fn'] = 0

        self.test_dir("test_internet", metrics)
        self.test_dir("test_nointernet", metrics)

        print metrics

        prec = (float(metrics['tp']) / (metrics['tp'] + metrics['fp']))
        rec = (float(metrics['tp']) / (metrics['tp'] + metrics['fn']))
        f = 2 * (prec * rec) / (prec + rec)
        print "prec: ", prec
        print "rec: ", rec
        print "f: ", f


    def test_dir(self, dir_name, metrics):
        _class = "internet" if dir_name is "test_internet" else "nointernet"
        for file_name in os.listdir(dir_name):
            text = open(dir_name + "/" + file_name, "r").read().decode("utf-8")
            result = self.classify(text)
            if result["internet"] > result["nointernet"] and _class is "internet":
                metrics['tp'] += 1
            elif result["internet"] < result["nointernet"] and _class is "nointernet":
                metrics['tn'] += 1
            elif result["internet"] < result["nointernet"] and _class is "internet":
                metrics['fn'] += 1
            else:
                metrics['fp'] += 1


naive = NaiveBayes()
naive.learn("internet")
naive.learn("nointernet")

naive.test()
