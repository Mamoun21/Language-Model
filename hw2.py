# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:36:27 2019

@author: soso
"""
#import nltk
import os
import math
from nltk.stem import PorterStemmer
p=PorterStemmer()

def readfile(path):
    wordlist=[]
    fp=open(path,'r')
    data=fp.read()
    word=data.split()
    for i in word:
        wordlist.append(p.stem(i))
    fp.close()
    return wordlist
def Bigram(data):
	lB = []
	bC = {}
	uC = {}
	for i in range(len(data)):
		if i < len(data) - 1:

			lB.append((data[i-1], data[i]))

			if (data[i-1], data[i]) in bC:
				bC[(data[i-1], data[i])] += 1
			else:
				bC[(data[i-1], data[i])] = 1

		if data[i] in uC:
			uC[data[i]] += 1
		else:
			uC[data[i]] = 1

	return lB,uC, bC
def BigramProb(lB, uC, bC):

	listOfProb = {}
	for bigram in lB:
		word1 = bigram[0]	
		listOfProb[bigram] = (float(bC.get(bigram)))/float((uC.get(word1)))
	return listOfProb 
def Smothing(lB, unC, bC):
	listOfProb = {}
	for i in lB:
		word1 = i[0]
		listOfProb[i] = float((bC.get(i) + 1))/float((uC.get(word1) + len(uC)))
	file = open('Smoothing.txt', 'w')
	file.write('Bigram'  + 'Probability' + '\n')
	for j in lB:
		file.write(str(j)+ ' : ' + str(listOfProb[j]) + '\n')
	file.close()
	return listOfProb
def output(bigramAddOne,uC):
    calcProb2 = 1
    List = []
    file2 = open("content.txt","r")
    data1=file2.read()
    for i in range(len(data1.split())-1):
        List.append((data1.split()[i], data1.split()[i+1]))	
    for i in range(len(List)):
        if List[i] in bigramAddOne:
            calcProb2 = calcProb2+ math.log(bigramAddOne[List[i]])
        else:
            if List[i][0] not in uC:
				uC[List[i][0]] = 1
            prob = float(1) / float((uC[List[i][0]] + len(uC)))
            calcProb2 =calcProb2+ math.log(prob)            
    print("the probablility is:",str(calcProb2))
mm= open('11.txt','w')
for path,dirs,files in os.walk('training'):
    for i in files:
        fileName=os.path.join(path,i)
        with open(fileName,'r')as myfile:
            mm.write(myfile.read())
fileName = '11.txt'
data = readfile(fileName)
lB, uC, bC = Bigram(data)
bProb = BigramProb(lB, uC, bC)
bigramAddOne = Smothing(lB, uC, bC)
output(bigramAddOne,uC)