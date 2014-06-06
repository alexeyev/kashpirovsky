import xml.etree.ElementTree as et

f = open('output.txt', 'w')
tree = et.parse('and_good_table.xml')
root = tree.getroot()
ns = 'http://www.romip.ru/common/merged-results-QA-facts-extraction'
for fact in root.iter('{%s}fact' % ns):
	firstWords = fact.attrib['firstText'].encode('utf-8').split()
	secondWords = fact.attrib['secondText'].encode('utf-8').split()
	print firstWords
	print secondWords
	for fword in firstWords:
		f.write(fword + '\t' + fact.attrib['cathegory'].encode('utf-8') +'\n')

	for sword in secondWords:
		f.write(sword + '\t' + fact.attrib['cathegory'].encode('utf-8') +'\n')