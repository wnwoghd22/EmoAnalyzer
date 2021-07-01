"""
state machine

0 : start
1 : noun phrase (NOMINITIVE)
2 : verbal phrase
    - if a verb has valency of 0, then switch state into 5
    - if a verb has valency of 1, then switch state into 3
    - if a verb has valency of 2, then switch state into 4
3 : noun phrase (DATIVE) - indirect object
    - if next noun phrase encountered, then switch state into 4
4 : noun phrase (ACCUSATIVE) - direct object

"""

class Parser:
    def __init__(self) :
        self.record = []
        self.holdEmoji = ''
        self.holdEmoticone = ''
        self.state = 0
        self.stack = [] # push-down automata

    def parse(self, taggedTokens) :
        self.stack = []
        self.record = []
        for tt in taggedTokens :
            if acceptToken(tt) : continue
            return False
        return self.record

    def acceptToken(token) :
        if self.state == 0 : # Start State
            if token['pos'] in ['n', 'det', 'adj'] : # Verbal Phrase (name, The, a, happy~...)
                stack.push(token['word'])
                self.state = 1
            elif token['pos'] in ['md', 'v'] : # question (May~ ?, Is~ ?, Does~ ?)
                self.state = 2
        
        elif self.state == 1 : # Verbal, NOMINITIVE
            if token['pos'] in ['n', 'det', 'adj'] :
                stack.push(token['word'])
                self.state = 1 # repeat again (The <name>...)

            elif token['pos'] in ['md', 'v'] : # encountered verbal phrase
                self.state = 