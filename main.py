from database import (
    create_tables,
    get_connection,
    create_user,
    get_user,
    add_entry,
    get_entries,
    delete_entry
    )

from crypto import(
    hash_master_password,
    verify_master_password,
    generate_key,
    encrypt_password,
    decrypt_password
)
#This code imports different functions from the 'database.py' and the 'crypto.py'
#files in the same directory. The 'database.py' file contains functions for interacting
#with the database. The 'crypto.py' file contains functions for hashing and verifying the
#master password, generating a cryptographic key, and encrypting and decrypting passwords.

def register():
    print("\n=== Register New User ===")
    username = input("Choose a username: ")
    master_password = input("Choose a master password: ")

    master_hash, salt = hash_password(master_password)

    create_user(username, master_hash, salt)
    print("User registered successfully!")

def login():
    print("\n=== Login ===")
    username = input("Username: ")
    master_password = input("Master Password:")

    user = get_user(username)
    if not user:
        print("User not found.")
        return None

    user_id, stored_username, stored_hash, stored_salt = user

    if verify_password(master_password, stored_hash, stored_salt):
        print("Login successful!")
        return user_id
    else:
        print("Incorrect password.")
        return None
    
def add_new_entry(user_id):
    print("\n=== Add New Entry ===")
    service = input("Service Name: ")
    username = input("Service Username: ")
    raw_password = input("Service password: ")

    encrypted = encrypt_password(raw_password)
    add_entry(user_id, service, username, encrypted)

    print("Entry added successfully!")

def view_entries(user_id):
    print("\n=== Your Entries ===")
    entries = get_entries(user_id)

    if not entries:
        print("No entries found.")
        return
    
    for entry in entries:
        entry_id, service, username, enc_pwd = entry
        decrypted = decrypt_password(enc_pwd)
        print(f"\nID: {entry_id}")
        print(f"Service: {service}")
        print(f"Username: {username}")
        print(f"Password: {decrypted}")

def delete_entry_cli(user_id):
    print("\n=== Delete Entry ===")
    entry_id = input("Enter entry ID to delete: ")

    delete_entry(entry_id)
    print("Entry deleted successfully!")

def main():
    create_tables()

    while True:
        print("\n=== Password Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input(" Choose an option: ")

        if choice == "1":
            register()

        elif choice == "2":
            if user_id:
                while True:
                    print("\n=== Dashboard ===")
                    print("1. Add Entry")
                    print("2. View Entries")
                    print("3. Delete Entry")
                    print("4. Logout")

                    sub_choice = input(" Choose an option: ")

                    if sub_choice == "1":
                        add_new_entry(user_id)
                    elif sub_choice == "2":
                        view_entries(user_id)
                    elif sub_choice == "3":
                        delete_entry_cli(user_id)
                    elif sub_choice == "4":
                        break
                    else:
                        print("Invalid option.")

            elif choice == "3":
                print("Goodbye")
                break

            else:
                print("Invalid option.")

if __name__ == "__main__":
    main()