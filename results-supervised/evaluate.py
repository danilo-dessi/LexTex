import sys
import scipy.stats


gold_file = sys.argv[1]
pred_file_task_1 = sys.argv[2]
#pred_file_task_2 = sys.argv[3]

header = True
header_values = []
gold_scores = {}
with open(gold_file, 'r') as f_gold:
	lines = f_gold.readlines()

	for line in lines:
		if header:
			header = False
			header_values = line.strip().split('\t')[1:]
			continue
		values = line.strip().split('\t')[1:]
		for i in range(len(header_values)):
			if i not in gold_scores:
				gold_scores[i] = []
			gold_scores[i] += [float(values[i])]


header = True
pred_scores_task_1 = {}
with open(pred_file_task_1, 'r') as f_pred:
	lines = f_pred.readlines()

	for line in lines:
		if header:
			header = False
			continue
		values = line.strip().split('\t')[1:]
		for i in range(len(header_values)):
			if i not in pred_scores_task_1:
				pred_scores_task_1[i] = []
			pred_scores_task_1[i] += [float(values[i])]


'''header = True
pred_scores_task_2 = {}
with open(pred_file_task_2, 'r') as f_pred:
	lines = f_pred.readlines()

	for line in lines:
		if header:
			header = False
			continue
		values = line.strip().split('\t')[1:]
		for i in range(len(header_values)):
			if i not in pred_scores_task_2:
				pred_scores_task_2[i] = []
			pred_scores_task_2[i] += [float(values[i])]'''

#print('\nEvaluation on Task 1: given a text compute a score for each emotion')
for i in range(len(header_values)):
	#given a text, computing a score for each emotion
	pearson = scipy.stats.pearsonr(pred_scores_task_1[i],gold_scores[i])[0]
	print('#', header_values[i] + ':', pearson)

'''print('\nEvaluation on Task 2: given a text and an emotion, compute the score for that emotion. ')
for i in range(len(header_values)):
	#given a text and an emotion that we know that that text has (i.e in the gold the score is greater than 0, computing a score for each emotion
	pred_scores_plus = []
	gold_scores_plus = []

	for j in range(len(gold_scores[i])):
		#print(len(gold_scores[i]), len(pred_scores_indipendent[i]))
		if gold_scores[i][j] > 0:
			gold_scores_plus += [gold_scores[i][j]]
			pred_scores_plus += [pred_scores_task_2[i][j]]

	pearson = scipy.stats.pearsonr(pred_scores_plus, gold_scores_plus)[0]
	print('#', header_values[i] + ':', pearson)
'''
	






