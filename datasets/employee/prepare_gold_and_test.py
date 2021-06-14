#This file will be not useful with new execution 

import os
import csv

with open('employee_test_gold.txt', 'r') as fr:
	with open('employee_test.txt', 'w+') as f:
		lines = fr.readlines()
		c = 0
		for row in lines:	
			f.write(row.split('\t')[0] + '\n')

