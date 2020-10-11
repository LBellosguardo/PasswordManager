import os
from pathlib import Path
import sys
from getpass import getpass

master = getpass('Enter a master password:\n')
master2 = getpass('Confirm master password:\n')

if master == master2:
    if 'zsh' in os.environ.get("SHELL", ""):
        with open(Path.home() / ".zshrc", 'a') as f:
            f.write(f'\nexport PM_MASTER="{master}"')
        f.close()
    # os.environ['PM_MASTER'] = str(master)
else:
    sys.exit()

print(os.urandom(16))
print('Copy the above byte string into the empty salt variable in dbencrypt.py')
