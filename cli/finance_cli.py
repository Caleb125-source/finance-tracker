from models.transaction import Income, Expense  # This imports the Transaction classes
from db import storage  # This is the database handler
from colorama import Fore, Style  # This colors the terminal's output
from tabulate import tabulate  # This formats the table to be arranged seamlessly


# Adding the transactions
def add_transaction(username: str, txn_type: str):
    try:
        amount = float(input("Amount: "))
        category = input("Category: ").strip()
        description = input("Description: ").strip()
    except ValueError:
        print(Fore.RED + "Invalid Amount." + Style.RESET_ALL)
        return

    # Create the right transaction type based on txn_type
    txn = Income(amount, category, description) if txn_type == "income" else Expense(amount, category, description)

    storage.add_transaction(username, txn.to_dict())
    print(Fore.GREEN + txn.summary() + Style.RESET_ALL)


# This part views the transactions
def view_transactions(username: str):
    txns = storage.get_transactions(username)
    if not txns:
        print(Fore.YELLOW + "No transactions found." + Style.RESET_ALL)
        return

    rows, total_income, total_expense = [], 0, 0

    for i, t in enumerate(txns):
        sign = "+" if t["type"] == "Income" else "-"
        rows.append([i, t["date"], t["type"], t["category"], t["description"], f"{sign}KES {t['amount']:.2f}"])

        # This is the tally totals
        if t["type"] == "Income":
            total_income += t["amount"]
        else:
            total_expense += t["amount"]

    print(tabulate(rows, headers=["#", "Date", "Type", "Category", "Desc", "Amount"], tablefmt="rounded_outline"))

    balance = total_income - total_expense
    bal_color = Fore.GREEN if balance >= 0 else Fore.RED

    print(f"\nIncome: KES {total_income:.2f} | Expenses: KES {total_expense:.2f} | {bal_color}Balance: KES {balance:.2f}{Style.RESET_ALL}")


# This is to delete transactions
def delete_transaction(username: str):
    view_transactions(username)
    try:
        index = int(input("\nEnter # of transaction to delete: "))
        deleted = storage.delete_transaction(username, index)
        msg = "Transaction deleted." if deleted else "Invalid index."
        color = Fore.GREEN if deleted else Fore.RED
        print(color + msg + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Please enter a number." + Style.RESET_ALL)