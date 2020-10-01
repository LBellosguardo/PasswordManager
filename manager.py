import sys

MASTER = '123'

connect = input('Please enter your master password or q to quit\n')

#If password entry does not match, keep prompting user for master password, or quit
while connect != MASTER:
    if connect.lower() == 'q' or connect.lower() == 'quit':
        print("Goodbye")
        sys.exit()
    connect = input('Please enter your master password or q to quit\n')
    
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

        