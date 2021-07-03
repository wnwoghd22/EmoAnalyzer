import re
import copy

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
        self.sentence = {}
        self.record = {}
        self.holdEmoji = ''
        self.holdEmoticone = ''
        self.state = 0
        self.stack = [] # push-down automata
        self.phrase = []

    def getTop(self) :
        return self.stack.pop() if len(self.stack) > 0 else None

    def getPhrase(self) :
        result = ' '.join(self.phrase)
        self.phrase.clear()
        return result

    def pushSentence(self, tag) :
        self.sentence[tag] = self.getPhrase()

    def pushRecord(self) :
        self.record['S' + str(len(self.record))] = copy.deepcopy(self.sentence)
        self.sentence.clear()

    def parse(self, taggedTokens, emoAnalyzer) :
        self.state = 0
        self.stack = []
        
        self.sentence = {}
        self.record = {}
        for tt in taggedTokens :
            emoAnalyzer.Analyze(tt)

            if not self.acceptToken(tt) :
                return False
        
        self.record['Emotion'] = emoAnalyzer.getEmo()

        print('parse success')

        return self.record

    #Start State
    def state0(self, token) :
        top = self.getTop()
        if top == None or top == '$':
            if token['pos'] in ['n', 'det', 'adj', 'pro'] :  # Verbal Phrase (name, The, a, happy~...)
                self.phrase.append(token['word'])
                self.stack.append('NP')
                self.state = 1
            elif token['pos'] in ['adv'] :
                self.phrase.append(token['word'])
                self.stack.append('ADJP')
                self.state = 1
            elif token['pos'] in ['md', 'v'] :  # Starts with Modal or Verb (May~ ?, Is~ ?, Does~ ?, Do~ ! ...)
                self.stack.append('Q')
                self.state = 2
        elif top == 'W' :
            if token['pos'] in ['n', 'det', 'adj', 'pro'] :
                self.phrase.append(token['word'])
                self.stack.append('WNP')
                self.state = 1
        elif top == 'S' :
            if token['pos'] in ['emot', 'emoj'] :
                self.stack.append('S')
                self.state = 0
        return True

    #Noun Phrase, NOMINITIVE
    def state1(self, token) :
        top = self.getTop()
        if top == 'NP' :
            if token['pos'] in ['n', 'det', 'adj', 'pro'] :
                self.phrase.append(token['word'])
                self.stack.append('NP')
                self.state = 1  # repeat again (The <name>...)
            elif token['pos'] in [',', 'cc', 'pos'] :  # adj, adj... / adj and adj / n, n... / n and n / possessive
                self.phrase.append(token['word'])
                self.stack.append('NP$')
                self.state = 1
            elif token['pos'] in ['md', 'v'] : # encountered verbal phrase
                self.pushSentence('SUBJECT')
                self.phrase.append(token['word'])
                if token.get('base') == 'be' :
                    self.stack.append('VP')
                    self.state = 6
                else :
                    self.stack.append('V' + str(token['valency']))  # V1, V2, V3
                    self.state = 5 if token['valency'] == 1 else token['valency'] + 1
            elif token['pos'] == '.' :
                self.pushSentence('SUBJECT')
                self.pushRecord()
                self.stack.append('S')
                self.stack.append('$')
                self.state = 0
        elif top == 'NP$' :
            if token['pos'] in ['n', 'det', 'adj'] :
                self.phrase.append(token['word'])
                self.stack.append('NP')
                self.state = 1  # repeat again (The <name>...)
            elif token['pos'] in [',', 'cc'] :  # ,, / and and ... double cc
                return False
        elif top == 'WNP' :
            if token['pos'] in ['md', 'v'] :
                self.pushSentence('W-SUBJECT')
                self.phrase.append(token['word'])
                if token.get('base') == 'be' :
                    self.stack.append('WVP')
                    self.state = 6
                else :
                    self.stack.append('WV' + str(token['valency']))  # V1, V2, V3
                    self.state = 5 if token['valency'] == 1 else token['valency'] + 1
        elif top == 'QVP' :  # verbal phrase, reversal
            if token['pos'] in ['n', 'det', 'adj'] :
                self.phrase.append(token['word'])
                self.stack.append('QVP')
                self.state = 1 
            elif token['pos'] == 'pre' :
                self.sentence['SUBJECT'] = self.getPhrase()
                self.phrase.append(token['word'])
                self.stack.append('QVP')
                self.state = 8
        elif top == 'ADJP' :
            if token['pos'] in [','] :
                self.phrase.append(token['word'])
                self.stack.append('ADJP$')
                self.state = 1
            elif token['pos'] in ['vbn'] :
                self.phrase.append(token['word'])
                self.stack.append('VP')
                self.state = 2
        elif top == 'ADJP$' :
            if token['pos'] in [','] :
                return False
            elif token['pos'] in ['n', 'pro'] :
                self.pushSentence('ADJ')
                self.pushRecord()
                self.phrase.append(token['word'])
                self.stack.append('S')
                self.stack.append('NP')
                self.state = 1
                
        #else

        return True

    #verb encountered
    def state2(self, token) :
        top = self.getTop()
        if re.match('V\d', top) != None : # present tense
            if token['pos'] in ['n'] :
                self.state = 5
        elif top == 'VP' :  # gerund, p.p
            if token['pos'] in ['adv'] :
                self.phrase.append(token['word'])
                self.stack.append('VP')
                self.state = 5
            elif token['pos'] == '.' :
                self.pushSentence('VP')
                self.pushRecord()
                self.stack.append
        elif top == 'Q' :
            if token['pos'] in ['n', 'det'] :
                self.phrase.append(token['word'])
                self.stack.append('QVP')  # verbal phrase, reversal
                self.state = 1
            elif token['pos'] == '.' :
                self.sentence['VP'] = self.getPhrase()

        return True

    def state3(self, token) :
        top = self.getTop()
        if top == 'V2' :
            if token['pos'] == 'wp' :
                self.pushSentence('VP')
                self.pushRecord()
                self.phrase.append(token['word'])
                self.stack.append('W') # wh- phrase
                self.state = 0
        elif top == 'WV2' :
            if token['pos'] == '.' :
                self.pushSentence('WV')
                self.pushRecord()
                self.stack.append('S')
                self.stack.append('$')
                self.state = 0
            elif token['pos'] == 'emot' :
                self.stack.append('WV2')
                self.state = 3
        return True

    def state4(self, token) :

        return True

    def state5(self, token) :
        top = self.getTop()
        if top == 'VP' :
            if token['pos'] == '.' :
                self.pushSentence('VP')
                self.pushRecord()
                self.stack.append('S')
                self.stack.append('$')
                self.state = 0
        return True

    #be verb
    def state6(self, token) :
        top = self.getTop()
        if top == 'VP' :
            if token['pos'] in ['vbg', 'vbn'] :
                self.phrase.append(token['word'])
                self.sentence['VP'] = ' '.join(self.phrase)
                self.phrase.clear()
                self.stack.append('V' + str(token['valency']))
                self.state = 8
            elif token['pos'] in ['adj', 'adv'] :
                self.phrase.append(token['word'])
                self.stack.append('VP')
                self.state = 7

        return True

    # <be> [<adv>...]<adj>
    def state7(self, token) :
        top = self.getTop()
        if top in ['VP'] :
            if token['pos'] == '.':
                self.pushSentence('VP')
                self.phrase.clear()
                self.stack.append('S')
                self.stack.append('$')
                self.state = 0
            elif token['pos'] in ['n', 'pro'] :
                self.pushSentence('VP')
                self.pushRecord()
                self.phrase.append(token['word'])
                self.stack.append('S')
                self.stack.append('NP')
                self.state = 1
            elif token['pos'] in ['vbg', 'vbn'] :
                self.phrase.append(token['word'])
                self.stack.append('VP')
                self.state = 2
        return True

    def state8(self, token) :
        top = self.getTop()

        return True

    #prepositional phrase
    def state9(self, token) :
        top = self.getTop()

        return True

    def acceptToken(self, token) :
        funclist = [
            Parser.state0,
            Parser.state1,
            Parser.state2,
            Parser.state3,
            Parser.state4,
            Parser.state5,
            Parser.state6,
            Parser.state7,
            Parser.state8,
            Parser.state9
        ]

        print('state' + str(self.state), self.stack, token)
        return funclist[self.state](self, token)
    