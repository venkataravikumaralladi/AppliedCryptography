"""
File Created: 26th September 2021
Author: Venkata Ravi K A 
-----

"""
from typing import Dict
import cProfile # cprofile is library that provides deterministi profiling.



class CessarCipher:
    ''' Ceaser Cipher:
            The security of Ceaser cipher is based on keeping the algorithm secret.
            Ceaser cipher always uses capital English letters
    '''

    NUMBER_OF_ENGLISH_ALPHABETS = 26
    
    def __init__(self):
        return
    
    @property
    def keyed(self) -> bool:
        return self._keyed

    @keyed.setter
    def keyed(self, value: bool):
        self._keyed = value
    
    def generate_encr_key(self, shift : int) -> Dict[int, int]:
        ''' Generate encryption key for Ceaser cipher.'''
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.encrytion_key = {}
        cnt = 0
        # create key
        for character in letters:
            self.encrytion_key[character] = letters[(cnt + shift) % len(letters)]
            cnt = cnt + 1
        
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
    # breakeing the ceaser cipher is easy because it has only 26 keys. 
    # Here keys are 26 because we can add numbers from 0 to 25 to each letter.
    # Below code is done by enemy.
    ceaser_ciph = CessarCipher()
    key = ceaser_ciph.generate_encr_key(3)
    print(key)
    message = 'HELLO WORLD'
    cipher = ceaser_ciph.encrypt(message)
    
    # now trying to break the cipher
    print(cipher)
    for i in range(26):
        dkey = ceaser_ciph.generate_encr_key(i)
        message = ceaser_ciph.encrypt(cipher)
        print(message)    
        
    # Let us evaluate time required to perform various combination of keys
    # which is permuation.
    def faculty(n):
    	if n <= 1:
    		return 1
    	else:
    		return faculty(n-1) * n
        
    
    def counter(n):
    	cnt = 0
    	for i in range(n):
    		cnt += 1
        
    	return cnt
    print('vlaue of cnt is :', counter(faculty(11)))
    cProfile.run("counter(faculty(11))")
    
    

    
    
    

