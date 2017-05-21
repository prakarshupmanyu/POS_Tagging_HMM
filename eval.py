from __future__ import division
import time
import sys
import os
import re
import math

outputFile = open('hmmoutput.txt', 'r')
actualOutputFile = open('hw5-data-corpus/catalan_corpus_dev_tagged.txt', 'r')
outWords = []
for line in outputFile:
	words = line.rstrip('\n').rstrip('\r').split(' ')
	for w in words:
		outWords.append(w)

expectedWords = []
for line in actualOutputFile:
	words = line.rstrip('\n').rstrip('\r').split(' ')
	for w in words:
		expectedWords.append(w)

matchedWords = 0
totalWords = 0
for i in range(len(outWords)):
	if outWords[i] == expectedWords[i]:
		matchedWords += 1
	else:
		print outWords[i] + " " + expectedWords[i]
	i += 1
	totalWords += 1

print "Matched Words: "+str(matchedWords)
print "Total Words: "+str(totalWords)
print "Accuracy: "+str(matchedWords/totalWords)
