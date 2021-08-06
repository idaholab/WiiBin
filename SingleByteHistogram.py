#Copyright 2020 Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED.

#python ByteHistogram.py <Input File> <Output Directory> | <Start Postion in Bytes> | <Length in Bytes> | <Max:Min Entropy> | <Block Size>

import sys
import os
import binascii
import subprocess

no00FF = False
writeVectorToFile = True
plotGraphs = False
showScreenOutput = False
CRED = '\033[91m'
CEND = '\033[0m'

knownArchitectures = ['amd64','mips','mipsel','powerpc','i386','armel','armhf','ppc64el','java','python27','python35','gcc','clang','tcc','AVR','dotNet']

bytecount = 0
processedByteCount = 0

#Argument Error Checking
try:
    fileSelected = sys.argv[2]
    file = open(sys.argv[2], "rb")
    bytesInFile = os.path.getsize(sys.argv[2])
except:
    print(CRED + 'Argument Error' + CEND)
    sys.exit()
    
try:
    offsetStart = sys.argv[4]
except:
    offsetStart = 0

try:
    length = sys.argv[5]
except:
    length = bytesInFile - int(offsetStart)

try:
    maxEntropy = float(sys.argv[6].split(':')[0])
    minEntropy = float(sys.argv[6].split(':')[1])
except:
    maxEntropy = 1.0
    minEntropy = 0.0

try:
    blockSize = int(sys.argv[7])
except:
    blockSize = 256

try:
    outPath = sys.argv[3]
except:
    print(CRED + 'Argument Error' + CEND)
    sys.exit()
if not os.path.exists(sys.argv[3]):
    os.makedirs(sys.argv[3])

#Binwalk Section
#Get Verbose Binwalk Entropy Scan Results
entropy = subprocess.check_output(['binwalk', '-E', '-v', '--block=' + str(blockSize), '--nplot', fileSelected]).split()
entropy = entropy[entropy.index(b'ENTROPY')+2:len(entropy)]
del entropy[1::3]
#Loop through Binwalk elements to decode them
for index in range(0,len(entropy)):
    entropy[index] = entropy[index].decode()


#Bytes to Read and throw away (Offset)
trashBytes = file.read(int(offsetStart))

#Read in 2 bytes
bytes = file.read(2)

#Make 260 Element Array
#histogram = [0] * 260
histogram = [0] * 258

#Make 254 Element Array
index = list(range(0,255))

print('Processing ' + fileSelected.split(os.sep)[-1])

#count = 0

while bytes:
    print((bytecount / bytesInFile) * 100, end='\r')
    if int(length) > bytecount:
        #Format bytes
        hex2bytes = binascii.hexlify(bytearray(bytes))
          
        #Index into array and increment count Endian checks    
        if hex2bytes == b'0001':
            histogram[256] = histogram[256] + 1
        if hex2bytes == b'0100':
            histogram[257] = histogram[257] + 1
            
        #Split Bytes
        hexbyte1 = hex2bytes[0:2] 
        hexbyte2 = hex2bytes[2:4]
        
	#Check Entropy to see if bytes should be ignored
        entropyValue = float(entropy[entropy.index(str((int(bytecount / blockSize)) * blockSize)) + 1])

        #Index into array and increment count
        if entropyValue <= maxEntropy and entropyValue >= minEntropy:
            histogram[int(hexbyte1,16)] = histogram[int(hexbyte1,16)] + 1
            processedByteCount = processedByteCount + 1
        bytecount = bytecount + 1
        if hexbyte2 != b'':     #Handles last value not 2 Bytes long
            if entropyValue <= maxEntropy and entropyValue >= minEntropy:
                histogram[int(hexbyte2,16)] = histogram[int(hexbyte2,16)] + 1
                processedByteCount = processedByteCount + 1 
            bytecount = bytecount + 1
    
    #Read another 2 bytes
    bytes = file.read(2)

#Save a copy of the non-Normalized count
normalCount = histogram[:]

#Normalize Histogram
try:
    histogram[:256] = [x / processedByteCount for x in histogram[:256]]
except:
    histogram[:256] = [0 for x in histogram[:256]]

#Calc Endianness
if histogram[256] < histogram[257]:
    histogram[256] = 0
    histogram[257] = 1
else:
    histogram[256] = 1
    histogram[257] = 0

if showScreenOutput == True:

    #Print AI Vector   
    print(histogram)
    print()

    #Print Histogram
    for h in range (0,64):
        print(str(hex(h)) + " : " + str(histogram[h]) + '\t' + str(hex(h+64)) + " : " + str(histogram[h+64]) + '\t' + str(hex(h+2*64)) + " : " + str(histogram[h+2*64]) + '\t' + str(hex(h+3*64)) + " : " + str(histogram[h+3*64]))

    #Print Top n Bytes
    print("\nMost Frequent Bytes")
    n=50

    topValues = sorted(zip(histogram[0:255],index,normalCount[0:255]), reverse=True)[:n]

    for t in range(0,n):
        print(str(hex(topValues[t][1])) + "\t" + str(topValues[t][1]) + '  \tNormalized Count: ' + str(topValues[t][0]) + '\t   Count: ' + str(topValues[t][2]))

    #Check for Endianness and Print Result
    maxEndianIndex = histogram.index(max(histogram[256:260]))
    if maxEndianIndex == 256 or maxEndianIndex == 258:
        print("\nBig Endian")
    else:
        print("\nLittle Endian")
    
    #Print bytes processed
    print('\n' + str(processedByteCount) + ' bytes Processed')

file.close()



#Write Vector to File
if writeVectorToFile == True:
    if sys.argv[1] == 'Directory':
        outputFile = open(outPath + sys.argv[2].split(os.sep)[-2] + '.csv','a')
    else:
        outputFile = open(outPath + sys.argv[2].split(os.sep)[-1] + '.csv','a')

    try:
        arch = str(fileSelected).split(os.sep)[-1].split('_')[1]

        if arch in knownArchitectures:
            outputFile.write(arch + ',' + str(histogram)[1:-1] + '\n')
        else:
            raise
    except:
        #outputFile.write('mips' + ',' + str(histogram)[1:-1] + '\n')
        outputFile.write(sys.argv[2] + ',' + str(histogram)[1:-1] + '\n')
        #outputFile.write('?' + ',' + str(histogram)[1:-1] + '\n')
    outputFile.close()
    
#Plot Graph
if plotGraphs == True:
    if no00FF:
        import matplotlib.pyplot as plot
        fig, ax = plot.subplots()
        ax.plot(range(1,255), histogram[1:255])
        ax.set(xlabel='Bytes', ylabel='Normalized Count',title='Byte Histogram (No 0x00 or 0xFF)')
        major_ticks = range(1,255)
        ax.set_xticks(major_ticks)
        ax.tick_params(axis='x', labelsize='10')
        ax.grid(which='both', alpha=0.1)
        ax2 = ax.twinx()
        ax2.plot(range(1,255), normalCount[1:255])
        ax2.set_ylabel('Count')
        fig.tight_layout()
        plot.show()
    else:
        import matplotlib.pyplot as plot
        fig, ax = plot.subplots()
        ax.plot(range(0,256), histogram[0:256])
        ax.set(xlabel='Bytes', ylabel='Normalized Count',title='Byte Histogram')
        major_ticks = range(0,256)
        ax.set_xticks(major_ticks)
        ax.tick_params(axis='x', labelsize='10')
        ax.grid(which='both', alpha=0.1)
        ax2 = ax.twinx()
        ax2.plot(range(0,256), normalCount[0:256])
        ax2.set_ylabel('Count')
        fig.tight_layout()
        plot.show()
