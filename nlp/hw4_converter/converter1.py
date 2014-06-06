__author__ = 'sunlight'


import xml.etree.ElementTree as ET
import base64

facts = ET.parse("./and_good_table.xml").getroot()
news1 = ET.parse("./news-080404.xml").getroot()
news2 = ET.parse("./news-vybory.xml").getroot()
news3 = ET.parse("./news-shevard.xml").getroot()

out = open("converted.txt", "w")

ns = 'http://www.romip.ru/common/merged-results-QA-facts-extraction'
for task in facts.iter('fact'):
	print task
	num = task.attrib['id']
	if num.count("qaf1"):
		news = news1
		num = num.replace("qaf1", "080404")
	elif num.count("qaf2"):
		news = news2
		num = num.replace("qaf2", "vybory")
	elif num.count("qaf3"):
		news = news3
		num = num.replace("qaf3", "shevard")

	for doc in news.iter('document'):
		if doc.find('docID').text == num:
			text = doc.find('content').text
			break

	text = base64.b64decode(text)
	text = text.decode("cp1251")

	print text
	for fact in task.iter('fact'):
		out.write(fact.attrib['firstText'])
		out.write("\n")
		out.write(fact.attrib['secondText'])
		out.write("\n")
		s = int(fact.attrib['systemOffset'])
		l = int(fact.attrib['systemLength'])
		out.write(text[s : s + l].replace("\n", ""))
		out.write("\n------------\n")