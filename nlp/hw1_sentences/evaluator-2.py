__author__ = 'achugr'

from xml.etree import ElementTree
import distance, sys

#true_corpus = "/Users/achugr/PycharmProjects/text-splitter/annotated-corpus.xml"
#parsed_corpus = "parsed-corpus.xml"

iter_true = ElementTree.iterparse(sys.argv[0])
iter_parsed = ElementTree.iterparse(sys.argv[1])

matches = 0
total_true = 0
total_parsed = 0

try:
    while True:
        event_true, elem_true = iter_true.next()
        total_true += 1
        event_parsed, elem_parsed = iter_parsed.next()
        total_parsed += 1
        if elem_true.tag == "sentence" and elem_parsed.tag == "sentence":
            print "comparison of %s ----- %s" % (elem_true.text, elem_parsed.text)
            # if elem_true.text.strip() == elem_parsed.text.strip():
            if distance.levenshtein(elem_true.text.strip(), elem_parsed.text.strip()) < 5:
                matches += 1
            else:
                match_found = False
                if len(elem_true.text) < len(elem_parsed.text):
                    while not match_found:
                        event_true, elem_true = iter_true.next()
                        total_true += 1
                        if elem_parsed.text.strip().endswith(elem_true.text.strip()):
                            match_found = True
                        else:
                            print "skipping true xml tag"
                else:
                    while not match_found:
                        event_parsed, elem_parsed = iter_parsed.next()
                        total_parsed += 1
                        if elem_true.text.strip().endswith(elem_parsed.text.strip()):
                            match_found = True
                        else:
                            print "skipping parsed xml tag"

        if event_true == "end" and elem_true.tag == "sentence":
            elem_true.clear()
        if event_parsed == "end" and elem_parsed.tag == "sentence":
            elem_parsed.clear()

except StopIteration, e:
    print "exception: ", e
    print "matches count: %s" % matches
    print "total true: %s" % (total_true - 1)
    print "total parsed: %s" % (total_parsed - 1)
    prec = float(matches) / float(total_parsed)
    rec = float(matches) / float(total_true)
    f_measure = 2.0 * prec * rec / (prec + rec)
    accur = float(matches) / float(total_parsed + total_true - matches)
    print "precision: %s" % prec
    print "recall: %s" % rec
    print "f measure: %s" % f_measure
    print "accuracy: %s" % accur
