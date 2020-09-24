#Copyright 2020 Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED.

#python GenerateTrainingDataCSV.py <Input Directory> <Output Directory> | <Max:Min Entropy>

import os
import sys

try:
   inputDir = sys.argv[1]
   outputDir = sys.argv[2]
   entropyFilter = sys.argv[3]
except:
   print('Argument Error')
   sys.exit()

os.system('python GenerateByteHistogram.py n ' + inputDir + ' ' + outputDir + ' 0 100000000000000000000 ' + entropyFilter + ' 512')

print('Done')
print('Training Data is csv format is located ' + outputDir)

