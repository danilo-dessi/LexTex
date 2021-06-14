import os
from bs4 import BeautifulSoup
import random


# ABSA-15_Laptops_Train_Data.xml
# ABSA15_Laptops_Test.xml

file = 'ABSA15_Laptops_Test.xml'
content = open(file, 'r', errors='ignore').read()
soup = BeautifulSoup(content,'html.parser')
#print(soup)
elements = soup.find_all('review')


all_categories = set()
texts = []
texts_categories = []


for e in elements:
	text = ''
	text_opinions = []

	sentences = e.find_all('sentences')
	for sentences_element in sentences:
		sentences_list = sentences_element.find_all('sentence')
		for sentence in sentences_list:
			text += ' ' + str(sentence.text).strip()

	try:
		opinions = e.find_all('opinions')
		for o in opinions:
			opinions_list = o.find_all('opinion')
			for opinion in opinions_list:
				#print(opinion['category'])
				if opinion['category'].startswith('LAPTOP'):
					text_opinions += [opinion['category']]
					all_categories.add(opinion['category'])
	except:
		print('err')
		pass

	texts += [text]
	texts_categories += [text_opinions]



all_categories = list(all_categories)

with open('absa15_test.txt', 'w+') as f:
	f.write('text\t' + '\t'.join(all_categories) + '\n')
	for i in range(len(texts)) :
		f.write(texts[i])
		for c in all_categories:
			if c in texts_categories[i]:
				f.write('\t' + str(1.0))
			else:
				f.write('\t' + str(0.0))
		f.write('\n')











