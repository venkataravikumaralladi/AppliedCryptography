"""
File Created: 16th November 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes on HMAC algorithm: 
        In cryptography, an HMAC (sometimes expanded as either keyed-hash message
        authentication code or hash-based message authentication code) is a specific
        type of message authentication code (MAC) involving a cryptographic hash
        function and a secret cryptographic key. As with any MAC, it may be used
        to simultaneously verify both the data integrity and the authenticity 
        of a message.
        

        HMAC can provide message authentication using a shared secret instead
        of using digital signatures with asymmetric cryptography. It trades off
        the need for a complex public key infrastructure by delegating the key
        exchange to the communicating parties, who are responsible for establishing
        and using a trusted channel to agree on the key prior to communication.
        
        Ref:
            https://en.wikipedia.org/wiki/HMAC
        
'''


import hashlib
import base64

def modify(m):
    l = list(m)
    l[0] = l[0] ^ 1
    return bytes(l)

# Alice and Bob share a secret key
secret_key = "secret key".encode()


# Alice wants to compute a MAC
m = "Hey Bob. You are still awesome.".encode()
sha256 = hashlib.sha256()
sha256.update(secret_key)
sha256.update(m)
hmac = base64.b64encode(sha256.digest())
print('[INFO] Alice message {} and hmac value {}'.format(m, hmac))

# Eve comes along
print('[INFO] Eve modifying message ')
m = modify(m)
print('[INFO] Eve modified message ', m)

# Bob receives and validates the HMAC
sha256 = hashlib.sha256()
sha256.update(secret_key)
sha256.update(m)
hmac = base64.b64encode(sha256.digest())
print('[INFO] Bob message {} and hmac value {}'.format(m, hmac))
print('[INFO] Note IMP bob hmac value is differnet from Alice hmac as Eve has modified message \
              this way Bob confirms message is changed. ')


