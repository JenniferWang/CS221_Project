
# python2.7 sentiment.py /Users/jennifer/Box\ Sync/CS\ 221\ Project/code/CS221_Project\ \(jiyue\@stanford.edu\)/svm/review_polarity/txt_sentoken/
import sys
from time import time
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import svm


# the training data folder must be passed as first argument
movie_reviews_data_folder = sys.argv[1]
dataset = load_files(movie_reviews_data_folder, shuffle=False)
print "n_samples: %d" % len(dataset.data)


# split the dataset in training and test set:
docs_train, docs_test, y_train, y_test = train_test_split(
    dataset.data, dataset.target, test_size=0.25, random_state=None)

print "Extracting features from the training dataset using a sparse vectorizer" 
t0 = time()
vectorizer = CountVectorizer(stop_words='english', max_df=0.95, min_df=0.05, ngram_range=(2, 2))
X_train = vectorizer.fit_transform(docs_train)
duration = time( ) - t0
print "done in %fs" % duration
print "n_samples: %d, n_features: %d" % X_train.shape
print vectorizer.get_feature_names()

#X_test = vectorizer.fit_transform(docs_test)

print "Extracting %d best features by a chi-squared test", 100
t0 = time()
ch2 = SelectKBest(chi2, k=100)
#print vectorizer.get_feature_names()[ch2.get_support()]
#X_train = ch2.fit_transform(X_train, y_train)
print "done in %fs" % (time() - t0)
print ch2

# Fit svm
clf = svm.SVC()
clf.fit(X_train, y_train) 
print clf.n_support_