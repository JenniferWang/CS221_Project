from sklearn import cross_validation
from collections import Counter

def readLabeledData(path, serials, labels, sentences, count):
	"""
	read the data and split the data into label and sentense
	"""
	_count = 0
	with open(path, 'r') as f:
		for line in f:
			if _count < count:
				splitted = line.split('<>')
				serials.append(splitted[0])
				labels.append(int(splitted[1]))
				sentences.append(splitted[2][:-2])
				_count += 1

customized_stop_words = ['a', 'about', 'above', 'an', 'and', 'are', "aren't", 'as', 'at',\
	'be', 'by', 'for', 'from', 'had', "here's", 'here', "how's", 'if', 'in', 'into',\
	 'is', "isn't", 'it', "it's", 'its', 'itself','of', 'off', 'on', 'out', 'over',\
	  'that', "that's",'the', 'this', 'those', 'to', 'was', 'were']

def crossValidation(clf, vectors, labels, size, folds, shuffle = False):
	"""
	return the error rate for classifying 0 to 1
	"""
	kfold = cross_validation.KFold(n = size, shuffle= shuffle, n_folds=folds)
	score = []
	for train_index, test_index in kfold:
		test_Vector = [vectors[idx] for idx in test_index]
		test_labels = [labels[idx] for idx in test_index]

		clf.fit(vectors[train_index], labels[train_index])
		error = 0
		totolNumber = Counter(test_labels)
		for index in test_index:
			machine_result = clf.predict(vectors[index])
 			if labels[index] == 0 and machine_result[0] == 1:
				error += 1
		score.append(float(error)/totolNumber[1])

	return score
