import pytest
from unittest.mock import patch, MagicMock
from cli.auth_cli import register, login


# ----------------- REGISTER TESTS -----------------

@patch("cli.auth_cli.storage")
@patch("cli.auth_cli.User")
def test_register_new_user(mock_user_cls, mock_storage):
    mock_storage.user_exists.return_value = False
    mock_storage.save_user = MagicMock()

    mock_user = MagicMock()
    mock_user.to_dict.return_value = {"username": "newuser"}
    mock_user_cls.return_value = mock_user

    inputs = iter(["newuser", "password123"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            register(None)

    mock_storage.save_user.assert_called_once()
    mock_print.assert_called()


@patch("cli.auth_cli.storage")
@patch("cli.auth_cli.User")
def test_register_existing_user(mock_user_cls, mock_storage):
    mock_storage.user_exists.return_value = True

    inputs = iter(["existinguser"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            register(None)

    mock_storage.save_user.assert_not_called()
    mock_print.assert_called()


# ----------------- LOGIN TESTS -----------------

@patch("cli.auth_cli.storage")
@patch("cli.auth_cli.User")
def test_login_success(mock_user_cls, mock_storage):
    mock_storage.get_user.return_value = {"password_hash": "hashedpass"}

    mock_user = MagicMock()
    mock_user.verify_password.return_value = True
    mock_user_cls.return_value = mock_user

    inputs = iter(["user1", "password123"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            result = login(None)

    assert result == "user1"
    mock_print.assert_called()


@patch("cli.auth_cli.storage")
def test_login_user_not_exist(mock_storage):
    mock_storage.get_user.return_value = None

    inputs = iter(["nouser", "pass"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            result = login(None)

    assert result is None
    mock_print.assert_called()


@patch("cli.auth_cli.storage")
@patch("cli.auth_cli.User")
def test_login_wrong_password(mock_user_cls, mock_storage):
    mock_storage.get_user.return_value = {"password_hash": "hashedpass"}

    mock_user = MagicMock()
    mock_user.verify_password.return_value = False
    mock_user_cls.return_value = mock_user

    inputs = iter(["user1", "wrongpass"])
    with patch("builtins.input", lambda _: next(inputs)):
        with patch("builtins.print") as mock_print:
            result = login(None)

    assert result is None
    mock_print.assert_called()