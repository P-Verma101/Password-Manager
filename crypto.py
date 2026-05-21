#Here we use bcrypt because its slow, which means 
#that it is good for security as it makes brute-force
#attacks more difficult. It also automatically handles
#salts. This is also an industry standard for password 
#hashing.
import bcrypt
#For this project Fernet is used because it is secure,
#handles key safely and its simple to use. Encryption is
#used to protect stored passwords, which you must be able
#to decrypt when decrypting the stored passwords.
from cryptography.fernet import Fernet

def hash_password(password: str) -> bytes:
    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed