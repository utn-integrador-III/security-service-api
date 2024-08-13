import os
import base64
from decouple import config
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class EncryptionUtil:
    def __init__(self):
        # Retrieve the password from an environment variable
        self.password = config('ENCRYPTION_PASSWORD').encode()

    def encrypt(self, data):
        # Check if the input data is a non-empty string
        if not isinstance(data, str) or not data:
            raise ValueError("Input data must be a non-empty string.")

        try:
            # Convert data to bytes
            data = data.encode()
            # Apply PKCS7 padding to the data
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(data) + padder.finalize()

            # Generate a unique salt for each encryption
            salt = os.urandom(16)

            # Derive a key from the password using PBKDF2HMAC with SHA256
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(self.password)

            # Generate a random IV (Initialization Vector)
            iv = os.urandom(16)
            # Create a Cipher object with the derived key and IV
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            # Encrypt the padded data
            ct = encryptor.update(padded_data) + encryptor.finalize()

            # Concatenate salt, IV, and ciphertext
            encrypted_data = salt + iv + ct
            # Encode the result to base64 for safe transmission/storage
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt(self, encrypted_data):
        # Check if the input encrypted data is a non-empty string
        if not isinstance(encrypted_data, str) or not encrypted_data:
            raise ValueError("Input encrypted data must be a non-empty string.")

        try:
            # Decode the base64 encoded encrypted data
            encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            # Extract the salt, IV, and ciphertext from the encrypted data
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ct = encrypted_data[32:]

            # Derive the key from the password using the extracted salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(self.password)

            # Create a Cipher object with the derived key and extracted IV
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            # Decrypt the ciphertext
            padded_data = decryptor.update(ct) + decryptor.finalize()

            # Remove PKCS7 padding from the decrypted data
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()

            # Convert the decrypted bytes back to a string
            return data.decode('utf-8')

        except ValueError as e:
            raise Exception("Decryption failed: Invalid padding or incorrect password.") from e
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")

    def verify_password(self, plain_password, encrypted_password):
        try:
            decrypted_password = self.decrypt(encrypted_password)
            return plain_password == decrypted_password
        except Exception as e:
            return False
