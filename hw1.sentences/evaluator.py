# -*- coding: utf-8 -*-

"""
Оценка качества разделения на предложения.

На вход подаётся золотой стандарт и разметка парсера.

Строим множество интервалов позиций, между которыми заключены предложения,
и смотрим на соответствующие "метрики".

Не очень-то показательные метрики:
P -- отношение совпавших интервалов к числу всех выделенных парсером
R -- отношение числа совпавших интервалов к числу предложений в "золотом стандарте"
F1 = 2PR / (P + R)
Accuracy -- |число совпавших (ибо tn = 0)| / |объединение всех рассматриваемых интервалов|

"""

import sys

try:
    print "true:", sys.argv[1]
    print "parsed:", sys.argv[2]
except:
    print "\nShould have 2 arguments, quitting."
    quit()

# ----------------BUILDING-INTERVALS----------------------------

from xml.sax import make_parser, handler

# yes, global variables

def get_intervals(xml):
	class IntervalsCollector(handler.ContentHandler):
            #global intervals
	    def __init__(self, intervals):
		self._elems = 0
		self._elem_types = {}

		self.in_sentence = False

		self.start = 1
		self.end = 0
                self.intervals = intervals

	    def startElement(self, name, attrs):
		if name == "sentence":
		    self.in_sentence = True

	    def endElement(self, name):
		if name == "sentence":
		    self.in_sentence = False

	    def characters(self, chars):
		if self.in_sentence:
		    print "[", chars.strip(), "]"
		    self.start = self.end + 1
		    self.end = self.start + len(chars.strip()) - 1
		    self.intervals += [(self.start, self.end)]
		    
        intervals = []
	parser = make_parser()
	parser.setContentHandler(IntervalsCollector(intervals))
	parser.parse(xml)
        return intervals

print get_intervals(sys.argv[1])

