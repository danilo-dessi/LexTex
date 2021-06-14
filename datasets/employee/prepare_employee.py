import os
import random
import csv


categories = ['work-balance-stars', 'culture-values-stars', 'carrer-opportunities-stars', 'comp-benefit-stars', 'senior-mangemnet-stars']
textualElements = ['summary', 'pros', 'cons']

id2values = {}

with open('employee_reviews.csv') as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter=',')
	headers = next(csv_reader, None)
	c = 0
	for row in csv_reader:

		hold = True
		for category in categories:
			if row[category] == 'none':
				hold = False

		if hold:
			id2values[c] = {}
			text = ' '.join([row[textualElement]  for textualElement in textualElements ])
			id2values[c]['text'] = text
			for category in categories:
				id2values[c][category] = float(row[category]) / 5.0
			c += 1

		

keys = list(id2values.keys())
random.shuffle(keys)
testNumber = int(len(keys) * 0.1)
keys_test = keys[0:testNumber]
keys_train = keys[testNumber:]

#print info
print('Test size:', len(keys_test))
print('Train size:', len(keys_train))

with open('employee_train.txt', 'w+') as f:
	f.write('text\t' + '\t'.join(categories) + '\n')
	for id in keys_train:
		f.write(id2values[id]['text'])
		for category in categories:
			f.write('\t' + str(id2values[id][category]))
		f.write('\n')

with open('employee_test_gold.txt', 'w+') as f:
	f.write('text\t' + '\t'.join(categories) + '\n')
	for id in keys_test:
		f.write(id2values[id]['text'])
		for category in categories:
			f.write('\t' + str(id2values[id][category]))
		f.write('\n')

with open('employee_test.txt', 'w+') as f:
	f.write('text\t' + '\n')
	for id in keys_test:
		f.write(id2values[id]['text'])
		f.write('\n')