import json
import re

def isLetter(c) :
    return isSmall(c) or isUpper(c)

def isUpper(c) :
    return c >= 'A' and c <= 'Z'

def isSmall(c) :
    return c >= 'a' and c <= 'z'

class Dictionary:
    def __init__(self, path) :
        self.list = []
        self.getList(path)

    def getList(self, path) :
        with open(path) as json_file: 
            data_json = json.load(json_file)
            self.list = data_json['list']

    def findWord(self, target) :
        for e in self.list:
            if isSmall(target[0]) or not isLetter(target[0]) :
                if e['word'] == target :
                    return e
            elif isUpper(target[0]) :        
                pattern = '^[' + target[0] + (chr(ord(target[0]) + ord('a') - ord('A'))) + ']' + target[1:] + '$'
                if re.match(pattern, e['word']) :
                    return e
