# -*- coding: utf-8 -*- 

import pymongo
from nltk.stem.snowball import RussianStemmer
import re
import string
from math import log


class Classifier:
	def __init__(self,host,port,db,collection):
		self.connection = pymongo.Connection(host,port)
		self.db = self.connection[db]
		self.collection = self.db[collection]

	def fillDicts(self,maxDocs = 0):
		self.classes = set()
		self.documentsInClass = dict() #количество документов в классе
		self.documentsNumber = 0 # число документов
		self.uniqueWords = set() # множество уникальных слов
		self.wordsInClass = dict() # количество слов в классе
		self.wordsFreq = dict() # частота появления слова в классе
		i = 0
		for document in self.collection.find():
			i+=1
			if i>maxDocs and maxDocs > 0:
				break
			if i%100 == 0:
				print "Processed " + str(i) + " documents"
			self.classes.add(document['topic'])
			match = re.findall(re.compile(u"[а-яА-Яa-zA-Z0-9]*"),document['body'])
			match = [word for word in match if word!='']
			self.documentsNumber+=1
			self.uniqueWords = self.uniqueWords | set(match)
			wordsFreq = dict()
			stemmer = RussianStemmer()
			for _match in match:
				stemmed = stemmer.stem(_match)
				if stemmed in wordsFreq:
					wordsFreq[stemmed] += 1
				else:
					wordsFreq[stemmed] = 1	
			if document['topic'] in self.wordsInClass:
				self.wordsInClass[document['topic']] += len(match)
				self.wordsFreq[document['topic']].update(wordsFreq)
				self.documentsInClass[document['topic']] += 1
			else:
				self.wordsInClass[document['topic']] = len(match)			
				self.wordsFreq[document['topic']] = wordsFreq
				self.documentsInClass[document['topic']] = 1

		
			
	def classify(self,input):
		match = [word for word in re.findall(re.compile(u"[а-яА-Яa-zA-Z0-9]*"),input) if word!='']		
		stemmed = [RussianStemmer().stem(word) for word in match]
		result = dict()
		for _class in self.classes:
			prob = log(float(self.documentsInClass[_class]) / self.documentsNumber)
			for word in stemmed:
				if word in self.wordsFreq[_class]:
					wordFreq = self.wordsFreq[_class][word]
				else:
					wordFreq = 0

				prob += log( float(wordFreq+1) / float( len(self.uniqueWords) + self.wordsInClass[_class]))
			result[_class] = prob
		return result

		




