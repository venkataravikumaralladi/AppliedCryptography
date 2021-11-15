# AppliedCryptography
This repository consists of my notes on cryptography

### Historical ciphers
`Ceaser cipher (ceaser_cipher.py)`: Cipher algorithm woked on the idea of algorithm to keep secret rather than key size. Ceaser cipher key size is 26. Once algorithm is known it is easy to break. This experience gives us important principle in cryptography called as `Kerckchoff's principle`. This principle states that attacker should not able to break the ciphers even attacker knows the algorithim. This is how new cryptography algorithm called as 'AES' is found during open competion. 

`Substituion cipher (substitution_cipher.py)`: Substitution cipher worked on idea that if key size is huge it can not be breaked. Substitution cipher key size is 26! (i.e., 26 factorial) which key size is approximately 88 bits (2^88). But that is not the case we can break substitution cipher with additional knowledge like letter frequency analayis. This is shown in file substitution_cipher_attack.py. Lesson learnt as part of substituion cipher if algorithm is weak even if we have huge key range it is easy to break.

### Modern ciphers
Modern Crpytography basic idea is based on `XOR` function. It has interesting property (message ^ random = cipher) and (cipher ^ random = message).

1. `One Time Pad (one_time_pad.py)`: It is unbreakable cipher because it is mathematically proven, but it is not practical to implement. So we use lower end of OTP for example 3DES. Stream ciphers are comprimised implementation of OTP. The One Time Pad is simply an XOR function. Here security lies in the random key stream. The beauty of OTP is the simplicity and proof that it is information theoretical secure given a TRUE random key stream. Requirments that OTP is unbreakable are i. key stream only used once. ii. key stream is generated by true randomness.
  The security of OTP can be understood as follows:

    - Given a cipher text
    - Guess a plain text of the same length.
    - Then there is a matching key stream that will decrypt the cipher text to that plain text.
    - As any key stream is possible it could be plain text        

    OTP is secured because if we guess a message we can generate that random key to get that message given cipher text, so all messages are equally likely. So if we
    decrpyt to any   thing then it does not matter how much computing power you have because we can never know if it is right one or not.

2. `Stream cipher (vrk_stream_cipher.py`: A stream cipher is like a OTP but don't have requirments like OTP. So stream cipher does not use TRUE randomness and can re-use keystream. Example of stream ciphers are A5/1 (G2 encryption) - 54 bits, A5/2 (export version)-17 bits, RC4 (WEP, SSL)-40 TO 2048 bits.  Stream cipher uses Pseudo random generator. In the implementation I used Linear Congruential generator (LCG) Ref: https://en.wikipedia.org/wiki/Linear_congruential_generator which is implemented in `C` language as reference.  
One great advantage of stream cipher is that if a bit is flipped by poor connection only that bit will be affected in the decryption.
Disadvantage of stream ciphers are stream ciphers cannot be authenticated, low entropy in pesudo-randomness, and reusability of key to name a few.

3. `DES cipher (des_usage.py and double_des_usage.py `:  Data Encryption Standard (DES): This is 64 bit block and 56 bit key size. We use DES algorithm which is already implemented in py_DES.py rather than implementing by ourselves. DES has a 56-bit key (the key is actually 64 bits, but every 8th bit is a parity check; so, only 56 of the 64 bits are meaningful).       
        Padding related notes in DES: DES also adds padding to encrypted message. DES algorithm requires that the input data to be 8-byte blocks. If you want to encrypt a text message that is not multiples of 8-byte blocks, the text message must be padded with additional bytes to make the text message to be multiples of 8-byte blocks. PKCS stands for public key cryptography standards
        
      Double DES: basically using DES algorithm twice. This is vulnerable to meet-in-the-middle attack. This can be fixed by using 3-DES algorithm

4. `Diffie-Hellman cipher (diffie_hellman_analysis.py `:  Key exchange between two parties in secured way is major challenge in symmetric key encryption algorithm. This is solved by idea provided by Diffie-Hellman algorithm which is based on discrete log problem which is hard to break. Diffie-Hellman algorithm idea is based on generator, modulus and prime numbers. A generator 'g' generates all the non-zero elements in the modulus. For example a generator 'g' modulus 7 will generate the elements 1,2,3,4,5, and 6 (but not in that order). The task is to find the smallest generator 'g' that generates all the elements 1,2,3,4,5 and 6 by calculating `g**0, g**1, g**2, g**3, g**4, g**5, and g**6`. In this example we can see that g=2 does not satisfy where as g=3 satisfies. Python implementation of primitives required for Diffie-Hellman and key generation is implemented in diffie_hellman_analysis.py
