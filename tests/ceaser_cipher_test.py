"""
File Created: 3rd September 2021
Author: Daniel Dorosz 
-----

"""


from cryptography.ceaser_cipher import CessarCipher

class TestCeaserCipher:
    def test_get_encryption_key(self):
        ceaser_ciph = CessarCipher()
        encr_key = ceaser_ciph.generate_encr_key(3)
        expected_encr_key = {'A': 'D', 'B': 'E', 'C': 'F', 'D': 'G', 'E': 'H',
                             'F': 'I', 'G': 'J', 'H': 'K', 'I': 'L', 'J': 'M',
                             'K': 'N', 'L': 'O', 'M': 'P', 'N': 'Q', 'O': 'R',
                             'P': 'S', 'Q': 'T', 'R': 'U', 'S': 'V', 'T': 'W',
                             'U': 'X', 'V': 'Y', 'W': 'Z', 'X': 'A', 'Y': 'B', 
                             'Z': 'C'}
        
        assert encr_key == expected_encr_key
        
        
    def test_get_encrypt_message(self):
        ceaser_ciph = CessarCipher()
        ceaser_ciph.generate_encr_key(3)
        encry_text = ceaser_ciph.encrypt('YOU ARE AWESOME')
        expected_encry_text = 'BRX DUH DZHVRPH'
        
        assert encry_text == expected_encry_text

    def test_get_decrypt_message(self):
        ceaser_ciph = CessarCipher()
        ceaser_ciph.generate_encr_key(3)
        msg = 'YOU ARE AWESOME'
        encry_text = ceaser_ciph.encrypt(msg)
        decryp_msg = ceaser_ciph.decrypt(encry_text)
        
        assert decryp_msg == msg