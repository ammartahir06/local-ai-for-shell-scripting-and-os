# Classes in Python

## Defining a Class

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} says woof!"
```

## Creating Instances

```python
my_dog = Dog("Rex", "Labrador")
print(my_dog.bark())
```

## Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"
```

## Class Methods and Static Methods

```python
class MathHelper:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def description(cls):
        return f"This is {cls.__name__}"
```
