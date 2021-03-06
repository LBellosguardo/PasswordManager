import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Generate an encryption key based on name of service, ensures same key for the same service every time
def generate_key(service):

    password = service.encode()
    # If None, paste the salt generated when running setup.py
    salt = None

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend())

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt(service, password):
    # Obtain key based on service name
    key = generate_key(service)
    # Use this key to encrypt the password for the service using Fernet class
    fernet = Fernet(key)
    encrypted = fernet.encrypt(bytes(password, encoding='utf8'))
    return encrypted

def decrypt(service, encrypted_str):
    # Obtain key for our service
    key = generate_key(service)
    
    fernet = Fernet(key)
    password = fernet.decrypt(encrypted_str)
    return password.decode('utf8')