import sqlite3
#This imports SQLite. This is used because
#the sqlite3 module in python lets the developer
#open the database, run SQL commands, create tables
#and insert data. This line is basically the line
#between Python and SQL. It allows both of the
#langauges to work together.


def get_connection():
    
    return sqlite3.connect("valut.db") 
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
    #This line creates a variable named 'cur'

    #This is where the actual tables will be

    conn.commit()
    conn.close()