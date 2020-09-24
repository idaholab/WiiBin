#Copyright 2020 Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED.

#python RollingWindowSplitPortionExtractor.py <Input Directory> <Output Directory> <Chunk Size in Bytes>

import subprocess
import sys
import glob
import random
import os

CGREEN = '\033[92m'
CRED = '\033[91m'
CEND = '\033[0m'

try:
    binaries = glob.glob(sys.argv[1] + '*')
except:
    print('Argument Error')
    sys.exit()

try:
    outPath = sys.argv[2]
except:
    print('Argument Error')
    sys.exit()
if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

try:
    chunkSize = int(sys.argv[3])
except:
    print('Argument Error')
    sys.exit()

print(CGREEN + 'Chunking File into ' + str(chunkSize) + 'byte' + ' Pieces' + CEND)

count = 1
totalBinaries = len(binaries)
totalBytes = 0


for i in binaries:
    print(CGREEN + '\n(' + str(count) + '/' + str(totalBinaries) + ')' + CEND)
    totalBytes = os.path.getsize(i)
    currentByte = 0

    while currentByte < totalBytes:
        subprocess.call('dd if=' + str(i) + ' of=' + outPath + str(i.split(os.sep)[-1]) + '__bytes-'+ str(chunkSize) +'__offset-'+ str(currentByte).zfill(8) +' skip=' + str(currentByte) + ' count=' + str(chunkSize) + ' iflag=skip_bytes,count_bytes', shell=True)
        
        currentByte = int(currentByte + chunkSize/2)

    count = count + 1

print(CGREEN + '----------- All Completed -------------' + CEND)
