# -*- coding: utf-8 -*-
from nltk.stem.snowball import RussianStemmer
from pymorphy.contrib import tokenizers
import xml.etree.ElementTree as ET

__author__ = 'achugr'


def init_dict(file_name, word_set):
    f = open("tweets/" + file_name, "r")
    for line in f.readlines():
        word_set.add(RussianStemmer().stem(line.strip().decode("utf-8")))


class KeyWordsBasedClassifier:
    positive_keywords = set()
    negative_keywords = set()

    def __init__(self):
        init_dict("positive_keywords_filtered.txt", self.positive_keywords)
        init_dict("negative_keywords_filtered.txt", self.negative_keywords)

    def classify(self, text, biggest_class):
        pos_count = 0
        neg_count = 0
        for word in tokenizers.extract_words(text):
            stemmed_word = RussianStemmer().stem(word)
            if stemmed_word in self.negative_keywords:
                print "negative word " + stemmed_word + " found in text: " + text
                neg_count += 1
            elif stemmed_word in self.positive_keywords:
                print "positive word " + stemmed_word + " found in text: " + text
                pos_count += 1

        result = dict()
        result['pos'] = pos_count
        result['neg'] = neg_count
        if result['pos'] == result['neg']:
            result[biggest_class] += 1
        return result

    def test(self):
        metrics = dict()
        metrics['tp'] = 0
        metrics['fp'] = 0
        metrics['tn'] = 0
        metrics['fn'] = 0

        self.test_file("markup-ready.xml", metrics)

        print metrics

        prec = (float(metrics['tp']) / (metrics['tp'] + metrics['fp'] + 0.001))
        rec = (float(metrics['tp']) / (metrics['tp'] + metrics['fn'] + 0.001))
        f = 2 * (prec * rec) / (prec + rec + 0.001)
        print "prec: ", prec
        print "rec: ", rec
        print "f: ", f

    def test_file(self, file_name, metrics):
        tree = ET.parse("tweets/" + file_name)
        root = tree.getroot()
        positive_count = 0
        negative_count = 0
        for tweet in root.findall('tweet'):
            if int(tweet.find('sent').text) == 0:
                negative_count += 1
            else:
                positive_count += 1

        print "pos count: " + str(positive_count) + " neg count " + str(negative_count)

        biggest_class = "neg" if negative_count > positive_count else "pos"

        for tweet in root.findall('tweet'):
            text = tweet.find('text').text
            sent = "neg" if int(tweet.find('sent').text) == 0 else "pos"
            result = self.classify(text, biggest_class)
            print "result " + str(result)
            if result["neg"] > result["pos"] and sent is "neg":
                metrics['tp'] += 1
            elif result["neg"] < result["pos"] and sent is "pos":
                metrics['tn'] += 1
            elif result["neg"] < result["pos"] and sent is "neg":
                metrics['fn'] += 1
            elif result["neg"] > result["pos"] and sent is "pos":
                metrics['fp'] += 1


classifier = KeyWordsBasedClassifier()
classifier.test()