"""
File Created: 16th November 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes on Hash functions:
         One of the application of hash function is to store password as
         shadow file (password) i.e., passwords are stored as hashvalues.
         
         Sample file of how passwords are stored for example in Apple iMac
         is shown in file hash_sample_apple_password_shadow_file.xml
'''

import hashlib

# base64 module provides functions for encoding binary data to printable ASCII characters
#  and decoding such encodings back to binary data
import base64

print('[INFO] *** Demonstrate passwords are stored as hash value ***')
iterations = 45454
salt = base64.b64decode("6VuJKkHVTdDelbNMPBxzw7INW2NkYlR/LoW4OL7kVAI=".encode())
# SALTED-SHA512-PBKDF2 # This is the hash algorithm we are using here, so we used hashlib.pbkdf2_hmac

password = "ps".encode()
# Note: This hash value will matches with hash value stored in
#       hash_sample_apple_password_shadow_file.xml file as we are using same parameters
#       here after we enter password. dklen here is the length of the derived key.
#       e.g. 64 bytes for SHA-512. Here we are asking 128 bytes
mypasswd = hashlib.pbkdf2_hmac("sha512", password, salt, iterations, dklen=128)
value = base64.b64encode(mypasswd)

print('[INFO]: password {} stored as hash value {} '.format(password, value))

print()
print('[INFO] *** Demonstrate importance of salt in password ***')
iterations = 45454
salt_alice = "600".encode()
password_alice = "password".encode()
value_alice = base64.b64encode(hashlib.pbkdf2_hmac("sha512", password_alice, salt_alice, iterations, dklen=128))
print('[INFO] Alice password hash_value {} salt_alice {} and value_alice {} '.format(value_alice, salt_alice, iterations))

salt_bob = "600".encode()
password_bob = "password".encode()
value_bob = base64.b64encode(hashlib.pbkdf2_hmac("sha512", password_bob, salt_bob, iterations, dklen=128))
print('[INFO] Bob password hash_value {} salt_alice {} and value_alice {} '.format(value_bob, salt_bob, iterations))
print('[INFO] Notice above Alice and Bob hash values are same if salt are same')

print()
print('[INFO] *** Demonstrate importance of iterations in password ***')
# Following are known parameters from computer shadow file by attacker
attacker_iterations = 45454
attakcer_salt = base64.b64decode("6VuJKkHVTdDelbNMPBxzw7INW2NkYlR/LoW4OL7kVAI=".encode())
attacker_validation = "SALTED-SHA512-PBKDF2"
attacker_entropy = b'9WS31k6RREVxEdcdl+tzTxAzOnQY3QSLfdsmQlX1UH8ymT4xyHT0fbn+wHlCmqjg4ZrGsSzVZfMyWYwTPwFBCJJSoFh5zfYBvfQwqbgtxZRK8KQrVAoXw8fwHjeaaVQrnPnABLu6rUZb+HwmVTN1Fr5IQ+fBj+pLy3WI/th+DkI='
                   #'9WS31k6RREVxEdcdl+tzTxAzOnQY3QSLfdsmQlX1UH8ymT4xyHT0fbn+wHlCmqjg4ZrGsSzVZfMyWYwTPwFBCJJSoFh5zfYBvfQwqbgtxZRK8KQrVAoXw8fwHjeaaVQrnPnABLu6rUZb+HwmVTN1Fr5IQ+fBj+pLy3WI/th+DkI='

# Here for demo purpose we are assuming password is of two characters
attacker_password = "??".encode()

# Note here above attacker hash value is differnt from actual password as here attacker is
# trying to attack. So attacker tries to guess the password with available information
# as shown below

def guess_password(salt, iterations, entropy):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for c1 in alphabet:
        for c2 in alphabet:
            password = str.encode(c1 + c2)
            # The below line is slow because of number of iterations.
            guess_value = base64.b64encode(hashlib.pbkdf2_hmac("sha512", password, salt,
                                             iterations, dklen=128))
            if guess_value == entropy:
                return password
            
            
attacker_guesspwd = guess_password(attakcer_salt, attacker_iterations, attacker_entropy)
print('[INFO] Attacker guessed password: ', attacker_guesspwd)
# calcutle the entroy with the guessed password
attacker_guess_password_hash_entropy_value = base64.b64encode(hashlib.pbkdf2_hmac("sha512", attacker_guesspwd, 
                                                                    attakcer_salt,
                                             attacker_iterations, dklen=128))
print(len(attacker_guess_password_hash_entropy_value))

