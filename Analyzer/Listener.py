import re
from .EmoAnalyzer import EmoAnalyzer
from .Parser import Parser

class Listener:
    def __init__(self) :
        self.emoAnalyzer = EmoAnalyzer()
        self.parser = Parser()
        self.emojiList = {
            '👏' : '\\U1F44F',
            '🙈' : '\\U1F648', 
            '😍' : '\\U1F60D', 
            '😫' : '\\U1F62B', 
            '😱' : '\\U1F631', 
            '🎷' : '\\U1F3B7'
        }

    def listen(self, input_s, dictionary) :
        self.emoAnalyzer.Clear()

        #tokenizer
        tokens = self.tokenize(input_s, dictionary)

        #tagger
        taggedTokens = self.tag(tokens, dictionary)

        #parsing
        record = self.parse(taggedTokens, self.emoAnalyzer)

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
            elif re.match('\d+', w) != None :
                tokens.append({
                    'word' : w,
                    'pos' : 'cd'
                })
            elif re.match('[^\,]+\,', w) != None : # ends with ,
                tokens.append(w[:-1])
                tokens.append({
                    'word' : ',',
                    'pos' : ','
                })

            elif self.emojiList.get(w) != None :
                tokens.append(self.emojiList[w])  # as UNICODE

            elif w in ['.', '!', '?'] :
                tokens.append({
                    'word' : w,
                    'pos' : '.'
                })

            else :
                tokens.append(w)

        return tokens

    def tag(self, tokens, dictionary) :
        taggedTokens = []

        for t in tokens :
            if isinstance(t, str) :
                taggedTokens.append(dictionary.findWord(t))
            else :
                taggedTokens.append(t)

        #for tt in taggedTokens :
        #    print(tt)

        return taggedTokens

    def parse(self, taggedTokens, emoAnalyzer) :
        return self.parser.parse(taggedTokens, emoAnalyzer)