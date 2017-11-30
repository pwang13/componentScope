import os
import json
import re
from collections import defaultdict

paths = ['/workplace/penw/react/src/NodeJS-SmartHomeReactNative/src', '/workplace/penw/react/src/NodeJS-BehaviorsReactNative/src', '/workplace/penw/react/src/NodeJS-elements/src', '/workplace/penw/homeFeed/src/Elements-Homefeeds/src']
matchStrings = ['/workplace\/penw\/react\/src\/NodeJS-SmartHomeReactNative\/src(.*)', '/workplace\/penw\/react\/src\/NodeJS-BehaviorsReactNative\/src(.*)', '/workplace\/penw\/react\/src\/NodeJS-elements\/src(.*)', '/workplace\/penw\/homeFeed\/src\/Elements-Homefeeds\/src(.*)']
modulenames = ['smart-home-react-native', 'behaviors-react-native', 'elements', 'homefeeds']
importRegex = '^import\s?{\s?(.*)}\s?from\s?\'(.*)\';$'

mydict = lambda: defaultdict(mydict)
data = mydict()
dependencies = mydict()
countKey = 'count'
componentKey = 'component'


def search(path, matchString, modulename):
    stack = []
    stack.append(path);
    while len(stack) > 0:
        tmp = stack.pop(len(stack) - 1)
        if(os.path.isdir(tmp)):
            for item in os.listdir(tmp):
                stack.append(os.path.join(tmp, item))
        elif(os.path.isfile(tmp)):
			read(tmp, matchString, modulename)

def addToDependencies(path, file, matchString, modulename):
	if path.endswith('styles.ts'):
		return
	m = re.search(matchString, path)
	newPath = modulename + m.group(1)
	if newPath not in dependencies:
		dependencies[newPath] = []
	dependencies[newPath].append(file)

def findSelfSupportDependencies():
	for path in dependencies.keys():
		for component in dependencies[path]:
			if not component.startswith('react') and not component.startswith('elements'):
				del dependencies[path]
				break

def read(path, matchString, modulename):
	flag = False
	curStr = ''
	with open(path) as f:
		for line in f:
			if len(line) - 2 < 0:
				continue
			isEndOfLine = line[len(line) - 2] == ';'
			isImport = line.startswith('import');
			if line.startswith('\/') or line.startswith('*'):
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

				components = [component.strip() for component in importM.group(1).split(',')]


				file = importM.group(2)
				if file.startswith('~'):
					file = file.replace("~", modulename)
				# for component in components:
				# 	if component not in data[file]:
				# 		data[file][component] = 0
				# 	data[file][component] += 1


				if file not in data:
					data[file][countKey] = 0

				for component in components:
					if len(component) == 0:
						continue
					if component.startswith('//'):
						continue
					if component not in data[file][componentKey]:
						data[file][componentKey][component] = 0
					data[file][componentKey][component] += 1

				addToDependencies(path, file, matchString, modulename)

				data[file][countKey] += 1
				curStr = ''


def writeData():
	f = open('paths.txt','w')
	for file in data:
		f.write(file + ' ' + str(data[file][countKey]) + '\n')
	f.close()

	f = open('components.txt', 'w')

	for file in data:
		for component in data[file][componentKey]:
			f.write(file + ' ' + component + ' ' + str(data[file][componentKey][component]) + '\n')
	f.close()

	f = open('dependencies.txt', 'w')
	for dependency in dependencies:
		f.write(dependency + ';' + ', '.join(dependencies[dependency]) + '\n')
	f.close()


# d = search(path = elementsPath, fileCallback = read)

for path, matchString, modulename in zip(paths, matchStrings, modulenames):
	# print modulename
	search(path, matchString, modulename)

# # print data

findSelfSupportDependencies()

print dependencies

writeData()


