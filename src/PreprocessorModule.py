import nltk
from nltk.corpus import stopwords 
from stanfordcorenlp import StanfordCoreNLP
import traceback
import json
import string
import os
import pandas as pd
import datetime
import subprocess
import time



class PreprocessorModule:

	'''
	This class is the interface for the Stanford Core NLP server.
	'''

	def __init__(self):
		if not os.path.exists('./workdir'):
			os.makedirs('./workdir')

		print('# Loading Stanford Core NLP.')
		self.__startCoreNLP()
		self.nlp = StanfordCoreNLP('http://localhost', port=10000)
		print('# Stanford Core NLP connected.')
		self.stop_words = set(stopwords.words('english'))


	def __startCoreNLP(self):
		command = ['java', '-mx4g', '-cp', "../stanford-corenlp-full-2018-10-05/*", 'edu.stanford.nlp.pipeline.StanfordCoreNLPServer', '-port', '10000', '-timeout', '15000']
		self.corenlpProcessId = subprocess.Popen(command, stdin=open(os.devnull, 'r'), stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
		time.sleep(10) # time for loading stanford core nlp


	def __closeCoreNLP(self):
		self.corenlpProcessId.kill()


	def __getLetterPos(self, pos):
		'''
		This method converts a pos tag into the format required by UKB
		'''
		if pos[0] == 'N':
			return 'n'
		elif pos[0] == 'V':
			return 'v'
		elif pos[0] == 'J':
			return 'a'
		else:
			return 'r'

	def __corenlp(self, text):
		'''
		This method send a text to Stanford core NLP and return a list of triples where  each word is associated with
		its lemma and pos tag.
		'''
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


	def runNoWeights(self, file):
		
		'''
		This method is used for parsing a single file ignoring possible weights that have been associated to texts.
		This is only used for assigning new scores to new resources (i.e. it is not employed for the training)
		It stores in the working directory the files that will be analyzed with the word sense disambiguation module
		'''
		#ctxData contains the association between a context and a text
		ctxData = {}
		ctx = 1
		if '.txt' in file:
			filename = os.path.splitext(os.path.basename(file))[0]
			file_out_sentences = filename + '.sent'
			file_out_words = filename + '.word'

			with open('./workdir/' + file_out_sentences, mode='a', encoding='utf-8') as fo:
				with open('./workdir/' + file_out_words, mode='a', encoding='utf-8') as fow:
					with open(file, mode='r', encoding='utf-8') as f:
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

							try:
								sentence = line.split('\t')[0]
								tokens = self.__corenlp(sentence.replace('#',''))
								tokens = [(word, lemma, token) for (word, lemma, token) in tokens if not (word in self.stop_words or word in string.punctuation) ] 

								#sentences and single words are separated to perform subsequently the best word sense disambiguation algorithm
								if len(tokens) > 1:
									fo.write('ctx' + str(ctx) + '\n')
									w_count = 1
									for token in tokens:
										fo.write(token[1] + '#' + self.__getLetterPos(token[2]) + '#' + 'w' + str(w_count)  + '#' + str(1) + ' ')
										w_count += 1

									fo.write('\n')
								else:
									fow.write('ctx' + str(ctx) + '\n')
									w_count = 1
									for token in tokens:
											fow.write(token[1] + '#' + self.__getLetterPos(token[2]) + '#' + 'w' + str(w_count)  + '#' + str(1) + ' ')
											w_count += 1

									fow.write('\n')

								ctxData['ctx' + str(ctx)] = line.split('\t')[0]
								ctx += 1
							except:
								print(file, ':', line)
		self.__closeCoreNLP()
		return ctxData



	def run(self, trainingDataDirectory, numberOfCategories):

		'''
		This method is used for parsing all files that are in a directory. This method is used only for training where more
		example text files can be used at once.
		It stores in the working directory the files that will be analyzed with the word sense disambiguation module
		'''
		
		# ctxData contains the association between contexts and relative weights
		ctxData = {}
		ctx = 1
		for file in os.listdir(trainingDataDirectory):
			print(str(datetime.datetime.now()) + ' - ' +  file)

			if '.txt' in file:
				filename = os.path.splitext(os.path.basename(file))[0]
				file_out_sentences = filename + '.sent'
				file_out_words = filename + '.word'

				with open('./workdir/' + file_out_sentences, mode='a', encoding='utf-8') as fo:
					with open('./workdir/' + file_out_words, mode='a', encoding='utf-8') as fow:
						with open(trainingDataDirectory + '/' + file, mode='r', encoding='utf-8') as f:
							try:
								lines = f.readlines()
							except:
								print(traceback.format_exc())
								print(file)
								continue
							
							for line in lines:
								weights = []

								try:
									sentence = line.split('\t')[0]
									for i in range(1, numberOfCategories + 1):
										weights += [float(line.strip().split('\t')[i])]

									tokens = self.__corenlp(sentence.replace('#',''))
									tokens = [(word, lemma, token) for (word, lemma, token) in tokens if not (word in self.stop_words or word in string.punctuation) ] 

									# sentences and single words are split to perform subsequently the best word sense disambiguation algorithm
									if len(tokens) > 1:
										fo.write('ctx' + str(ctx) + '\n')
										w_count = 1
										for token in tokens:
											fo.write(token[1] + '#' + self.__getLetterPos(token[2]) + '#' + 'w' + str(w_count)  + '#' + str(1) + ' ')
											w_count += 1

										fo.write('\n')
									else:
										fow.write('ctx' + str(ctx) + '\n')
										w_count = 1
										for token in tokens:
												fow.write(token[1] + '#' + self.__getLetterPos(token[2]) + '#' + 'w' + str(w_count)  + '#' + str(1) + ' ')
												w_count += 1

										fow.write('\n')

									ctxData['ctx' + str(ctx)] = weights
									
									ctx += 1
								except IndexError:
									print('The training files do not contain', numberOfCategories, 'categories.')
									exit(1)
								except:
									print(file, ':', line)
		self.__closeCoreNLP()
		return ctxData




