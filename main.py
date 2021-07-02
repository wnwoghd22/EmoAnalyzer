import random 
import re
import json
from Analyzer.Listener import Listener
from Analyzer.Speaker import Speaker
from Dictionary.Dictionary import Dictionary
 
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

        """
        self.keys = {} 
        self.initials = [] 
        self.finals = [] 
        self.quits = [] 
        self.pres = {} 
        self.reversals = {} 
        self.shopping_list = [] 
        self.memory = []
        """
 
    """
    def loadDictionary(self, path): 
         with open(path) as json_file: 
             data_json = json.load(json_file) 
             self.initials = data_json['initial'] 
             self.finals = data_json['final'] 
             self.quits = data_json['quit'] 
             for reversal_json in data_json['post']: 
                 self.reversals[reversal_json['key']] = reversal_json['reversal'] 
             for preprocess_json in data_json['pres']: 
                 for alternative_json in preprocess_json['alternatives']: 
                     self.pres[alternative_json] = preprocess_json['key'] 
             for keyword_json in data_json['keywords']: 
                 decomp_list = [] 
                 for decomp_json in keyword_json['decomps']: 
                     decomp_list.append(Decomp(decomp_json['decomp_key'], decomp_json['answers'], True if decomp_json['save'] == 'True' else False)) 
                 for key in keyword_json['key']: 
                     self.keys[key] = Key(keyword_json['key'], decomp_list, keyword_json['weight']) 

    def _match_decomp(self, decomp_key, save, s, key): 
         re_search_str = decomp_key 
         if decomp_key == '': 
             return True 
         if save: 
             num = int(re.findall('\d+', decomp_key)[0]) 
 
             re_search_str = re.sub('\d', '((?:high-end|basic) computer|[a-z]+)', decomp_key) 
             m = re.match(re_search_str, s) 
             if m is not None: 
                 if num == 1: 
                     self.shopping_list.append(m.group(1)) 
                     return True 
                 if num == 2: 
                     if m.group(1) in self.shopping_list: 
                         self.shopping_list.remove(m.group(1)) 
                         return True 
             if num == 3: 
                 self.memory.append('You brought up ' + self._reverse_sentence(s) + 'before. Is that clear to you now?') 
         elif bool(re.search(re_search_str, s)): 
             return True 
         return False 
  
    def _reverse_sentence(self, sentence): 
         output = '' 
         for word in sentence.split(): 
             if word in self.reversals: 
                 word = self.reversals[word] 
             output += word + ' ' 
         return output 
 
    def _get_possible_answers(self, answers, user_input, decomp_key): 
         possible_answers = [] 
         for possible_answer in answers: 
             num = re.findall('\d{1}&', possible_answer) 
             if num: 
                 if self.shopping_list: 
                     if num[0] == '0&': 
                         possible_answer = re.sub('0&', ', '.join(self.shopping_list), possible_answer) 
                         possible_answers.append(possible_answer) 
                     if num[0] == '1&': 
                         possible_answer = re.sub('1&', self.shopping_list[-1], possible_answer) 
                         possible_answers.append(possible_answer) 
                 if num[0] == '3&': 
                     repeat = re.sub(decomp_key[:-2], '', user_input) 
                     possible_answer = re.sub('3&', self._reverse_sentence(repeat), possible_answer) 
                     possible_answers.append(possible_answer) 
                 if num[0] == '9&': 
                     possible_answer = re.sub('9&', self._reverse_sentence(user_input), possible_answer).capitalize() 
                     possible_answers.append(possible_answer) 
             elif not num: 
                 possible_answers.append(possible_answer) 
         return possible_answers 
 
    def _match_key(self, key, s): 
         output = None 
         for decomp in key.decomps: 
             if self._match_decomp(decomp.decomp_key, decomp.save, s, key): 
                 possible_answers = self._get_possible_answers(decomp.answers, s, decomp.decomp_key) 
                 if possible_answers: 
                     output = random.choice(possible_answers) 
             if output is None: 
                 continue 
 
 
             break 
         return output 
    
    def respond(self, user_input): 
         user_input = user_input.lower() 
         if user_input in self.quits: 
             return None 
 
 
         special_chars = ",.'!.?;:&" 
         user_input = ''.join(re.findall('[^' + special_chars + ']', user_input)) 
 
 
         for alternative in self.pres: 
             user_input = re.sub(alternative, self.pres[alternative], user_input) 
 
 
         words = [w for w in user_input.split(' ') if w] 
 
 
         keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys] 
         keys = sorted(keys, key=lambda k: -k.weight) 
 

         output = None 
 

         for key in keys: 
             output = self._match_key(key, user_input) 
             if output: 
                 break 
         if not output: 
             if self.memory: 
                 index = random.randrange(len(self.memory)) 
                 output = self.memory.pop(index) 
             else: 
                 output = random.choice(self._get_possible_answers(self.keys['xnone'].decomps[0].answers, user_input,'')) 
 

         return "".join(output) 
    """

    def run(self):
        while True:
            user_input = input('> ')
            output = self.speaker.respond(self.listener.listen(user_input, self.dictionary))

            if output is None:
                break
            print(output)
            #if output.endswith('...'): break

        #print(random.choice(self.finals)) 

def main():
    bot = Bot()
    bot.run()
 
if __name__ == '__main__': 
     main() 
