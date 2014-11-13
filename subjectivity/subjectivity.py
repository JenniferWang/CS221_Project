# -*- coding: utf-8 -*-
# python2.7 subjectivity.py /Users/jennifer/Box\ Sync/CS\ 221\ Project/code/CS221_Project\ \(jiyue\@stanford.edu\)/svm/review_polarity/txt_sentoken/
from subjectivity_util import * 
import sys
from sklearn.datasets import load_files


# the training data folder must be passed as first argument
movie_reviews_data_folder = sys.argv[1]
dataset = load_files(movie_reviews_data_folder, shuffle=False)

reviewList = dataset['data']
splitted_reviewList = []
dict_tagged_reviewList = []
score_reviewList = []


splitter = Splitter()
dicttagger = DictionaryTagger(['dicts/subjective.yml'])
labels = ['weaksubj', 'strongsubj']

# split each sentence into word list
workload = 5
# workload = len(reviewList)
for i in xrange(workload):
	splitted_reviewList.append(splitter.split(reviewList[i]))
	dict_tagged_reviewList.append(dicttagger.tag(splitted_reviewList[i]))
	score_reviewList.append(sentence_score(dict_tagged_reviewList[i], labels))

pprint(score_reviewList)


# create tag dictionary



#splitedText = testSplitter.split(text)
#print splitedText
