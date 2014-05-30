Для weka взяли те же тексты (learn/, test/), теми же средствами их нормализовали, СЛИЛИ в одну папку mixed_to_be_split_preprocessed, построили по ней arff-файл. Затем разделили его на две части, скопировав заголовок (иначе не работает). А потом применили NaiveBayes так: learn_preprocessed.arff с тестовым множеством test_preprocessed.arff.

-------------------

МЫ

{'fp': 3, 'tn': 6, 'fn': 1, 'tp': 8}
prec:  0.72720661758
rec:  0.88879013443
f:  0.799425313123

-------------------

WEKA

Time taken to build model: 0.03 seconds

=== Evaluation on test set ===
=== Summary ===

Correctly Classified Instances          15               83.3333 %
Incorrectly Classified Instances         3               16.6667 %
Kappa statistic                          0.6667
Mean absolute error                      0.1562
Root mean squared error                  0.3843
Relative absolute error                 31.2432 %
Root relative squared error             76.0926 %
Total Number of Instances               18     

=== Detailed Accuracy By Class ===

               TP Rate   FP Rate   Precision   Recall  F-Measure   ROC Area  Class
                 0.667     0          1         0.667     0.8        1        internet
                 1         0.333      0.75      1         0.857      0.889    nointernet
Weighted Avg.    0.833     0.167      0.875     0.833     0.829      0.944

=== Confusion Matrix ===

 a b   <-- classified as
 6 3 | a = internet
 0 9 | b = nointernet
