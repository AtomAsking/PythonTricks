"""This is a simple example of a User class with name and birthday attributes.
The age of the user is calculated based on the birthday.
The user can be compared with other users based on their birthday.
"""
from __future__ import annotations  # "Forward References" for type hints

from datetime import datetime, timedelta, timezone


class User:
    """User class with name and birthday attributes."""

    def __init__(self, name: str, birthday: datetime):
        """
        Initialize User with name and birthday.

        :param name: str
        :param birthday: datetime
        """
        self.name = name
        self.birthday = birthday

    @property
    def age(self) -> int:
        """
        Calculate the age of the user.

        :return: int
        """
        now = datetime.now(tz=timezone(timedelta(hours=8)))
        age = now.year - self.birthday.year
        if (now.month, now.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age

    def __eq__(self, other: User):
        return self.name == other.name and self.birthday == other.birthday

    def __lt__(self, other: User):
        return self.birthday < other.birthday

    def __le__(self, other: User):
        return self.birthday <= other.birthday

    def __str__(self):
        return f"{self.name} is {self.age} years old."

    def __repr__(self):
        return f"User(name={self.name}, birthday={self.birthday})"


if __name__ == "__main__":
    user1 = User("foo", datetime(year=1994, month=12, day=18))
    print(user1.age)

    user2 = User("bar", datetime(year=1994, month=12, day=18))
    print(user2.age)

    print(user1 == user2)  # False
    print(user1 > user2)  # False
    print(user1 >= user2)  # True

    # user1.age = 10  # AttributeError: can't set attribute
    # del user1.age  # AttributeError: can't delete attribute
