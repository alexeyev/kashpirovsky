# -*- coding: utf-8 -*-
#!/usr/bin/env python
 
import sys
import re
import os
import codecs
from os import listdir
 
files = []
entered_category = ""
entered_dir = ""
out_file = ""
if len(sys.argv) == 4:
	entered_dir = sys.argv[1]
	entered_category = sys.argv[2]
	out_file = sys.argv[3]
else:
	print "Usage: word_counter.py dir_name category_name output_filename"
	
words_to_ignore = ["что","как","на","по","где","об",
"в","вне","для","до","вместо","за","из","из-за","из-под",
"к","кроме","между","над","о","от","перед","под","при","про",
"ради","с","сквозь","среди","у","через","я","он","это","она",
"этот","они","мы","который","то","свой","что","весь","так","ты",
"все","тот","вы","такой","его","себя","как","сам","другой",
"наш","мой","кто","ее","где","там","какой","их","потом","каждый",
"оно","кто-то","как-то","зачем","туда","сюда","где-то","уже"]
things_to_strip = [".",",","?",")","(","\"",":",";","'s"]
words_min_size = 3

file_name_pattern = re.compile('(\d*)_' + entered_category + '.txt')
for file_name in os.listdir(entered_dir):
    m = file_name_pattern.match(file_name)
    if m is not None:
        files.append(file_name);
 
text = ""
for file in files:
	f = open(file,"rU")
	for line in f:
		text += line
 
words = text.lower().split()
wordcount = {}
for word in words:
	for thing in things_to_strip:
		if thing in word:
			word = word.replace(thing,"")
	if word not in words_to_ignore and len(word.decode('utf-8')) >= words_min_size:
		if word in wordcount:
			wordcount[word] += 1
		else:
			wordcount[word] = 1
		
sortedbyfrequency =  sorted(wordcount,key=wordcount.get,reverse=True)
 
words_file = f = codecs.open(out_file + ".txt", "w", "utf-8")
for word in sortedbyfrequency:
	uword = unicode(word, 'utf-8', errors='ignore')
	new_string = uword + " " + str(wordcount[word]) + "\n"
	words_file.write(new_string)

