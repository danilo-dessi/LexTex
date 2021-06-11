import os
import numpy as np

class ScoreLevelModule:
	def __init__(self):
		self.ctxData = None 
		self.wordnetSynsets = {}
		self.ctxLemmas = {}


	def __parse(self):
		files = os.listdir('./workdir/')
		for file in files:
			if file.startswith('ukb_'):
				with open('./workdir/' + file, 'r') as f:
					lines = f.readlines()
					for i in range(1, len(lines)):
						line = lines[i].split()
						ctx = line[0]
						syn = line[2]
						lemma = line[4]

						if syn not in self.wordnetSynsets:
							self.wordnetSynsets[syn] = {'ctx': [], 'lemmas': [], 'weights': []}

						if ctx not in self.ctxLemmas:
							self.ctxLemmas[ctx] = []
						self.ctxLemmas[ctx] += [lemma]

						self.wordnetSynsets[syn]['ctx'] += [ctx]
						self.wordnetSynsets[syn]['lemmas'] += [lemma]
		
	def __normalizer(self, listValues):
		s = sum(listValues)
		return [ x / s for x in listValues ]


	def __score(self, norm, coeff):

		keys = list(self.wordnetSynsets.keys())
		for syn in keys:
			all_scores = []
			
			for ctx in self.wordnetSynsets[syn]['ctx']:
				all_scores += [self.ctxData[ctx]]
			all_scores = np.array(all_scores)
			all_scores_nan = np.where(all_scores == 0, np.nan, all_scores) #put nan instead of 0
			average = np.nanmean(all_scores_nan, axis = 0) # computing of averages of columns ignoring nan
			average[np.isnan(average)] = 0 # conversion of nan in zero

			if norm:
				average = self.__normalizer(average)

			if coeff:
				no_zeros = np.count_nonzero(all_scores,  axis=0)
				tot = np.sum(no_zeros)
				cf = no_zeros / tot

				average = np.prod([average, cf], axis=0) #average weighting with cf

			if norm:
				average = self.__normalizer(average)

			
			self.wordnetSynsets[syn]['weights'] = list(average)
			
	def run(self, ctxData, norm, coeff):
		self.ctxData = ctxData
		self.__parse()
		self.__score(norm, coeff)

		return self.wordnetSynsets





		