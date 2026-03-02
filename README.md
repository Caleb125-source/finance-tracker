Personal Finance Tracker (CLI)

A Python Command-Line Interface (CLI) application to manage personal finances by tracking income and expenses. This project demonstrates Object-Oriented Programming (OOP), persistent JSON storage, user authentication, and modular design.

(a).Project Overview
The Personal Finance Tracker allows users to:
1.Securely register and log in
2.Add income and expense transactions
3.View all transactions in a structured format
4.Delete transactions by ID
5.Save and retrieve data using JSON files for persistence

The application uses OOP principles (classes, inheritance, encapsulation) and a modular structure for maintainability.

(b).Features
User Authentication: Register and login with hashed passwords (bcrypt)
Transaction Management: Add, view, and delete Income and Expense transactions
Persistent Storage: Save user and transaction data in JSON files
CLI Interaction: Clean interactive menus and prompts
OOP Design: Base Transaction class, Income and Expense subclasses, and User class

(c).Project Structure
finance_tracker/
│
├── Pipfile
├── .gitignore
├── README.md
│
├── data/
│   ├── users.json
│   └── transactions.json
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── transaction.py
│
├── db/
│   ├── __init__.py
│   └── storage.py
│
├── cli/
│   ├── __init__.py
│   ├── auth_cli.py
│   └── finance_cli.py
│
├── tests/
│   ├── __init__.py      (optional but recommended)
│   ├── test_user.py
│   └── test_transaction.py
│
└── main.py

(d).Setup Instructions

1.Clone the repository:
git clone https://github.com/<your-username>/finance-tracker.git
cd finance-tracker

2.Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3.Install dependencies:
pip install -r requirements.txt

Step-by-Step Usage
1.Start the CLI:
python main.py
2.Register a new user:
Select Register
Enter username and password
User is saved to users.json
3.Login:
Select Login
Enter credentials
On success, session begins for that user
4.Add a transaction:
Select Add Transaction
Choose type: Income or Expense
Enter amount, category, description
Transaction is saved to transactions.json
5.View all transactions:
Select View Transactions
Transactions display in a table: ID, Type, Amount, Category, Description, Date
6.Delete a transaction:
Select Delete Transaction
Enter transaction ID
Transaction is removed from JSON file
7.Exit the application:
Choose the exit option from the menu

Dependencies
Python 3.10+
Standard Library: datetime, json, argparse
External Packages:
bcrypt – password hashing
pytest – unit testing

Testing
Run all tests:
pytest -x tests/

Covers:
Transaction, Income, Expense behavior
User creation, password hashing, verification
Integration: User + Transaction workflow
Sample JSON & CLI Outputs
Sample users.json
[
  {
    "username": "alice",
    "password_hash": "$2b$12$7Hn7B4t8..."
  }
]
Sample transactions.json
[
  {
    "id": 1,
    "username": "alice",
    "type": "Income",
    "amount": 1500.0,
    "category": "Salary",
    "description": "Monthly paycheck",
    "date": "2026-03-02 15:42"
  },
  {
    "id": 2,
    "username": "alice",
    "type": "Expense",
    "amount": 200.0,
    "category": "Groceries",
    "description": "Weekly shopping",
    "date": "2026-03-02 17:15"
  }
]
Sample CLI Flow
$ python main.py
Welcome to Personal Finance Tracker!
1. Register
2. Login
Select option: 1

Enter username: alice
Enter password: ****
User registered successfully!

$ python main.py
Select option: 2
Enter username: alice
Enter password: ****
Login successful!

$ python main.py
Enter transaction type (Income/Expense): Income
Enter amount: 1500
Enter category: Salary
Enter description: Monthly paycheck
Transaction added successfully!

$ python main.py
Viewing all transactions:
ID | Type    | Amount | Category | Description        | Date
1  | Income  | 1500   | Salary   | Monthly paycheck   | 2026-03-02 15:42
2  | Expense | 200    | Groceries| Weekly shopping    | 2026-03-02 17:15

JSON files must exist in data/ folder before running CLI
Role-based permissions not implemented yet
CLI session is in-memory; future versions can add persistent sessions and reports
This version is a step-by-step guide, showing project setup, CLI workflow, functionality, and sample outputs, without the team breakdown.
