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

class IntervalsCollector(handler.ContentHandler):
    """ Не является thread-safe! """
    
    def __init__(self):
        self._elems = 0
        self._elem_types = {}
        self.intervals = {}

    def startElement(self, name, attrs):
        self._elems = self._elems + 1
        self._elem_types[name] = self._elem_types.get(name, 0) + 1

    def endDocument(self):
        pass

    def getIntervals(self, xml):
        self.parse(xml)

            
parser = make_parser()
parser.setContentHandler(IntervalsCollector())
parser.parse(sys.argv[1])

