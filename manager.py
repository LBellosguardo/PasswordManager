import dbencrypt as dbe
import random
import string
import sqlite3
import sys
from cryptography.fernet import Fernet
from getpass import getpass
from time import sleep

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
    except sqlite3.Error as e:
        print(e)
    return conn

def retrieve_password(conn, cursor):
    
    print('Services:')
    cursor.execute('SELECT service FROM passwords ORDER BY service')
    print(cursor.fetchall())
    service = input('Which service would you like to retrieve information for?\n').lower()
    
    cursor.execute('SELECT * FROM passwords WHERE service == ?', (service,))
    result = cursor.fetchone()
    if result != None:    
        user = dbe.decrypt(service, result[1])
        password = dbe.decrypt(service, result[2])
        print(f'Username: {user}')
        print(f'Password: {password}')
        choice = input("Press 'm' to return to the main menu\n").lower()
        while choice != 'm':
            choice = input("Press 'm' to return to the main menu\n").lower()
                
    else:
        print(f'No entry for {service} was found')
        sleep(3)

def add_password(conn, cursor):
    
    service = input('What is the name of the website or service?\n')
    u_name = input(f'What is your {service} username? (This can also be your email)\n')
    choice = input('Would you like a password to be automatically generated for you? (y/n)\n')
    if choice == 'y':
        pw = generate_password()
        cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, dbe.encrypt(service, u_name), dbe.encrypt(service, pw)))
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
            cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, dbe.encrypt(service, u_name), dbe.encrypt(service, pw)))
    conn.commit()
    
def delete_password(conn, cursor):
        print('Services:')
        cursor.execute('SELECT service FROM passwords ORDER BY service')
        print(cursor.fetchall())
        service = input('Which service would you like to delete the information for?\n').lower()
        
        cursor.execute('SELECT * FROM passwords WHERE service == ?', (service,))
        result = cursor.fetchone()
        if result != None:
            confirm = getpass(f"Are you sure you want to delete the entry for {service}? " 
                                + "This cannot be undone.\nEnter your master password to proceed\n")
            if confirm == MASTER:
                cursor.execute('DELETE FROM passwords WHERE service = ?', (service,))
                print(f'Entry for {service} successfully deleted. Returning to main menu...')
                sleep(3)
            else:
                print('Master password does not match. Returning to main menu...')
                sleep(3)
        else:
            print(f"No entry for {service} was found. Returning to main menu...")
            sleep(3)
        
        conn.commit()
    
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
        print("u: Update an existing entry (username, password, or both)")
        print('d: Delete the information for a particular service')
        print("g: Generate a new secure password (does not save this password for now)")
        print("c: Change your master password (maybe, idk if this feature will stay)")
        print("q: Quit the password manager")
        print('-' * 15)
        
        command = input()
        
        if command == 'q':
            print("Goodbye")
            conn.close()
            sys.exit()

        if command == 'a':
            add_password(conn, c)
            
        if command == 'r':
            retrieve_password(conn, c)
        
        if command == 'd':
            delete_password(conn, c)      
              
        if command == 'g':
            print(generate_password())