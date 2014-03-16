#!/bin/bash
# запуск - sh test.sh path/with/raw path/with/parsed
for i in {0..9}
do
   python parser.py $1/$i.txt $2/$i.txt
done
