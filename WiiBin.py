#Copyright 2020 Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED.

#Buffered File with 0x00's
#Offset measured from center of chunk
#Adjustable slide %
#Added .Net Bytecode
#Added startup Notes
#Additional Error checking
#Added DotNet Bytecode
#Added Compiler Detection
#Added Percent Compressed or Encrypted

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
import sys
import subprocess
import math
import zipfile

programPath = '.' + os.sep
selectedFilename = ''

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

def goButtonArch():
   #Clear resultsbox
   resultsBox.delete(1.0, END)
   
   #Check if Arch or Compiler Radio Button Selected
   if radioValue.get() == 0:
      resultsBox.insert(END, 'Radio Button Not Selected')
      return None
      
   #Clear Current PickleFiles
   modelPath = programPath + 'PickledSKLearnModels'
   models = os.listdir(modelPath)
   for model in models:
      if model.endswith(".sav"):
         os.remove(os.path.join(modelPath, model))
      
   #Unzip Selected PickledModels
   if radioValue.get() == 1:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if radioValue.get() == 2:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Compilers.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if radioValue.get() == 3:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if radioValue.get() == 4:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures_and_Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')


   #Copy file to Input Dir
   global selectedFilename
   try:
      shutil.copy(selectedFilename, programPath + 'Input')
   except:
      resultsBox.insert(END, 'File not selected. Select a file and try again.')
      return None

   try:
      os.system('python3 GenerateByteHistogram.py a ' + programPath + 'Input' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' 0')
   except:
      os.system('python GenerateByteHistogram.py a ' + programPath + 'Input' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' 0')
      
   results = open(programPath + 'Output' + os.sep + 'Results.txt','r')
   contents = results.read()
   
   header = 'Type\tProbability\t\tAlgorthim\n------------------------------------------\n'

   resultsBox.insert(END,header + contents)
   
   #Set Endianess GUI Box
   endianLabelText.set(getEndianess())
   
   clearDirectories()

def goButtonData():
   #Clear resultsbox
   resultsBox.delete(1.0, END)

   #Check if Arch or Compiler Radio Button Selected
   if radioValue.get() == 0:
      resultsBox.insert(END, 'Radio Button Not Selected')
      return None

   #Clear Current PickleFiles
   modelPath = programPath + 'PickledSKLearnModels'
   models = os.listdir(modelPath)
   for model in models:
      if model.endswith(".sav"):
         os.remove(os.path.join(modelPath, model))
      
   #Unzip Selected PickledModels
   if radioValue.get() == 1:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if radioValue.get() == 2:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Compilers.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if radioValue.get() == 3:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')
   if radioValue.get() == 4:
      zip = zipfile.ZipFile(programPath + 'PickledSKLearnModels' + os.sep + 'Architectures_and_Bytecode.zip')
      zip.extractall(programPath + 'PickledSKLearnModels')

   #Copy file to Input Dir
   global selectedFilename
   try:
      shutil.copy(selectedFilename, programPath + 'Input')
   except:
      resultsBox.insert(END, 'File not selected. Select a file and try again.')
      return None
   
   #ZeroBuffer
   zero=[0]*int((int(chunkEntryText.get())/2)-1)
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
      os.system('python3 RollingWindowExtractor.py ' + programPath + 'Input' + os.sep + ' ' + programPath + 'OutputTemp' + os.sep + ' ' + chunkEntryText.get() + ' ' + slideEntryText.get())

      os.system('python3 GenerateByteHistogram.py d ' + programPath + 'OutputTemp' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' ' + votesEntryText.get())
   except:
      os.system('python RollingWindowExtractor.py ' + programPath + 'Input' + os.sep + ' ' + programPath + 'OutputTemp' + os.sep + ' ' + chunkEntryText.get() + ' ' + slideEntryText.get())

      os.system('python GenerateByteHistogram.py d ' + programPath + 'OutputTemp' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' ' + votesEntryText.get())
   
   results = open(programPath + 'Output' + os.sep + 'Results.txt','r')
   contents = results.readlines()

   #Convert to list
   finalList = []
   for i in range(0,len(contents)):
      finalList.append(str(contents[i].rstrip('\n')))

   #Generate final String
   finalString = 'File\tByte Offset\t\tAgreement\n'\
                 + '-------------------------------------------------------\n'
   for i in range(0,len(finalList)):
      finalString = finalString + str(int(finalList[i].split(',')[0])+1) + '\t' + str(math.trunc((int(finalList[i].split(',')[0]))*(int(chunkEntryText.get())*(int(slideEntryText.get())/100)))).zfill(7) + '\t\t' +  str(finalList[i].split(',')[1]) + '\n'
      
   if len(finalList) == 0:
   	finalString = 'No Data Offset Matches Found'

   resultsBox.insert(END,finalString)
   
   #Set Endianess GUI Box
   endianLabelText.set('<????>')
   
   clearDirectories()

def entropyPercentage(passedFile):
   upperLimit = entropyEntryText.get().split(':')[0]
   fileSize = os.path.getsize(passedFile)

   entropy = subprocess.check_output(['binwalk', '-E', '-v', '--block=' + str(blocksizeEntryText.get()), '--nplot', passedFile]).split()
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


def fileSelectButton():
   global selectedFilename
   fileSelectedLabelText.set('Loading Selected File...')
   selectedFilename =  filedialog.askopenfilename(initialdir = programPath,title = "Select Binary")
   
   #Check for Zero size files
   ##############################################
   while os.path.getsize(selectedFilename) <= 0:
       print("Zero-byte file detected. Please select a different file.")
       selectedFilename =  filedialog.askopenfilename(initialdir = programPath,title = "Select Binary")
   
   #Check Entropy Percentage
   entropyPercent = entropyPercentage(selectedFilename)
   percentLabelText.set(entropyPercent)
   fileSelectedLabelText.set(selectedFilename)
   
   entropyNumber = float(entropyPercent.split('%')[0])
   
   if entropyNumber >= 66:
      percentLabel.config(fg="red")
      messagebox.showwarning("Entropy Warning", "Warning: Selected Binary is " + str(entropyPercent) + " Compressed or Encrypted.  WiiBin Results Should Not Be Trusted.")
   elif entropyNumber >= 33:
      percentLabel.config(fg="orange")
      messagebox.showwarning("Entropy Warning", "Warning: Selected Binary is " + str(entropyPercent) + " Compressed or Encrypted.  WiiBin Results Might Not Be Reliable.")
   elif entropyNumber >= 0:
      percentLabel.config(fg="green")

def entropyLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"The window of entropy that will be considered when generating byte histograms.  Anything outside of that window will be ignored. Syntax=Max:Min")

def blocksizeLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"The size of individual block (in bytes) considered during entropy analysis. Default=512")
   
def chunksizeLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"The size of chunk in bytes that the data offset process will break the inputed file into. Default=10000")
   
def slidesizeLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"The percent of the chunk size that the sliding window is slid Default=50")

def reqVotesLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"Number of ML algorithms that must agree on an file for it to be reported as part of the data offset output. Default=5 (Simple Majority)")
   
def radioArchSelected():
   entropyEntryText.set('0.9:0.1')
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"Mode Changed to Architecture")
   
def radioCompSelected():
   entropyEntryText.set('1.0:0.0')
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"Mode Changed to Compiler")
   
def radioByteSelected():
   entropyEntryText.set('0.9:0.1')
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"Mode Changed to Bytecode")
   
def radioArchByteSelected():
   entropyEntryText.set('0.9:0.1')
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"Mode Changed to Architecture & Bytecode")
   

#############Initialization###################
root = Tk()
root.configure(width=40)
root.title("WiiBin")
root.geometry("655x390")
root.resizable(0, 0)

radioValue = IntVar()

buttonText = StringVar()
buttonText.set('Select File...')
fileSelectButton = Button(root, textvariable=buttonText, command=fileSelectButton)
fileSelectButton.place(x=10,y=10)

fileSelectedLabelText = StringVar()
fileSelectedLabel = Entry(root,textvariable=fileSelectedLabelText,bd=0,bg='#D9D9D9',width=62)
fileSelectedLabel.place(x=130,y=15)
fileSelectedLabelText.set('<File Path>')

entropyLabel = Label(root,text='Entropy Span:')
entropyLabel.place(x=10,y=45)
entropyLabel.bind("<Button>", entropyLabelClicked)

entropyEntryText = StringVar()
entropyEntry = Entry(root,width=7,textvariable=entropyEntryText)
entropyEntry.place(x=108,y=45)
entropyEntryText.set('0.9:0.1')

blocksizeLabel = Label(root,text='Block Size (b):')
blocksizeLabel.place(x=180,y=45)
blocksizeLabel.bind("<Button>", blocksizeLabelClicked)

blocksizeEntryText = StringVar()
blocksizeEntry = Entry(root,width=4,textvariable=blocksizeEntryText)
blocksizeEntry.place(x=279,y=45)
blocksizeEntryText.set('512')

chunkLabel = Label(root,text='Chunk Size (b):')
chunkLabel.place(x=330,y=45)
chunkLabel.bind("<Button>", chunksizeLabelClicked)

chunkEntryText = StringVar()
chunkEntry = Entry(root,width=6,textvariable=chunkEntryText)
chunkEntry.place(x=434,y=45)
chunkEntryText.set('10000')

slideLabel = Label(root,text='Slide (%):')
slideLabel.place(x=520,y=70)
slideLabel.bind("<Button>", slidesizeLabelClicked)

slideEntryText = StringVar()
slideEntry = Entry(root,width=3,textvariable=slideEntryText)
slideEntry.place(x=590,y=70)
slideEntryText.set('50')

votesLabel = Label(root,text='Req\'d Votes:        of 8')
votesLabel.place(x=500,y=45)
votesLabel.bind("<Button>", reqVotesLabelClicked)

votesEntryText = StringVar()
votesEntry = Entry(root,width=2,textvariable=votesEntryText)
votesEntry.place(x=590,y=45)
votesEntryText.set('5')

goButtonArch = Button(root,text="Determine Type",command=goButtonArch)
goButtonArch.place(x=10,y=75)

goButtonData = Button(root,text="Determine Offsets",command=goButtonData)
goButtonData.place(x=145,y=75)

radioButtonArch = Radiobutton(root, text="Architecture", variable=radioValue, value=1, command=radioArchSelected)
radioButtonArch.place(x=292,y=68)
radioButtonByte = Radiobutton(root, text="Bytecode", variable=radioValue, value=3, command=radioByteSelected)
radioButtonByte.place(x=292,y=90)
radioButtonComp = Radiobutton(root, text="Compiler", variable=radioValue, value=2, command=radioCompSelected)
radioButtonComp.place(x=400,y=68)
radioButtonArchByte = Radiobutton(root, text="Arch&Byte", variable=radioValue, value=4, command=radioArchByteSelected)
radioButtonArchByte.place(x=400,y=90)

endianLabel = Label(root,text='Endianness:', justify=RIGHT)
endianLabel.place(x=500,y=93)

endianLabelText = StringVar()
endianLabel = Label(root,width=7,textvariable=endianLabelText)
endianLabel.place(x=580,y=93)
endianLabelText.set('<????>')

percentLabel = Label(root,text='Percent Compressed/Encrypted:', justify=RIGHT)
percentLabel.place(x=370,y=112)

percentLabelText = StringVar()
percentLabel = Label(root,width=7,textvariable=percentLabelText)
percentLabel.place(x=580,y=112)
percentLabelText.set('<????>')

resultsBox = Text(root, width=75, height=14, padx=5, pady=5, borderwidth=2, relief=RIDGE)
resultsBox.place(x=10, y= 130)

scrollb = Scrollbar(root, command=resultsBox.yview)
scrollb.place(x=630, y=350)
resultsBox['yscrollcommand'] = scrollb.set

resultsBox.insert(END,'Welcome to WiiBin 1.7.1\n----------------------\n\nNotes:\n\nThe smaller the Slide (%) and Chunk Size, the more accurate the detection and longer the runtime.\n\nToo small a Chuck Size will cause make ML difficult and less accurate.\n\nThe minimum detectable code segment size is limited to half of the selected Chunk Size.\n\nTo detect smaller code segments the Chunk Size most be reduced.')

clearDirectories()

root.mainloop()

