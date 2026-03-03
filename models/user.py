import bcrypt


class User:
    """
    Represents a system user with secure password hashing.
    """

    def __init__(self, username: str, raw_password: str = None, password_hash: str = None):
        self.username = username

        if raw_password is not None:
            # Creating a new user
            self._password_hash = self._hash_password(raw_password)
        elif password_hash is not None:
            # Loading existing user from storage
            self._password_hash = password_hash.encode("utf-8")
        else:
            raise ValueError("Either raw_password or password_hash must be provided.")

    # ----- PRIVATE HASHING METHOD -----
    def _hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    # ----- VERIFY PASSWORD -----
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self._password_hash)

    # ----- SERIALIZATION -----
    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self._password_hash.decode("utf-8")
        }

    def __repr__(self):
        return f"User(username='{self.username}')"