"""
File Created: 29th September 2021
Author: Venkata Ravi K A
-----

"""

import pytest
from cryptography.substitution_cipher import SubstitutionCipher

@pytest.fixture
def create_subs_obj() -> SubstitutionCipher:
    return SubstitutionCipher(seed=237)

class TestSubstitutionCipher:
    def test_get_encryption_key(self,
                                create_subs_obj : SubstitutionCipher):
        expected_encr_key = {'A': 'T', 'B': 'P', 'C': 'F', 'D': 'I', 'E': 'Q', 'F': 'B',
                             'G': 'H', 'H': 'X', 'I': 'U', 'J': 'A', 'K': 'Z', 'L': 'O',
                             'M': 'D', 'N': 'W', 'O': 'S', 'P': 'L', 'Q': 'M', 'R': 'V',
                             'S': 'K', 'T': 'C', 'U': 'N', 'V': 'R', 'W': 'Y', 'X': 'E',
                             'Y': 'G', 'Z': 'J'}
        
        encr_key = create_subs_obj.generate_encr_key()      
        assert encr_key == expected_encr_key
        
        
    def test_get_encrypt_message(self,
                                 create_subs_obj : SubstitutionCipher):
        
        create_subs_obj.generate_encr_key()
        encry_text = create_subs_obj.encrypt('HELLO WORLD')
        expected_encry_text = 'XQOOS YSVOI'
        
        assert encry_text == expected_encry_text

    def test_get_decrypt_message(self,
                                 create_subs_obj : SubstitutionCipher):
        
        create_subs_obj.generate_encr_key()
        msg = 'YOU ARE AWESOME'
        encry_text = create_subs_obj.encrypt(msg)
        decryp_msg = create_subs_obj.decrypt(encry_text)
        
        assert decryp_msg == msg