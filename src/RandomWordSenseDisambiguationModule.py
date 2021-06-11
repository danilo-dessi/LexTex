#!/bin/sh

import os
import subprocess
import datetime
import random


class WordSenseDisambiguationModule:

    def __init__(self):
        self.word2synsets = {}



    def __loadAllSynsets(self):
        with open('../ukb-3.1/scripts/wn30_dict.txt', 'r') as f:
            rows = f.readlines()

            for row in rows:
                word = row.strip().split(' ')[0]
                syns = row.strip().split(' ')[1:]
                self.word2synsets[word] = [syn.split(':')[1] for syn in syns]


    def run(self, mode):
        self.__loadAllSynsets()

        print('# Random Disambiguation Module is running')
        files = os.listdir('./workdir/')
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            fileext = os.path.splitext(os.path.basename(file))[1]
            print('-', str(datetime.datetime.now()), file)
            if fileext == '.sent':
                f = open( './workdir/' + file, 'r')
                fo = open('./workdir/ukb_' + file, "w")

                rows = f.readlines()
                for i in range(0, len(rows), 2):
                    ctx = rows[i].strip()
                    values = rows[i + 1].strip().split(' ')
                    
                    for value in values:
                        e = value.split('#')
                        if e[0] in self.word2synsets:
                            fo.write(ctx + ' ')
                            fo.write(e[2] + ' ' + random.choice(self.word2synsets[e[0]]) + ' !! ' + e[0] + '\n')
                            print(e[2] + ' ' + random.choice(self.word2synsets[e[0]]) + ' !! ' + e[0] + '\n')
                fo.flush()
                fo.close()
                f.close()  


