#Copyright 2020 Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED.

#python GenerateByteHistogram.py <Arch: a, Data Offsets: d, None: n> <Input Directory> <Output Directory> | <Start Postion in Bytes> | <Length in Bytes> | <Max:Min Entropy> | <Block Size> | <Required Votes>

#Required Votes refers to number of ML algorithms that must agree for data offset location
#Not used for standard arch detection

import subprocess
import sys
import glob
import os

CGREEN = '\033[92m'
CRED = '\033[91m'
CEND = '\033[0m'

inputType = 'Directory'

try:
    outPath = sys.argv[3]
except:
    print(CRED + 'Argument Error' + CEND)
    sys.exit()
if not os.path.exists(sys.argv[3]):
    os.makedirs(sys.argv[3])

#Write Header
if os.path.isdir(sys.argv[2]):
    filePath = outPath + sys.argv[2].split(os.sep)[-2] + '.csv'
    inputType = 'Directory'
    if os.path.exists(filePath):
        os.remove(filePath)
elif os.path.isfile(sys.argv[2]):
    filePath = outPath + sys.argv[2].split(os.sep)[-1] + '.csv'
    inputType = 'File'
    if os.path.exists(filePath):
        try:
            os.remove(filePath)  #Try Multiple time to remove file
            os.remove(filePath)
            os.remove(filePath)
        except:
            pass
else:
    print('Input Error')
    sys.exit()

try:
    binaries = glob.glob(sys.argv[2] + '*')
    binaries.sort()
except:
    print(CRED + 'Argument Error' + CEND)
    sys.exit()

count = 1
total = len(binaries)

outputFile = open(filePath,'a')
outputFile.write('Arch,0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1E,0x1F,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D,0x2E,0x2F,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3E,0x3F,0x40,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4A,0x4B,0x4C,0x4D,0x4E,0x4F,0x50,0x51,0x52,0x53,0x54,0x55,0x56,0x57,0x58,0x59,0x5A,0x5B,0x5C,0x5D,0x5E,0x5F,0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6A,0x6B,0x6C,0x6D,0x6E,0x6F,0x70,0x71,0x72,0x73,0x74,0x75,0x76,0x77,0x78,0x79,0x7A,0x7B,0x7C,0x7D,0x7E,0x7F,0x80,0x81,0x82,0x83,0x84,0x85,0x86,0x87,0x88,0x89,0x8A,0x8B,0x8C,0x8D,0x8E,0x8F,0x90,0x91,0x92,0x93,0x94,0x95,0x96,0x97,0x98,0x99,0x9A,0x9B,0x9C,0x9D,0x9E,0x9F,0xA0,0xA1,0xA2,0xA3,0xA4,0xA5,0xA6,0xA7,0xA8,0xA9,0xAA,0xAB,0xAC,0xAD,0xAE,0xAF,0xB0,0xB1,0xB2,0xB3,0xB4,0xB5,0xB6,0xB7,0xB8,0xB9,0xBA,0xBB,0xBC,0xBD,0xBE,0xBF,0xC0,0xC1,0xC2,0xC3,0xC4,0xC5,0xC6,0xC7,0xC8,0xC9,0xCA,0xCB,0xCC,0xCD,0xCE,0xCF,0xD0,0xD1,0xD2,0xD3,0xD4,0xD5,0xD6,0xD7,0xD8,0xD9,0xDA,0xDB,0xDC,0xDD,0xDE,0xDF,0xE0,0xE1,0xE2,0xE3,0xE4,0xE5,0xE6,0xE7,0xE8,0xE9,0xEA,0xEB,0xEC,0xED,0xEE,0xEF,0xF0,0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF,BE,LE' + '\n')
outputFile.close()

for i in binaries:

    bytesInFile = os.path.getsize(i)

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
        blockSize = 512
        
    try:
        requiredVotes = int(sys.argv[8])
    except:
        requiredVotes = 0

    print(CGREEN + '(' + str(count) + '/' + str(total) + ')' + CEND)

    try:
       subprocess.call('python3 SingleByteHistogram.py ' + str(inputType) + ' ' + str(i) + ' ' + str(outPath) + ' ' + str(offsetStart) + ' ' + str(length) + ' ' + str(maxEntropy) + ':' + str(minEntropy) + ' ' + str(blockSize), shell=True)
    except:
       subprocess.call('python SingleByteHistogram.py ' + str(inputType) + ' ' + str(i) + ' ' + str(outPath) + ' ' + str(offsetStart) + ' ' + str(length) + ' ' + str(maxEntropy) + ':' + str(minEntropy) + ' ' + str(blockSize), shell=True)
    count = count + 1

print(CGREEN + 'Byte Histogram Generation Complete' + CEND)

#-----------------------------------------------------ML Portion----------------------------------
if sys.argv[1] in ['a','d']:
    print(CGREEN + '\nMachine Learning Started' + CEND)
    import pandas as pd
    import numpy as np
    import sys
    import pickle

    inputTestData = outputFile.name

    testData = pd.read_csv(inputTestData)

    #Parse X & Y data from Datasets
    x_test = testData[['0x00','0x01','0x02','0x03','0x04','0x05','0x06','0x07','0x08','0x09','0x0A','0x0B','0x0C','0x0D','0x0E','0x0F','0x10','0x11','0x12','0x13','0x14','0x15','0x16','0x17','0x18','0x19','0x1A','0x1B','0x1C','0x1D','0x1E','0x1F','0x20','0x21','0x22','0x23','0x24','0x25','0x26','0x27','0x28','0x29','0x2A','0x2B','0x2C','0x2D','0x2E','0x2F','0x30','0x31','0x32','0x33','0x34','0x35','0x36','0x37','0x38','0x39','0x3A','0x3B','0x3C','0x3D','0x3E','0x3F','0x40','0x41','0x42','0x43','0x44','0x45','0x46','0x47','0x48','0x49','0x4A','0x4B','0x4C','0x4D','0x4E','0x4F','0x50','0x51','0x52','0x53','0x54','0x55','0x56','0x57','0x58','0x59','0x5A','0x5B','0x5C','0x5D','0x5E','0x5F','0x60','0x61','0x62','0x63','0x64','0x65','0x66','0x67','0x68','0x69','0x6A','0x6B','0x6C','0x6D','0x6E','0x6F','0x70','0x71','0x72','0x73','0x74','0x75','0x76','0x77','0x78','0x79','0x7A','0x7B','0x7C','0x7D','0x7E','0x7F','0x80','0x81','0x82','0x83','0x84','0x85','0x86','0x87','0x88','0x89','0x8A','0x8B','0x8C','0x8D','0x8E','0x8F','0x90','0x91','0x92','0x93','0x94','0x95','0x96','0x97','0x98','0x99','0x9A','0x9B','0x9C','0x9D','0x9E','0x9F','0xA0','0xA1','0xA2','0xA3','0xA4','0xA5','0xA6','0xA7','0xA8','0xA9','0xAA','0xAB','0xAC','0xAD','0xAE','0xAF','0xB0','0xB1','0xB2','0xB3','0xB4','0xB5','0xB6','0xB7','0xB8','0xB9','0xBA','0xBB','0xBC','0xBD','0xBE','0xBF','0xC0','0xC1','0xC2','0xC3','0xC4','0xC5','0xC6','0xC7','0xC8','0xC9','0xCA','0xCB','0xCC','0xCD','0xCE','0xCF','0xD0','0xD1','0xD2','0xD3','0xD4','0xD5','0xD6','0xD7','0xD8','0xD9','0xDA','0xDB','0xDC','0xDD','0xDE','0xDF','0xE0','0xE1','0xE2','0xE3','0xE4','0xE5','0xE6','0xE7','0xE8','0xE9','0xEA','0xEB','0xEC','0xED','0xEE','0xEF','0xF0','0xF1','0xF2','0xF3','0xF4','0xF5','0xF6','0xF7','0xF8','0xF9','0xFA','0xFB','0xFC','0xFD','0xFE','0xFF','BE','LE']] #Inputs
    y_test = testData['Arch'] #Output

    if sys.argv[1] == 'a':
        #Load Pickled Model
        model1 = pickle.load(open('PickledSKLearnModels/NeuralNetwork.sav', 'rb'))
        model2 = pickle.load(open('PickledSKLearnModels/AdaBoost.sav', 'rb'))
        model3 = pickle.load(open('PickledSKLearnModels/RandomForrest.sav', 'rb'))
        model4 = pickle.load(open('PickledSKLearnModels/kNN.sav', 'rb'))
        model5 = pickle.load(open('PickledSKLearnModels/Tree.sav', 'rb'))
        model6 = pickle.load(open('PickledSKLearnModels/SVM.sav', 'rb'))
        model7 = pickle.load(open('PickledSKLearnModels/NaiveBayes.sav', 'rb'))
        model8 = pickle.load(open('PickledSKLearnModels/LogisticRegression.sav', 'rb'))

        y_pred1 = model1.predict(x_test)
        y_pred2 = model2.predict(x_test)
        y_pred3 = model3.predict(x_test)
        y_pred4 = model4.predict(x_test)
        y_pred5 = model5.predict(x_test)
        y_pred6 = model6.predict(x_test)
        y_pred7 = model7.predict(x_test)
        y_pred8 = model8.predict(x_test)
        
        nn_score1 = model1.predict_proba(x_test)
        nn_score2 = model2.predict_proba(x_test)
        nn_score3 = model3.predict_proba(x_test)
        nn_score4 = model4.predict_proba(x_test)
        nn_score5 = model5.predict_proba(x_test)
        #nn_score6 = model6.predict_proba(x_test)
        nn_score7 = model7.predict_proba(x_test)
        nn_score8 = model8.predict_proba(x_test)
        
        probabilityPercent1 = max(nn_score1[0])*100
        probabilityPercent2 = max(nn_score2[0])*100
        probabilityPercent3 = max(nn_score3[0])*100
        probabilityPercent4 = max(nn_score4[0])*100
        probabilityPercent5 = max(nn_score5[0])*100
        #probabilityPercent6 = max(nn_score6[0])*100
        probabilityPercent7 = max(nn_score7[0])*100
        probabilityPercent8 = max(nn_score8[0])*100

        results = open("Output/Results.txt","w")
        
        outString = str(y_pred1[0]) + '\t' + str(round(probabilityPercent1,2)) + '%\t\tNeuralNetwork\n'\
                  + '------------------------------------------\n'\
                  + str(y_pred2[0]) + '\t' + str(round(probabilityPercent2,2)) + '%\t\tAdaBoost\n'\
                  + str(y_pred3[0]) + '\t' + str(round(probabilityPercent3,2)) + '%\t\tRandomForest\n'\
                  + str(y_pred4[0]) + '\t' + str(round(probabilityPercent4,2)) + '%\t\tkNN\n'\
                  + str(y_pred5[0]) + '\t' + str(round(probabilityPercent5,2)) + '%\t\tTree\n'\
                  + str(y_pred6[0]) + '\t' + str('N/A') + '\t\tSVM\n'\
                  + str(y_pred7[0]) + '\t' + str(round(probabilityPercent7,2)) + '%\t\tNaiveBayes\n'\
                  + str(y_pred8[0]) + '\t' + str(round(probabilityPercent8,2)) + '%\t\tLogisticRegression'
        
        results.write(outString)
        results.close()

    else:
        #Load All Pickled Models
        model1 = pickle.load(open('PickledSKLearnModels/NeuralNetwork.sav', 'rb'))
        model2 = pickle.load(open('PickledSKLearnModels/AdaBoost.sav', 'rb'))
        model3 = pickle.load(open('PickledSKLearnModels/RandomForrest.sav', 'rb'))
        model4 = pickle.load(open('PickledSKLearnModels/kNN.sav', 'rb'))
        model5 = pickle.load(open('PickledSKLearnModels/Tree.sav', 'rb'))
        model6 = pickle.load(open('PickledSKLearnModels/SVM.sav', 'rb'))
        model7 = pickle.load(open('PickledSKLearnModels/NaiveBayes.sav', 'rb'))
        model8 = pickle.load(open('PickledSKLearnModels/LogisticRegression.sav', 'rb'))

        y_pred1 = model1.predict(x_test)
        y_pred2 = model2.predict(x_test)
        y_pred3 = model3.predict(x_test)
        y_pred4 = model4.predict(x_test)
        y_pred5 = model5.predict(x_test)
        y_pred6 = model6.predict(x_test)
        y_pred7 = model7.predict(x_test)
        y_pred8 = model8.predict(x_test)

        results = open("Output/Results.txt","w")
        goodRows = []
        
        for i in range(0, len(y_pred1)):
            #Make in to List
            votes = [y_pred1[i], y_pred2[i], y_pred3[i], y_pred4[i], y_pred5[i], y_pred6[i], y_pred7[i], y_pred8[i]]
            
            #Calc percent agreements
            agreementString = max(set(votes), key=votes.count)
            agreementCount = votes.count(agreementString)
            agreementPercentage = int(agreementCount) / int(len(votes))
        
            if agreementCount >= requiredVotes:
            #if str(y_pred1[i]) == str(y_pred2[i]) == str(y_pred3[i]) == str(y_pred4[i]) == str(y_pred5[i]) == str(y_pred6[i]) == str(y_pred7[i]) == str(y_pred8[i]):
                goodRows.append(i)
                results.write(str(i) + ',' + str(agreementString) + ' (' + str(agreementCount) + ' of ' + str(len(votes)) + ') ' + str(agreementPercentage*100) + '%\n')
                #results.write(str(i) + ',' + str(y_pred1[i]) + '\n')
        results.close()

else:
    #Don't process ML
    sys.exit()

print('\nDone\n')

