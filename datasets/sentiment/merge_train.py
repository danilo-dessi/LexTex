import os

with open('sentiment_train.txt', 'w+') as fw:
	fw.write('text\tanger\tfear\tjoy\tsadness\tsurprise\n')
	for file in os.listdir('original_train/'):
		print(file)
		with open('original_train/' + file) as fr:
			rows = fr.readlines()
			for row in rows:
				fw.write(row.strip() + '\n')