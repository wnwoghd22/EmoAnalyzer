import random 
import re
import json
from Analyzer.Listener import Listener
from Analyzer.Speaker import Speaker
from Dictionary.Dictionary import Dictionary
from Analyzer.EmoAnalyzer import Emotion
 
class Key: 
    def __init__(self, word, decomps, weight): 
        self.word = word 
        self.decomps = decomps 
        self.weight = weight
 
class Decomp: 
    def __init__(self, decomp_key, answers, save): 
        self.decomp_key = decomp_key 
        self.answers = answers 
        self.save = save 

class Bot: 
    def __init__(self):
        self.speaker = Speaker()
        self.listener = Listener()
        self.dictionary = Dictionary('./Dictionary/data.json')

    def run(self, sentence = None) :
        if sentence != None :
            output = self.speaker.respond(self.listener.listen(sentence, self.dictionary))
            return
        while True:
            user_input = input('> ')
            output = self.speaker.respond(self.listener.listen(user_input, self.dictionary))

            if output is None:
                break
            
            #print(output)

        return
        

def main():
    bot = Bot()
    
    sample = open('./sample.txt', 'r')
    lines = sample.read().splitlines()
    for line in lines :
        print(line)
        #bot.run(line)
    
    bot.run()

if __name__ == '__main__': 
     main() 
