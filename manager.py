import dbencrypt as dbe
import random
import string
import sqlite3
import sys
from cryptography.fernet import Fernet
from getpass import getpass

MASTER = '123'

connect = getpass('Please enter your master password or q to quit\n')

#If password entry does not match, keep prompting user for master password, or quit
while connect != MASTER:
    if connect.lower() == 'q' or connect.lower() == 'quit':
        print("Goodbye")
        sys.exit()
    connect = input('Please enter your master password or q to quit\n')
    
def generate_password(length=16, special=True):
    password = ""
    characters = string.ascii_letters + string.digits
    if special:
        characters += '!@#$%^&*'
    for i in range(length):
        password += random.choice(characters)
    return password

#Establishes connection to database and catches any errors with connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

if connect == MASTER:
    
    conn = create_connection('password_manager.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords (
            service text PRIMARY KEY,
            username text,
            password text
            );''')
        
    # Main menu loop
    while True:
        
        print('-' * 15)
        print('Main Menu')
        print('r: Retrieve one of your usernames and password')
        print('a: Add a new username and password')
        print("u: Update an existing entry (username, password, or both")
        print('d: Delete the information for a particular service')
        print("g: Generate a new secure password (does not save this password for now)")
        print("c: Change your master password (maybe, idk if this feature will stay)")
        print("q: Quit the password manager")
        print('-' * 15)
        
        command = input()
        
        if command == 'q':
            print("Goodbye")
            sys.exit()

        if command == 'a':
            service = input('What is the name of the website or service?\n')
            u_name = input(f'What is your {service} username? (This can also be your email)\n')
            choice = input('Would you like a password to be automatically generated for you? (y/n)\n')
            if choice == 'y':
                pw = generate_password()
                c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, dbe.encrypt(service, u_name), dbe.encrypt(service, pw)))
                print(f'Your newly generated password is: {pw}\nIt has been encrypted and saved to your vault.')
            else:
                pw, pw2 = 'abc', 'xyz'
                while pw != pw2:
                    # Have user enter password twice to ensure their entry is correct
                    pw = getpass('Please enter your desired password:\n')
                    pw2 = getpass('Please confirm password:\n')
                    if pw == 'm' or pw2 == 'm':
                        break
                    if pw != pw2:
                        print('Passwords did not match, please try again, or press m for main menu')
                if pw == pw2:
                    c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, dbe.encrypt(service, u_name), dbe.encrypt(service, pw)))
            conn.commit()
            
        if command == 'g':
            print(generate_password())