#!/usr/bin/python3
#Classifies docs in file, organised by date

import pickle
from os import listdir
from pprint import pprint
from word_replace import replace_words
from nltk import word_tokenize
import numpy as np
import matplotlib.pyplot as plt
import datetime

#2 class doc
file =(
open("/home/s/Project/experiments/experiment_python_programs/"
     "classifiers/doc_2c_unibitri_classifier.pickle", "rb"))

classifier = pickle.load(file)
file.close()
triple = False
whole_year = False
bonus = False
path = "/home/s/Project/Dissertation"

with open(path+"/kcnawatch_words.txt", "r") as file:
    kcnawatch_words = file.read().splitlines()

date_array = []
filepath_array = []


filepath = path+"/nuke2006_fixed/"#FOLDER nuke2006
current_date = datetime.date(2006, 9, 11) #STARTDATE nuke2006
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/satellite_nuke_missile2009/"#FOLDER satellite2009
current_date = datetime.date(2009, 3, 8) #STARTDATE satellite2009
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/satellite_nuke_missile2009/"#FOLDER nuke2009
current_date = datetime.date(2009, 4, 27) #STARTDATE nuke2009
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/satellite_nuke_missile2009/"#FOLDER missile2009
current_date = datetime.date(2009, 6, 6) #STARTDATE missile2009
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/cheonan_articles_fixed/"#FOLDER cheonan2010
current_date = datetime.date(2010, 2, 26) #STARTDATE cheonan2010
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/yeonpyeong_articles_fixed/"#FOLDER yeonpyeong2010
current_date = datetime.date(2010, 10, 26) #STARTDATE yeonpyeong2010
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/satellite2012/"#FOLDER satellite2012
current_date = datetime.date(2012, 11, 14) #STARTDATE satellite2012
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/nuke2013/"#FOLDER nuke2013
current_date = datetime.date(2013, 1, 15) #STARTDATE nuke2013
date_array += [current_date]
filepath_array += [filepath]

filepath = path+"/missile2014/"#FOLDER missile2014
current_date = datetime.date(2014, 6, 2) #STARTDATE missile2014
date_array += [current_date]
filepath_array += [filepath]

#adds the 'bonus content' from presentation
date_array += [datetime.date(2015, 8, 6)]
filepath_array += [path+"/2015/"]

#adds 2011
date_array += [datetime.date(2011, 1, 1)]
filepath_array += [path+"/2011/"]

#0 = nuke2006, 1 = satellite2009, 2 = nuke2009, 3 = missile2009,
#4 = cheonan2010, 5 = yeonpyeong2010, 6 = satellite2012,
#7 = nuke2013, 8 = missile2014, 9 = 'bonus content', 10 = 2011

#CHANGE THIS VARIABLE
incident = 10



#also needs incident 1
#triple = True
#also needs incident 9
#bonus = True
#also needs incident 10
whole_year = True
l = listdir(filepath_array[incident])
filepath = filepath_array[incident]
current_date = date_array[incident]
date_for_average = date_array[incident]
d = {}
kcnawatch = {}
dates = []

if triple == True:
    num_days = 147
elif whole_year == True:
    num_days = 365
elif bonus == True:
    num_days = 15
else:
    num_days = 57 #the day + 28 days before + 28 days after
    
for x in range(0, num_days):
    year = str(current_date.year)
    month = str(current_date.month)
    day = str(current_date.day)
    if int(month) < 10:
        month = "0" + month
    if int(day) < 10:
        day = "0" + day
    a = year + "." + month + "." + day
    dates += [a]
    current_date += datetime.timedelta(days=1)

for date in dates:
    d[date] = [0,0,0,0] #pos, neu, neg, article count
    kcnawatch[date] = [0,0] #number of matches, article count

for file in l:
    with open(filepath+file) as f:
        date = file[:10]
        if date in dates:
            s = f.read()
            current = d[date]

            if "\n" in s:
                s = s.replace("\n", " ")
        
            s = replace_words(s)

            #kcna watch dates calculated
            for entry in kcnawatch_words:
                if entry == "war":
                    kcnawatch[date][0] += s.count(" war ")
                if entry == "doom":
                    kcnawatch[date][0] += s.count(" doom ")
                else:
                    kcnawatch[date][0] += s.count(entry)
            kcnawatch[date][1] += 1

            #bayes' dates calculated
            #http://stackoverflow.com/questions/14716437/nltk-classify-interface-using-trained-classifier
            s = dict([(word, True) for word in word_tokenize(s)])
        
            if classifier.classify(s) == "pos":
                current[0] += 1
                current[3] += 1
            if classifier.classify(s) == "neutral":
                current[1] += 1
                current[3] += 1
            if classifier.classify(s) == "neg":
                current[2] += 1
                current[3] += 1


#pprint(d)

ratio = []
kcnawatch_ratio = []
pos = []
neu = []
neg = []

#total no. of articles
##for date in dates:
##    pos += [d[date][0]]
###   neu += [d[date][1]]
##    neg += [d[date][2]]

#ratio
for date in dates:
    #pos:neg ratio
    if d[date][2] != 0:
       ratio += [d[date][0]/d[date][2]]
    else:
       ratio += [0]

    #neg:pos ratio (rare)
##    if d[date][0] != 0:
##       ratio += [d[date][2]/d[date][0]]
##    else:
##       ratio += [2]
       
    if kcnawatch[date][1] != 0:
       kcnawatch_ratio += [kcnawatch[date][0]/kcnawatch[date][1]]
    else:
       kcnawatch_ratio += [kcnawatch[date][0]/1]

print(sum(ratio))
print(sum(kcnawatch_ratio))

##sort = sorted(ratio)
##print(sort)
##print(sum(ratio)/365)
##
##q25, q50, q75 = np.percentile(sort, [25, 50, 75])
##iqr = q75 - q25
##
##print(q25)
##print(q50)
##print(q75)
##print(iqr)

##new_sort = []
##
##for r in ratio:
##    if r < 2.67:
##        new_sort += [r]

##print(sum(new_sort))
##print(len(new_sort))
##print(sum(new_sort)/len(new_sort))

##print(sorted(ratio)[92])
##print(sorted(ratio)[183])
##print(sorted(ratio)[276])
##print(sum(sorted(ratio)[:340]))
       
#print(sum(kcnawatch_ratio))

#% of articles
#for date in dates:
#    pos += [(d[date][0]/d[date][3])]
#    neu += [(d[date][1]/d[date][3])]
#    neg += [(d[date][2]/d[date][3])]
    

title_array = ["2006_Nuclear_Test", "2009_Satellite_Launch",
               "2009_Nuclear_Test", "2009_Missile_Test",
               "2010_ROKS_Cheonan_Sinking", "2010_Yeonpyeong_Island_Shelling",
               "2012_Satellite_Launch", "2013_Nuclear_Test",
               "2014_Missile_Test", "bonus content", "2011"]
id_array = ["2006-10-09", "2009-04-05", "2009-05-25", "2009-07-04",
            "2010-03-26", "2010-11-23", "2012-12-12", "2013-02-12",
            "2014-06-30", "BONUS", "2011"]

plt.gca().set_color_cycle(['black', 'red'])
plt.plot(ratio,'x-')
#plt.plot(kcnawatch_ratio,'x-')
plt.gca().grid(True)
#whole year
if whole_year == True:
    plt.xticks(np.arange(0, 365, 30))
else:
    times = ["T-28", "T-21", "T-14", "T-7", "T", "T+7", "T+14", "T+21", "T+28"]
    plt.xticks(np.arange(0, 57, 7), times) #0-56 (8 weeks), spaced 7 (days) apart
plt.xlabel(id_array[incident] + " +- days")
plt.ylabel("Ratio pos:neg articles")
plt.suptitle(title_array[incident])
#plt.legend(["positive", "neutral", "negative"])

plt.savefig(path+"/graphs/standard/"+title_array[incident]+".png", bbox_inches="tight")
#plt.savefig(path+"/graphs/standard/2011_no_outliers.png", bbox_inches="tight")

plt.show()
