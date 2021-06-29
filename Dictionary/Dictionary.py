import json

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
            if e['word'] == target:
                return e
