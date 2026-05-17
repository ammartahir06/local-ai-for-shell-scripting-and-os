# Loops in Python

## For Loop

Iterate over a sequence of items.

```python
# Print numbers 0 through 4
for i in range(5):
    print(i)
```

## While Loop

Repeat while a condition is true.

```python
# Count down from 5
count = 5
while count > 0:
    print(count)
    count -= 1
```

## Iterating Over a List

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

## List Comprehension

A concise way to create lists from loops.

```python
squares = [x ** 2 for x in range(10)]
```
