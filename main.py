import argparse
from colorama import Fore, Style, init
from cli.auth_cli import register, login
from cli.finance_cli import add_transaction, view_transactions, delete_transaction

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
╔══════════════════════════════════════╗
║    💰 Personal Finance Tracker CLI   ║    
║         Powered by Python & JSON     ║
╚══════════════════════════════════════╝{Style.RESET_ALL}
"""


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        prog="finance",
        description="Personal Finance Tracker"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Auth subcommands
    subparsers.add_parser("register", help="Create a new account")
    subparsers.add_parser("login", help="Log in to your account")

    args = parser.parse_args()

    # Route auth commands
    if args.command == "register":
        register(args)
        return

    if args.command == "login" or args.command is None:
        username = login(args) if args.command == "login" else prompt_login()
        if not username:
            return
        finance_menu(username)


def prompt_login():
    from cli.auth_cli import login
    print("Please log in to continue.\n")
    return login(None)


def finance_menu(username: str):
    """Interactive menu after login."""
    while True:
        print(f"\n{Fore.CYAN}--- Finance Menu ({username}) ---{Style.RESET_ALL}")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Delete a Transaction")
        print("5. Logout / Exit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            add_transaction(username, "income")
        elif choice == "2":
            add_transaction(username, "expense")
        elif choice == "3":
            view_transactions(username)
        elif choice == "4":
            delete_transaction(username)
        elif choice == "5":
            print(Fore.YELLOW + "👋 Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "❌ Invalid choice." + Style.RESET_ALL)


if __name__ == "__main__":
    main()