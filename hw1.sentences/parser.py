# -*- coding: utf-8 -*-

import re

def dot(position, par):
    return re.compile("^[\\.\\?!] $").match(par[position - 1 : position + 1])
    #return ". " == par[position - 1 : position + 1]

def double_num(position, par):
    return par[position - 1]

fpatterns = [dot]

IN = 0
OUT = 1

def analyze_paragraph(text):
    # in/out of quotes
    # print "working with:", text
    state = OUT
    splitting = []
    previous = 0
    for i in xrange(len(text)):
        if i == "\"":
            state = (state + 1) % 2
        if state == OUT:
            for pattern in fpatterns:
                if pattern(i, text):
                    splitting += [text[previous : i + 1]]
                    previous = i + 1
                break
    if previous == 0:
        splitting = [text]
    return splitting

if __name__ == "__main__":
    with open("example.raw.txt", "r+") as f:
        for line in f:
	    stripped = line.strip()
	    for sentence in analyze_paragraph(stripped):
                print sentence
