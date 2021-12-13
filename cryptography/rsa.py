"""
File Created: 13th December 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes on RSA algorithm: 
        This is used for secure communication. Asymmetric key algorithm.
        Idea is based on facorization, modulus and prime numbers.
        Factorization is hard problem to solve.
        
        Ref:
            https://en.wikipedia.org/wiki/RSA_(cryptosystem)
        
'''

import math
import random

class RSAUtils:
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
            
class RCA:
    '''
        Implements RCA Key geneation.
        Key generation. There are 5 steps.
            Ref: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
    '''
    def __init__(self):
        '''
        constructor for DiffieHellmanUtils class

        Returns
        -------
        None.

        '''
        self.rca_utils = RSAUtils()
        return
    
    
    def _generate_two_primes(self, primenum_start:int) -> (int, int):
        '''
        Generates two prime numbers between primenum_start and 2 * primenum_start

        Parameters
        ----------
        primenum_start : int
            prime number to be found from this number.

        Returns
        -------
        int, int
            two prime numbers.

        '''
        #Step1: Generate two ditinct primes
        p = self.rca_utils.get_prime(primenum_start)
        q = self.rca_utils.get_prime(primenum_start)
        return p, q
    
    def lcm(self, a:int, b:int)->int:
        '''
        Compute lambda(n) where lambda is Carmichael's totient function. 
        Since n = pq, λ(n) = lcm(λ(p),λ(q)), and since p and q are prime,
        λ(p) = φ(p) = p − 1 and likewise λ(q) = q − 1. 
        Hence λ(n) = lcm(p − 1, q − 1).
        lambda(n) is kept secret. lcm(a,b) = |ab|/gcd(a,b).

        Parameters
        ----------
        a : int
            DESCRIPTION.
        b : int
            DESCRIPTION.

        Returns
        -------
        int
            DESCRIPTION.

        '''
        return a*b//math.gcd(a,b)
    
    def get_e(self, lambda_n:int)->int:
        '''
        generated public component. Choose an integer e such that 1 < e < λ(n) 
        and gcd(e, λ(n)) = 1; that is, e and λ(n) are coprime.

        Parameters
        ----------
        lambda_n : int
            lambda_n value which is totient coefficient of n.

        Returns
        -------
        int
            public compoenent e if found None .

        '''
        for e in range(2, lambda_n):
            if math.gcd(e, lambda_n)==1:
                return e
            
        return None
    
    def get_d(self, e:int, lambda_n:int)->int:
        '''
        Determine d as d ≡ e−1 (mod λ(n)); that is, 
        # d is the modular multiplicative inverse of e modulo λ(n)
        # s means: solve for d the equation d⋅e ≡ 1 (mod λ(n))

        Parameters
        ----------
        e :int
            public component of key
        lambda_n : int
            lambda_n value which is totient coefficient of n..

        Returns
        -------
        int
            return private component if found else None.

        '''
        for d in range(2, lambda_n):
             if (d*e) % lambda_n == 1:
                 return d
        return None
    
    def generate_rsa_key(self, num_start:int) -> (int, int, int):
        '''
        Generated RSA key

        Parameters
        ----------
        num_start : int
            finds prime number starting from this number.

        Returns
        -------
        (int, int, int)
            modulo_n, public component, private component.

        '''
        #Step1: Generate two ditinct primes starting from num_start
        p, q = self._generate_two_primes(num_start)
        print('[INFO] Generated primes p and q are : ', p, q)
        
        #Step 2:  compute p*q
        modulo_n = p * q
        print('[INFO] Computed modulo_n : ', modulo_n)
        
        #Step3:Compute lambda(n) where lambda is Carmichael's totient function.
        # since p and q are prime  λ(p) = φ(p) = p − 1 and likewise λ(q) = q − 1. 
        # so we lambda of n is lcm of p-1 and q-1
        lambda_n = self.lcm(p-1, q-1)
        print('[INFO] lambda n:', lambda_n)
        
        # Step4: Choose an integer e such that 1 < e < λ(n) and gcd(e, λ(n)) = 1; 
        # that is, e and λ(n) are coprime.
        e = self.get_e(lambda_n)
        print('[INFO] public component: ', e)
        
        #step 5: Determine d as d ≡ e−1 (mod λ(n)); that is, 
        # d is the modular multiplicative inverse of e modulo λ(n)
        # s means: solve for d the equation d⋅e ≡ 1 (mod λ(n)); 
        d = self.get_d(e, lambda_n)
        print('[INFO] Secret component: ', d)
        
        #Done with key generation
        return modulo_n, e, d
    
    def rsa_break_factor(self, n:int)->(int, int):
        '''
        RSA security is lost if we are able to factor.
        Ref: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Integer_factorization_and_RSA_problem

        Parameters
        ----------
        n : int
            factor the number n.

        Returns
        -------
        (int, int)
            returns factors for n.

        '''
        for p in range(2, n):
            if n % p == 0:
                return p, n//p
    
        
if __name__ == '__main__':
    rsa = RCA()
    n ,e, d = rsa.generate_rsa_key(300)
    print("[INFO] Public key (e,n): ", e,n)
    print("[INFO] secret key d: ", d)

    # This is Bob wanting to send a message
    m = 117
    c = m**e % n
    print("[INFO] Bob sends message text: ", m)
    print("[INFO] Bob sends cipher text: ", c)
    
    # This is Alice decrypting the cipher
    m = c**d % n
    print("[INFO] Alice message received", m)
    
    print('[INFO] *** Folllowing is demo for breaking RSA cipher ***')
    print('[INFO] RSA cipher can be break if we can factor a number')
    print('[INFO] Eve trying to break')
    print('[INFO] Eve knows e, n, and c')
    print('[INFO] EVE e, n are: ', e, n)
    print('[INFO] Eve want to factor number n: ', n)
    eve_factors_p, eve_factors_q = rsa.rsa_break_factor(n)
    print('[INFO] Eve calculated factors for number {} are {} and {} '.format(n,  eve_factors_p, eve_factors_q))
    # once Eve has factors he/she can generate private/public keys first calculate lambda_n
    eve_lambda_n = rsa.lcm(eve_factors_p-1, eve_factors_q-1)
    print('[INFO] Eve calulates lambda_n after factorization ', eve_lambda_n)
    print('[INFO] Eve calculates private compoennt d with avilable information')
    eve_d = rsa.get_d(e, eve_lambda_n)
    print('[INFO] Eve calculates private compoennt d with avilable information ', eve_d)
    eve_msg = c**eve_d % n
    print('[INFO] Eve interprted message: ', eve_msg)
    
    # RSA security also depends on type of message we are sending. Suppose assume Bob is not
    # careful in sending a message. Bob wants to send amessage to Alice
    print('[INFO] *** Folllowing is demo for breaking RSA cipher if message is not proper ***')
    print('[INFO] This is Bob not being careful')
    bob_not_careful_message ='Alice is awesome'
    for m_c in bob_not_careful_message:
         bob_c = ord(m_c)**e % n
         print(bob_c, ' ', end="")
    print()

    # Notice above output here we have encryptions. Above for loop prints following
    # 106671  191208  106455  228418  38013  45541  106455  134961  45541  120348 
    # 154079  38013  134961  166247  73092  38013
    # # Notice above output here we have encryptions. Here we are looking from Eve's prespective
    # she does not know what the Bob message is saying to Alice. 
    # But she can see 38013 mutliple times. So letter 'e' encrypted to same thing
    # So Eve could just encrypt all the characters with public key, and construct
    # the message from cipher text. Eve can perform frequency analysis.
    # So there are two points here
    # i. If we use raw message there is no security even though you use big primes.
    # ii. We need some randomness inside the messages. So we pad message with randomness.
    # Eve can do frequency analysis if message is not padded with randomness.
    
    # RSA is determinitistic algorithm so there is no security if we use big primes
    # So we have to include padding i.e., randomness in message. PKCS#1 and OAEP techniques can be
    # used. (See my notes on July 8
    # https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Padding
    







    






















    
    