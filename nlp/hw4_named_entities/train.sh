#!/bin/bash
java -cp /Users/achugr/csc/nlp_2014/mallet-2.0.7/class:/Users/achugr/csc/nlp_2014/mallet-2.0.7/lib/mallet-deps.jar cc.mallet.fst.SimpleTagger --train true --model-file data/classifier data/ru_corpus_balanced_2.train.evaluated.txt