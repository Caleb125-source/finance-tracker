import bcrypt

class User:
    """
    Represents a system user with secure password hashing.
    Demonstrates encapsulation and authentication logic.
    """

  
    def __init__(self, username, raw_password=None, password_hash=None):
        self.username = username
        if raw_password is not None:
            self._password_hash = self._hash_password(raw_password)
        elif password_hash is not None:
            if isinstance(password_hash, str):
                password_hash = password_hash.encode("utf-8")
            self._password_hash = password_hash
        else:
            raise ValueError("Must provide either raw_password or password_hash")
                

    # ----- PRIVATE HASHING METHOD -----
    def _hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    # ----- VERIFY PASSWORD -----
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self._password_hash)

    # ----- PROPERTY (READ-ONLY ACCESS) -----
    @property
    def password_hash(self):
        return self._password_hash

    # ----- SERIALIZATION -----
    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self._password_hash.decode("utf-8")
        }

    # ----- DESERIALIZATION -----
    @classmethod
    def from_dict(cls, data: dict):
        user = cls.__new__(cls)
        user.username = data["username"]
        user._password_hash = data["password_hash"].encode("utf-8")
        return user

    def __repr__(self):
        return f"User(username='{self.username}')"
    