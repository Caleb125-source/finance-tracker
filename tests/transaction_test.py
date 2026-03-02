import pytest
from models.transaction import Transaction, Income, Expense

# ---------- Transaction base class ----------
def test_transaction_creation():
    username = "user1"
    amount = 100
    category = "General"
    description = "Test transaction"
    
    t = Transaction(username, amount, category, description)
    
    # Check attributes
    assert t.username == username
    assert t.amount == amount
    assert t.category == category
    assert t.description == description
    assert isinstance(t.date, str)
    assert t.id > 0

def test_transaction_amount_validation():
    t = Transaction("user1", 100, "General")
    
    # Valid amount
    t.amount = 50
    assert t.amount == 50
    
    # Invalid amount raises ValueError
    with pytest.raises(ValueError):
        t.amount = 0
    with pytest.raises(ValueError):
        t.amount = -10

# ---------- Income subclass ----------
def test_income_creation_and_summary():
    inc = Income("user1", 500, "Salary", "Monthly paycheck")
    
    # Inherited attributes
    assert inc.username == "user1"
    assert inc.amount == 500
    assert inc.category == "Salary"
    
    # Type in to_dict()
    assert inc.to_dict()["type"] == "Income"
    
    # Summary string
    summary = inc.summary()
    assert "[INCOME]" in summary
    assert "500" in summary
    assert "Salary" in summary

# ---------- Expense subclass ----------
def test_expense_creation_and_summary():
    exp = Expense("user1", 200, "Bills", "Monthly bills")
    
    # Inherited attributes
    assert exp.username == "user1"
    assert exp.amount == 200
    assert exp.category == "Bills"
    
    # Type in to_dict()
    assert exp.to_dict()["type"] == "Expense"
    
    # Summary string
    summary = exp.summary()
    assert "[EXPENSE]" in summary
    assert "200" in summary
    assert "Bills" in summary