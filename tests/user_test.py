import pytest
from models.user import User

def test_user_creation():
    username = "user1"
    password = "securepass123"
    
    user = User(username, password)
    
    # Username matches
    assert user.username == username
    
    # Password is hashed
    assert user.password_hash != password
    assert isinstance(user.password_hash, bytes)

def test_password_verification():
    password = "securepass123"
    user = User("user1", password)
    
    # Correct password returns True
    assert user.verify_password(password) is True
    
    # Incorrect password returns False
    assert user.verify_password("wrongpass") is False

def test_to_dict_and_from_dict():
    password = "securepass123"
    user = User("user1", password)
    
    # Serialize to dict
    data = user.to_dict()
    assert data["username"] == "user1"
    assert isinstance(data["password_hash"], str)
    
    # Deserialize from dict
    user2 = User.from_dict(data)
    assert user2.username == "user1"
    assert isinstance(user2.password_hash, bytes)
    
    # Password verification should still work
    assert user2.verify_password(password) is True