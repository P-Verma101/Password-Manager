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
    #This function uses the 'bcrypt' library to securely 
    #hash the password. This function takes the parametter 
    #'password' as a string and returns the hashed password
    #as bytes.
    password_bytes = password.encode()
    #This creates a variable 'password_bytes' which converts 
    #the password strong into bytes. This variable uses the
    #'.encode()' method. It converts the string into its UTF-8
    #byte representatiion. This is important because the 'bcrypt'
    #library requires the password to be in bytes format, NOT
    #string format.

    salt = bcrypt.gensalt()
    #This variable generates a cryptographic salt. The variable 
    #'bcrypt.gensalt()' creates a random salt to be used in hashing.
    #A salt is a random value that is added to the password before
    #hashing to makes sure tha even if 2 uses have the same password,
    #their hashes will be different. The salt is automatically included
    # in the final hash output so it can be verified later.

    hashed = bcrypt.hashpw(password_bytes, salt)
    #This variable actually hashes the password. The 'bcrypt.hashpw()'
    # takes the password bytes and the salt, then generates a secure hash.
    #The function uses the Blowfish cipher with a keyed hash algorithm. This
    #variable will result in a hash that includes the salt and the cost factor.
    #This makes it self-cintained for verification.

    return hashed
    #This variable returns the hashed password to the caller.

def verify_master_password(password: str, hashed: bytes) -> bool:
    #This function uses the 'bcrypt' library to verify if a provided password
    #matches a stored hash. It takes the 'password' as a string and the 'hashed'
    #password as bytes, and returns a boolean which indicates whether the password
    #is correct or not. 

    ssword_bytes = password.encode()
    #This 'ssword_bytes' variable converts the plaintext password string into bytes.
    #The '.encode()' is a string method that converts a string into its UTF-8 byte
    #representation.

    return bcrypt.checkpw(password_bytes, hashed)
    #This line verifies the password by using the 'bcrypt.checkpw()' to turn the input
    #password and the stored hash, then compares them. It automatically extracts the
    #sat from the stored hash and applies it to the imput password. If they match it returns
    #True, otherwise it returns False.
