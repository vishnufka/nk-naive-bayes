#! /usr/bin/python3

#Experiment for documents, 2 classes, unigrams only.
#98.4% accuracy, 79 minutes to train
#stopwords removed, lowercase words, entity consolidation, 75/25 train/test

import time
import pickle
from word_replace import replace_words
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

#allows the runtime of the program to be measured
start_time = time.time()

#initialises list of stopwords
sw = stopwords.words("english")

#opens files, reads into lists 
with open("/home/s/Project/experiments/corpus/docs/docs_pos.txt") as pos:
    list_pos = pos.readlines()
with open("/home/s/Project/experiments/corpus/docs/docs_neg.txt") as neg:
    list_neg = neg.readlines()

#tags each sentence with either positive or negative sentiment
list_pos_tagged = []
list_neg_tagged = []

for line in list_pos:
    l = replace_words(line.lower())
    list_pos_tagged += [(l, "pos")]

for line in list_neg:
    l = replace_words(line.lower())
    list_neg_tagged += [(l, "neg")]
    
#Adapted from:
#http://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-
#training-for-sentiment-analysis - Barber, J., 2013.
#http://www.nltk.org/book/ch06.html - Bird, S., Klein, E., Loper, E., 2009.
    
#specifies size of training/test sets. 75/25 train/test split
#
list_train = list_pos_tagged[29:] + list_neg_tagged[37:]
list_test = list_pos_tagged[:29] + list_neg_tagged[:37]

#reads sentences, puts words that appear into a set
set_train_unigrams = set()
for entry in list_train:
    for word in word_tokenize(entry[0]):
        set_train_unigrams.add(word)
        
set_test_unigrams = set()
for entry in list_test:
    for word in word_tokenize(entry[0]):
        set_test_unigrams.add(word)

#turns the set into a dictionary for each sentence
list_train_unigrams = []
list_train_final = []
list_test_unigrams = []
list_test_final = []

for entry in list_train:
    list_train_unigrams += [({word: (word in word_tokenize(entry[0])) for word in set_train_unigrams if word not in sw}, entry[1])]

for entry in list_test:
    list_test_unigrams += [({word: (word in word_tokenize(entry[0])) for word in set_test_unigrams if word not in sw}, entry[1])]

list_train_final = list_train_unigrams
list_test_final = list_test_unigrams

#trains and tests the classifier
#prints accuracy, prints most informative features
print("doc_2c_uni")
classifier = nltk.NaiveBayesClassifier.train(list_train_final)
classifier.show_most_informative_features(50)
print(nltk.classify.accuracy(classifier, list_test_final))

#writes classifier to file using pickle
with open("/home/s/Project/experiments/experiment_python_programs/classifiers/doc_2c_uni_classifier.pickle", "wb") as f:
    pickle.dump(classifier, f)
    
#prints runtime
print("completed in " + str(((time.time() - start_time)/60)) + " minutes")
