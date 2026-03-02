import pytest
from unittest.mock import patch, MagicMock
from cli.finance_cli import add_transaction, view_transactions


def test_add_transaction_income():
    with patch("builtins.input", side_effect=["100", "Food", "Lunch"]):
        with patch("finance_cli.storage") as mock_storage:
            with patch("finance_cli.Income") as mock_income:
                
                mock_instance = MagicMock()
                mock_instance.to_dict.return_value = {"amount": 100}
                mock_instance.summary.return_value = "Income added"
                mock_income.return_value = mock_instance

                add_transaction("john", "income")

                mock_storage.add_transaction.assert_called_once()


def test_view_transactions():
    fake_transactions = [
        {
            "type": "Income",
            "date": "2024-01-01",
            "category": "Salary",
            "description": "Monthly pay",
            "amount": 1000
        }
    ]

    with patch("finance_cli.storage") as mock_storage:
        mock_storage.get_transactions.return_value = fake_transactions

        view_transactions("john")

        mock_storage.get_transactions.assert_called_once()