# -*- coding: utf-8 -*-
import sys

try:
    print "true:", sys.argv[1]
    print "parsed:", sys.argv[2]
except:
    print "\nShould have 2 arguments, quitting."
    quit()

#todo:
