# -*- coding: utf-8 -*-

import string
from nlp.hw1_sentences import parser
from pymongo import MongoClient

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
    abbreviation_pattern = re.compile(u'[А-Я]{1,6}')

    dictionaries = dict()

    classes_count = dict()

    files_features = {}


    def __init__(self):
        for file in os.listdir("dicts/"):
            self.dictionaries[file] = set()
            for line in open("dicts/" + file, "r"):
                self.dictionaries[file].add(line.decode("utf-8").strip())


    def count_dict_features(self, dict_name, words):
        count = 0
        for word in words:
            if word in self.dictionaries[dict_name]:
                count += 1
        return count

    def eval_features(self, number, clazz, text):
        features = {}
        words_count = 0
        average_length = 0
        latin_words = 0
        words = list()

        if clazz in self.classes_count:
            self.classes_count[clazz] += 1
        else:
            self.classes_count[clazz] = 0

        for word in tokenizers.extract_words(text):
            words.append(word)
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

        # dict features
        features['auto_dict'] = self.count_dict_features("auto.txt", words)
        features['economics_dict'] = self.count_dict_features("economics.txt", words)
        features['hi_tech_dict'] = self.count_dict_features("hi_tech.txt", words)
        features['internet_dict'] = self.count_dict_features("internet.txt", words)
        features['kultura_dict'] = self.count_dict_features("kultura.txt", words)
        features['politics_dict'] = self.count_dict_features("politics.txt", words)
        features['science_dict'] = self.count_dict_features("science.txt", words)
        features['social_dict'] =self.count_dict_features("social.txt", words)
        features['sport_dict'] = self.count_dict_features("sport.txt", words)

        abbrevations_count = 0
        for token in text.split():
            if self.abbreviation_pattern.match(token):
                abbrevations_count += 1
                # print token
                # else:
                #     print "not match: ", token

        # features['abbrevation_count'] = abbrevations_count
        # if abbrevations_count>30:
        #     print number, " ", abbrevations_count
        # print features
        self.files_features[number] = features

    def process_dir(self, dir_name, result_file):
        for file_name in os.listdir(dir_name):
            m = self.file_name_pattern.match(file_name)
            if m is not None:
                f = open(file_name, "r")
                text = f.read().decode("utf-8")
                self.eval_features(m.group(1), m.group(2), text)

        self.save(result_file)

    def save(self, result_file, files_features):
        features_file = open(result_file + ".csv", "w")
        keys = self.files_features[0].keys()
        # features_file.write("file_number")
        for key in keys:
            features_file.write(key)
            features_file.write(",")

        features_file.write("\n")
        print "i am here ", files_features
        for row in files_features:
            # features_file.write(str(file_number))
            counter = 0
            for key in keys:
                features_file.write(str(row[key]))
                if counter < len(keys) - 1:
                    features_file.write(",")
                counter += 1
            features_file.write("\n")
        features_file.flush()
        features_file.close()

    def split_learn_test(self):
        learn = list()
        test = list()
        counts = dict()
        print self.files_features
        for key in self.files_features:
            row = self.files_features[key]
            if row['class'] in counts:
                counts[row['class']] += 1
            else:
                counts[row['class']] = 0

            if counts[row['class']] < min([self.classes_count[c] for c in self.classes_count]):
                if counts[row['class']] % 3 == 0:
                    test.append(row)
                else:
                    learn.append(row)

        self.save("learn-lenta", learn)
        self.save("test-lenta", test)


    def print_stats(self):
        for clazz in self.classes_count:
            print clazz, " - ", self.classes_count[clazz]

    def process_mongo(self):
        client = MongoClient('localhost', 27017)
        db = client.news_db
        collection = db.news_collection
        topics = set()
        class_map = dict()
        # sport,auto,culture,internet,hi_tech,politics,economics,science,society
        class_map['sport'] = {"Футбол", "Теннис", "Баскетбол", "Хоккей", "Бокс", "Биатлон"}
        class_map['auto'] = {"Авто"}
        class_map['culture'] = {"Искусство", "Театр", "Музыка", "Книги", "Кино"}
        class_map['internet'] = {"Интернет", "Coцсети"}
        class_map['hi_tech'] = {"Техника", "Космос", "Софт", "Оружие"}
        class_map['politics'] = {"Политика"}
        class_map['economics'] = {"Госэкономика"}
        class_map['science'] = {"Наука"}
        class_map['society'] = {"Общество", "Конфликты"}
        class_map['events'] = {"События", "Происшествия"}

        number = 0
        for doc in collection.find():

            for clazz in class_map.keys():
                for topic_name in class_map[clazz]:
                    if doc['topic'] == topic_name.decode("utf-8"):
                        if len(doc['body']) > 0:
                            self.eval_features(number, clazz, doc['body'])
                            number += 1

        # self.save("learn-lenta")
        self.split_learn_test()


eval = FeatureEvaluator()
# eval.process_dir("test_set/", "test")
# eval.process_dir("learn_set/", "learn")
eval.process_mongo()
eval.print_stats()

# client = MongoClient('localhost', 27017)
# db = client.news_db
# collection = db.news_collection
#
# topics = set()
#
# for doc in collection.find():
#     topics.add(doc['topic'])
#
# for topic in topics:
#     print topic