from database import create_tables, get_connection
from crypto import (
    hash_master_password,
    verify_master_password,
    generate_key,
    encrypt_password,
    decrypt_password
)
#Both of these import commands will import the 2 modules that were
#built in crypto.py and database.py. These will be used to handle 
#the data storage and encryption for the password manager.

def 