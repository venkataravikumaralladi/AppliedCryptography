"""
File Created: 8th November 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes: 
        Double Data Encryption Standard (DES): This is 64 bit block and 56 bit key size.
        We use DES algorithm which is already implemented in py_DES.py rather
        than implementing by ourselves.
        DES has a 56-bit key (the key is actually 64 bits, but every 8th bit
        is a parity check; so, only 56 or the 64 bits are meaningful).
        
        Double DES: basically using DES algorithm twice. Here we reduce key space i.e.,
        0 to 255 but use DES algorithm twice. In DES key smallest bit is eliminated
        as mentioned as parity bit so though we have 255 keys we have 7 bit. 
        So for Double DES algorithm we have 14 bit key size. But security is not
        14 bits and this is what we show below.
        
        Here we brute force 7 bits each twice using two different for loops 
        rather than nested for loop. So we can think of security as 9 bits
        instead of 16 bits(here assuming 8 bits we are using). So in 
        summary double DES adds one bit of security. 
        
        Double DES is vulnerable to meet-in-the-middle attack as shown below.
        In this demo we reduced key space to 7 bit  for demo purpose so that
        we can store data in look up dictionary for brute force attack.
        
        3-DES:
            3DES was developed in 1999 by IBM – by a team led by Walter Tuchman.
            3DES prevents a meet-in-the-middle attack. 3DES has a 168-bit key and enciphers blocks of 64
            bits. 3DES effectively has 112-bit security. 
            E( k3,, D( k2, E(k1, p ))).
            Why would we want to do decryption as the second step?
            One reason might be that by taking k2=k1; 2-key, 3DES becomes
            single DES with key . 3DES can communicate with single DES.

        
        

        
'''
from py_DES import *
import random

message = "01234567"
# here we take random key but minimized the key space to one byte
key_11 = random.randrange(0, 256)
# here we are key as per DES algorithm 56-bit key by appending 0's
key_1 = bytes([key_11, 0, 0, 0, 0, 0, 0, 0])

# here we take random key but minimized the key space to one byte
key_21 = random.randrange(0, 256)
# here we are key as per DES algorithm 56-bit key by appending 0's
key_2 = bytes([key_21, 0, 0, 0, 0, 0, 0, 0])

# initialization vector.
iv = bytes([0]*8)

k1 = des(key_1, ECB, iv, pad=None, padmode=PAD_PKCS5)
k2 = des(key_2, ECB, iv, pad=None, padmode=PAD_PKCS5)

# Alice sending the encrypted message
cipher = k1.encrypt(k2.encrypt(message))
print("Key 11:", key_11)
print("Key 21:", key_21)
print("Encrypted", cipher)

# This is Bob
message = k2.decrypt(k1.decrypt(cipher))
print("Decrypted:", message)

# Eve's attack on Double DES
# Insert your Double DES attack here (yes, you are Eve)
# Here we are simulating meet-in-the-middle attack where attacks 
# have knowledge of one message/cipher pair.

lookup = {}
# Note: In this example we have cipher = k1.encrypt(k2.encrypt(message))
for key2 in range(256): #first 8 bits
	brute_frc_key2 = bytes([key2, 0,0,0,0,0,0,0])
	brute_frc_key2_des = des(brute_frc_key2, ECB, iv, pad= None, padmode=PAD_PKCS5)
	lookup[brute_frc_key2_des.encrypt(message)] = key2
    
for key1 in range(256):
    brute_frc_key1 = bytes([key1, 0,0,0,0,0,0,0])
    brute_frc_key1_des = des(brute_frc_key1, ECB, iv, pad= None, padmode=PAD_PKCS5)
    # Meet in the middle means here we are checking if we are meeting above
    # encrypted message in lookup table is meeting with decrypt of cipher with second key.
    if brute_frc_key1_des.decrypt(cipher) in lookup:
        print('brute force key11: ', key1)
        print('brute force key21: ', lookup[ brute_frc_key1_des.decrypt(cipher)])
        brute_frc_key2 = bytes([lookup[ brute_frc_key1_des.decrypt(cipher)], 0,0,0,0,0,0,0])
        brute_frc_key2_des = des(brute_frc_key2, ECB, iv, pad= None, padmode=PAD_PKCS5)
        brute_frc_key1 = bytes([key1, 0,0,0,0,0,0,0])
        brute_frc_key1_des = des(brute_frc_key1, ECB, iv, pad= None, padmode=PAD_PKCS5)
        
        print('Eve breaked message successully: ', 
              brute_frc_key2_des.decrypt(brute_frc_key1_des.decrypt(cipher)))
        break
    
 
