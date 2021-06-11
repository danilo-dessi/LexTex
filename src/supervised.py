import sklearn
import os
import datetime
import sys
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeRegressor	
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import numpy as np

class Supervised:
	def __init__(self):
		self.trainLocation = ''
		self.testLocation = ''
		self.trainTexts = []
		self.trainScores = []
		self.testTexts = []
		self.header = []

	def load(self, trainLocation, testLocation):
		self.trainLocation = trainLocation
		self.testLocation = testLocation

		with open(trainLocation, 'r') as f:
			rows = f.readlines()
			c = 0
			for row in rows:
				try:
					if c == 0:
						self.header = row
						c += 1
						continue
					c += 1
					values = row.strip().split('\t')
					self.trainScores += [[float(v) for v in values[1:]]]
					self.trainTexts += [values[0]]

				except:
					pass
			
		

		with open(testLocation, 'r') as f:
			rows = f.readlines()
			c = 0
			for row in rows:
				if c == 0:
					c += 1
					continue
				values = row.strip().split('\t')
				self.testTexts += [values[0]]


	def trainModel(self):

		vectorizer = TfidfVectorizer()
		tfidf = vectorizer.fit_transform(self.trainTexts + self.testTexts)
		X_train = tfidf[:len(self.trainTexts)]
		X_test = tfidf[len(self.trainTexts):]
		print(tfidf.shape)
		print(X_train.shape)
		print(X_test.shape)
		
		
		clf = SVR( C=1.0, epsilon=0.2, verbose=True)
		#clf = DecisionTreeRegressor(max_depth=10)
		#clf = RandomForestRegressor(max_depth=10)

		n_categories = len(self.trainScores[0])	
		result = {}

		print('Number of categories:', n_categories)

		for c in range(n_categories):
			print(datetime.datetime.now(), 'Training on category:', c)
			y = [v[c] for v in self.trainScores]
			clf.fit(X_train, y) 
			print(datetime.datetime.now(), 'Predicting on category:', c)
			y_pred = clf.predict(X_test)
			result[c] = y_pred


		out = os.path.basename(self.testLocation)
		with open('../results-supervised/supervised_svr_' + out, 'w+') as f:
			f.write(self.header)

			for i in range(len(self.testTexts)):
				f.write(self.testTexts[i] + '\t')

				values = []
				for c in range(n_categories):
					values += [result[c][i]]
				s = sum(values)
				normValues = [str(v / s) for v in values]

				f.write('\t'.join(normValues))
				f.write('\n')



if __name__ == '__main__':
    print('START:', str(datetime.datetime.now()))
    s = Supervised()
    s.load(sys.argv[1], sys.argv[2])
    s.trainModel()
    print('END:', str(datetime.datetime.now()))


