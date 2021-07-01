"""
state machine

For simple parsing process, all rules are defined 'left-recursively'.
also stack (push-down) is used.

0 : start
1 : noun phrase (NOMINITIVE)
2 : verbal phrase
    - if a verb has valency of 1, then switch state into 5
    - if a verb has valency of 2, then switch state into 3
    - if a verb has valency of 3, then switch state into 4
    - if be verb, switch state into 6
3 : noun phrase (DATIVE) - indirect object
    - if next noun phrase encountered, then switch state into 4
4 : noun phrase (ACCUSATIVE) - direct object

5 : adverb

6 : adj

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
        elif token['pos'] in ['md', 'v'] :  # question (May~ ?, Is~ ?, Does~ ?)
                stack.push('VP')
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
            elif token['pos'] in [',', 'cc'] :  # adj, adj... / adj and adj / n, n... / n and n
                self.phrase.push(token['word'])
                self.stack.push('NP$')
                self.state = 1
            elif token['pos'] in ['md', 'v'] : # encountered verbal phrase
                self.record['SUBJECT'] = ' '.join(phrase)
                self.phrase.clear()
                self.stack.push('NP')
                self.state = 2
        elif top == 'NP$' :
            if token['pos'] in ['n', 'det', 'adj'] :
                self.phrase.push(token['word'])
                self.stack.push('NP')
                self.state = 1  # repeat again (The <name>...)
            elif token['pos'] in [',', 'cc'] :  # ,, / and and ... double cc
                return False
        #else

        return True



    def acceptToken(self, token) :
        funclist = [
            Parser.state0,
            Parser.state1,
        ]

        funclist[self.state](self, token)

        """
        if self.state == 0 :  # Start State
            funclist[0](self, token)
        
        elif self.state == 1 :  # Verbal, NOMINITIVE
            funclist[1](self, token)
        """

    