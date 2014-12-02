from utility import readLabeledData, customized_stop_words, crossValidation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from sklearn import svm
from numpy import asarray
from sklearn.naive_bayes import MultinomialNB


DATAPATH = 'sentences.txt'
size = 3000
choice = '2'
serials = []
labels = []
sentences = []

# read data
readLabeledData(DATAPATH, serials, labels, sentences, count = size)
labels = asarray(labels)
print 'Read %d data' % len(sentences)
print

# use unigram model/ bigram model to build the vector for the svm
print "Extracting features from the training dataset using a sparse vectorizer" 
vectorizer = CountVectorizer(stop_words=customized_stop_words, max_df=0.95, min_df=0.01, ngram_range=(1, 2))
vectorized_data = vectorizer.fit_transform(sentences)
print "n_samples: %d, n_features: %d" % vectorized_data.shape
print vectorizer.get_feature_names()


# Fit svm, tune the parameters:class_weights, C
# if we use non linear kernel, need to tune the parameter of the linear kernel
if choice == '1':
	for weight in range(1, 10):
		for c in range(1, 10):
			clf = svm.SVC(kernel='linear', class_weight={0: float(weight)/10}, C = float(c)) 
			print "Use linear kernel, the score of 5- fold cross validation of weight = %f, C = %f is " %(float(weight)/10, float(c)/5)
			print crossValidation(clf, vectorized_data, labels, size, folds = 5, shuffle = False)
			print 

if choice == '2':
	for c in range(1, 10):
		clf = svm.SVC(kernel='rbf', C = float(c)/10, class_weight = 'auto') 
		print "Use rbf kernel, the score of 5-fold cross validation of C = %f is " % float(c)
		print crossValidation(clf, vectorized_data, labels, size, folds = 5, shuffle = False)
		print 

if choice == '3':
	clf = MultinomialNB()
	print crossValidation(clf, vectorized_data, labels, size, folds = 5, shuffle = False)

# test on the testing data
#clf.predict()


# read and write the result into a new file





