#Copyright 2020 Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED.

from tkinter import *
from tkinter import filedialog
import shutil
import os
import math

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

   #Copy file to Input Dir
   global selectedFilename
   shutil.copy(selectedFilename, programPath + 'Input')

   try:
      os.system('python3 GenerateByteHistogram.py a ' + programPath + 'Input' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' 0')
   except:
      os.system('python GenerateByteHistogram.py a ' + programPath + 'Input' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' 0')
      
   results = open(programPath + 'Output' + os.sep + 'Results.txt','r')
   contents = results.read()
   
   header = 'Arch\tProbability\t\tAlgorthim\n------------------------------------------\n'

   resultsBox.insert(END,header + contents)
   
   #Set Endianess GUI Box
   endianLabelText.set(getEndianess())
   
   clearDirectories()

def goButtonData():
   #Clear resultsbox
   resultsBox.delete(1.0, END)

   #Copy file to Input Dir
   global selectedFilename
   shutil.copy(selectedFilename, programPath + 'Input')

   #Split File Via Rolling Window
   try:
      os.system('python3 RollingWindowExtractor.py ' + programPath + 'Input' + os.sep + ' ' + programPath + 'OutputTemp' + os.sep + ' ' + chunkEntryText.get())

      os.system('python3 GenerateByteHistogram.py d ' + programPath + 'OutputTemp' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' ' + votesEntryText.get())
   except:
      os.system('python RollingWindowExtractor.py ' + programPath + 'Input' + os.sep + ' ' + programPath + 'OutputTemp' + os.sep + ' ' + chunkEntryText.get())

      os.system('python GenerateByteHistogram.py d ' + programPath + 'OutputTemp' + os.sep + ' ' + programPath + 'Output' + os.sep + ' 0 100000000000000000000 ' + entropyEntryText.get() + ' ' + blocksizeEntryText.get() + ' ' + votesEntryText.get())
   
   results = open(programPath + 'Output' + os.sep + 'Results.txt','r')
   contents = results.readlines()

   #Convert to list
   finalList = []
   for i in range(0,len(contents)):
      finalList.append(str(contents[i].rstrip('\n')))

   #Generate final String
   finalString = 'File\tByte Offset\t\t\tArchitecture Agreement\n'\
                 + '-------------------------------------------------------\n'
   for i in range(0,len(finalList)):
      finalString = finalString + str(int(finalList[i].split(',')[0])+1) + '\t' + str(math.trunc((int(finalList[i].split(',')[0]))*(int(chunkEntryText.get())/2))).zfill(7) + '-' + str(math.trunc((int(finalList[i].split(',')[0]))*(int(chunkEntryText.get())/2))+int(chunkEntryText.get())).zfill(7)  + '\t\t\t' +  str(finalList[i].split(',')[1]) + '\n'
      
   if len(finalList) == 0:
   	finalString = 'No Data Offset Matches Found'

   resultsBox.insert(END,finalString)
   
   #Set Endianess GUI Box
   endianLabelText.set('<????>')
   
   clearDirectories()

def fileSelectButton():
   global selectedFilename
   selectedFilename =  filedialog.askopenfilename(initialdir = programPath,title = "Select file")
   fileSelectedLabelText.set(selectedFilename)


def entropyLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"The window of entropy that will be considered when generating byte histograms.  Anything outside of that window will be ignored. Syntax=Max:Min  Default=0.9:0.1")

def blocksizeLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"The size of individual block (in bytes) considered during entropy analysis. Default=512")
   
def chunksizeLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"The size of chunk in bytes that the data offset process will break the inputed file into. (50% overlap is applied) Default=10000")

def reqVotesLabelClicked(event):
   resultsBox.delete(1.0, END)
   resultsBox.insert(END,"Number of ML algorithms that must agree on an file for it to be reported as part of the data offset output. Default=8 (Unanimous)")

#############Initialization###################
root = Tk()
root.configure(width=40)
root.title("WiiBin")
root.geometry("655x390")
root.resizable(0, 0)

fileSelectButton = Button(root,text="Select File...",command=fileSelectButton)
fileSelectButton.place(x=10,y=10)

fileSelectedLabelText = StringVar()
fileSelectedLabel = Label(root,textvariable=fileSelectedLabelText)
fileSelectedLabel.place(x=120,y=15)
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
chunkLabel.place(x=325,y=45)
chunkLabel.bind("<Button>", chunksizeLabelClicked)

chunkEntryText = StringVar()
chunkEntry = Entry(root,width=6,textvariable=chunkEntryText)
chunkEntry.place(x=434,y=45)
chunkEntryText.set('10000')

votesLabel = Label(root,text='Req\'d Votes:        of 8')
votesLabel.place(x=500,y=45)
votesLabel.bind("<Button>", reqVotesLabelClicked)

votesEntryText = StringVar()
votesEntry = Entry(root,width=2,textvariable=votesEntryText)
votesEntry.place(x=590,y=45)
votesEntryText.set('5')

goButtonArch = Button(root,text="Determine Architecture",command=goButtonArch)
goButtonArch.place(x=10,y=75)

goButtonData = Button(root,text="Determine Data Offsets",command=goButtonData)
goButtonData.place(x=200,y=75)

endianLabel = Label(root,text='Endianess:', justify=RIGHT)
endianLabel.place(x=480,y=80)

endianLabelText = StringVar()
endianLabel = Label(root,width=7,textvariable=endianLabelText)
endianLabel.place(x=560,y=80)
endianLabelText.set('<????>')

resultsBox = Text(root, width=75, height=15, padx=5, pady=5, borderwidth=2, relief=RIDGE)
resultsBox.place(x=10, y= 110)

scrollb = Scrollbar(root, command=resultsBox.yview)
scrollb.place(x=630, y=350)
resultsBox['yscrollcommand'] = scrollb.set

clearDirectories()

root.mainloop()

