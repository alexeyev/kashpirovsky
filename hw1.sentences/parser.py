# -*- coding: utf-8 -*-

import re

# todo: move patterns to global variables

def basic(position, par):
    return re.compile("^[\.\?!] $").match(par[position - 1 : position + 1])

def prev_capital(position, par):
    return re.compile("[A-ZА-Я]").match(par[position - 2: position - 1])

def next_capt(position, par):
    return basic(position, par) and re.compile(" [A-ZА-Я0-9]").match(par[position : position + 2]) and not prev_capital(position, par)

def check_shortenings(pos, par):
    return next_capt(pos, par) and not re.compile(u" [a-zа-я]{1,2}\. $").match(par[pos - 5 : pos + 1])

def num(pos, par):
    return re.compile("[0-9][\\.\\?!]+ $").match(par[pos - 5 : pos + 1])


fpatterns = [check_shortenings] #, num]

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
                print "<sentence>" + sentence + "</sentence>"
