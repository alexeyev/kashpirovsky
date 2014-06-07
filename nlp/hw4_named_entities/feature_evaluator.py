# -*- coding: utf-8 -*-
from itertools import izip
import os
import re
import string
import subprocess
import nltk
from nltk.corpus import stopwords
from sklearn.metrics import classification_report
# from classification import precision_recall
from subprocess import call


__author__ = 'achugr'

data_line_pattern = re.compile("^(?!#)(.*)\s(.*)")
org_types = {'ОАО', 'ООО', 'llc', 'ИП', 'ЗАО', 'НКО', 'ТСЖ', 'ОП'}


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


class NameChecker:
    female_names_file = "data/female-names-v1-14376.txt"
    male_names_file = "data/male-names-v1-14999.txt"
    surnames_file = "data/surnames-184624.txt"

    names = set()
    surnames = set()

    def __init__(self):
        for line in open(self.female_names_file, "r"):
            self.names.add(line.strip())
        for line in open(self.male_names_file, "r"):
            self.names.add(line.strip())
        for line in open(self.surnames_file, "r"):
            self.surnames.add(line.strip())

    def is_name(self, word):
        return word in self.names

    def is_surname(self, word):
        return word in self.surnames


class Window:
    window = list()

    def __init__(self, window_size, window_center):
        self.window_size = window_size
        self.window_center = window_center

    def append(self, word):
        if len(self.window) < self.window_size:
            self.window.append(word)
        else:
            self.window.pop(0)
            self.window.append(word)

    def center(self):
        return self.window[self.window_center]

    def __iter__(self):
        first_pos = self.window_center - self.window_size + 1
        return izip(range(first_pos, first_pos + self.window_size), self.window.__iter__())

    def __len__(self):
        return len(self.window)

    def is_full(self):
        return len(self.window) == self.window_size


class FeatureEvaluator:
    name_checker = NameChecker()

    def check_latin_word(self, word):
        for ch in word.lower():
            if ch in string.ascii_lowercase:
                return True
        return False

    def calc_features(self, window):
        features = dict()

        for pos, word in window:
            # print "pos is: ", pos
            features['big_letters_' + str(pos)] = sum(x.isupper() for x in word.decode('utf-8'))
            features['is_org_type_' + str(pos)] = word in org_types
            features['is_latin_' + str(pos)] = self.check_latin_word(word)
            is_name = self.name_checker.is_name(word)
            if is_name:
                print "is name! ", word
            features['is_name_' + str(pos)] = is_name
            features['is_surname_' + str(pos)] = self.name_checker.is_surname(word)

        return features


    def eval(self, input_file_name, output_file_name):
        fr = open(input_file_name, "r")
        fw = open(output_file_name, "w")
        window = Window(3, 1)
        features_names = list()

        for line in fr:
            m = data_line_pattern.match(line.strip())
            if m is not None:
                word = m.group(1)
                clazz = m.group(2)
                window.append(word)
                if word not in stopwords.words('russian'):
                    print "word: ", m.group(1), " class: ", clazz

                    if window.is_full():
                        features = self.calc_features(window)
                        if len(features_names) is 0:
                            features_names = features.keys()
                            fw.write("word ")
                            for name in features_names:
                                fw.write(name + " ")
                            fw.write("class\n")

                        fw.write(word + " ")
                        for name in features_names:
                            fw.write(str(features[name]) + " ")
                        fw.write(clazz)
                        fw.write("\n")

    def calc_metrics(self):
        true_test = list()
        classes = {'B-ORG', 'B-PER', 'I-ORG', 'I-PER', 'O'}
        for line in open("data/ru_corpus.test.txt", "r"):
            m = data_line_pattern.match(line.strip())
            if m is not None:
                if m.group(1) not in stopwords.words('russian'):
                    true_test.append(m.group(2))
                    print m.group(2)
        test = list()
        print "test corpus size: ", len(true_test)
        for line in open("data/test.txt"):
            clazz = line.strip()
            if clazz in classes:
                test.append(clazz)

        print "true test len: ", len(true_test)
        print "test len: ", len(test)

        print classification_report(true_test, test)
        # nb_precisions, nb_recalls = precision_recall(true_test, test)
        # print nltk.metrics.scores.precision(true_test, test)

    def train(self, file_name):
        # os.chdir("/Users/achugr/csc/nlp_2014/kashpirovsky/nlp/hw4_named_entities/data")
        print os.listdir(".")
        call(["java", "-cp",
              "/Users/achugr/csc/nlp_2014/mallet-2.0.7/class:/Users/achugr/csc/nlp_2014/mallet-2.0.7/lib/mallet-deps.jar",
              "cc.mallet.fst.SimpleTagger", "--train", "true", "--model-file", "data/classifier",
              file_name])

    def test(self, file_name):

        # os.chdir("/Users/achugr/csc/nlp_2014/kashpirovsky/nlp/hw4_named_entities/data")
        f = open("test.txt", "w")
        call(["java", "-cp",
              "/Users/achugr/csc/nlp_2014/mallet-2.0.7/class:/Users/achugr/csc/nlp_2014/mallet-2.0.7/lib/mallet-deps.jar",
              "cc.mallet.fst.SimpleTagger", "--model-file", "data/classifier", file_name], stdout=f)


eval = FeatureEvaluator()
# eval.eval("data/ru_corpus_balanced_2.train.txt", "data/ru_corpus_balanced_2.train.evaluated.txt")
# eval.eval("data/ru_corpus.test.txt", "data/ru_corpus.test.evaluated.txt")
# eval.train("data/ru_corpus.train.evaluated.txt")
# eval.test("data/ru_corpus.test.evaluated.txt")
eval.calc_metrics()
# eval.eval("data/ru_corpus.train.txt", "data/ru_corpus.train.evaluated.txt")
# eval.calc_metrics()
