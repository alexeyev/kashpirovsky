# coding: utf-8

import os
from xml.etree import ElementTree

from xml.sax import make_parser, handler

def get_data(fil):
    class IntervalsCollector(handler.ContentHandler):
        #global intervals
        def __init__(self, arr):
            self.arr = arr
            self.in_sentence = False
        def startElement(self, name, attrs):
            if name == "sentence":
                self.in_sentence = True
        def endElement(self, name):
            if name == "sentence":
                self.in_sentence = False
        def characters(self, chars):
            if self.in_sentence:
                #print "[", chars.strip(), "]"
                self.arr += [chars.strip()]
    data = []
    parser = make_parser()
    parser.setContentHandler(IntervalsCollector(data))
    parser.parse(fil)
    return data

dir = '.'

pd = []
ad =[]

for dirname in os.listdir(dir):
    subdir = os.path.join(dir, dirname)
    if os.path.isdir(subdir):
        parsed = os.path.join(subdir, "parsed")
        annotated = os.path.join(subdir, "xml_annotated")
        for f in sorted(os.listdir(parsed)):
            pd += get_data(os.path.join(parsed, f))
            ad += get_data(os.path.join(annotated, f))

with open("all_parsed.xml", "w+") as wr:
    wr.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<sentences>\n")
    for text in pd:
        wr.write("<sentence>" + (text).encode("utf-8") + "</sentence>\n")
    wr.write("</sentences>")

with open("all_annotated.xml", "w+") as wr:
    wr.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<sentences>\n")
    for text in ad:
        wr.write("<sentence>" + (text).encode("utf-8") + "</sentence>\n")
    wr.write("</sentences>")

