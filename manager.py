import dbencrypt as dbe
import os
import pyperclip
import random
import re
import sqlite3
import string
import sys
from cryptography.fernet import Fernet
from getpass import getpass
from time import sleep

# Set password as an environment variable in .zshrc file
MASTER = os.environ.get('PM_MASTER')

connect = getpass("Please enter your master password or 'q' to quit\n")

# If password entry does not match, keep prompting user for master password, or quit
while connect != MASTER:
    if connect.lower() == 'q':
        print("Goodbye")
        sys.exit()
    connect = getpass("Please enter your master password or 'q' to quit\n")

# Method which generates a random 16-character password    
def generate_password():
    password = ""
    characters = string.ascii_letters + string.digits + '!@#$%^&*'
    
    for i in range(16):
        password += random.choice(characters)
    # If password does not have an uppercase, lowercase, special character, or digit, generate a new one
    if not bool(re.search(r'[!@#$%^&*]', password)) or (password == password.lower()) \
                or (password == password.upper()) or not bool(re.search(r'\d', password)):
        password = generate_password()
    return password

def return_to_main():
    key = input("Press 'm' to return to the main menu\n")
    while key != 'm':
        key = input("Press 'm' to return to the main menu\n")

# Establishes connection to database and catches any errors with connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def show_services(conn, cursor):
    print('\nServices:')
    cursor.execute('SELECT service FROM passwords ORDER BY service')
    res = cursor.fetchall()
    for line in res:
        print (' - ' + line[0])
        
def retrieve_password(conn, cursor):
    show_services(conn, cursor)
    service = input('Which service would you like to retrieve information for?\n').lower()
    
    cursor.execute('SELECT * FROM passwords WHERE service == ?', (service,))
    result = cursor.fetchone()
    if result != None:    
        user = dbe.decrypt(service, result[1])
        password = dbe.decrypt(service, result[2])
        print(f'Username: {user}')
        print(f'Password: {password}')
        pyperclip.copy(password)
        print('Your password has been copied to your clipboard')
        sleep(1)
        return_to_main()   
    else:
        print(f'No entry for {service} was found')
        return_to_main()

def add_password(conn, cursor):
    
    service = input('What is the name of the website or service?\n').lower()
    u_name = input(f'What is your {service} username? (This can also be your email)\n')
    choice = input('Would you like a password to be automatically generated for you? (y/n)\n')
    if choice == 'y':
        pw = generate_password()
        cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, dbe.encrypt(service, u_name), dbe.encrypt(service, pw)))
        pyperclip.copy(pw)
        print(f'Your newly generated password is: {pw}\nIt has been encrypted and saved to your vault.')
        sleep(1)
        print(f'Your password has been copied to your clipboard. Make sure you update it for your {service} account')
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
            pyperclip.copy(pw)
            print(f'Your password has been successfully encrypted and saved to your vault.')
            sleep(1)
            print(f'Your password has been copied to your clipboard. Make sure you update it for your {service} account')
    conn.commit()
    return_to_main()
    
def delete_password(conn, cursor):
        show_services(conn, cursor)
        service = input('Which service would you like to delete the information for?\n').lower()
        
        cursor.execute('SELECT * FROM passwords WHERE service == ?', (service,))
        result = cursor.fetchone()
        if result != None:
            confirm = getpass(f"Are you sure you want to delete the entry for {service}? " 
                                + "This cannot be undone.\nEnter your master password to proceed\n")
            if confirm == MASTER:
                cursor.execute('DELETE FROM passwords WHERE service = ?', (service,))
                print(f'Entry for {service} successfully deleted.')
                return_to_main()
            else:
                print('Master password does not match. Returning to main menu...')
                sleep(3)
        else:
            print(f"No entry for {service} was found.")
            return_to_main()
        
        conn.commit()
 
def update_password(conn, cursor):
    show_services(conn, cursor)
    service = input('Which service would you like to update information for?\n').lower() 
    
    cursor.execute('SELECT * FROM passwords WHERE service == ?', (service,))
    result = cursor.fetchone()
    if result != None:
        uname_select = input('Would you like to update your username information? (y/n)\n')
        if uname_select == 'y':
            new_uname = input(f'Please enter your updated username for {service}:\n')
            cursor.execute('''UPDATE passwords
                              SET username = ?
                              WHERE service = ?''', (dbe.encrypt(service, new_uname), service))
        password_select = input('Would you like to update your password? (y/n)\n')
        if password_select == 'y':
            choice = input('Would you like a password to be automatically generated for you? (y/n)\n')
            if choice == 'y':
                pw = generate_password()
                cursor.execute('''UPDATE passwords
                                  SET password = ?
                                  WHERE service = ?''', (dbe.encrypt(service, pw) , service))
                pyperclip.copy(pw)
                print(f'Your updated generated password is: {pw}\nIt has been copied to your clipboard, encrypted and saved to your vault.')
                
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
                    cursor.execute('''UPDATE passwords
                                      SET password = ?
                                      WHERE service = ?''', (dbe.encrypt(service, pw), service))
                    pyperclip.copy(pw)
                    print("Your password has been successfully copied to your clipboard, encrypted, and saved in your vault.")
       
        print(f"Don't forget to update your new information in your {service} account")
        return_to_main()
    else:
        print(f"No entry for {service} was found.")
        return_to_main()
            

# Only connect to database if connection password matches master password            
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
          
        if command == 'u':
            update_password(conn, c)
                
        if command == 'g':
            pw = generate_password()
            pyperclip.copy(pw)
            print('Generated password: ' + pw)
            print('Your generated password has been copied to your clipboard')
            return_to_main()
            
            