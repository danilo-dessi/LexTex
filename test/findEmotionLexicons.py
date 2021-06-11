'''
This file perform a sentiment analysis task employing one between Depeche Mood or EmoWordNet lexicon.
Example:

python3 findEmotionLexicons gold.txt plain_task_1_evaluated_with_DepecheMood_tfidf.txt plain_task_2_evaluated_with_DepecheMood_tfidf.txt 




'''

import sys
import os
import numpy as np
import datetime
import shutil
import nltk
from nltk.corpus import stopwords 
from stanfordcorenlp import StanfordCoreNLP
import json
import string

CONSIDERED_EMOTION_POSITION = [3, 1, 6, 8]
HEAD = 'TEXT\tANGER\tFEAR\tJOY\tSADNESS\n'


class LexiconScorer:
	def __init__(self):
		self.test = ''
		self.text2lemmasAndTags = {}
		self.lexicon = {}
		self.nlp = StanfordCoreNLP('http://192.167.144.244', port=9000)
		self.stop_words = set(stopwords.words('english'))

	def __corenlp(self, text):
		tokens = []

		props = {'annotators': 'tokenize,ssplit,pos,lemma', 'pipelineLanguage': 'en', 'outputFormat': 'json'}
		try:
			corenlp_out = json.loads(self.nlp.annotate(text, properties=props))
		except:
			print('Stanford Core NLP is not responding. Please try later')
			print(traceback.format_exc())
			exit(1)
		
		for sentence in corenlp_out['sentences']:
			for token in sentence['tokens']:
				tokens += [(token['word'], token['lemma'], token['pos'])]
		return tokens


	def __parseArgs(self, argv):
		self.test = argv[1]
		if not os.path.isfile(self.test):
			print('The test resource', self.test, 'does not exist.')
			exit(1)

		self.lexicon_path = argv[2]
		if not os.path.isfile(self.test):
			print('The lexicon resource', self.test, 'does not exist.')
			exit(1)

		return self.test != ''

	def __getLetterPos(self, pos):
		if pos[0] == 'N':
			return 'n'
		elif pos[0] == 'V':
			return 'v'
		elif pos[0] == 'J':
			return 'a'
		else:
			return 'r'



	def parse(self):
		with open(self.test, mode='r', encoding='utf-8') as f:

			try:
				lines = f.readlines()
			except:
				print(traceback.format_exc())
				print(file)

			head = True
			for line in lines:
				if head:
					head = False
					continue
				text = line.strip().split('\t')[0]
				tokens = self.__corenlp(text.strip().replace('#',''))
				lemmasAndTags = [(lemma, self.__getLetterPos(tag)) for (word, lemma, tag) in tokens if not (word in self.stop_words or word in string.punctuation) ] 

				self.text2lemmasAndTags[text] = lemmasAndTags


	def loadLexicon(self):
		with open(self.lexicon_path, 'r') as f:
			lines = f.readlines()
			for line in lines:
				if not line.startswith('//') and not line.startswith('Lemma#PoS'):
					if 'EmoWordNet1.0.txt' == os.path.basename(self.lexicon_path):
						values = line.strip().split(';')
					else:
						values = line.strip().split('\t')
					consideredValues = []
					for i in CONSIDERED_EMOTION_POSITION:
						consideredValues += [float(values[i])]
					self.lexicon[values[0]] = consideredValues


	def score(self):
		with open(os.path.splitext(self.test)[0] + '_task_1_evaluated_with_' + os.path.splitext(os.path.basename(self.lexicon_path))[0] + '.txt', 'w') as f:
			with open(os.path.splitext(self.test)[0] + '_task_2_evaluated_with_' + os.path.splitext(os.path.basename(self.lexicon_path))[0] + '.txt', 'w') as fs:
				f.write(HEAD)
				fs.write(HEAD)
				for text in self.text2lemmasAndTags:
					scores = []
					print(text)
					for (lemma, tag) in self.text2lemmasAndTags[text]:
						key = lemma + '#' + tag
						if key in self.lexicon:
							scores += [self.lexicon[key]]
							print(key, self.lexicon[key])

					if len(scores) > 0:
						scores = np.array(scores)
						print(scores)
						averagedScores = np.mean(scores, axis=0)
						print('average', averagedScores)
						s = sum(averagedScores)
						normalizedScores = [x / s for x in averagedScores ]
						print('norm average', normalizedScores)

						scoresString = '\t'.join(map(str, normalizedScores))     # given a text, compute a score for each emotion
						scoresStringNotNorm = '\t'.join(map(str, averagedScores)) # emotion not normalized, scores are indipendent
						f.write(text + '\t' + scoresString + '\n')
						fs.write(text + '\t' + scoresStringNotNorm + '\n')
					else:
						scoresString = '\t'.join(['0'] * len(CONSIDERED_EMOTION_POSITION))
						f.write(text + '\t' + scoresString + '\n')
						fs.write(text + '\t' + scoresString + '\n')
					print('\n\n')


	def run(self, argv):
	    self.__parseArgs(argv)
	    self.loadLexicon()
	    self.parse()
	    self.score()

if __name__ == '__main__':
	emo = LexiconScorer()
	emo.run(sys.argv)
	





