import sys
import random
import string

MASTER = '123'

connect = input('Please enter your master password or q to quit\n')

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

if connect == MASTER:
    # Main menu loop
    while True:
        
        print('-' * 15)
        print('Main Menu')
        print('r: Retrieve one of your usernames and password')
        print('a: Add a new username and password')
        print("u: Update an existing entry (username, password, or both")
        print("g: Generate a new secure password (does not save this password for now)")
        print("c: Change your master password (maybe, idk if this feature will stay)")
        print("q: Quit the password manager")
        print('-' * 15)
        
        command = input()
        
        if command == 'q':
            print("Goodbye")
            sys.exit()

        if command == 'g':
            print(generate_password())