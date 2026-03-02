from models.user import user    #This imports the User class to create user objects
from db import storage          #This imports storage to save and load the user's data
from colorama import Fore, Style #This imports color tools for the colored terminal output

def register(args):
    username = input("Choose a username: ").strip() #This asks the user to pick a username and strip removes the extra spaces

    if storage.user_exists(username): #This stops registraton if the username is already takn
        print(Fore.RED + "Username is already taken." + Style.RESET_ALL)
        return

    password = input("Choose a passord: ").strip()

    user = User(username=username, raw_password=password) #This creates a new User object with the given username and password

    storage.save_user(user.to_dict()) #This one saves the users to the database as a dictionary

    print(Fore.Green + f"Account created for '{username}'. Your can log in." + Style.RESET_ALL)

def login(args):
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user_data = storage.get_user(username) #This one looks up the user through the database

    if not user_data:#This one prints out an error message if the user is not found 
        print(Fore.RED + "User does not exist." + Style.RESET_ALL)
        return None

    user = User(username=username, password_hash=user_data["password_hash"])#This rebuilds the User object using the stored password hash

    if user.verify_password(password):
        print(Fore.Green + f"Welcome back, {username}!" + Style.TESET_ALL)
        return username #Returns username to show a successful login
    else:
        print(Fore.Red + "Incorrect Password." + Style.RESET_ALL)
        return None #This returns None to show that the login has failed
