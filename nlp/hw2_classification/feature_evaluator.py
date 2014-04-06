# -*- coding: utf-8 -*-

import string
from nlp.hw1_sentences import parser

__author__ = 'achugr'

import os
from os import listdir
from os.path import isfile, join
import re
import pymorphy
from pymorphy.contrib import tokenizers


def check_latin_word(word):
    for ch in word.lower():
        if ch in string.ascii_lowercase:
            return True
    return False


class FeatureEvaluator:
    file_name_pattern = re.compile('(\d*)_(.*)\.txt')
    digit_patter = re.compile('\d')
    quotes_pattern = re.compile('\".*\"')

    files_features = {}


    def eval_features(self, number, clazz, text):
        print text

        features = {}
        words_count = 0
        average_length = 0
        latin_words = 0
        for word in tokenizers.extract_words(text):
            words_count += 1
            average_length += len(word)
            if check_latin_word(word):
                latin_words += 1

        sentences = parser.analyze_paragraph(text)

        features['sentences_count'] = len(sentences)
        average_sentence_len = 0
        for sentence in sentences:
            average_sentence_len += len(sentence)

        features['average_sentence_length'] = average_sentence_len / len(sentences)

        excl_marks = "!" in text

        features['words_count'] = words_count
        features['average_length'] = average_length / words_count
        features['class'] = clazz
        features['latin_words'] = latin_words
        features['excl_marks'] = excl_marks
        features['quotes_count'] = len(self.quotes_pattern.findall(text))
        features['digits_count'] = len(self.digit_patter.findall(text))

        self.files_features[number] = features

    def process_dir(self, dir_name):
        for file_name in os.listdir(dir_name):
            m = self.file_name_pattern.match(file_name)
            if m is not None:
                f = open(file_name, "r")
                text = f.read().decode("utf-8")
                self.eval_features(m.group(1), m.group(2), text)

        self.save()

    def save(self):
        features_file = open("features.csv", "w")
        keys = self.files_features[self.files_features.keys()[0]].keys()
        # features_file.write("file_number")
        for key in keys:
            features_file.write(key)
            features_file.write(",")

        features_file.write("\n")

        for file_number in self.files_features:
            # features_file.write(file_number)
            for key in keys:
                features_file.write(str(self.files_features[file_number][key]))
                features_file.write(", ")
            features_file.write("\n")
        features_file.flush()
        features_file.close()



eval = FeatureEvaluator()
eval.process_dir(".")

# print string.lowercase
