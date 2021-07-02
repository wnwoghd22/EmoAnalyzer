"""
state machine

For simple parsing process, all rules are defined 'left-recursively'.
also stack (push-down) is used.

0 : start
1 : noun phrase (NOMINITIVE)
    - if be verb, switch state into 6
    - if normal verb, switch state into 2
2 : verbal phrase
    - if a verb has valency of 1, then switch state into 5
    - if a verb has valency of 2, then switch state into 3
    - if a verb has valency of 3, then switch state into 4
3 : noun phrase (DATIVE) - indirect object
    - if next noun phrase encountered, then switch state into 4
4 : noun phrase (ACCUSATIVE) - direct object

5 : adverb

6 : be verb
    - if encounter gerund or p.p, then switch state into 8
    - adj -> state 7
7 : <be> <adj>

8 : gerund, p.p (AUX + ~ing / ~n, ed)

9 : prepositional phrase

"""

class Parser:
    def __init__(self) :
        self.record = []
        self.holdEmoji = ''
        self.holdEmoticone = ''
        self.state = 0
        self.stack = [] # push-down automata
        self.phrase = []

    def getTop(self) :
        return self.stack.pop() if self.stack.len() > 1 else None

    def parse(self, taggedTokens) :
        self.stack = []
        self.record = {}
        for tt in taggedTokens :
            if acceptToken(tt) : continue
            return False
        return self.record

    #Start State
    def state0(self, token) :
        if token['pos'] in ['n', 'det', 'adj'] :  # Verbal Phrase (name, The, a, happy~...)
                phrase.push(token['word'])
                stack.push('NP')
                self.state = 1
        elif token['pos'] in ['md', 'v'] :  # Starts with Modal or Verb (May~ ?, Is~ ?, Does~ ?, Do~ ! ...)
                stack.push('Q')
                self.state = 2

        return True

    #Noun Phrase, NOMINITIVE
    def state1(self, token) :
        top = self.getTop()
        if top == 'NP' :
            if token['pos'] in ['n', 'det', 'adj'] :
                self.phrase.push(token['word'])
                self.stack.push('NP')
                self.state = 1  # repeat again (The <name>...)
            elif token['pos'] in [',', 'cc', 'pos'] :  # adj, adj... / adj and adj / n, n... / n and n / possessive
                self.phrase.push(token['word'])
                self.stack.push('NP$')
                self.state = 1
            elif token['pos'] in ['md', 'v'] : # encountered verbal phrase
                self.record['SUBJECT'] = ' '.join(phrase)
                self.phrase.clear()
                self.phrase.push(token['word'])
                if w['base'] == 'be' :
                    self.stack.push('VP')
                    self.state = 6
                else :
                    self.stack.push('V' + token['valency'])  # V1, V2, V3
                    self.state = 2
            elif token['pos'] == '.' :
                self.record['SUBJECT'] = ' '.join(phrase)
                self.phrase.clear()
                self.stack.push('S')
                self.state = 0
        elif top == 'NP$' :
            if token['pos'] in ['n', 'det', 'adj'] :
                self.phrase.push(token['word'])
                self.stack.push('NP')
                self.state = 1  # repeat again (The <name>...)
            elif token['pos'] in [',', 'cc'] :  # ,, / and and ... double cc
                return False
        elif top == 'QVP' :  # verbal phrase, reversal
            if token['pos'] in ['n', 'det', 'adj'] :
                self.phrase.push(token['word'])
                self.stack.push('QVP')
                self.state = 1 
            elif token['pos'] == 'pre' :
                self.record['SUBJECT'] = ' '.join(self.phrase)
                self.phrase.push(token['word'])
                self.stack.push('QVP')
                self.state = 8
        #else

        return True

    #verb encountered
    def state2(self, token) :
        top = self.getTop()
        if top.startswith('V') :
            if token['pos'] in ['n'] :
                    self.state = 5
        elif top == 'Q' :
            if token['pos'] in ['n', 'det'] :
                self.stack.push('QVP')  # verbal phrase, reversal
                self.state = 1
            elif token['pos'] == '.' :
                self.record['VP'] = ' '.join(self.phrase)

        return True


    #be verb
    def state6(self, token) :
        top = self.getTop()
        if top == 'VP' :
            if token['pos'] in ['vbg', 'vbn'] :
                self.phrase.push(token['word'])
                self.record['VP'] = ' '.join(self.phrase)
                self.phrase.clear()
                self.stack.push('V' + token['valency'])
                self.state = 8


        return True

    def acceptToken(self, token) :
        funclist = [
            Parser.state0,
            Parser.state1,
        ]

        funclist[self.state](self, token)
    