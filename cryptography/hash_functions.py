"""
File Created: 16th November 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes on Hash functions
        We want hash functions to have following properties
            i. It is one way deterministic function
            ii. The output is dependent on all input bits.
            iii. Output is uniformly distributed.
            iv. Impossible (difficult) to make a collision.
        
        Hashfunctions are used in 
                     digital signatures (uses asymmertic key)
                     shadow file (password) i.e., passwords are stored as hashvalues
                     HMAC use symmetirc key
        
        Ref:
            https://docs.python.org/3/library/hashlib.html
            
           
        
'''

import hashlib


print('[INFO] *** demonstrate first property of hash function one way deterministic function ***')
msg_detr_test = "This is the hash value message".encode()

sha256_1 = hashlib.sha256()
# Now feed the above object with bytes-like objects (normally bytes) using the update() method.
sha256_1.update(msg_detr_test)
d1 = sha256_1.digest()
print('[INFO] First time: hash value of message {} using sha256 is {} '.format(msg_detr_test, d1))

# If wd do that again we get exact same hash digest which confirms that it is one way deterministic function
sha256_2 = hashlib.sha256()
# Now feed the above object with bytes-like objects (normally bytes) using the update() method.
sha256_2.update(msg_detr_test)
d2 = sha256_2.digest()
print('[INFO] Second time: hash value of message {} using sha256 is {} '.format(msg_detr_test, d1))
print('[INFO] notice above in both cases we got same hash value for same message which confirms determinitic')

# Second property is that hash value should depend on all input. i.e., 
# if we change one bit in message hash value should change like unpredictable.
print('[INFO] *** demonstrate second  property of hash function value output should depend on all input ***')
def modify(m:str)->bytes:
	l = list(m)
	l[0] = l[0] ^ 1 # modify one bit
	return bytes(l)

modify_msg = modify(msg_detr_test)
print('[INFO] modify message is: ', modify_msg)
# calculate hash value for modify message
sha256_3 = hashlib.sha256()
# Now feed the above object with bytes-like objects (normally bytes) using the update() method.
sha256_3.update(modify_msg)
d3 = sha256_3.digest()
print(d3) # compare with d2 which is completely different.
print('[INFO] Modify message {} using sha256 hash value is {} '.format(msg_detr_test, d3))
print('[INFO] above you can see that single bit change causes hash value changed undeterministically')


print('[INFO] *** DIGITAL SIGNATURE DEMO using RSA and Hash functions ***')
print('[INFO] step 1: generate Alice private and public compononets from rsa.py and copy here')
# These are Alice's RSA keys
# Public key (e,n): 5 170171
# Secret key (d) 9677
n = 170171
e = 5
d = 9677
print('[INFO]: Alice public key n: {} and e: {}'.format(n,e))
print('[INFO]: Alice private key n: {} and d: {}'.format(n, d))

# This is the message that Alice wants to sign and send to Bob
alice_message = "Bob you are awesome".encode()

# Step 1: hash the message
sha256 = hashlib.sha256()
sha256.update(alice_message)
h = sha256.digest()

# we need to convert the digest from bytes to integer 
# If you notice above hash value is bigger than modulus since we used smaller values in
# key generation so we do mod n for h. So we get modified minimum hash value.
# In real time we don't do mod n. But here we are doing this as we are small 
# values for key generation for demo purpose.
h = int.from_bytes(h, "big") % n
print("[INFO] Step1: Alice calcutes hash value of message {} hash value is {} ".format(alice_message, h))

# Step 2: decrypt the hash value (use secret exponent)
print('[INFO] Alice sign the message with private key')
sign = h**d % n
print('[INFO] Alice sign the message {} with private key sign value {}'.format(alice_message, sign))

# Step 3: send message with signature to Bob
print('[INFO] Alice sending message to Bob')


# This is Eve being evil and modifies the message
# INSERT CODE HERE THAT MODIFIES THE MESSAGE
def modify(m):
    l = list(m)
    l[0] = l[0] ^ 1
    return bytes(l)
# uncomment below line to test modify message   
# message = modify(alice_message)
message = alice_message



# Bob verifying the signature
print('[INFO] Bob verifying the signature')
# Step 1: calculate the hash value of the message
sha256 = hashlib.sha256()
sha256.update(message)
h = sha256.digest()

# we need to convert the digest from bytes to integer 
# If you notice above hash value is bigger than modulus since we used smaller values in
# key generation so we do mod n for h. So we get modified minimum hash value.
# In real time we don't do mod n. But here we are doing this as we are small 
# values for key generation for demo purpose.
h = int.from_bytes(h, "big") % n
print("[INFO] Step1: Bob calcutes hash value of recvd message {} hash value is {} ".format(message, h))

# Step 2: Verify the signature
verification = sign**e % n
print('[INFO] Step2: Bob verifies the signature with Alice public key value is: ', verification)

if verification != h:
    print('[INFO] Message has been modified')
else:
    print('[INFO] Verification correct')
