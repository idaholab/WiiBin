#Copyright 2020 Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED.

import shutil
import os
import sys
import subprocess
import math
import zipfile

def clearDirectories():
   if os.path.exists(programPath + 'Input'):
       shutil.rmtree(programPath + 'Input')
   if os.path.exists(programPath + 'Output'):
       shutil.rmtree(programPath + 'Output')
   if os.path.exists(programPath + 'OutputTemp'):
       shutil.rmtree(programPath + 'OutputTemp')
   os.mkdir(programPath + 'Input')
   os.mkdir(programPath + 'Output')
   os.mkdir(programPath + 'OutputTemp')
   
def getEndianess():
   inputResults = open(programPath + 'Output' + os.sep + 'Input.csv','r')
   contents = inputResults.read()
   inputResults.close()
   
   #Read last Entry (Big Endian Status bit)
   contents = contents[-2:-1]
   
   if '0' in contents:
       contents = 'Big'
   else:
       contents = 'Little'
   
   return contents

def goButtonArch(selectedFilename):
   #Clear Current PickleFiles
   modelPath = programPath + 'PickledSKLearnModels'
   models = os.listdir(modelPath)
   for model in models:
      if model.endswith(".sav"):
         os.remove(os.path.join(modelPath, model))
      
   #Unzip Selected PickledModels
   if selectedMode == 'Arch':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if selectedMode == 'Comp':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Compilers.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if selectedMode == 'Byte':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if selectedMode == 'Arch_Byte':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures_and_Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')

   #Copy file to Input Dir
   try:
      shutil.copy(selectedFilename, programPath + 'Input')
   except:
      print('Error: File Not Selected')
      exit()

   try:
      os.system('python3 GenerateByteHistogram.py a ' + programPath + 'Input' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + str(entropySpan) + ' ' + str(blockSize) + ' 0')
   except:
      os.system('python GenerateByteHistogram.py a ' + programPath + 'Input' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + str(entropySpan) + ' ' + str(blockSize) + ' 0')
      
   results = open(programPath + 'Output' + os.sep + 'Results.txt','r')
   contents = results.read()
   
   #Set Endianess GUI Box
   endiannessOutput = getEndianess()
   
   return endiannessOutput, 'Type	Probability	Algorthim\n------------------------------------------\n' + contents

def goButtonData(selectedFilename):
   #Clear Current PickleFiles
   modelPath = programPath + 'PickledSKLearnModels'
   models = os.listdir(modelPath)
   for model in models:
      if model.endswith(".sav"):
         os.remove(os.path.join(modelPath, model))
      
   #Unzip Selected PickledModels
   if selectedMode == 'Arch':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if selectedMode == 'Comp':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Compilers.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if selectedMode == 'Byte':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if selectedMode == 'Arch_Byte':
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures_and_Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')

   #Copy file to Input Dir
   try:
      shutil.copy(selectedFilename, programPath + 'Input')
   except:
      print('Error: File Not Selected')
      exit()
   
   #ZeroBuffer
   zero=[0]*int((int(chunkSize)/2)-1)
   zeroBuffer=bytearray(zero)
   
   #Pad Original File with Leading and Trailing Zeros
   old = open('Input' + os.sep + selectedFilename.split(os.sep)[-1], 'rb')
   new = open('Input' + os.sep + 'temp__' + selectedFilename.split(os.sep)[-1], 'wb')
   new.write(zeroBuffer)
   new.write(old.read())
   new.write(zeroBuffer)
   old.close()
   new.close()
   os.remove('Input' + os.sep + selectedFilename.split(os.sep)[-1])
   os.rename('Input' + os.sep + 'temp__' + selectedFilename.split(os.sep)[-1], 'Input' + os.sep + selectedFilename.split(os.sep)[-1])

   #Split File Via Rolling Window
   try:
      os.system('python3 RollingWindowExtractor.py ' + programPath + 'Input' + os.sep + ' ' + programPath + 'OutputTemp' + os.sep + ' ' + str(chunkSize) + ' ' + str(slidePercentage))

      os.system('python3 GenerateByteHistogram.py d ' + programPath + 'OutputTemp' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + str(entropySpan) + ' ' + str(blockSize) + ' ' + str(requiredVotes))
   except:
      os.system('python RollingWindowExtractor.py ' + programPath + 'Input' + os.sep + ' ' + programPath + 'OutputTemp' + os.sep + ' ' + str(chunkSize) + ' ' + str(slidePercentage))

      os.system('python GenerateByteHistogram.py d ' + programPath + 'OutputTemp' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + str(entropySpan) + ' ' + str(blockSize) + ' ' + str(requiredVotes))
   
   results = open(programPath + 'Output' + os.sep + 'Results.txt','r')
   contents = results.readlines()

   #Convert to list
   finalList = []
   for i in range(0,len(contents)):
      finalList.append(str(contents[i].rstrip('\n')))

   #Generate final String
   finalString = 'File\tByte Offset\tAgreement\n'\
                 + '-------------------------------------------------------\n'
   for i in range(0,len(finalList)):
      finalString = finalString + str(int(finalList[i].split(',')[0])+1) + '\t' + str(math.trunc((int(finalList[i].split(',')[0]))*(int(chunkSize)*(int(slidePercentage)/100)))).zfill(7) + '\t\t' +  str(finalList[i].split(',')[1]) + '\n'
      
   if len(finalList) == 0:
   	finalString = 'No Data Offset Matches Found'

   return 'N/A', finalString
   

def entropyPercentage(passedFile):
   upperLimit = entropySpan.split(':')[0]
   fileSize = os.path.getsize(passedFile)

   entropy = subprocess.check_output(['binwalk', '-E', '-v', '--block=' + str(blockSize), '--nplot', passedFile]).split()
   entropy = entropy[entropy.index(b'ENTROPY')+2:len(entropy)]
   del entropy[1::3]

   #Loop through Binwalk elements to decode them
   for index in range(0,len(entropy)):
      entropy[index] = entropy[index].decode()

   entropy.append(str(fileSize))

   byteTotal = 0
   for index in range(1,len(entropy),2):
      if float(entropy[index]) > float(upperLimit):
         byteTotal = byteTotal + (float(entropy[index+1])-float(entropy[index-1]))

   percentage = str(round((byteTotal / fileSize) * 100, 2)) + '%'
   return percentage

#---------------------------------------------------------------------------------
programPath = '.' + os.sep

try:
   inputFilepath = sys.argv[1]
except:
   print('Usage: python3 WiiBinCLI.py <Full Filepath> <Entropy Span> <Block Size> <Chunk Size> <Required Votes out of 8> <Mode> <Slide Percentage> <Function>')
   print('Example: python3 WiiBinCLI.py /bin/bash 0.9:0.1 512 10000 5 Arch 50 Type')
   print('Mode: Arch, Comp, Byte, Arch_Byte')
   print('Function: Type, Offset')
   print('WiiBin 1.8')
   exit()
   
try:
   entropySpan = sys.argv[2]
except:
   entropySpan = '0.9:0.1'
   
try:
   blockSize = sys.argv[3]
except:
   blockSize = 512
   
try:
   chunkSize = sys.argv[4]
except:
   chunckSize = 10000
   
try:
   requiredVotes = sys.argv[5]
except:
   requiredVotes = 5
   
try:
   selectedMode = sys.argv[6]
except:
   selectedMode = 'Arch'
   
try:
   slidePercentage = sys.argv[7]
except:
   slidePercentage = 50
   
try:
   selectedFunction = sys.argv[8]
except:
   selectedFunction = 'Type' 
   

endiannessOutput = ''
compressedEncryptedOutput = ''
mainOutput = ''
   
#Check for Zero size files
while os.path.getsize(inputFilepath) <= 0:
   print("Zero-byte file detected. Please select a different file.")
   exit()

clearDirectories()

if selectedFunction == 'Type':
   endiannessOutput, mainOutput = goButtonArch(inputFilepath)
else:
   endiannessOutput, mainOutput = goButtonData(inputFilepath)
   
#Check Entropy Percentage
compressedEncryptedOutput = entropyPercentage(inputFilepath)

OutputString = "Compressed/Encrypted Percentage: " + compressedEncryptedOutput + '\n\n' + "Endianness: " + endiannessOutput + '\n\n' + mainOutput

fileOutput = open(inputFilepath.split(os.sep)[-1] + '.result.txt', 'w')
fileOutput.write(OutputString)
fileOutput.close()

print()
print(OutputString)
