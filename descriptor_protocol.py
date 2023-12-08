"""
This module demonstrates the descriptor protocol.
"""


class IntField:
    """This class represents an integer field"""
    def __get__(self, instance, owner):
        """This method is called when the attribute is accessed"""
        print("get", end=": ")
        return instance.v

    def __set__(self, instance, value):
        """This method is called when the attribute is set"""
        if isinstance(value, int):
            print("set:", self, instance, value)
            instance.v = value
        else:
            raise TypeError("must be an integer")

    def __delete__(self, instance):
        """This method is called when the attribute is deleted"""
        print("delete")
        del instance.v


class Person:
    """This class represents a person"""
    age = IntField()  # age descriptor


p1 = Person()
p1.age = 10  # set: <__main__.IntField object at 0x10942afa0> <__main__.Person object at 0x10942af70> 10
print(p1.age)  # get: 10

p2 = Person()
p2.age = 20  # set: <__main__.IntField object at 0x10942afa0> <__main__.Person object at 0x10942aa00> 20
print(p2.age)  # get: 20

print(p1.age)  # get: 10

del p1.age  # delete
print(p1.__dict__)  # {}

p2.age = "abc"  # TypeError: must be an integer
