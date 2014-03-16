# -*- coding: utf-8 -*-

"""
Конвертер из старого формата (каждое предложение -- новая строчка) в новый.
Из директории -- в директорию.

Пример:
$python corpus_alexeyev/annotated/ corpus_alexeyev/xml_annotated/

"""

import sys, os

try:
    print "previously annotated files dir:", sys.argv[1]
    print "new annotated files dir:", sys.argv[2]
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
except:
    print "\nPlease provide correct arguments"
    quit()

def convert(fr, fw):
    fw.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
    fw.write("<sentences>\n")
    for line in fr:
        stripped = line.strip().decode("utf-8")
        if stripped != "":
            fw.write("<sentence>" + stripped.encode("utf-8") + "</sentence>\n")
    fw.write("</sentences>")
        
if __name__ == "__main__":
    for fi in os.listdir(sys.argv[1]):
        with open(sys.argv[2] + "/" + fi, "w+") as fw:
            convert(open(sys.argv[1] + fi, "r+"), fw)
    print "Done"
