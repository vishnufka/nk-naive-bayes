#! /usr/bin/python3

#Experiment for documents, 2 classes, unigrams, bigrams and trigrams.
#xx% accuracy, xx minutes to train
#stopwords removed, lowercase words, entity consolidation, 75/25 train/test
#bigrams/trigrams that appear 4 or more times
#200 most common bigrams and 200 most common trigrams

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

#initialises bigram and trigram measure
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

#opens files, reads into lists 
with open("/home/s/Project/experiments/corpus/docs/docs_pos.txt") as pos:
    list_pos = pos.readlines()
with open("/home/s/Project/experiments/corpus/docs/docs_neg.txt") as neg:
    list_neg = neg.readlines()

#tags each sentence with either positive or negative sentiment
list_pos_tagged = []
list_neg_tagged = []
all_words = ""

for line in list_pos:
    l = replace_words(line.lower())
    list_pos_tagged += [(l, "pos")]
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
#148 neg + 117 pos = total size of corpus  
list_train = list_pos_tagged[29:] + list_neg_tagged[37:]
list_test = list_pos_tagged[:29] + list_neg_tagged[:37]

#finds bigrams and trigrams
finder = BigramCollocationFinder.from_words(word_tokenize(all_words))
finder.apply_freq_filter(4)
bigram_list = finder.nbest(bigram_measures.pmi, 500)

tri_finder = TrigramCollocationFinder.from_words(word_tokenize(all_words))
tri_finder.apply_freq_filter(4)
trigram_list = tri_finder.nbest(trigram_measures.pmi, 500)


#reads sentences, puts words that appear into a set
set_train_unigrams = set()
for entry in list_train:
    for word in word_tokenize(entry[0]):
        set_train_unigrams.add(word)

set_train_bigrams = set()
for entry in list_train:
    for bg in bigram_list:
        beegee = bg[0] + " " + bg[1]
        set_train_bigrams.add(beegee)

set_train_trigrams = set()
for entry in list_train:
    for tg in trigram_list:
        teegee = tg[0] + " " + tg[1] + " " + tg[2]
        set_train_trigrams.add(teegee)
        
set_test_unigrams = set()
for entry in list_test:
    for word in word_tokenize(entry[0]):
        set_test_unigrams.add(word)

set_test_bigrams = set()
for entry in list_test:
    for bg in bigram_list:
        beegee = bg[0] + " " + bg[1]
        set_test_bigrams.add(beegee)

set_test_trigrams = set()
for entry in list_test:
    for tg in trigram_list:
        teegee = tg[0] + " " + tg[1] + " " + tg[2]
        set_test_trigrams.add(teegee)

#turns the set into a dictionary for each sentence
list_train_final = []
list_test_final = []
count = 0

for entry in list_train:
    a = {word: word in word_tokenize(entry[0]) for word in set_train_unigrams}
    b = {bg: (bg in entry[0]) for bg in set_train_bigrams}
    c = {tg: (tg in entry[0]) for tg in set_train_trigrams}
    d = a.copy()
    d.update(b)
    d.update(c)
    list_train_final += [(d, entry[1])]
    count += 1
    print(len(list_train)+len(list_test)-count)

for entry in list_train:
    a = {word: word in word_tokenize(entry[0]) for word in set_test_unigrams}
    b = {bg: (bg in entry[0]) for bg in set_test_bigrams}
    c = {tg: (tg in entry[0]) for tg in set_test_trigrams}
    d = a.copy()
    d.update(b)
    d.update(c)
    list_test_final += [(d, entry[1])]
    count += 1
    print(len(list_train)+len(list_test)-count)

#trains and tests the classifier
#prints accuracy, prints most informative features
print("doc_2c_unibitri")
classifier = nltk.NaiveBayesClassifier.train(list_train_final)
classifier.show_most_informative_features(200)
print(nltk.classify.accuracy(classifier, list_test_final))

#writes classifier to file using pickle
with open("/home/s/Project/experiments/experiment_python_programs/classifiers/doc_2c_unibitri_classifier.pickle", "wb") as f:
    pickle.dump(classifier, f)
    
#prints runtime
print("completed in " + str(((time.time() - start_time)/60)) + " minutes")
