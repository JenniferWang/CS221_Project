# -*- coding: utf-8 -*-
"""
basic_sentiment_analysis
~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the code and examples described in 
http://fjavieralba.com/basic-sentiment-analysis-with-python.html
"""

from pprint import pprint
import nltk
import yaml
import sys
import os
import re

class Splitter(object):

	def __init__(self):
		self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
		self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

	def split(self, text):
		"""
		input format: a paragraph of text (string)
		output format: a list of lists of words.
			e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
		"""
		sentences = self.nltk_splitter.tokenize(text)
		tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
		return tokenized_sentences



class POSTagger(object):

	def __init__(self):
		pass
		
	def pos_tag(self, sentences):
		"""
		input format: list of lists of words
			e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
		output format: list of lists of tagged tokens. Each tagged tokens has a
		form, a lemma, and a list of tags
			e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
					[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
		"""
		pos = [nltk.pos_tag(sentence) for sentence in sentences]
		#adapt format
		pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
		return pos


class DictionaryTagger(object):

	def __init__(self, dictionary_paths):
		files = [open(path, 'r') for path in dictionary_paths]
		dictionaries = [yaml.load(dict_file) for dict_file in files]
		map(lambda x: x.close(), files)
		self.dictionary = {}
		self.max_key_size = 0
		for curr_dict in dictionaries:
			for key in curr_dict:
				if key in self.dictionary:
					self.dictionary[key].extend(curr_dict[key])
				else:
					self.dictionary[key] = curr_dict[key]
					self.max_key_size = max(self.max_key_size, len(key))

	def tag(self, postagged_sentences):
		return [self.tag_sentence(sentence) for sentence in postagged_sentences]

	def tag_sentence(self, splitted_sentence):
		"""
		input : one splitted sentence ( a list of words)
				['The', 'staff', 'of', 'the', 'restaurant', 'is', 'nice', 'and',...]
		output: taged sentenct:
				[...('restaurant'), ('is'), ('nice', ['positive']), ...]
		"""

		tag_sentence = []
		N = len(splitted_sentence)
		if self.max_key_size == 0:
			self.max_key_size = N

		i = 0
		while (i < N):
			j = min(i + self.max_key_size, N) #avoid overflow
			tagged = False
			while (j > i):
				expression_form = ' '.join(splitted_sentence[i:j]).lower()
				literal = expression_form

				if literal in self.dictionary:
					is_single_token = j - i == 1
					original_position = i
					i = j
					taggings = [tag for tag in self.dictionary[literal]]
					tagged_expression = (expression_form, taggings)
					tag_sentence.append(tagged_expression)
					tagged = True

				else:
					j = j - 1

			if not tagged:
				tag_sentence.append(splitted_sentence[i])
				i += 1
		return tag_sentence


if __name__ == '__main__':
	splitter = Splitter()

	text = """What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad. Apart from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."""
	splitted_sentences =  splitter.split(text)

	dicttagger = DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml'])
	dict_tagged_sentences = dicttagger.tag(splitted_sentences)
	pprint(dict_tagged_sentences)
