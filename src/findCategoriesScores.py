import sys
import os
import numpy as np
from PreprocessorModule import PreprocessorModule
from WordSenseDisambiguationModule import WordSenseDisambiguationModule
import datetime
import shutil
import time



class findCategoriesScores:

	def __init__(self):
		self.categoriesNumber = 0
		self.lexiconName = ''
		self.test = ''
		self.mode = ''
		self.lexicon = {}
		self.ctxData = None
		self.preprocessor = PreprocessorModule()
		self.wordsenser = WordSenseDisambiguationModule()
		self.header = 'TEXT\n'


	def parseLexicon(self):

		with open(self.lexiconName, 'r') as f:
			lines = f.readlines()
			head = True
			for line in lines:
				
				if head:
					self.header = line
					head = False
					continue

				values = line.strip().split()
				syn = values[0]
				weights = []
				for i in range(2, self.categoriesNumber + 2):
					weights += [float(values[i])]
	
				self.lexicon[syn] = weights 
				

	def score(self):

		finalScores = {}
		files = os.listdir('./workdir/')
		for file in files:
			if file.startswith('ukb_'):
				with open('./workdir/' + file, 'r') as f:
					lines = f.readlines()
					for i in range(1, len(lines)):
						line = lines[i].split()
						ctx = line[0]
						syn = line[2]

						if ctx not in finalScores:
							finalScores[ctx] = []

						if syn in self.lexicon:
							finalScores[ctx] += [self.lexicon[syn]]

		for ctx in finalScores:
			print(ctx, finalScores)
		
		with open(os.path.splitext(self.test)[0] + '_v1_evaluated_with_' + os.path.splitext(os.path.basename(self.lexiconName))[0] + '.txt', 'w') as f:
			with open(os.path.splitext(self.test)[0] + '_v2_evaluated_with_' + os.path.splitext(os.path.basename(self.lexiconName))[0] + '.txt', 'w') as fs:
				f.write(self.header)
				fs.write(self.header)
				for ctx in self.ctxData:
					text = self.ctxData[ctx].strip()
					if ctx in finalScores and len(finalScores[ctx]) > 1:
						scores = np.array(finalScores[ctx])
						#print('score:', scores)
						
						averagedScores = np.nanmean(scores, axis=0)
						#print('averaged scores:', averagedScores, '\n')
						
						s = np.nansum(averagedScores)
						normalizedScores = [x / s for x in averagedScores ]

						#print('normalized scores:', normalizedScores, '\n')
						scoresString = '\t'.join(map(str, normalizedScores))
						scoresStringNotNorm = '\t'.join(map(str, averagedScores))
						
						#print(text + '\t' + scoresString + '\n')
						#time.sleep(5) 
						f.write(text + '\t' + scoresString + '\n')
						fs.write(text + '\t' + scoresStringNotNorm + '\n')
					else:
						scoresString = '\t'.join(['0.0'] * self.categoriesNumber)
						f.write(text + '\t' + scoresString + '\n')
						fs.write(text + '\t' + scoresString + '\n')


	def __parseArgs(self, argv):
		i = 1
		while i < len(argv):
			if argv[i] == '-c' or argv[i] == '--categories':
				try:
					self.categoriesNumber = int(argv[i + 1])
				except:
					print("Value '", argv[i + 1], "' is not valid as number of classes. ")
					exit(1)
				if self.categoriesNumber <= 0:
					print("The number of classes must be > 0. ")
					exit(1)
				i += 2	
			elif argv[i] == '-l' or argv[i] == '--lexicon':
				self.lexiconName = argv[i + 1] 
				if not os.path.isfile(self.lexiconName):
					print('The lexicon', self.lexiconName, 'does not exist.')
					exit(1)
				i += 2
			elif argv[i] == '-t' or argv[i] == '--test':
				self.test = argv[i + 1]
				if not os.path.isfile(self.test):
					print('The test resource', self.test, 'does not exist.')
					exit(1)
				i += 2
			elif argv[i] == '-m' or argv[i] == '--mode':
				if argv[i + 1] not in ['ppr', 'ppr_w2w']:	
					print("Mode '", argv[i + 1], "' is not valid. ")
					exit(1)
				else:
					self.mode = argv[i + 1]
					i += 2
			else:
				print("The parameter '", argv[i], argv[i + 1], "' is not valid.")
				exit(1)
		return self.lexiconName != '' and self.test != '' and self.categoriesNumber != 0 and self.mode != ''


	def run(self, argv):
            self.__parseArgs(argv)
            if not os.path.exists('./workdir'):
                os.makedirs('./workdir')
            self.ctxData = self.preprocessor.runNoWeights(self.test)
            self.wordsenser.run(self.mode)
            self.parseLexicon()
            self.score()
            shutil.rmtree('./workdir')


if __name__ == '__main__':
    print('START:', str(datetime.datetime.now()))
    framework = findCategoriesScores()
    framework.run(sys.argv)
    print('END:', str(datetime.datetime.now()))




