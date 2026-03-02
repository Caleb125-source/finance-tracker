from datetime import datetime


class Transaction:
    """
    Base class for all financial transactions.
    Demonstrates encapsulation, class attributes, and validation.
    """

    _id_counter = 1  # class attribute shared by all transactions

    def __init__(self, username, amount, category, description=""):
        self.id = Transaction._id_counter
        Transaction._id_counter += 1

        self.username = username
        self._amount = amount  # encapsulated attribute
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ----- Encapsulation with validation -----
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero.")
        self._amount = value

    # ----- Convert object to dictionary (for storage layer) -----
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "type": self.__class__.__name__,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, amount={self.amount})"


# Income subclass

class Income(Transaction):
    """Represents income transactions"""

    def __init__(self, username, amount, category, description=""):
        super().__init__(username, amount, category, description)

    def summary(self):
        return f"[INCOME] +{self.amount} | {self.category} | {self.date}"


# Expense subclass

class Expense(Transaction):
    """Represents expense transactions"""

    def __init__(self, username, amount, category, description=""):
        super().__init__(username, amount, category, description)

    def summary(self):
        return f"[EXPENSE] -{self.amount} | {self.category} | {self.date}"