"""
File Created: 29th September 2021
Author: Venkata Ravi K A
-----

"""

import pytest
from cryptography.ceaser_cipher import CessarCipher

@pytest.fixture
def create_cipher_obj() -> CessarCipher:
    return CessarCipher()

class TestCeaserCipher:
    def test_get_encryption_key(self,
                                create_cipher_obj : CessarCipher):
        encr_key = create_cipher_obj.generate_encr_key(3)
        expected_encr_key = {'A': 'D', 'B': 'E', 'C': 'F', 'D': 'G', 'E': 'H',
                             'F': 'I', 'G': 'J', 'H': 'K', 'I': 'L', 'J': 'M',
                             'K': 'N', 'L': 'O', 'M': 'P', 'N': 'Q', 'O': 'R',
                             'P': 'S', 'Q': 'T', 'R': 'U', 'S': 'V', 'T': 'W',
                             'U': 'X', 'V': 'Y', 'W': 'Z', 'X': 'A', 'Y': 'B', 
                             'Z': 'C'}
        
        assert encr_key == expected_encr_key
        
        
    def test_get_encrypt_message(self,
                                 create_cipher_obj : CessarCipher):
        create_cipher_obj.generate_encr_key(3)
        encry_text = create_cipher_obj.encrypt('HELLO WORLD')
        expected_encry_text = 'KHOOR ZRUOG'
        
        assert encry_text == expected_encry_text

    def test_get_decrypt_message(self,
                                 create_cipher_obj : CessarCipher):
        
        create_cipher_obj.generate_encr_key(3)
        msg = 'HELLO WORLD'
        encry_text = create_cipher_obj.encrypt(msg)
        decryp_msg = create_cipher_obj.decrypt(encry_text)
        
        assert decryp_msg == msg