import sqlite3
#This imports SQLite. This is used because
#the sqlite3 module in python lets the developer
#open the database, run SQL commands, create tables
#and insert data. This line is basically the line
#between Python and SQL. It allows both of the
#langauges to work together.


def get_connection():
    
    return sqlite3.connect("vault.db") 
    #This creates a file named 'valut.db' that is essentially 
    #the database file that needs to be made. it opens the database
    #so that the program can read and write into it. If the file
    #doesn't exist, it wil be created.

def create_tables():
    conn = get_connection()
    #This line calls creates a variable named 'conn' that is set
    #equal to the get_connection() function. This means that the
    #program will use the 'conn' variable to interact with the 
    #database file that is created in the get_connection() function.

    cur = conn.cursor()
    #This line creates a variable named 'cur' that is set to equal
    #'conn.cursor()'. This means that the program will use the 'cur'
    #variable to execute the SQL commands that will be used to create
    #the tables in the database. The 'cursor' is a control structure
    #that enables the traversal over the record in a database. Basically,
    #this is used to execute SQL commands and get data from the database.

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                master_password_hash BLOB,
                salt BLOB,
                enc_key BLOB
                )""")
    
    #Here the 'CREATE TABLE' makes a new table. the 'IF NOT EXISTS' is put
    #in to make sure that the table is only created if it doesn't already
    #exist. The  'id INTEGER PRIMARY KEY' creats a unique ID for each user 
    #that is created. The 'username TEXT' creates a the username column that
    #stores the username as a text. The 'master_password_hash BLOB' is the
    #column that stores the hashed master password as a binary large object.
    #Basically, this is used to store the hashed password in a secure way. The
    # 'salt BLOB' is the column that stores the salt used for hashing the master
    #pasword as a binary large object. Basically, this is used to store the salt
    #in a secure way. Salt is random data that is used as an additional input to
    #the hashing process. It is used to protect against certain types of attacks.

    cur.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                service TEXT,
                username TEXT,
                password_enc BLOB,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """)
    #This line creates a new table that is named entries. It uses the 'execute' 
    #method of the 'cur' variable to run the SQL command that creates the table.
    #The 'CREATE TABLE IF NOT EXISTS entries' creats a tabled named entries and 
    #The 'IF NOT EXISTS' ensures that no error occurs if the table already exists.
    #This line will do NOTHING if the table already exists. The opening parenthesis
    #mark the start of the column definitions. The 'id INTEGER PRIMARY KEY' defines
    #a column named 'id' and gives it the data type of INTEGER. The 'PRIMARY KEY'
    #assigns this column as the primary key for the table. This means that each value 
    #in this column must be unique and CANNOT be NULL. The 'user_id INTEGER', creates
    #a column named 'user_id' that has the INTEGER data type. This will store a
    #reference to the 'id' column in the 'users' table. The 'service TEXT' creates a
    #column named 'service' that has the TEXT data type. This will store the name of
    #the service/website /app that the password is for. The 'username TEXT' is a column
    #named 'username' that has the TEXT data type. This will store the username for the 
    #service. The 'password_enc BLOB' creates a column named 'password_enc' which has the 
    #BLOB data type. This will store the the encrypted password in a binary format. The 
    #'FOREIGN KEY (user_id) REFERENCES users(id)' creates a foreign key constraint that 
    #links the 'user_id' column in the 'entries' table to the 'id' column in the 'users'
    #table. This means that each entry in the 'entries' table must be associated with 
    #a valid user in the 'users' table.

    conn.commit()
    #This line commits the changes to the database. This means that any 
    #changes that were made to the database with the SQL commands with 
    #the 'cur' variable will be saved to the database file.

    conn.close()
    #This line closes the connection to the database. This is important 
    #because it frees up resources and ensures that the database file is 
    #not left open without reason. It is good practice to close the
    #connection to the data when it is no longer needed.

def create_user(username, master_password_hash, salt, enc_key):
    #This function registers a new user. This function stores the user's 
    #usernames and a hash of their master password. This function also
    #stores a salt which is used to make the hash resistent to precomputed
    #or rainbow-table attacks. It DOES NOT store the raw password, not
    #just the hash and the salt which is needed to verify it later.

    conn = get_connection()
    #This line of code initalizes a variable named 'conn' that is set equal
    #to the function 'get_connection()'. This means that the function will 
    #use the 'conn' variable to interact with the file that is created in the 
    #'get_connection()' function. This is important because it allows the
    #function to read and write to the database file.

    cur = conn.cursor()
    #This line creates a variable named 'cur' that is set to equal
    #'conn.cursor()'. This means that the program will use the 'cur'
    #variable to execute the SQL commands that will be used to create
    #the tables in the database. The 'cursor' is a control structure
    #that enables the traversal over the record in a database. Basically,
    #this is used to execute SQL commands and get data from the database.


    cur.execute("""INSERT INTO users (username, master_password_hash, salt, enc_key) VALUES (?, ?, ?)""", (username, master_password_hash, salt, enc_key))
    #This line of code runs a SQL command that adds a new row to the users table. The '?' marks are placeholders and will be filled with
    #the username, master_password_hash, and salt values that are passed to the function. 

    conn.commit()
    #This line saves the changes made to the database.

    conn.close()
    #This line of code closes the connection to the database, freeing up resources.



def get_user(username):
    #This function looks up a single user by their username and returns
    #their stored information which in this case was their id, username,
    #password hash and salt.

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""SELECT id, username, master_password_hash, salt, enc_key FROM users WHERE username = ?""", (username,))

    row = cur.fetchone()
    #This line of code grabs one result row from the SQL query that just run. Since the a username should be unique,
    #there is at most one matching row, so it returns that single row as a tuple, or 'None' if no user matched.

    conn.close()
    #This closes the database connection, smae as in the other functions.

    return row
    #This sends that result back to whatever code called 'get_user()', so it can check if a user was found and use
    #their stored hash/salt to verify a login.

def add_entry(user_id, service, username, password_enc):
    #This function a that saves a new password entry for a specific service/website into the 'entries' table and
    #links it to the user who owns it.

    conn = get_connection()
    #This line of code initalizes a variable named 'conn' that calls the 'get_connection()' function that returns
    #a connection to the database file. This means that the function will use the 'conn' variable to interact with
    #the file that is created in the 'get_connection()' function.

    cur = conn.cursor()
    #This line of code creates a variable named 'cur' that is set to equal 'conn.cursor()'. This means that the 
    #program will use the 'cur' variable to execute the SQL commands that will be used to create the tables in the 
    #database. The 'cursor' part of this line is a control structure that enables the traversal over the record in
    # a database. Basically, this is used to execute SQL commands and get data from the database. 

    cur.execute("""INSERT INTO entries (user_id, service, username, password_enc) VALUES (?, ?, ?, ?)""", (user_id, service, username, password_enc))
    #This inserts a new row into the 'entries' table. It uses the '?' placeholders filled safely with the four values
    #into the function. This is important because it prevents SQL injection attacks, which is when a malicious user
    #tries to manipulate the SQL query by inserting special characters or SQL commands into the input fields.

    conn.commit()
    #This line saves the changes made to the database. It is important because it ensures that the new entry is
    #actually stored in the database file. Without this line, the new entry would not be saved and would be lost 
    #when the connection is closed.

    conn.close()
    #This line of code closes the connection to the database. This is important because it frees up resources and
    #ensures that the database file is not left open without reason. It is good practice to close the connection
    #to the database when it is no longer needed.


def get_entries(user_id):
    #This function retrieves all the password entries belong to a specfic user. It takes the user's ID as input
    #and returns a list of tuples, where each tuple contains the entry's ID, service name, username, and encrypted
    #password. This allows the user to view and manage their stored passwords.

    conn = get_connection()
    #This line of code initalizes a variable named 'conn' variable and is set equal to the 'get_connection()' function.
    #This means that the function will use the 'conn' variable to interact with the file that is created in the 
    #'get_connection()' function. This is important because it allows the function to read and write to the database file.

    cur = conn.cursor()
    #This line of code intializes a variable named 'cur' that is set equal to the 'conn.cursor()' which is responsible for
    #executing the SQL commands that will be used to create the tables in the database.

    cur.execute("""SELECT id, service, username, password_enc FROM entries WHERE user_id = ?""", (user_id,))
    #This line of code runs a SQL query that selects the 'id', 'service', 'username', and 'password_enc'
    #columns from the 'entries' table where the 'user_id' matches the provided user_id. The '?' is a 
    #placeholder that is safely filled with the user_id value to prevent the risk of SQL injection attacks.

    rows = cur.fetchall()
    #This line of code retrieves all the rows that match the query and stores them in the 'rows' variable.
    #This retirevies all the rows in tuple form and each tuple contains the entry's ID, service name, 
    #username, and encrypted password. This allows the user to view and manage their stored passwords.

    conn.close()
    #This line of code closes the connection to the database.

    return rows
    #This line of code returns the list of tupels so that the calling code can use it to display the 
    #entries to the user or perform other operations on them.

def delete_entry(entry_id):
    #This function deletes a specific password entry from the 'entries' and takes the entry's ID as an
    #input. It removes the entry from the database, allowing the user to manage their stored passwords.

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM entries WHERE id = ?", (entry_id,))

    conn.commit()
    conn.close()

