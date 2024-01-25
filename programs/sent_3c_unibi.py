#! /usr/bin/python3

#Experiment for sentences, 3 classes, unigrams and bigrams.
#85.6% accuracy, 24 minutes to train
#stopwords removed, lowercase words, entity consolidation, 75/25 train/test
#bigrams that appear 4 or more times, 500 most common bigrams

import time
import pickle
from word_replace import replace_words
import nltk
from nltk.collocations import *
from nltk import word_tokenize
from nltk.corpus import stopwords

#allows the runtime of the program to be measured
start_time = time.time()

#initialises list of stopwords
stopwords_list = stopwords.words("english")

#initialises bigram measure
bigram_measures = nltk.collocations.BigramAssocMeasures()

#opens files, reads into lists 
with open("/home/s/Project/experiments/corpus/sents/sents_pos.txt") as pos:
    list_pos = pos.readlines()
with open("/home/s/Project/experiments/corpus/sents/sents_neu.txt") as neu:
    list_neu = neu.readlines()
with open("/home/s/Project/experiments/corpus/sents/sents_neg.txt") as neg:
    list_neg = neg.readlines()

#tags each sentence with either positive or negative sentiment
list_pos_tagged = []
list_neu_tagged = []
list_neg_tagged = []
all_words = ""

for line in list_pos:
    l = replace_words(line.lower())
    list_pos_tagged += [(l, "pos")]
    all_words += l + " "

for line in list_neu:
    l = replace_words(line.lower())
    list_neu_tagged += [(l, "neutral")]
    all_words += l + " "

for line in list_neg:
    l = replace_words(line.lower())
    list_neg_tagged += [(l, "neg")]
    all_words += l + " "
    
#Adapted from:
#http://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-
#training-for-sentiment-analysis - Barber, J., 2013.
#http://www.nltk.org/book/ch06.html - Bird, S., Klein, E., Loper, E., 2009.
    
#specifies size of training/test sets. 75/25 train/test split
list_train = list_pos_tagged[100:] + list_neu_tagged[100:] + list_neg_tagged[100:]
list_test = list_pos_tagged[:100] + list_neu_tagged[:100] + list_neg_tagged[:100]

#finds 
finder = BigramCollocationFinder.from_words(word_tokenize(all_words))
finder.apply_freq_filter(4)
bigram_list = finder.nbest(bigram_measures.pmi, 500)

#reads sentences, puts words that appear into a set
set_train_unigrams = set()
for entry in list_train:
    for word in word_tokenize(entry[0]):
        set_train_unigrams.add(word.lower())

set_train_bigrams = set()
for entry in list_train:
    for bg in bigram_list:
        beegee = bg[0] + " " + bg[1]
        set_train_bigrams.add(beegee)
        
set_test_unigrams = set()
for entry in list_test:
    for word in word_tokenize(entry[0]):
        set_test_unigrams.add(word.lower())

set_test_bigrams = set()
for entry in list_test:
    for bg in bigram_list:
        beegee = bg[0] + " " + bg[1]
        set_test_bigrams.add(beegee)

#turns the set into a dictionary for each sentence
list_train_final = []
list_test_final = []
count = 0

for entry in list_train:
    a = {word: word in word_tokenize(entry[0]) for word in set_train_unigrams}
    b = {bg: (bg in entry[0]) for bg in set_train_bigrams}
    d = a.copy()
    d.update(b)
    list_train_final += [(d, entry[1])]
    count += 1
    print(len(list_train)+len(list_test)-count)

for entry in list_train:
    a = {word: word in word_tokenize(entry[0]) for word in set_test_unigrams}
    b = {bg: (bg in entry[0]) for bg in set_test_bigrams}
    d = a.copy()
    d.update(b)
    list_test_final += [(d, entry[1])]
    count += 1
    print(len(list_train)+len(list_test)-count)

#trains and tests the classifier
#prints accuracy, prints most informative features
print("sent_3c_unibi")
classifier = nltk.NaiveBayesClassifier.train(list_train_final)
classifier.show_most_informative_features(200)
print(nltk.classify.accuracy(classifier, list_test_final))

#writes classifier to file using pickle
with open("/home/s/Project/experiments/experiment_python_programs/classifiers/sent_3c_unibi_classifier.pickle", "wb") as f:
    pickle.dump(classifier, f)
    
#prints runtime
print("completed in " + str(((time.time() - start_time)/60)) + " minutes")
