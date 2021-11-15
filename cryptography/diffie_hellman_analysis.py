"""
File Created: 9th November 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes on Diffie Hellman algorithm: 
        This is used for key exchange. Idea is based on generator, modulus and prime numbers.
        https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
        
'''

import math
import random

class DiffieHellmanUtils:
    '''
    '''
    def __init__(self):
        '''
        constructor for DiffieHellmanUtils class

        Returns
        -------
        None.

        '''
        return
    
    def find_generator_for_mod(self, mod_val:int)->(int, list):
        '''
        find generator starting from 2. Find the minimum generator value for given mod val.
        For example generator for mod 7 should generate values 1,2,3,4,5, and 6 in any order
        # when raised to power starting from 0. In this example we should get 
        # g as 3 as it generates values 1,2,3,4,5 and 6

        Parameters
        ----------
        mod_val : int
            minimum generator value to found for given mod val..

        Returns
        -------
        int
            minimum generator value for given mod val.
        list
            sequence of values in range of 1 to mod_val-1

        '''
        g = 2
        added = []
        while(g < mod_val):
            added = []
            for i in range(mod_val):
                # calulate g**power mod mod_val
                val = (g**i) % mod_val
                if val not in added:
                    added.append(val)
                    if(len(added) == (mod_val - 1)):
                        # we found generator so make g = 8 and break after printing the sequence.
                        g = mod_val + 1
                        for i in added:
                            print(i)
                
            g = g + 1
        return g, added
    
    def is_prime(self, num:int)->bool:
        '''
        checks is given number is prime or not

        Parameters
        ----------
        num : int
            number to be checked is it prime or not.

        Returns
        -------
        bool
            True if bool else False.

        '''
        
        for i in range(2, math.isqrt(num)):
            if num % i == 0:
                return False
        return True
    
    def get_prime(self, size:int)->int:
        '''
        returns first prime in range of size and 2*size

        Parameters
        ----------
        size : int
            range of numbers starting from number size.

        Returns
        -------
        int
            first prime in range of size and 2*size.

        '''
        while True:
            p = random.randrange(size, 2*size)
            if self.is_prime(p):
                return p
            
    def is_generator(self, g:int, mod_p:int)->bool:
        '''
        checks if argument g is generator for mod_p value.
        For example if we have mod_p value as 7 and we want to find generator for example 
        if g = 2 then we have 1,2,4,1 which we can see 1 is repeated in range of(0, 6 i.e., 0 to 5)
        so 2 is not a generator ofr mod 7. Now if we try g = 3 then we have sequence in which 1
        is not repeated in range 0 to 5.

        Parameters
        ----------
        g : int
            generator.
        mod_p : int
            mod p value.

        Returns
        -------
        bool
            True if g is generator for mod p value else False.

        '''
        # if power of any thing goes to 1 then it restarts again
        for i in range(1, mod_p-1):
            if (g**i) % mod_p ==1:
                return False
        return True
            
    def get_generator(self, mod_p:int)->int:
        '''
        gets first generator value for given mod_p argument.

        Parameters
        ----------
        mod_p : int
            mod p value for which first generator to be found.

        Returns
        -------
        int
            smallest generator value for given mod p.

        '''
        for g in range(2, mod_p):
            if self.is_generator(g, mod_p):
                return g
            

            
if __name__ == '__main__':
    df_hellman = DiffieHellmanUtils()
    mod_p = df_hellman.get_prime(100)
    print('first prime in range of [100,200]: ', mod_p )
    g = df_hellman.get_generator(mod_p)
    print('first generator of mod p :', mod_p, ' is :', g)
    
    print('*** Diffee Hellman key demo *** ')
    df_hellman = DiffieHellmanUtils()
    # public (green)
    p = df_hellman.get_prime(10000)
    g = df_hellman.get_generator(p)
    print('public data g and p values are: ', g, p)

    # Alice
    a = random.randrange(0, p)
    g_a = (g**a) % p
    # Alice sends this out in the public
    print("Alice : g_a", g_a)
    
    # Bob
    b = random.randrange(0, p)
    g_b = (g**b) % p
    # Bob sends this out in the public
    print("Bob : g_b", g_b)
    
    # Back to Alice
    g_ab_alice = (g_b**a) % p
    print("Alice g_ab", g_ab_alice)
    
    # Back to Bob
    g_ab_bob =(g_a**b) % p
    print("Bob g_ab", g_ab_bob)

    
