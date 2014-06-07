# -*- coding: utf-8 -*-
import re

__author__ = 'achugr'

data_line_pattern = re.compile("^(?!#)(.*)\s(.*)")


class DataSetBalancer:
    not_O_classes = {'B-ORG', 'B-PER', 'I-ORG', 'I-PER'}

    def balance(self, file_name, balanced_file_name):
        f = open(file_name, "r")
        f_balanced = open(balanced_file_name, "w")

        prev_entity = 0
        lines = f.readlines()
        data = list()

        for line in lines:
            m = data_line_pattern.match(line.strip())
            if m is not None:
                word = m.group(1).replace(" ", "*")
                clazz = m.group(2).replace(" ", "*")
                data.append({'word': word, 'class': clazz})

        for i in range(3, len(data) - 3):
            needed = False
            for j in range(i - 3, i):
                if data[j]['class'] is not 'O':
                    needed = True
            for j in range(i, i + 3):
                if data[j]['class'] is not 'O':
                    needed = True

            if needed:
                f_balanced.write(data[i]['word'] + " " + data[i]['class'] + "\n")

        f_balanced.flush()
        f_balanced.close()


balancer = DataSetBalancer()
balancer.balance("data/ru_corpus.train.txt", "data/ru_corpus_balanced_2.train.txt")