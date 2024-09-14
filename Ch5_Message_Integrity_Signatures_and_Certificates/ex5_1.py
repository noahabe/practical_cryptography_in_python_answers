# ex5_1.py 

# FAKE MAC WITH SYMMETRIC ENCRYPTION
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib


class MessageWasTamperedWithError(Exception):
    '''
    Raised when the ciphertext has been tampered with 
    by Eve.
    '''

    def __init__(self, expected_mac: str, actual_mac: str):
        self.expected_mac = expected_mac
        self.actual_mac = actual_mac

    def __str__(self): 
        return f"\nExpected: {self.expected_mac}.\nBut got: {self.actual_mac}"

class Encryptor:
    def __init__(self, key, nonce):
        aesContext = Cipher(
            algorithms.AES(key),
            modes.CTR(nonce),
            backend=default_backend()
        )
        self.encryptor = aesContext.encryptor()
        self.hasher = hashlib.sha256()

    def update_encryptor(self, plaintext):
        ciphertext = self.encryptor.update(plaintext)
        self.hasher.update(ciphertext)
        return ciphertext

    def finalize_encryptor(self):
        return self.encryptor.finalize() + self.hasher.digest()


class Decryptor:
    def __init__(self, key: bytes, nonce: bytes, digest: bytes):
        aesContext = Cipher(
            algorithms.AES(key),
            modes.CTR(nonce),
            backend=default_backend()
        )
        self.decryptor = aesContext.decryptor()
        self.hasher = hashlib.sha256()
        self.digest = digest

    def update_decryptor(self, ciphertext: bytes):
        '''Make sure that ciphertext doesn't include the MAC'''
        plaintext = self.decryptor.update(ciphertext)
        self.hasher.update(ciphertext)
        return plaintext

    def finalize_decryptor(self):
        if self.hasher.digest() != self.digest:
            raise MessageWasTamperedWithError(
                expected_mac=self.hasher.digest(),
                actual_mac=self.digest
            )
        return self.decryptor.finalize()

    @staticmethod
    def get_mac(ciphertext: bytes):
        return ciphertext[-32:]


if __name__ == '__main__':
    key = os.urandom(32)
    nonce = os.urandom(16)

    encryptionManager = Encryptor(key, nonce)
    plaintext = b"Hi Bob, this is Alice !"
    ciphertextWithMac = encryptionManager.update_encryptor(plaintext)
    ciphertextWithMac += encryptionManager.finalize_encryptor()

    decryptionManager = Decryptor(
        key=key, nonce=nonce, digest=Decryptor.get_mac(ciphertextWithMac))
    _plaintext = decryptionManager.update_decryptor(
        ciphertext=ciphertextWithMac[:-32])
    _plaintext += decryptionManager.finalize_decryptor()

    assert (plaintext == _plaintext)

    print("[+] Successful!!")