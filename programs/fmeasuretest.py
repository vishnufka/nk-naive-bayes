#http://streamhacker.com/2010/05/17/text-classification-sentiment-analysis-precision-recall/

import collections
import nltk.metrics
from nltk import word_tokenize
from nltk.classify import NaiveBayesClassifier
from word_replace import replace_words
import time
import pickle
from word_replace import replace_words
import nltk
from nltk.collocations import *
from nltk import word_tokenize
from nltk.corpus import stopwords

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

#opens files, reads into lists 
with open("/home/s/Project/experiments/corpus/docs/docs_pos.txt") as pos:
    list_pos = pos.readlines()
with open("/home/s/Project/experiments/corpus/docs/docs_neg.txt") as neg:
    list_neg = neg.readlines()

#tags each sentence with either positive or negative sentiment
posfeats = []
negfeats = []
all_words = ""

for line in list_pos:
    l = replace_words(line.lower())
    posfeats += [(l, "pos")]
    all_words += l + " "

for line in list_neg:
    l = replace_words(line.lower())
    negfeats += [(l, "neg")]
    all_words += l + " "

negcutoff = int(len(negfeats)*3/4)
poscutoff = int(len(posfeats)*3/4)
 
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

#finds bigrams and trigrams
finder = BigramCollocationFinder.from_words(word_tokenize(all_words))
finder.apply_freq_filter(4)
bigram_list = finder.nbest(bigram_measures.pmi, 500)

tri_finder = TrigramCollocationFinder.from_words(word_tokenize(all_words))
tri_finder.apply_freq_filter(4)
trigram_list = tri_finder.nbest(trigram_measures.pmi, 500)

#Adapted from:
#http://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-
#training-for-sentiment-analysis - Barber, J., 2013.
#http://www.nltk.org/book/ch06.html - Bird, S., Klein, E., Loper, E., 2009.

set_train_unigrams = set()
for entry in trainfeats:
    for word in word_tokenize(entry[0]):
        set_train_unigrams.add(word.lower())

set_train_bigrams = set()
for entry in trainfeats:
    for bg in bigram_list:
        beegee = bg[0] + " " + bg[1]
        set_train_bigrams.add(beegee)

set_train_trigrams = set()
for entry in trainfeats:
    for tg in trigram_list:
        teegee = tg[0] + " " + tg[1] + " " + tg[2]
        set_train_trigrams.add(teegee)

set_test_unigrams = set()
for entry in testfeats:
    for word in word_tokenize(entry[0]):
        set_test_unigrams.add(word.lower())

set_test_bigrams = set()
for entry in testfeats:
    for bg in bigram_list:
        beegee = bg[0] + " " + bg[1]
        set_test_bigrams.add(beegee)

set_test_trigrams = set()
for entry in testfeats:
    for tg in trigram_list:
        teegee = tg[0] + " " + tg[1] + " " + tg[2]
        set_test_trigrams.add(teegee)

list_train_final = []
list_test_final = []
count = 0
for entry in testfeats:
    a = {word: word in word_tokenize(entry[0]) for word in set_train_unigrams}
    b = {bg: (bg in entry[0]) for bg in set_train_bigrams}
    c = {tg: (tg in entry[0]) for tg in set_train_trigrams}
    d = a.copy()
    d.update(b)
    d.update(c)
    list_train_final += [(d, entry[1])]
    count += 1
    print(count)

for entry in trainfeats:
    a = {word: word in word_tokenize(entry[0]) for word in set_test_unigrams}
    b = {bg: (bg in entry[0]) for bg in set_test_bigrams}
    c = {tg: (tg in entry[0]) for tg in set_test_trigrams}
    d = a.copy()
    d.update(b)
    d.update(c)
    list_test_final += [(d, entry[1])]
    count += 1
    print(count)

classifier = NaiveBayesClassifier.train(list_test_final)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
 
for i, (feats, label) in enumerate(list_test_final):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

print("doc unibitri")
print('pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos']))
print('pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos']))
print('pos F-measure:', nltk.metrics.f_measure(refsets['pos'], testsets['pos']))
print('neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg']))
print('neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg']))
print('neg F-measure:', nltk.metrics.f_measure(refsets['neg'], testsets['neg']))


#################################################################

#http://streamhacker.com/2010/05/17/text-classification-sentiment-analysis-precision-recall/

#opens files, reads into lists 
with open("/home/s/Project/experiments/corpus/docs/docs_pos.txt") as pos:
    list_pos = pos.readlines()
with open("/home/s/Project/experiments/corpus/docs/docs_neg.txt") as neg:
    list_neg = neg.readlines()

#tags each sentence with either positive or negative sentiment
posfeats = []
negfeats = []

for line in list_pos:
    l = replace_words(line.lower())
    posfeats += [(l, "pos")]

for line in list_neg:
    l = replace_words(line.lower())
    negfeats += [(l, "neg")]

negcutoff = int(len(negfeats)*3/4)
poscutoff = int(len(posfeats)*3/4)
 
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))


#Adapted from:
#http://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-
#training-for-sentiment-analysis - Barber, J., 2013.
#http://www.nltk.org/book/ch06.html - Bird, S., Klein, E., Loper, E., 2009.

set_train_unigrams = set()
for entry in trainfeats:
    for word in word_tokenize(entry[0]):
        set_train_unigrams.add(word.lower())

set_test_unigrams = set()
for entry in testfeats:
    for word in word_tokenize(entry[0]):
        set_test_unigrams.add(word.lower())

set_test_bigrams = set()
for entry in testfeats:
    for bg in bigram_list:
        beegee = bg[0] + " " + bg[1]
        set_test_bigrams.add(beegee)

list_train_final = []
list_test_final = []
count = 0
for entry in testfeats:
    a = {word: word in word_tokenize(entry[0]) for word in set_train_unigrams}
    d = a.copy()
    list_train_final += [(d, entry[1])]
    count += 1
    print(count)

for entry in trainfeats:
    a = {word: word in word_tokenize(entry[0]) for word in set_test_unigrams}
    d = a.copy()
    list_test_final += [(d, entry[1])]
    count += 1
    print(count)

classifier = NaiveBayesClassifier.train(list_test_final)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
 
for i, (feats, label) in enumerate(list_test_final):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

print("doc uni") 
print('pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos']))
print('pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos']))
print('pos F-measure:', nltk.metrics.f_measure(refsets['pos'], testsets['pos']))
print('neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg']))
print('neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg']))
print('neg F-measure:', nltk.metrics.f_measure(refsets['neg'], testsets['neg']))
