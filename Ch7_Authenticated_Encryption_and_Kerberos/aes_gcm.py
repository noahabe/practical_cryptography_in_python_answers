# this is code given in listing 7-1 and 7-2 of the book.

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
import os, sys, struct 

READ_SIZE = 4096

def encrypt_file(plainpath, cipherpath, password: bytes): 
    # Derive key with a random 16-byte salt 
    salt = os.urandom(16)
    kdf = Scrypt(
        salt=salt, 
        length=32, 
        n = 2 ** 14, 
        r = 8, 
        p = 1, 
        backend=default_backend(),
    )
    key = kdf.derive(password) 

    # Generate a random 96-bit IV. 
    iv = os.urandom(12) 

    # Construct an AES-GCM Cipher object with the given key and IV. 
    encryptor = Cipher(
        algorithm=algorithms.AES(key), 
        mode=modes.GCM(iv),
        backend=default_backend(),
    ).encryptor()
    associated_data = iv + salt 

    # associated_data will be authenticated but not encrypted, 
    # it must also be passed in on decryption. 
    encryptor.authenticate_additional_data(associated_data)

    with open(cipherpath, 'wb+') as fcipher: 
        # Make space for the header (12 + 16 + 16), overwritten last 
        fcipher.write(b'\x00' * (12 + 16 + 16))

        # Encrypt and write the main body 
        with open(plainpath, 'rb') as fplain: 
            for plaintext in iter(lambda: fplain.read(READ_SIZE), b''): 
                ciphertext = encryptor.update(plaintext) 
                fcipher.write(ciphertext)

            ciphertext = encryptor.finalize() # Always b''.
            fcipher.write(ciphertext) # For clarity.

        header = associated_data + encryptor.tag 
        fcipher.seek(0, 0) 
        fcipher.write(header) 

def decrypt_file(cipherpath, plainpath, password: bytes): 
    with open(cipherpath, 'rb') as fcipher: 
        # read the IV (12 bytes) and the salt (16 bytes)
        associated_data = fcipher.read(12 + 16)
        
        iv = associated_data[:12]
        salt = associated_data[12:]

        # derive the same key from the password + salt.
        kdf = Scrypt(
            salt=salt, 
            length=32, 
            n = 2 ** 14, 
            r = 8, 
            p = 1, 
            backend=default_backend(),
        )
        key = kdf.derive(password) 

        # get the tag. GCM tags are always 16 bytes. 
        tag = fcipher.read(16) 

        # Construct an AES-GCM cipher object with the given key and IV
        # For decryption, the tag is passed in as a parameter
        decryptor = Cipher(
            algorithm=algorithms.AES(key),
            mode=modes.GCM(
                initialization_vector=iv, 
                tag=tag,
            ), 
            backend=default_backend(),
        ).decryptor()

        decryptor.authenticate_additional_data(associated_data)

        with open(plainpath, 'wb+') as fplain: 
            for ciphertext in iter(lambda: fcipher.read(READ_SIZE), b''):
                plaintext = decryptor.update(ciphertext) 
                fplain.write(plaintext)
        decryptor.finalize()