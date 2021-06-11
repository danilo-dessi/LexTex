import os

doc = {}
for file in os.listdir('gold/'):
	with open('gold/' + file, 'r') as f:
		lines = f.readlines()
		for line in lines:
			#print(line)
			id = line.strip().split('\t')[0]

			if 'mystery' not in id:
				text = line.strip().split('\t')[1]
				category = line.strip().split('\t')[2]
				category_score = line.strip().split('\t')[3]

				if id not in doc:
					doc[id] = {}
				doc[id]['text'] = text
				doc[id][category] = category_score
			



with open('gold.txt', 'w') as f_gold:
	with open('plain.txt', 'w') as f_plain:
		f_gold.write('Text\tanger\tfear\tjoy\tsadness\n')
		f_plain.write('Text\n')
		for id in doc:
			line = ''
			for c in ['anger', 'fear', 'joy', 'sadness']:
				if c in doc[id]:
					line += str(doc[id][c]) + '\t'
				else:
					line += '0.0\t'
			f_gold.write(doc[id]['text'] + '\t' + line + '\n')
			f_plain.write(doc[id]['text'] + '\n')






