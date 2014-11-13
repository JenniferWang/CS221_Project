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
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences



if __name__ == '__main__':
	testSplitter = Splitter()
	text = "input format: a paragraph of text. output format: a list of lists of words."
	print testSplitter.split(text)
