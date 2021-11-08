"""
File Created: 6th November 2021
Author: Venkata Ravi K A 
-----

"""

'''
    Notes: 
        A stream cipher is like a OTP but don't have requirments like OTP.
        So stream cipher does not use TRUE randomness and can re-use keystream.
        Example of stream ciphers are A5/1 (G2 encryption) - 54 bits,
                                      A5/2 (export version)-17 bits,
                                      RC4 (WEP, SSL)-40 TO 2048 bits
                                      
    Generate random key string:
        
        We need to generate random key string. Note here important point is that
        key should not be entirely random because we should be able to regenerate it.
        So you have a randomness that you generate the sequence of random bytes,
        it would be possible for your receiver to regenerate that coming from a 
        small key.
        So key is like starting the sequence of randomness engine to keep it random.
        
        Important point of stream cipher is that stream cipheres are like OTP except that
        we need to able to make a random sequence that can be regenerated. So we use
        Linear Congruential generator (LCG) Ref: https://en.wikipedia.org/wiki/Linear_congruential_generator
        
    Advantages of stream cipher:
        1. One great advantage of stream cipher is that if a bit is flipped by poor connection
           only that bit will be affected in the decryption.
        
        
'''
import random

class KeyStream:
    '''
    Generates keystream for stream cipher using Linear Congruential Generator (LCG)
    '''
    def __init__(self, key:int=1):
        '''
        constructor for KeyStream class.

        Parameters
        ----------
        key : int, optional
            DESCRIPTION. The default is 1.
                         key acts a seed for LCG.

        Returns
        -------
        None.

        '''
        self.init = key
        self.next = key
        # below are constants according to ANSI C https://en.wikipedia.org/wiki/Linear_congruential_generator
        self.a    = 1103515245
        self.c    = 12345
        return
    
    def reset(self):
        '''
        Resets the random key to initial seed value

        Returns
        -------
        None.

        '''
        self.next = self.init
    
    def rand(self) -> int:
        '''
        Implements random according to LCG defined in C https://en.wikipedia.org/wiki/Linear_congruential_generator

        Returns
        -------
        int
            DESCRIPTION.

        '''
        self.next = (self.a * self.next + self.c) % 2**31
        return self.next
    
    
    def get_key_byte(self) -> int:
        '''
        Often in random function we don't reveal its higher state ie. return value of rand function
        so we only take one byte by taking mod of 256. i.e., generates random number from 0 to 256

        Returns
        -------
        int
            DESCRIPTION.

        '''
        # return self.rand() % 256
        # corrected the bug above to increase random bit size from 8 bit to 31 bits.
        # with this change low entropy bug eve cannot able to decrypt with brute force.
        return (self.rand() // 2**23)%256
    
class VRKStreamCipher:
    '''
    Simple stream cipher class
    '''
    def __init__(self, key:KeyStream):
        '''
        constructor for simple stream cipher class. For stream cipher
        encrypt and decrypt function is same.

        Parameters
        ----------
        key : KeyStream
            key stream used for encryption and decrption.

        Returns
        -------
        None.

        '''
        self.key = key
        return
    
    def encrypt(self, message:str)->bytes :
        '''
        encrypt and decrypt the message based on the input message

        Parameters
        ----------
        message : str
            input message which can be either message or cipher text.

        Returns
        -------
        bytes 
            returns byte stream of message or cipher based on input message.

        '''
        
        return bytes([message[i] ^ self.key.get_key_byte() for i in range(len(message))])
    
    
    def transmit(self, cipher:bytes, liklihood:int) -> bytes:
        '''
        We want to do is simulate during transmit to flip a bit in a message

        Parameters
        ----------
        cipher : bytes
            DESCRIPTION.
        liklihood : int
            DESCRIPTION.

        Returns
        -------
        bytes
            DESCRIPTION.

        '''
        b = []
        for char in cipher:
            if random.randrange(0, liklihood) == 0:
                # flip one bit at random from 0 to 7 position
                val = 2 ** random.randrange(0,8)
                char = char ^ val
            b.append(char)
        return bytes(b)
    
    def modify_bnk_specific_msg(self, cipher:str) -> bytes:
        '''
        Here we are assuming we know the format of message as below
        Send Bob:   10$

        Parameters
        ----------
        cipher : str
            DESCRIPTION.

        Returns
        -------
        bytes
            DESCRIPTION.

        '''
        mod = [0] * len(cipher)
        mod[10] = ord(' ') ^ ord('1')
        mod[11] = ord(' ') ^ ord('0')
        mod[12] = ord('1') ^ ord('0')
        
        return bytes(mod[i] ^ cipher[i] for i in range(len(cipher)))
    
# helper function to simulate key reuse problem
def get_key_to_simulate_keyreuse_eve(msg:str, cipher:bytes)->bytes:
    return bytes([msg[i] ^ cipher[i] for i in range(len(cipher))])

# helper function to simulate key reuse problem
def crack_cipher_keyreuse_eve(eves_key_stream:bytes, alice_reuse_second_cipher:bytes)->bytes:
    length = min(len(eves_key_stream), len(alice_reuse_second_cipher))
    return bytes([eves_key_stream[i] ^ alice_reuse_second_cipher[i] 
                  for i in range(length)])

# helper function to simulate brute force attack on low entropy randomness
def simulate_brute_force_attk_key(message:str, cipher:str)->bytes:
    for k in range(2**31):
        bf_key = KeyStream(k)
        for i in range(len(message)):
            xor_value = message[i] ^ cipher[i]
            if xor_value != bf_key.get_key_byte():
                break
            else:
                return k
    return False
    
    
if __name__ == '__main__':
    key = KeyStream(10)   
    strm_cipher = VRKStreamCipher(key)
    message = "Hello World!".encode()
    cipher = strm_cipher.encrypt(message)
    # output of cipher below: b'3\xfd\x9d\xba8dz\r\x81\xdcM\x8f'
    print(cipher)
    # let us simulate the scramble a bit 
    cipher = strm_cipher.transmit(cipher, 5)
    print('now decrypting...')  
    # reset the key to beginning so same first random values used to encrypt are used for decrypt.
    key.reset()
    print(strm_cipher.encrypt(cipher)) # output: b'Jel,o World!'
    
    #Following scenario explains problem of authenticity in stream cipher
    print('*** simulating authentication problem in stream cipher ***')
    #This is Alice
    print('This is Alice')
    alice_key = KeyStream(10)
    alice_strm_cipher = VRKStreamCipher(alice_key)
    alice_msg_to_bank = 'Send Bob:   10$'.encode()
    print('Alice sent message: ', alice_msg_to_bank)
    alice_msg_cipher = alice_strm_cipher.encrypt(alice_msg_to_bank)
    print('Alice send message cipher: ', alice_msg_cipher)

    # This is Bob modifying the message
    print('This is Bob acting like Eve')
    alice_msg_cipher = alice_strm_cipher.modify_bnk_specific_msg(alice_msg_cipher)

    # This is the Bank
    print('This is bank')
    bank_key = KeyStream(10)
    bank_strm_cipher = VRKStreamCipher(bank_key)
    bank_msg_recvd_from_alice = bank_strm_cipher.encrypt(alice_msg_cipher)
    print('bank message is: ', bank_msg_recvd_from_alice)
    
    #Following scenario explains the problem of key reusability in stream cipher
    print('*** simulating key reuse problem in stream cipher ***')
    # This is the message that Eve gives Alice
    eve_message = "This is my long message that Eve tricks Alice into using".encode()

    # This is Alice
    print('Key reuse: This is Alice sending eve message to Bob')
    print('Alice first msg: ', eve_message)
    alice_key_reuse = KeyStream(10)
    alice_reuse_key_strm_cipher = VRKStreamCipher(alice_key_reuse)
    alice_reuse_key_cipher = alice_reuse_key_strm_cipher.encrypt(eve_message)
    print('Alice first msg cipher: ', alice_reuse_key_cipher)

    # This is Eve getting the key stream
    print('This is Eve interpreting cipher message and getting key')
    eves_key_stream = get_key_to_simulate_keyreuse_eve(eve_message, alice_reuse_key_cipher)
    print('Eve extacted key: ', eves_key_stream)

    # This is Bob
    print('Key reuse: This is bob receiving first message from Alice')
    bob_reuse_key = KeyStream(10)
    bob_reuse_key_strm_cipher = VRKStreamCipher(bob_reuse_key)
    bob_reuse_key_first_msg = bob_reuse_key_strm_cipher.encrypt(alice_reuse_key_cipher)
    print('Bob receiving first message ', bob_reuse_key_first_msg )

    # This is Alice sending a new message
    print('Key reuse: This is Alice sending another message to Bob with same key as before')
    alice_reuse_second_message = "Hey Bob. Let's take over the world domination.".encode()
    print('Alice sendin second message: ', alice_reuse_second_message )
    alice_resue_key_second = KeyStream(10)
    alice_reuse_key_second_strm_cipher = VRKStreamCipher(alice_resue_key_second)
    alice_reuse_second_cipher = alice_reuse_key_second_strm_cipher.encrypt(alice_reuse_second_message)
    
    # This is Eve extracting the message
    print('This is Eve cracking the second message seen as cipher')
    eves_decryption = crack_cipher_keyreuse_eve(eves_key_stream, alice_reuse_second_cipher)
    print(eves_decryption)
    
    print('*** simulating low entropy *** ')
    # This is Alice
    secret_key = 34567
    print('Alice low entropy secret key: ', secret_key)
    alice_low_entroypy_key = KeyStream(secret_key)
    header = "MESSAGE: "
    alice_low_entroypy_message = header + "My secret message to Bob"
    alice_low_entroypy_message = alice_low_entroypy_message.encode()
    alice_low_entropy_key_strm_cipher = VRKStreamCipher(alice_low_entroypy_key)
    low_entroypy_cipher = alice_low_entropy_key_strm_cipher.encrypt( alice_low_entroypy_message)

    # This is Bob
    bob_low_entropy_key = KeyStream(secret_key)
    bob_low_entropy_key_strm_cipher = VRKStreamCipher(bob_low_entropy_key)
    bob_low_entropy_message = bob_low_entropy_key_strm_cipher.encrypt( low_entroypy_cipher)
    print('Bob low entropy recvd: ', bob_low_entropy_message)
    
    # This is Eve
    # Here how does Eve knows this is correct decrytion. This is where header
    # comes in to the picture, i.e., structure of the message comes in like header
    # that attacker knows.
    # 
    bf_key = simulate_brute_force_attk_key(header.encode(), low_entroypy_cipher)
    print("Eve's brute force key:", bf_key)
    eve_low_entropy_key = KeyStream(bf_key)
    eve_low_entropy_key_strm_cipher = VRKStreamCipher(eve_low_entropy_key)
    eve_low_entropy_message = eve_low_entropy_key_strm_cipher.encrypt(low_entroypy_cipher)
    print('Eve decripyted low entropy message: ', eve_low_entropy_message)


    
    
    