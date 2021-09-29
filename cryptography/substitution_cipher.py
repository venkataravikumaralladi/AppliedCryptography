"""
File Created: 29th September 2021
Author: Venkata Ravi K A 
-----

"""
from typing import Dict
import random



class SubstitutionCipher:
    ''' Ceaser Cipher:
            substitution cipher which is like ceaser cipher, but it has complexity that
            increases the key space insanely.
            Acutally ceaser cipher is an example of substitution cipher.
            A substitution cipher has 26! possible permutations i.e., possible keys.
            26! is approximately equal to 2^88, so we have 88 bit security.
            Substution cipher always uses capital English letters
    '''

    NUMBER_OF_ENGLISH_ALPHABETS = 26
    
    letter_freq = {'a': 0.0817, 'b': 0.0150, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270, 'f': 0.0223,
                   'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015, 'k': 0.0077, 'l': 0.0403,
                   'm': 0.0241, 'n': 0.0675, 'o': 0.0751, 'p': 0.0193, 'q': 0.0010, 'r': 0.0599,
                   's': 0.0633, 't': 0.0906, 'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
                   'y': 0.0197, 'z': 0.0007}
    
    def __init__(self, seed : int =237):
        self.rng=random.Random(seed)
        return
    
    @property
    def keyed(self) -> bool:
        return self._keyed

    @keyed.setter
    def keyed(self, value: bool):
        self._keyed = value
    
    def generate_encr_key(self) -> Dict[int, int]:
        ''' Generate encryption key for Ceaser cipher.'''
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ciph_letters = list(letters)
        self.encrytion_key = {}
        ciph_letters = list(letters)
        # create key
        for character in letters:
            self.encrytion_key[character] = ciph_letters.pop(self.rng.randrange(0, len(ciph_letters)))
        
        self.keyed = True
        return self.encrytion_key
    
    def get_decryption_key(self):
        ''' Generate decrpytion key from encryption key for Ceaser cipher.'''
        if(self.keyed == False):
            raise RuntimeError("encyption key not generated.")
            
        self.decryption_key = {}
        for key in self.encrytion_key:
            self.decryption_key[self.encrytion_key[key]] = key
        return self.decryption_key

    def encrypt(self, message : str)-> str:
        ''' encrypt the message from generated key for Ceaser cipher.
            Here for simplicity we encrypt only alphabets.
        '''
        cipher = ''
        for c in message:
            if c in self.encrytion_key:
                cipher += self.encrytion_key[c]
            else:
                cipher += c
        return cipher
    
    def decrypt(self, encryp_msg : str)-> str:
        ''' encrypt the message from generated key for Ceaser cipher.
            Here for simplicity we encrypt only alphabets.
        '''
        self.get_decryption_key()
        msg = ''
        for c in encryp_msg:
            if c in self.decryption_key:
                msg += self.decryption_key[c]
            else:
                msg += c
        return msg
    
  
if __name__ == '__main__':
    # breakeing the substitution cipher is do able with the knowledge of
    # language used. In English for example we have frequncies which can be use
    # to used. For example what character is apperaring most in cipher text
    # may be mapped to character 'e' as this is mostly used in English.
    # This means though we have 88 bit key size with additional knowledge
    # the cipher can be breakable. English plain text letter frequency is
    # below for reference.
    letter_freq = {'a': 0.0817, 'b': 0.0150, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270, 'f': 0.0223,
               'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015, 'k': 0.0077, 'l': 0.0403,
               'm': 0.0241, 'n': 0.0675, 'o': 0.0751, 'p': 0.0193, 'q': 0.0010, 'r': 0.0599,
               's': 0.0633, 't': 0.0906, 'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
               'y': 0.0197, 'z': 0.0007}
    
    