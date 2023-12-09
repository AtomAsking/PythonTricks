# This is a custom metaclass demo
# Used to automatically capitalize method names in a class when creating a class
# For example: the method name say in User will be changed to SAY
# Usage: add metaclass=UpperAttrMetaclass in the class
# For example: class User(metaclass=UpperAttrMetaclass):
# The metaclass is a class that creates classes.
# Like "type", it is a class that creates classes.
# The difference is that "type" is a built-in metaclass, and the metaclass is a custom metaclass.
# If we need a custom metaclass, we need to inherit from type.


class UpperAttrMetaclass(type):
    """The purpose of the custom metaclass is to control the process of instantiating the User class."""

    def __new__(cls, *args, **kwargs):
        """
        args: is a tuple, and type(name, bases, dict) is written the same way.
        """
        print("*" * 50)
        name = args[0]  # User
        bases = args[1]  # (<class '__main__.A'>,)
        dct = args[2]  # {'__module__': '__main__', '__qualname__': 'User', '__doc__': '...', '__init__': <function User.__init__ at 0x106f120d0>, 'say': <function User.say at 0x106f12160>}
        kwds = kwargs  # {}，This is always empty.
        print(name, bases, dct, kwds, sep="\n", end="\n" + "*" * 50 + "\n")
        uppercase_attr = {}
        for name, value in dct.items():
            if not name.startswith("__"):
                uppercase_attr[name.upper()] = value
            else:
                uppercase_attr[name] = value
        return super().__new__(cls, name, bases, uppercase_attr, **kwds)


class A:
    """There's no point, it's just so that 'bases' isn't empty"""
    pass


class User(A, metaclass=UpperAttrMetaclass):
    """This specifies that the metaclass used when we create the User class is UpperAttrMetaclass"""

    def __init__(self, name):
        self.name = name

    def say(self):
        print(f"i am {self.name}")


print(hasattr(User, "say"))  # False
print(hasattr(User, "SAY"))  # True
f = User("foo")
print(f)  # <__main__.User object at 0x106f16760>
f.SAY()  # i am foo
# f.say()  # AttributeError: 'User' object has no attribute 'say'
print(f.__dict__)  # {'name': 'foo'}
print(
    User.__dict__,
)  # {'__init__': <function User.__init__ at 0x106f120d0>, 'SAY': <function User.say at 0x106f12160>, ...}
