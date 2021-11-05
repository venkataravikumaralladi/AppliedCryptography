"""
File Created: 29th September 2021
Author: Venkata Ravi K A 
-----

"""

'''
  Frequency analysis:
      Following are steps:
          1. First calculate the frequecies of letters in cipher text
          2. Calculate the match with frequencies of the langauge we know
             for example for english letter 'e' is most widely used, so if
             'r' in cipher text is occuring at high frequency then it is 
             possible 'r' is 'e'.
          3. But is is possible when calculating the difference we can get
             like below.
                letter 'a' frequency different with actual english letters as below
                    [('k', 0.0), ('v', 0.0021), ('j', 0.0062), ('x', 0.0062), ('q', 0.0067),..., ('e', 0.1193)]
                ...
                similary letter 'c' frequency we can have as below
                    [('k', 0.0), ('v', 0.0021), ('j', 0.0062), ('x', 0.0062), ..., ('e', 0.1193)]
            so above both 'a' and 'c' letters in cipher text map to 'k' in actual english character, which is
            not correct.
                    
          4. We have to find for cipher character which is most likely plain text that will map to. And above
             in step 3 we land in to scenario some of the cipher characters map to same plain text characters.
             So next step we take here is guess a key and see what it comes to. We can see that the 'guess'
             is not prefect, and we want to improve the solution from that. (because some times we know
             that this character matches this character.) Next we do new guess, so we need a mechanisim in 
             order to do that. So we write 'guess_key' function.
             Here we have to put mechanism 'here we need a mechanism that if that plain letter is already
             used by previous cipher character'. So we use 'plain_chars_left' class variable.
             
          5. We have to tell our algorithm we already guessed for few letters correctly. This is done
             through set_key_mapping.
             
          6. We will iterate multiple times with guessing. for example after setting
                  attk.set_key_mappings('r', 'e')

             following output is observed for one of the line
                 P: bewiuse tre cmiwtnwe of tre bisnw zojezeats of yiti ns
                 C: lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wi
                 
            then we attk.set_key_mappings('p', 'h')
            
            Basically what we are doing is manually looking the text and see what letter we can predict
            and iteratively do this.
                 
            from above we can guess letter 'p' should match to letter 'h'
      Here we kind of know that we need to calculate the differences between the
      frequencies we calculate from cipher text and our knowledge of english
      language letter frequencies.
      
'''

import operator
import sys

class SubstitutionCipherAttack:
    '''
      Breakeing the substitution cipher is do able with the knowledge of
      language used. In English for example we have frequncies which can be use
      to used. For example what character is apperaring most in cipher text
      may be mapped to character 'e' as this is mostly used in English.
      This means though we have 88 bit key size with additional knowledge
      the cipher can be breakable. English plain text letter frequency is
      below for reference.
    '''
    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.plain_chars_left = 'abcdefghijklmnopqrstuvwxyz'
        self.cipher_chars_left = 'abcdefghijklmnopqrstuvwxyz'
        self.freq = {}
        for c in self.alphabet:
            self.freq[c] = 0
        self.mappings = {}
        self.key = {}
        self.english_letter_freq = {'a': 0.0817, 'b': 0.0150, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270, 
                                    'f': 0.0223,                'g': 0.0202, 'h': 0.0609, 'i': 0.0697,
                                    'j': 0.0015, 'k': 0.0077, 'l': 0.0403, 'm': 0.0241, 'n': 0.0675,
                                    'o': 0.0751, 'p': 0.0193, 'q': 0.0010, 'r': 0.0599, 's': 0.0633,
                                    't': 0.0906, 'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
                                    'y': 0.0197, 'z': 0.0007}
        return
    
    def calculate_freq(self, cipher : str):
        '''       
        Calculate letter frencies provided cipher text
        Parameters
        ----------
        cipher : str
            cipher text for which letter frequencies to be calculated.

        Returns
        -------
        None.

        '''
        letter_cnt = 0
        for c in cipher:
            if c in self.alphabet:
                self.freq[c] = self.freq[c] + 1
                letter_cnt = letter_cnt + 1
        # calculate probability of letter in given cipher text
        for c in self.freq:
            self.freq[c] = round(self.freq[c]/letter_cnt, 4)
        return
    
    def print_freq(self):
        '''
        Prints letter frequencies provided cipher text

        Returns
        -------
        None.

        '''
        new_line_cnt = 0
        for c in self.freq:
            print(c, ':', self.freq[c], ' ', end='')
            if new_line_cnt % 3 == 2:
                print()
            new_line_cnt += 1
            
    def calculate_cipher_char_matches(self):
        '''
        We need to figure out what cipher text characters match to real character.
        but we don't know whether first match is best match, so we have to figure out
        and try various gymanistics in our head. So we create a self.mappings dictionary

        Returns
        -------
        None.

        '''
        for cipher_char in self.alphabet:
            map = {}
            for plain_char in self.alphabet:
                map[plain_char] = round(abs(self.freq[cipher_char] - self.english_letter_freq[plain_char]), 4)
            self.mappings[cipher_char] = sorted(map.items(), key=operator.itemgetter(1))
            
        return
    
    def set_key_mapping(self, cipher_char:str, plain_char:str):
        '''
        we guessed mapping for few letters so we do that here

        Parameters
        ----------
        cipher_char : str
            cipher character.
        plain_char : str
            plain text character.

        Returns
        -------
        None.

        '''
        if cipher_char not in self.cipher_chars_left or plain_char not in self.plain_chars_left:
            print('ERROR: key mapping error', cipher_char, plain_char)
            sys.exit(-1)
        self.key[cipher_char] = plain_char
        self.plain_chars_left = self.plain_chars_left.replace(plain_char, '')
        self.cipher_chars_left = self.cipher_chars_left.replace(cipher_char, '')
    
            
    def guess_key(self):
        '''
        This function guess key

        Returns
        -------
        TYPE
            none.

        '''        
        # here we need a mechanism that if that plain letter is already used by previous cipher character.
        # We want to check for each cipher character to find the most likely plain character.
        for cipher_char in self.cipher_chars_left:
            # loop through all the possible mappings and take the first one that is available.
            for plain_char, diff in self.mappings[cipher_char]:
                if plain_char in self.plain_chars_left:
                    self.key[cipher_char] = plain_char
                    self.plain_chars_left = self.plain_chars_left.replace(plain_char, '')
                    break
                
        return
    
    def get_key(self) -> dict:
        '''
        Returns key

        Returns
        -------
        dict
            returns key dictionary that maps cipher letters to plain letters.

        '''
        
        return self.key
    
    def decrpyt(self, key:dict, cipher:str)->str:
        '''
        Method decrpyt the cipher text with given key

        Parameters
        ----------
        key : dict
            cipher letters mapping to plain letters.
        cipher : str
            cipher text to be decrypted.

        Returns
        -------
        str
            returns decrypted message.

        '''
        guess_msg = ''
        for c in cipher:
            if c in key:
                guess_msg += key[c]
            else:
                guess_msg += c
        return guess_msg
        
            
if __name__ == '__main__':
    cipher = """lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wi
                bpr xjvni mkd ymibrut jx irhx wi bpr riirkvr jx
                ymbinlmtmipw utn qmumbr dj w ipmhh but bj rhnvwdmbr bpr
                yjeryrkbi jx bpr qmbm mvvjudwko bj yt wkbrusurbmbwjk
                lmird jk xjubt trmui jx ibndt
                  wb wi kjb mk rmit bmiq bj rashmwk rmvp yjeryrkb mkd wbi
                iwokwxwvmkvr mkd ijyr ynib urymwk nkrashmwkrd bj ower m
                vjyshrbr rashmkmbwjk jkr cjnhd pmer bj lr fnmhwxwrd mkd
                wkiswurd bj invp mk rabrkb bpmb pr vjnhd urmvp bpr ibmbr
                jx rkhwopbrkrd ywkd vmsmlhr jx urvjokwgwko ijnkdhrii
                ijnkd mkd ipmsrhrii ipmsr w dj kjb drry ytirhx bpr xwkmh
                mnbpjuwbt lnb yt rasruwrkvr cwbp qmbm pmi hrxb kj djnlb
                bpmb bpr xjhhjcwko wi bpr sujsru msshwvmbwjk mkd
                wkbrusurbmbwjk w jxxru yt bprjuwri wk bpr pjsr bpmb bpr
                riirkvr jx jqwkmcmk qmumbr cwhh urymwk wkbmvb"""
    attk = SubstitutionCipherAttack()
    attk.calculate_freq(cipher)
    attk.print_freq()
    print()
    attk.calculate_cipher_char_matches()
    #for char in attk.alphabet:
    #    print('***', char)
    #    print(attk.mappings[char])
    # we guessed following key mapping
    attk.set_key_mapping('c', 'w')
    attk.set_key_mapping('f', 'q')
    attk.set_key_mapping('g', 'z')
    attk.set_key_mapping('o', 'g')
    attk.set_key_mapping('p', 'h')
    attk.set_key_mapping('a', 'x')
    attk.set_key_mapping('d', 'd')
    attk.set_key_mapping('e', 'v')
    attk.set_key_mapping('m', 'a')
    attk.set_key_mapping('q', 'k')
    attk.set_key_mapping('r', 'e')
    attk.set_key_mapping('s', 'p')
    attk.set_key_mapping('t', 'y')
    attk.set_key_mapping('u', 'r')
    attk.set_key_mapping('v', 'c')
    attk.set_key_mapping('w', 'i')
    attk.set_key_mapping('x', 'f')
    attk.set_key_mapping('y', 'm')
    
    attk.guess_key()
    key = attk.get_key()
    print(key)
    decr_msg = attk.decrpyt(key, cipher)
    decr_msg_lines = decr_msg.splitlines()
    cipher_msg_lines = cipher.splitlines()
    for i in range(len(decr_msg_lines)):
        print('P:', decr_msg_lines[i])
        print('C:', cipher_msg_lines[i])
        
        
    
    # We need to figure out what cipher text characters match to real character.
    # but we don't know whether first match is best match, so we have to figure out
    # and try various gymanistics in our head. So we create a mappings dictionary above class.
                
                

