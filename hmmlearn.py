from __future__ import division
import time
import sys
import os
import re
import math

def getFileName():
	if not len(sys.argv) == 2:
		print "Please provide 1 file name"
		sys.exit()
	return sys.argv[1]

def readFile(trainingFile):
	if not os.path.isfile(trainingFile):
		print "Please check whether training file exists or not"
		sys.exit()
	global tranCount, emCount, tagList, eachTagCount, eachEmCount
	inputFile = open(trainingFile, 'r')
	for line in inputFile:
		words = line.rstrip('\n').rstrip('\r').split(' ')
		current = 'START'
		for wt in words:
			wordTag = wt.rsplit('/', 1)	#Split the string "asdasd/asdasd/VB" into "asdasd/asdasd" & "VB"
			wd = wordTag[0]				# = "asdasd/asdasd"
			tag = wordTag[1]			# = "VB"
			if tag not in tagList:
				tagList.append(tag)
			if current not in tranCount:
				tranCount[current] = {}
				eachTagCount[current] = 0
			if tag not in tranCount[current]:
				tranCount[current][tag] = 0
			tranCount[current][tag] += 1
			eachTagCount[current] += 1
			
			if tag not in emCount:
				emCount[tag] = {}
				eachEmCount[tag] = 0
			if wd not in emCount[tag]:
				emCount[tag][wd] = 0
			emCount[tag][wd] += 1
			eachEmCount[tag] += 1
			current = tag
	inputFile.close()

#take two lists and return first-second
def diff(first, second):
	second = set(second)
	return [item for item in first if item not in second]

def smoothTranCount():
	global tranCount, tagList, tranProb, eachTagCount
	#fill the rows of tranCount
	keysNotInTranCount = diff(tagList, tranCount.keys())
	tranCount.update((x,{}) for x in keysNotInTranCount)
	eachTagCount.update((x,0) for x in keysNotInTranCount)
	for tag in tagList:
		tranProb[tag] = {}
		if tag not in tranCount:
			print "Error: tag not found"
		tagNotADestinationFromCurrentTag = diff(tagList, tranCount[tag].keys())
		#fill columns for the row tranCount[tag]
		tranCount[tag].update((x,0) for x in tagNotADestinationFromCurrentTag)
		tranCount[tag].update((x,y+1) for x,y in tranCount[tag].items())
		eachTagCount[tag] += len(tagList)
		tranProb[tag].update((x,math.log(y/eachTagCount[tag], 2)) for x,y in tranCount[tag].items())
	#add start to the tranCount
	tranProb['START'] = {}
	tagNotADestinationFromStartTag = diff(tagList, tranCount['START'].keys())
	tranCount['START'].update((x,0) for x in tagNotADestinationFromStartTag)
	tranCount['START'].update((x,y+1) for x,y in tranCount['START'].items())
	eachTagCount['START'] += len(tagList)
	tranProb['START'].update((x,math.log(y/eachTagCount['START'], 2)) for x,y in tranCount['START'].items())

def buildModel():
	global tranProb, emCount, eachEmCount
	modelFile = open('hmmmodel.txt', 'w')
	for iniTag in tranProb:
		for nextTag in tranProb[iniTag]:
			modelFile.write("t_"+str(iniTag)+"_"+str(nextTag)+" "+str(tranProb[iniTag][nextTag])+"\n")
	for tag in emCount:
		for word in emCount[tag]:
			modelFile.write("e_"+str(tag)+"_"+str(word)+" "+str(math.log(emCount[tag][word]/eachEmCount[tag], 2))+"\n")
	modelFile.close()

def main():
	trainingFileName = getFileName()
	readFile(trainingFileName)
	smoothTranCount()
	buildModel()

start = time.time()
tranCount = {}
emCount = {}
tagList = []
tranProb = {}
emProb = {}
eachTagCount = {}
eachEmCount = {}

main()
end = time.time()
print (end-start)
