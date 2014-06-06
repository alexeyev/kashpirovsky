__author__ = 'sunlight'


import re
import difflib

fin = open('converted.txt', 'r', encoding = "utf-8")
out = open('marking.txt', 'w', encoding = "utf-8")

def compare(e, word):
    s = difflib.SequenceMatcher(None, e, word)
    if e == word:
        return True
    elif len(word) > 3 and s.ratio() >= 0.5:
        return True
    else:
        return False

def isentity(entity, word):
    t = False
    for e in entity:
        if compare(e, word):
            t = True
    return t

previous = ""

while 1:
    org = fin.readline().replace('"','').lower().split()
    if not org:
        break
    per = fin.readline().replace('"','').lower().split()
    text = fin.readline().replace('"','').split()
    b = fin.readline()

    for word in text:
        word = re.sub("[,.!:()]", '', word)
        word.replace('"','')
        if word in ['-'] or len(word) < 1:
            continue
        out.write(word)
        if isentity(per, word.lower()):
            cla = "PER"
        elif isentity(org, word.lower()):
            cla = "ORG"
        else:
            cla = "O"

        out.write('\t')
        if cla != "O":
            if cla == previous:
                out.write("I-")
            else:
                out.write("B-")
        out.write(cla + '\n')
        previous = cla