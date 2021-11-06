# AppliedCryptography
This repository consists of my notes on cryptography

### Historical ciphers
`Ceaser cipher (ceaser_cipher.py)`: Cipher algorithm woked on the idea of algorithm to keep secret rather than key size. Ceaser cipher key size is 26. Once algorithm is known it is easy to break. This experience gives us important principle in cryptography called as `Kerckchoff's principle`. This principle states that attacker should not able to break the ciphers even attacker knows the algorithim. This is how new cryptography algorithm called as 'AES' is found during open competion. 

`Substituion cipher (substitution_cipher.py)`: Substitution cipher worked on idea that if key size is huge it can not be breaked. Substitution cipher key size is 26! (i.e., 26 factorial) which key size is approximately 88 bits (2^88). But that is not the case we can break substitution cipher with additional knowledge like letter frequency analayis. This is shown in file substitution_cipher_attack.py. Lesson learnt as part of substituion cipher if algorithm is weak even if we have huge key range it is easy to break.

### Modern ciphers
