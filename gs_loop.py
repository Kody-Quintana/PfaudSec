# For fixing corrupted PDFs
# Integrate into main.py later

import time
import os
import shutil
import subprocess


def folder_check(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

def ghostscript(path):
    orig_list = []
    rep_list = []
    length = -1
    for root, dirs, files in os.walk(path):
        for k, i in enumerate(files):
            if i.endswith('.pdf'):
                print(root + '/' + i)
                folder_check(root + '/repair/')
                p = subprocess.Popen(['gs',
                    '-sOutputFile="' + str(root + '/repair/' + i + '"'),
                    '-sDEVICE=pdfwrite',
                    '-dPDFSETTINGS=/prepress',
                    '-dBatch',
                    '-dNOPAUSE',
                    '-dQUIET',
                    '"' + str(root + '/' + i) + '"'],
                    stdin=subprocess.PIPE)
                orig_list.append(root + '/' + i)
                rep_list.append(root + '/repair/' + i)
                length = length + 1

                p.communicate()
                p.wait()
                shutil.copy(root + '/repair/' + i, root + '/' + i)
    print('Done.\n' + str(length) + ' converted')


ghostscript('/home/user/PfaudSec/test_work_dir_')
