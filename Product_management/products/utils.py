from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Secret key, ensure it is securely generated and stored
SECRET_KEY = os.urandom(32)  # 32 bytes = 256 bits for AES-256
print("Secret Key:", SECRET_KEY.hex())


def encrypt_data(plain_text):
    iv = os.urandom(16)  # Initialization vector for AES
    cipher = Cipher(
        algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()

    # Padding to ensure the plaintext length is a multiple of block size (16 bytes for AES)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    encrypted_text = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_text  # Combine IV and encrypted text


def decrypt_data(encrypted_text):
    iv = encrypted_text[:16]  # Extract the first 16 bytes as the IV
    encrypted_data = encrypted_text[16:]
    cipher = Cipher(
        algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend()
    )
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(decrypted_data) + unpadder.finalize()
    return plain_text.decode()
