"""
File Created: 8th November 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes: 
        Data Encryption Standard (DES): This is 64 bit block and 56 bit key size.
        We use DES algorithm which is already implemented in py_DES.py rather
        than implementing by ourselves.
        DES has a 56-bit key (the key is actually 64 bits, but every 8th bit
        is a parity check; so, only 56 or the 64 bits are meaningful).
        
        Padding related notes in DES:
            
        DES also adds padding to encrypted message. DES algorithm requires that
        the input data to be 8-byte blocks. If you want to encrypt a text message
        that is not multiples of 8-byte blocks, the text message must be padded
        with additional bytes to make the text message to be multiples of 8-byte
        blocks. PKCS stands for public key cryptography standards

        PKCS5 Padding schema is actually very simple. It follows the following rules:

            The number of bytes to be padded equals to 
                "8 - numberOfBytes(clearText) mod 8". So 1 to 8 bytes will be padded 
                to the clear text data depending on the length of the clear text data.
                
            All padded bytes have the same value - the number of bytes padded.
            PKCS5Padding schema can also be explained  below, if M is the 
            original clear text and PM is the padded clear text:

                    If numberOfBytes(clearText) mod 8 == 7, PM = M + 0x01
                    If numberOfBytes(clearText) mod 8 == 6, PM = M + 0x0202
                    If numberOfBytes(clearText) mod 8 == 5, PM = M + 0x030303
                    ...
                    If numberOfBytes(clearText) mod 8 == 0, PM = M + 0x0808080808080808

        
'''
from py_DES import *


print('*** Scenario 1:  How block modes helps us in encrypting same block to different encrypted values ')

# below message we have repeated 8 characters.First 8 characters are 01234567
# and second 8 characters are same as first set i.e., 01234567.
# DES block size is 64bits.
message = "0123456701234567"

# key is 8 bytes, though key size of DES is 56 bits.
key = "DESCRYPT"

# Initialization vector
iv = bytes([0]*8)
# create the cipher here
# demo 1: ECB mode
# k = des(key, ECB, iv, pad=None, padmode=PAD_PKCS5)
# demo 2: CBC mode
k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
cipher = k.encrypt(message)


# Alice sending the encrypted message
# encrypt the message to cipher
print("Length of plain text:", len(message))
print("Length of cipher text:", len(cipher))
print('Encrypted: ', cipher[0:8])
print('Encrypted: ', cipher[8:16])
print('Encrypted: ', cipher[16:])

# Bob decrypting the cipher text
# decrypt the cipher to message
print("Decrypted:", message)

'''
Notes:
    Length of cipher is more than message because of padding
Output of above algorithm: with demo 1: mode: ECB mode
    
Length of plain text: 16
Length of cipher text: 24
Encrypted:  b'\xa9\xe2\xa1-\x00\xe09\xb7'
Encrypted:  b'\xa9\xe2\xa1-\x00\xe09\xb7'
Encrypted:  b'\x00\xb1\xc4\xec\x90\xea\xa3\xde'
Decrypted: 0123456701234567

Notice in above output first block and second block are encrypted to same as we
used ECB block mode. 
See reference: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation.
This is well explained with image encrytion
    A striking example of the degree to which ECB can leave plaintext data patterns 
    in the ciphertext can be seen when ECB mode is used to encrypt a bitmap image
    which uses large areas of uniform color. While the color of each individual 
    pixel is encrypted, the overall image may still be discerned, as the pattern
    of identically colored pixels in the original remains in the encrypted version.
    
Output of above algorithm: with demo 2: mode: CBC mode

    Length of plain text: 16
    Length of cipher text: 24
    Encrypted:  b'\xa9\xe2\xa1-\x00\xe09\xb7'
    Encrypted:  b'\xc3J\x8eG\x0eu\x8bS'
    Encrypted:  b'\xeag\xf9$\x1c\xde\xa7f'
    Decrypted: 0123456701234567

'''

print(' *** Scenario 2: Modifying single bit will effect multiple bits in block cipher. *** ')
def modify(cipher:str)->str:
    '''
    

    Parameters
    ----------
    cipher : str
        cipher text to modify.

    Returns
    -------
    modified cipher text.

    '''
    # insert code here
    modify = [0]*len(cipher)
    modify[10] = ord(' ') ^ ord('1')
    modify[11] = ord(' ') ^ ord('0')
    modify[12] = ord('1') ^ ord('1')
    return bytes([modify[i] ^ cipher[i] for i in range(len(cipher))])

alice_message = "Give Bob:    10$ and send them to him"
alice_key = "DESCRYPT"
alice_iv = bytes([0]*8)
alice_des = des(alice_key, CBC, alice_iv, pad=None, padmode=PAD_PKCS5)


# Alice sending the encrypted message
alice_cipher = alice_des.encrypt(alice_message)
print("Alice Length of plain text:", len(alice_message))
print("Alice Length of cipher text:", len(alice_cipher))
print("Alice Encrypted:", alice_cipher)

# Bob modifying the cipher text
print('Bob modifyting cipher and Bob does not know any thing about the key ')
alice_cipher = modify(alice_cipher)

# this is the bank decrypting the message
bank_message = alice_des.decrypt(alice_cipher)
print("Bank Decrypted message ", bank_message)

'''
 Notice here changing bits here change the meaning of message and is not decryptable
 which adds more security in block cipher then stream cipher.
 It is found that by modifying the one single bit or byte of block, DES will destroy
 entire text of the block to unredable by decrypter.
 
 *** Scenario 2: Modifying single bit will effect multiple bits in block cipher. *** 
        Alice Length of plain text: 37
        Alice Length of cipher text: 40
        Alice Encrypted: b'\xe7p\xdcX\x0fdr\xa2^Z\xd9nG\x1a6\xb5\x00]s\xd6\x90d\xf7\xd3\x19&us.\xa4\x03X\x80Qji\xe1x\xd7!'
        Bob modifyting cipher and Bob does not know any thing about the key 
        Bank Decrypted message  b'Give Bob\xd7\xb2\xcd\xfb4Q[\xf5 a\x7ft send them to him'
'''
