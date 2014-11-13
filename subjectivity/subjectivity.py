# -*- coding: utf-8 -*-
# python2.7 sentiment.py /Users/jennifer/Box\ Sync/CS\ 221\ Project/code/CS221_Project\ \(jiyue\@stanford.edu\)/svm/review_polarity/txt_sentoken/
import subjectivity_util
from sklearn.datasets import load_files


# the training data folder must be passed as first argument
movie_reviews_data_folder = sys.argv[1]
dataset = load_files(movie_reviews_data_folder, shuffle=False)
print "n_samples: %d" % len(dataset.data)