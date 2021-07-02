import re
from .EmoAnalyzer import EmoAnalyzer
from .Parser import Parser

class Listener:
    def __init__(self) :
        self.emoAnalyzer = EmoAnalyzer()
        self.parser = Parser()

    def listen(self, input_s, dictionary) :
        #tokenizer
        tokens = self.tokenize(input_s, dictionary)

        #tagger
        taggedTokens = self.tag(tokens, dictionary)

        #parsing
        record = self.parse(taggedTokens, dictionary)

        return record

    def tokenize(self, input_s, dictionary) :
        tokens = []

        words = [w for w in input_s.split(' ') if w]

        for w in words :
            if re.match('[^\']+\'[^\']*', w) != None : #if word contains ' (apostrophe)
                tokens.append(w[:w.find("'")])
                tokens.append(w[w.find("'"):])
            elif re.match('\d+.\d+.\d+', w) != None : # DDD.DDD.DDD (date format etc.)
                tokens.append({
                    'word' : w,
                    'pos' : 'n' #date ?
                })
            elif re.match('[^\.]+\.', w) != None : # ends with . (Mr. , ... , end of sentence)
                #need to add logic to catch Mr. , Ms. , others...
                
                #if end of sentence
                tokens.append(w[:w.find(".")])
                tokens.append({
                    'word' : '.',
                    'pos' : '.'
                })
            elif re.match('.+[\!\?]', w) != None :  # ends with ! or ?
                tokens.append(w[:-1])
                tokens.append({
                    'word' : w[-1],
                    'pos' : '.'
                })

            elif re.match('[^\,]+\,', w) != None : # ends with ,
                tokens.append(w[:-1])
                tokens.append({
                    'word' : ',',
                    'pos' : ','
                })

            else :
                tokens.append(w)

        return tokens

    def tag(self, tokens, dictionary) :
        taggedTokens = []

        for t in tokens :
            print(t)

        return taggedTokens

    def parse(self, taggedTokens, dictionary) :
        return self.parser.parse(taggedTokens)