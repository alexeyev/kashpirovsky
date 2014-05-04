import xml.etree.ElementTree as et

f = open('output.txt', 'w')
tree = et.parse('and_good_table.xml')
root = tree.getroot()
ns = 'http://www.romip.ru/common/merged-results-QA-facts-extraction'
for fact in root.iter('{%s}fact' % ns):
    f.write(fact.attrib['firstText'].encode('utf-8') + '\t' + fact.attrib['cathegory'].encode('utf-8') +'\n')
    f.write(fact.attrib['secondText'].encode('utf-8') + '\t' + fact.attrib['cathegory'].encode('utf-8') +'\n')