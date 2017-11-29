import os
import json
import re
from collections import defaultdict

paths = ['/workplace/penw/react/src/NodeJS-SmartHomeReactNative/src', '/workplace/penw/react/src/NodeJS-BehaviorsReactNative/src', '/workplace/penw/react/src/NodeJS-elements/src']
matchStrings = ['/workplace\/penw\/react\/src\/NodeJS-SmartHomeReactNative\/src(.*)', '/workplace\/penw\/react\/src\/NodeJS-BehaviorsReactNative\/src(.*)', '/workplace\/penw\/react\/src\/NodeJS-elements\/src(.*)']
modulenames = ['smart-home-react-native', 'behaviors-react-native', 'elements']
importRegex = '^import\s?{\s?(.*)}\s?from\s?\'(.*)\';$'

mydict = lambda: defaultdict(mydict)
data = mydict()


def search(path, matchString, modulename):
    stack = []
    stack.append(path);
    while len(stack) > 0:
        tmp = stack.pop(len(stack) - 1)
        if(os.path.isdir(tmp)):
            for item in os.listdir(tmp):
                stack.append(os.path.join(tmp, item))
        elif(os.path.isfile(tmp)):
            if fileCallback:
                read(tmp, matchString, modulename)

    return data

def read(path, matchString, modulename):
	flag = False
	curStr = ''
	with open(path) as f:
		for line in f:
			if len(line) - 2 < 0:
				continue
			isEndOfLine = line[len(line) - 2] == ';'
			isImport = line.startswith('import');
			if line.startswith('\/'):
				continue;
			if not flag and not isImport:
				break
			if not flag and isImport and not isEndOfLine:
				flag = True
				curStr = line.strip()
			elif not flag and isImport and isEndOfLine:
				curStr = line.strip()
			elif flag and not isEndOfLine:
				curStr += line.strip()
			elif flag and isEndOfLine:
				curStr += line.strip()
				flag = False

			if isEndOfLine:
				importM = re.search(importRegex, curStr)
				if importM is None:
					continue
				if importM.group(2).startswith('.'):
					continue

				components = importM.group(1).split(',')
				file = importM.group(2)
				if file.startswith('~'):
					file = file.replace("~", modulename)
				# for component in components:
				# 	if component not in data[file]:
				# 		data[file][component] = 0
				# 	data[file][component] += 1

				if file not in data:
					data[file] = 0
				data[file] += 1


				# print importM.group(1), importM.group(2)
				curStr = ''

def writeData():
	f = open('helloworld.txt','w')
	for file in data:
		f.write(file + ' ' + str(data[file]) + '\n')
	f.close()

# d = search(path = elementsPath, fileCallback = read)

for path, matchString, modulename in paths, matchStrings, modulenames:
	search(path, matchString, modulename)

# print data

# writeData()
