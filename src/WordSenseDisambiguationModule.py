#!/bin/sh

import os
import subprocess
import datetime


class WordSenseDisambiguationModule:

    def run(self, mode):
        print('# Disambiguation Module is running')
        files = os.listdir('./workdir/')
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            fileext = os.path.splitext(os.path.basename(file))[1]
            print('-', str(datetime.datetime.now()), file)
            if fileext == '.sent':
                ukb_wsd_command = ['../ukb-3.1/bin/ukb_wsd', '--' + mode, '-K', '../ukb-3.1/scripts/wn30g.bin', '-D', '../ukb-3.1/scripts/wn30_dict.txt', './workdir/' + file]
                fo = open('./workdir/ukb_' + file, "wb")
                subprocess.call(ukb_wsd_command, stdout=fo)
                fo.flush()
                fo.close()
            elif fileext == '.word':
                ukb_wsd_command = ['../ukb-3.1/bin/ukb_wsd', '--ppr', '-K', '../ukb-3.1/scripts/wn30g.bin', '-D', '../ukb-3.1/scripts/wn30_dict.txt', './workdir/' + file]
                fo = open('./workdir/ukb_' + file, "wb")
                subprocess.call(ukb_wsd_command, stdout=fo)
                fo.flush()
                fo.close()
        print('# Disambiguation Module finished')



