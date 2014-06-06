# -*- coding: utf-8 -*-
from pymorphy.contrib import tokenizers

__author__ = 'achugr'

from math import log
import os
import re
from nltk.stem.snowball import RussianStemmer
from xml.dom import minidom
import xml.etree.ElementTree as ET


class NaiveBayes:
    classes = set()
    docs_in_class = dict()   # количество документов в классе
    docs_number = 0          # число документов
    unique_words_set = set() # множество уникальных слов
    words_in_class = dict()  # количество слов в классе
    words_freq = dict()      # частота появления слова в классе

    def learn(self, class_name):
        dir_name = "."
        file_name = "tweets_by_trend.xml"

        self.classes.add(class_name)
        self.words_freq[class_name] = {}

        if class_name is "negative":
            code = 0
        else:
            code = 1

        print "processing", file_name

        tree = ET.parse(dir_name + "/" + file_name)
        root = tree.getroot()
        for tweet in root.findall('tweet'):
            sent = int(tweet.find('sent').text)
            if sent == code:
                text = tweet.find('text').text
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

    self.test_dir("test/positive", metrics)
    self.test_dir("test/negative", metrics)

    print metrics

    prec = (float(metrics['tp']) / (metrics['tp'] + metrics['fp'] + 0.001))
    rec = (float(metrics['tp']) / (metrics['tp'] + metrics['fn'] + 0.001))
    f = 2 * (prec * rec) / (prec + rec + 0.001)
    print "prec: ", prec
    print "rec: ", rec
    print "f: ", f


def test_dir(self, dir_name, metrics):
    _class = "positive" if dir_name == "test/positive" else "negative"
    print _class
    for file_name in os.listdir(dir_name):
        print 'testing', file_name
        text = open(dir_name + "/" + file_name, "r").read().decode("utf-8")
        result = self.classify(text)
        if result["positive"] > result["negative"] and _class is "positive":
            metrics['tp'] += 1
        elif result["positive"] < result["negative"] and _class is "negative":
            metrics['tn'] += 1
        elif result["positive"] < result["negative"] and _class is "positive":
            metrics['fn'] += 1
        else:
            metrics['fp'] += 1


naive = NaiveBayes()
naive.learn("positive")
naive.learn("negative")

naive.test()
