# -*- coding: utf-8 -*-

def extractAttribute(expression):
	"""
	
	input: 'key=val'
	output:['key','val']

	"""
	key = ''
	val = ''
	for i in range(len(expression)):
		if expression[i] == '=':
			val = expression[ i+1:]
			break
		else:
			key = key + expression[i]	
	if val == '':
		print expression
		print 'errror in the dictionary'
	return [key, val]

def parseTff(path, newPath):
	with open(newPath, 'w+') as w:
		with open(path) as f:
			for line in f:
				splitted = line.split()
				result = [extractAttribute(splitted_word) for splitted_word in splitted] 
				#nice: [positive]
				word = result[2][1]
				subjectivity = result[0][1]
				newLine = '%s: [%s]' % (word, subjectivity) 
				w.write(newLine+'\n')

path = 'dicts/subjclueslen.tff'
newPath = 'dicts/subjective.yml'
parseTff(path, newPath)


