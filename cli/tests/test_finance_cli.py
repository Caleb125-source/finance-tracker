import pytest
from unittest.mock import patch, MagicMock
from cli.finance_cli import add_transaction, view_transactions, delete_transaction


# ----------------- ADD TRANSACTION TESTS -----------------

@patch("cli.finance_cli.storage")
@patch("cli.finance_cli.Income")
@patch("cli.finance_cli.Expense")
def test_add_income_transaction(mock_expense, mock_income, mock_storage):
    mock_txn = MagicMock()
    mock_txn.to_dict.return_value = {"type": "Income", "amount": 1000}
    mock_txn.summary.return_value = "Income Summary"
    mock_income.return_value = mock_txn

    inputs = iter(["1000", "Salary", "Monthly pay"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            add_transaction("user1", "income")

    mock_storage.add_transaction.assert_called_once()
    mock_print.assert_called()


@patch("cli.finance_cli.storage")
def test_add_transaction_invalid_amount(mock_storage):
    inputs = iter(["invalid", "Category", "Desc"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            add_transaction("user1", "income")

    mock_storage.add_transaction.assert_not_called()
    mock_print.assert_called()


# ----------------- VIEW TRANSACTIONS TESTS -----------------

@patch("cli.finance_cli.storage")
def test_view_transactions_empty(mock_storage):
    mock_storage.get_transactions.return_value = []

    with patch("builtins.print") as mock_print:
        view_transactions("user1")

    mock_print.assert_called()


@patch("cli.finance_cli.storage")
def test_view_transactions_with_data(mock_storage):
    mock_storage.get_transactions.return_value = [
        {"type": "Income", "date": "2026-03-02", "category": "Salary", "description": "Pay", "amount": 1000},
        {"type": "Expense", "date": "2026-03-02", "category": "Food", "description": "Lunch", "amount": 200},
    ]

    with patch("builtins.print") as mock_print:
        view_transactions("user1")

    mock_print.assert_called()


# ----------------- DELETE TRANSACTION TESTS -----------------

@patch("cli.finance_cli.storage")
@patch("cli.finance_cli.view_transactions")
def test_delete_transaction_valid(mock_view, mock_storage):
    mock_view.return_value = None
    mock_storage.delete_transaction.return_value = True

    inputs = iter(["0"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            delete_transaction("user1")

    mock_print.assert_called()


@patch("cli.finance_cli.storage")
@patch("cli.finance_cli.view_transactions")
def test_delete_transaction_invalid_index(mock_view, mock_storage):
    mock_view.return_value = None
    mock_storage.delete_transaction.return_value = False

    inputs = iter(["99"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            delete_transaction("user1")

    mock_print.assert_called()


@patch("cli.finance_cli.storage")
@patch("cli.finance_cli.view_transactions")
def test_delete_transaction_non_integer(mock_view, mock_storage):
    mock_view.return_value = None

    inputs = iter(["abc"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            delete_transaction("user1")

    mock_print.assert_called()