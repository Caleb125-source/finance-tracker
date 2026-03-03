from models.user import User
from db import storage
from colorama import Fore, Style


def register(args):
    username = input("Choose a username: ").strip()

    if storage.user_exists(username):
        print(Fore.RED + "Username is already taken." + Style.RESET_ALL)
        return

    password = input("Choose a password: ").strip()

    user = User(username=username, raw_password=password)

    storage.save_user(user.to_dict())

    print(Fore.GREEN + f"Account created for '{username}'. You can log in." + Style.RESET_ALL)


def login(args):
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user_data = storage.get_user(username)

    if not user_data:
        print(Fore.RED + "User does not exist." + Style.RESET_ALL)
        return None

    user = User(username=username, password_hash=user_data["password_hash"])

    if user.verify_password(password):
        print(Fore.GREEN + f"Welcome back, {username}!" + Style.RESET_ALL)
        return username
    else:
        print(Fore.RED + "Incorrect Password." + Style.RESET_ALL)
        return None
    