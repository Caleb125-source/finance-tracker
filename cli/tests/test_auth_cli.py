import pytest
from unittest.mock import patch, MagicMock
from cli.auth_cli import register, login


def test_register_success():
    # Mock user input
    with patch("builtins.input", side_effect=["john", "1234"]):
        with patch("auth_cli.storage") as mock_storage:
            mock_storage.user_exists.return_value = False

            with patch("auth_cli.User") as mock_user:
                mock_instance = MagicMock()
                mock_instance.to_dict.return_value = {"username": "john"}
                mock_user.return_value = mock_instance

                register(None)

                # Check that save_user was called
                mock_storage.save_user.assert_called_once()


def test_login_success():
    with patch("builtins.input", side_effect=["john", "1234"]):
        with patch("auth_cli.storage") as mock_storage:
            mock_storage.get_user.return_value = {
                "password_hash": "hashed_pw"
            }

            with patch("auth_cli.User") as mock_user:
                mock_instance = MagicMock()
                mock_instance.verify_password.return_value = True
                mock_user.return_value = mock_instance

                result = login(None)

                assert result == "john"