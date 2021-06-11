import os
import sys
from PreprocessorModule import PreprocessorModule
from WordSenseDisambiguationModule import WordSenseDisambiguationModule
from ScoreLevelModule import ScoreLevelModule
import shutil
import datetime

class LexTex:

	'''
	This is the main class.
	See <link> for details..
	'''

	def __init__(self):
		self.trainingDataDirectory = '' # the directory that contains the training resources
		self.lexiconName = ''  			# the name of the resulting lexicon
		self.mode = ''     		 		# the default mode for using UKB. ppr is used by default
		self.categoriesNumber = 0		# the number od categories. There must be at least categoriesNumber columns for each text
		self.ctxData  = {}				# the dictionary that associates each context with the list of weights. There is a context. for each text
		self.categories = []
		self.preprocessor = PreprocessorModule()
		self.scorer = ScoreLevelModule()
		self.wordsenser = WordSenseDisambiguationModule()
		self.lexicon = None				# a dictionary from wordnet synsets to lemmas and weights
		self.norm = True #  flag for normalizing averages
		self.coeff = True # flag for applying the cf coefficient

	def __parseArgs(self, argv):
		print(argv)

		i = 1
		while i < len(argv):
			if argv[i] == '-d' or argv[i] == '--directory':
				if os.path.isdir(argv[i + 1]):
					self.trainingDataDirectory = argv[i + 1]
					i += 2
				else:
					print("Directory '", argv[i + 1], "' does not exist. ")
					exit(1)
			elif argv[i] == '-ln' or argv[i] == '--lexicon-name':
				self.lexiconName = argv[i + 1]
				i += 2
			elif argv[i] == '-m' or argv[i] == '--mode':
				if argv[i + 1] not in ['ppr', 'ppr_w2w']:
					print("Mode '", argv[i + 1], "' is not valid. ")
					exit(1)
				else:
					self.mode = argv[i + 1]
					i += 2
			elif argv[i] == '-c' or argv[i] == '--categories':
				try:
					self.categoriesNumber = int(argv[i + 1])
				except:
					print("Value '", argv[i + 1], "' is not valid as number of categories. ")
					exit(1)
				if self.categoriesNumber <= 0:
					print("The number of categories must be > 0. ")
					exit(1)
				i += 2	
			elif argv[i] == '-lc' or argv[i] == '--label-categories':
				try:
					self.categories = argv[i + 1].strip().split(',')
					self.categoriesNumber = len(self.categories)
				except:
					print("Labels names '", argv[i + 1], "' are not valid ")
					exit(1)
				if self.categoriesNumber <= 0:
					print("The number of classes must be > 0. ")
					exit(1)
				i += 2	
			elif argv[i] == '-nn' or argv[i] == '--no-norm':
				self.norm = False
				i += 1
			elif argv[i] == '-nc' or argv[i] == '--no-coeff':
				self.coeff = False
				i += 1	
			else:
				print("The parameter '", argv[i], argv[i + 1], "' is not valid.")
				print('Please use \'python3 LexTex.py -d <directory> -m <mode> -c <number_of_categories> -ln <lexicon_name>\'')
				i += 2

		return self.trainingDataDirectory != '' and self.lexiconName != '' and self.mode != '' and self.categoriesNumber != 0



	def __save(self):
		with open(self.lexiconName, 'a') as fo:
			for syn in self.lexicon:
				lemmasString = ','.join(set(self.lexicon[syn]['lemmas']))
				weightsString = '\t'.join(map(str, self.lexicon[syn]['weights']))
				fo.write(syn + '\t' + lemmasString + '\t' + weightsString + '\n')


	def run(self, argv):
		b = self.__parseArgs(argv)
		if b:
			self.ctxData = self.preprocessor.run(self.trainingDataDirectory, self.categoriesNumber)
			self.wordsenser.run(self.mode)
			self.lexicon = self.scorer.run(self.ctxData, self.norm, self.coeff)
			self.__save()
			shutil.rmtree('./workdir')
		else:
			print('Please use \'python3 LexTex.py -d <directory> -m <mode> -c <number_of_classes> -l <lexicon_name>\'')




if __name__ == '__main__':
        print('START:', str(datetime.datetime.now()))
        framework = LexTex()
        framework.run(sys.argv)
        print('END:', str(datetime.datetime.now()))
