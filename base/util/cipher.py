from cryptography.fernet import Fernet

FERNET_KEY = b'YUIQMJdZc7VZoVMCTa4SMuR4gEbUwfRUt0bOYhFuo6o='

cipher_suite = Fernet(FERNET_KEY)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data