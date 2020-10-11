import os
from pathlib import Path
import sys
from getpass import getpass

if 'PM_MASTER' not in os.environ:
    master = getpass('Enter a master password:\n')
    master2 = getpass('Confirm master password:\n')

    if master == master2:
        if 'zsh' in os.environ.get("SHELL", ""):
            with open(Path.home() / ".zshrc", 'a') as f:
                f.write(f'\nexport PM_MASTER="{master}"')
            f.close()
    else:
        print('Passwords did not match. Ending program...')
        sys.exit()

    print(os.urandom(16))
    print('Copy the above byte string into the empty salt variable in dbencrypt.py')

else:
    print('Password manager has already been set up')
