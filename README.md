# Password Manager 

## About
This is an offline password manager which holds your username and password credentials for any number of services on a local database.
All data is encrypted when entered and decrypted when retrieved. This project was made for educational purposes and is not meant to compete with
professional grade password management software. There is currently no GUI component and runs on the user's terminal / command line.

## How to Install
1. Download/clone the source code into the desired directory of your machine
2. Create a virtual environment for this project (named 'venv' by convention). In your current directory, run ```virtualenv venv```
3. Activate your virtual environment by running ```source venv/bin/activate```
4. Install the packages in the requirements.txt file using ```pip install -r requirements.txt```
5. Now you can run setup.py (```python setup.py```). This will prompt you to create your master password to access the 
password manager. It will then generate a random encryption salt which you muct copy to your clipboard, and paste into the 
'salt' variable in dbencrypt.py on line 15.
- ##### Important: If you did not copy the salt after running setup.py, you can generate a new one by running 
  ```
  import os
  print(os.urandom(16))
  ``` 
  ##### in a new script, but do not change salts after already saving passwords to the database, or else you will not be able to retrieve them.
  
6. Make sure to close any terminal sessions / code editors so that the new environment variable can be saved and recognized in a new session
7. Now you are ready to run `python manager.py` using your newly created master password. Make sure your virtual environment is activated.

## Demos

### Adding a New Service:
![](https://github.com/LBellosguardo/ProjectDemos/blob/main/Addpass.gif)
### Retrieving the Information for a Service:
![](https://github.com/LBellosguardo/ProjectDemos/blob/main/Retrievepass.gif)
### Updating the Credentials for a Service:
![](https://github.com/LBellosguardo/ProjectDemos/blob/main/Updatepass.gif)
### Deleting the Entry for a Service:
![](https://github.com/LBellosguardo/ProjectDemos/blob/main/Deletepass.gif)
### Generate a New Secure Password:
![](https://github.com/LBellosguardo/ProjectDemos/blob/main/Generatepass.gif)

## Outstanding Issues:

setup.py Only configured for MacOS. Windows and Linux systems currently must add environment variable manually.
