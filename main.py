#This code imports different functions from the 'database.py' and the 'crypto.py'
#files in the same directory. The 'database.py' file contains functions for interacting
#with the database. The 'crypto.py' file contains functions for hashing and verifying the
#master password, generating a cryptographic key, and encrypting and decrypting passwords.
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


def register():
    #This function prints a header for the registration screen

    print("\n=== Register New User ===")
    #This line of code prints the words 'Register New User' at the top of the screen

    username = input("Choose a username: ")
    #This line of code asks the user to choose a username

    master_password = input("Choose a master password: ")
    #This line of code asks the user to input a master password

    master_hash = hash_master_password(master_password)
    #This line of code hashes the password using bcrypt. This is because the bcrypt embeds
    #the salt inside the hash inside itself. Only one value results from this.


    create_user(username, master_hash, None)
    #This line of code saves the new user and passes 'None' for the salt column because it
    #is no longer generated separately.

    print("User registered successfully!")
    #This line of code prints "User registered successfully!" to the screen


def login():
    #This line of code prints a header to the screen.

    print("\n=== Login ===")
    #This line of code prints the word "Login" to the screen as a header

    username = input("Username: ")
    #This line of code asks the user to input a username in front of "Username: "

    master_password = input("Master Password:")
    #This line of code asks the user to input a password in front of "Master Password: "

    user = get_user(username)
    #This line of code sets a variable 'user' equal to the 'get_user' function that passes
    #the variable 'username' as an argument. This variable looks up the stored user row by 
    #username and sets it equal to the 'user' variable.

    if not user:
        #This 'if' conditional deals with the aftermath of, if nothing is found. 

        print("User not found.")
        #If this conditional is True then the words "User not found." are printed to the
        #screen.

        return None
        #This returns 'None' to the screen after the message it printed because the conditional
        #is true.

    user_id, stored_username, stored_hash, stored_salt = user
    #This line of code takes the 'user' variable which is a single row returned from the 'get_user'
    #function as a tuple and splits it into four separate variables, one for each column in that row.
    #This means that the variable 'user_id' is given the value of id, the variable 'stored_username'
    #is assigned the username value from the 'get_user' function, the variable 'stored_hash' is
    #assigned the 'master_password_hash' value from the 'get_user' function and the 'stored_salt' variable
    #is assigned the 'salt' value from the 'get_user' function. This method is called tuple unpacking.
    #Instead of accessing each value awkwardly by index    

    if verify_master_password(master_password, stored_hash):
        #This is a conditional statement. This line first calls the verify_master_password function that runs
        #and returns either true or false based on whether the plaintext password and user that were just 
        #entered were successfully pulled from the database. If the pull is successful then the result is
        #'True' then the message "Login successful!" is printed and the user id is returned.
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
            user_id = login()
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