from __future__ import division
import operator
import time
import sys
import os
import re

def getFileName():
	if not len(sys.argv) == 2:
		print "Please provide 1 file name - the one that contains test data"
		sys.exit()
	return sys.argv[1]

def readFile():
	global transitionProb, emissionProb
	#read the probabilities from model file
	fileName = "hmmmodel.txt"
	if not os.path.isfile(fileName):
		print "Please check whether hmmmodel.txt exists or not"
		sys.exit()
	inputFile = open(fileName, 'r')
	for line in inputFile:
		lineParts = line.rstrip('\n').rstrip('\r').split(' ')
		matrixParams = lineParts[0].split('_', 2)	#splitting t_AB_VB and e_WW_sda_sadas_sada_232_sad. Need to split only on first 2 _ signs
		if matrixParams[0] == 't':
			if matrixParams[1] not in transitionProb:
				transitionProb[matrixParams[1]] = {}
			transitionProb[matrixParams[1]][matrixParams[2]] = float(lineParts[1])
		elif matrixParams[0] == 'e':
			if matrixParams[2] not in emissionProb:
				emissionProb[matrixParams[2]] = {}
			emissionProb[matrixParams[2]][matrixParams[1]] = float(lineParts[1])
	inputFile.close()

def computeTags(line):
	global transitionProb, emissionProb
	tagList = transitionProb['START'].keys()
	prob = {}
	backP = {}
	words = line.split(' ')
	wordPosition = 1
	minusInfinity = -float('inf')
	for w in words:
		prob[wordPosition] = {}
		for tag in tagList:
			if wordPosition == 1:
				prob[wordPosition][tag] = transitionProb['START'][tag]
				if w in emissionProb:
					if tag in emissionProb[w]:
						prob[wordPosition][tag] += emissionProb[w][tag]
					else:
						prob[wordPosition][tag] += minusInfinity	#min(emissionProb[w].iteritems(), key=operator.itemgetter(1))[1]
			else:
				bpKey1 = str(wordPosition) + "_" + tag
				maxBpValue = 0
				nonNullKeys = list(k for k, v in prob[wordPosition-1].items() if v > minusInfinity)
				for key in nonNullKeys:
					p = prob[wordPosition-1][key] + transitionProb[key][tag]
					#print str(prob[wordPosition-1][key]) + " * " + str(transitionProb[key][tag])
					#print maxBpValue
					if bpKey1 not in backP:
						maxBpValue = p
						backP[bpKey1] = str(wordPosition-1) + "_" + key
					if p > maxBpValue:
						maxBpValue = p
						backP[bpKey1] = str(wordPosition-1) + "_" + key

					if w in emissionProb:
						if tag in emissionProb[w]:
							p += emissionProb[w][tag]
						else:
							p += minusInfinity	#min(emissionProb[w].iteritems(), key=operator.itemgetter(1))[1]
					if tag not in prob[wordPosition]:
						prob[wordPosition][tag] = p
					elif prob[wordPosition][tag] < p:
						prob[wordPosition][tag] = p
				#print bpKey1 + " " + backP[bpKey1]
		wordPosition += 1
	wordPosition -= 1
	if not wordPosition == len(prob):
		print "Something is wrong here"
	return {'prob':prob, 'backP':backP}
	
def getTagSequence(backP, bpKey2):
	tagSeq = []
	while bpKey2 in backP:
		tag = bpKey2.split('_')[1]
		tagSeq.insert(0, tag)
		bpKey2 = backP[bpKey2]
	tag = bpKey2.split('_')[1]
	tagSeq.insert(0, tag)
	#print tagSeq
	return tagSeq

def createTaggedLine(line, tagSequence):
	words = line.split(' ')
	#print len(words)
	#print len(tagSequence)
	if not len(words) == len(tagSequence):
		print "Something is wrong now"
	taggedLine = ""
	for i in range(len(words)):
		taggedLine += words[i] + '/' + tagSequence[i] + " "
	return taggedLine.rstrip(' ')

def getTaggedLine(line):
	#print line
	viterbiParams = computeTags(line)
	prob = viterbiParams['prob']
	wordPosition = len(prob)
	mostProbableState = max(prob[wordPosition].iteritems(), key=operator.itemgetter(1))[0]
	bpKey2 = str(wordPosition) + "_" + mostProbableState
	tagSequence = getTagSequence(viterbiParams['backP'], bpKey2)
	return createTaggedLine(line, tagSequence)

def processTestFile(fileName):
	if not os.path.isfile(fileName):
		print "Please check whether test file exists or not"
		sys.exit()
	inputFile = open(fileName, 'r')
	outputFile = open('hmmoutput.txt', 'w')
	lineCount = 1
	for line in inputFile:
		#print lineCount
		taggedLine = getTaggedLine(line.rstrip('\n').rstrip('\r'))
		#print taggedLine
		outputFile.write(taggedLine+'\n')
		lineCount += 1
	inputFile.close()
	outputFile.close()

def main():
	fileName = getFileName()
	readFile()
	processTestFile(fileName)

start = time.time()
transitionProb = {}
emissionProb = {}

main()
end = time.time()
print (end-start)
