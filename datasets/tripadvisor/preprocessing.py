import os
import json
import ast
import math

sentences = {}
aspects = ['service', 'location', 'cleanliness', 'business']

for file in os.listdir('data'):
	with open('data/' + file, 'r') as f:
		lines = f.readlines()

		for line in lines:
			content = ast.literal_eval(line)
			for segment in content['segments']:
				sentences[segment] = {'service' : content['ratingService']}
				sentences[segment]['location'] = content['ratingLocation']
				sentences[segment]['cleanliness'] = content['ratingCleanliness']
				sentences[segment]['business'] = content['ratingBusiness']
				#sentences[segment]['overall'] = content['ratingOverall']

sentences_number =  len(sentences.keys())
print('Number of sentences: ', sentences_number)
train_number  = math.ceil((sentences_number / 100) * 80)
print('Number of sentences for train:', train_number)
test_number  = sentences_number - train_number
print('Number of sentences for test:', test_number)

c = 0
with open('tripadvisor_train.txt', 'w+') as f_train:
	with open('tripadvisor_test.txt', 'w+') as f_test:
		f_train.write('text\t' + '\t'.join(aspects) + '\n')
		f_test.write('text\t' + '\t'.join(aspects) + '\n')
		for sentence in sentences:
			out = sentence

			for aspect in aspects:
				out += '\t' + str(max(0.0, float(sentences[sentence][aspect]) / 5.0))
			out += '\n'

			if c < train_number:
				f_train.write(out)
				c += 1
			else:
				f_test.write(out)




