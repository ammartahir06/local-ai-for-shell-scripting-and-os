"""Built-in Python code training corpus for the Markov chain engine.

Contains categorized Python code snippets covering common student topics.
This module is used by the train_model.py script to build the n-gram model.
"""

CORPUS = [
    # --- Loops ---
    '''
# Print numbers from 0 to 9 using a for loop
for i in range(10):
    print(i)
''',
    '''
# Sum all numbers in a list
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
print(f"Sum: {total}")
''',
    '''
# While loop countdown
count = 10
while count > 0:
    print(count)
    count -= 1
print("Liftoff!")
''',
    '''
# List comprehension to create squares
squares = [x ** 2 for x in range(10)]
print(squares)
''',
    '''
# Nested loop to create a multiplication table
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i} x {j} = {i * j}", end="\\t")
    print()
''',
    '''
# Iterate over a dictionary
student_grades = {"Alice": 90, "Bob": 85, "Charlie": 92}
for name, grade in student_grades.items():
    print(f"{name}: {grade}")
''',
    '''
# Filter even numbers using list comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [n for n in numbers if n % 2 == 0]
print(evens)
''',
    '''
# Enumerate to get index and value
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
''',

    # --- Functions ---
    '''
# Define a function that calculates factorial
def factorial(n):
    """Calculate the factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"5! = {result}")
''',
    '''
# Function with default parameters
def greet(name, greeting="Hello"):
    """Greet a person with a custom message."""
    return f"{greeting}, {name}!"

print(greet("Alice"))
print(greet("Bob", "Hi"))
''',
    '''
# Function that returns multiple values
def min_max(numbers):
    """Return the minimum and maximum of a list."""
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {low}, Max: {high}")
''',
    '''
# Lambda function for sorting
students = [("Alice", 90), ("Bob", 85), ("Charlie", 92)]
students.sort(key=lambda s: s[1], reverse=True)
for name, grade in students:
    print(f"{name}: {grade}")
''',
    '''
# Fibonacci function using iteration
def fibonacci(n):
    """Return the first n Fibonacci numbers."""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib[:n]

print(fibonacci(10))
''',

    # --- File I/O ---
    '''
# Read a text file
with open("example.txt", "r") as f:
    content = f.read()
print(content)
''',
    '''
# Write to a text file
lines = ["Hello, world!", "Python is great.", "File I/O is easy."]
with open("output.txt", "w") as f:
    for line in lines:
        f.write(line + "\\n")
''',
    '''
# Read a file line by line
with open("data.txt", "r") as f:
    for line in f:
        print(line.strip())
''',
    '''
# Read and write CSV files
import csv

# Writing CSV
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age", "City"])
    writer.writerow(["Alice", 30, "New York"])
    writer.writerow(["Bob", 25, "London"])

# Reading CSV
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
''',
    '''
# Read JSON file
import json

with open("config.json", "r") as f:
    data = json.load(f)
print(data)
''',
    '''
# Write JSON file
import json

data = {"name": "Alice", "scores": [90, 85, 92]}
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
''',

    # --- Classes and OOP ---
    '''
# Define a simple class
class Dog:
    """A simple Dog class."""
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        """Make the dog bark."""
        return f"{self.name} says woof!"

    def __str__(self):
        return f"{self.name} ({self.breed})"

my_dog = Dog("Rex", "Labrador")
print(my_dog.bark())
print(my_dog)
''',
    '''
# Inheritance example
class Animal:
    """Base class for animals."""
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement speak()")

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

animals = [Cat("Whiskers"), Dog("Rex")]
for animal in animals:
    print(animal.speak())
''',
    '''
# Class with properties
class Circle:
    """A circle with radius, area, and circumference."""
    import math

    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

    @property
    def circumference(self):
        import math
        return 2 * math.pi * self._radius

c = Circle(5)
print(f"Area: {c.area:.2f}")
print(f"Circumference: {c.circumference:.2f}")
''',

    # --- Sorting and Searching ---
    '''
# Bubble sort implementation
def bubble_sort(arr):
    """Sort a list using bubble sort algorithm."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
print(bubble_sort(numbers))
''',
    '''
# Binary search implementation
def binary_search(arr, target):
    """Search for target in a sorted list using binary search."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

sorted_list = [1, 3, 5, 7, 9, 11, 13]
index = binary_search(sorted_list, 7)
print(f"Found at index: {index}")
''',
    '''
# Sort a list of dictionaries
students = [
    {"name": "Alice", "grade": 90},
    {"name": "Bob", "grade": 85},
    {"name": "Charlie", "grade": 92},
]
sorted_students = sorted(students, key=lambda s: s["grade"], reverse=True)
for s in sorted_students:
    print(f"{s['name']}: {s['grade']}")
''',

    # --- Data Structures ---
    '''
# Stack implementation using a list
class Stack:
    """A simple stack data structure."""
    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.pop())  # 3
print(stack.peek())  # 2
''',
    '''
# Dictionary operations
# Create a dictionary
person = {"name": "Alice", "age": 30, "city": "New York"}

# Access values
print(person["name"])
print(person.get("email", "Not found"))

# Add and update
person["email"] = "alice@example.com"
person["age"] = 31

# Iterate
for key, value in person.items():
    print(f"{key}: {value}")

# Dictionary comprehension
squares = {x: x ** 2 for x in range(6)}
print(squares)
''',
    '''
# Working with sets
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Set operations
print(f"Union: {set_a | set_b}")
print(f"Intersection: {set_a & set_b}")
print(f"Difference: {set_a - set_b}")
print(f"Symmetric difference: {set_a ^ set_b}")
''',

    # --- String Operations ---
    '''
# String manipulation examples
text = "Hello, World!"

# Common string methods
print(text.upper())
print(text.lower())
print(text.replace("World", "Python"))
print(text.split(", "))
print(text.strip())
print(text.startswith("Hello"))
print(text.find("World"))
''',
    '''
# String formatting
name = "Alice"
age = 30

# f-string formatting
print(f"My name is {name} and I am {age} years old.")

# format method
print("My name is {} and I am {} years old.".format(name, age))

# Padding and alignment
for i in range(1, 6):
    print(f"{i:>3}: {'*' * i}")
''',

    # --- Error Handling ---
    '''
# Try-except error handling
def divide(a, b):
    """Safely divide two numbers."""
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError:
        print("Error: Invalid input types")
        return None
    else:
        return result
    finally:
        print("Division operation completed")

print(divide(10, 3))
print(divide(10, 0))
''',
    '''
# Custom exception
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the balance."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw {amount}: only {balance} available"
        )

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

account = BankAccount(100)
try:
    account.withdraw(150)
except InsufficientFundsError as e:
    print(e)
''',

    # --- Recursion ---
    '''
# Recursive function to calculate power
def power(base, exp):
    """Calculate base raised to exp using recursion."""
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

print(power(2, 10))  # 1024
''',
    '''
# Recursive function to reverse a string
def reverse_string(s):
    """Reverse a string using recursion."""
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]

print(reverse_string("hello"))  # olleh
''',

    # --- List Operations ---
    '''
# Common list operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sorting
print(sorted(numbers))
print(sorted(numbers, reverse=True))

# Slicing
print(numbers[2:5])
print(numbers[::2])
print(numbers[::-1])

# Map and filter
doubled = list(map(lambda x: x * 2, numbers))
big = list(filter(lambda x: x > 4, numbers))
print(f"Doubled: {doubled}")
print(f"Greater than 4: {big}")
''',
    '''
# Flatten a nested list
def flatten(nested_list):
    """Flatten a nested list into a single list."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

nested = [1, [2, 3], [4, [5, 6]], 7]
print(flatten(nested))  # [1, 2, 3, 4, 5, 6, 7]
''',

    # ===================================================================
    # DATA STRUCTURES & ALGORITHMS (DSA)
    # ===================================================================

    # --- Linked List ---
    '''
# Singly linked list implementation
class Node:
    """A node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Singly linked list with common operations."""
    def __init__(self):
        self.head = None

    def append(self, data):
        """Add a node to the end of the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data):
        """Add a node to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        """Delete the first node with the given data."""
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    def find(self, data):
        """Search for a node with the given data. Returns True if found."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def reverse(self):
        """Reverse the linked list in place."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        """Convert linked list to a Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __str__(self):
        return " -> ".join(str(x) for x in self.to_list())


# Usage
ll = LinkedList()
for val in [1, 2, 3, 4, 5]:
    ll.append(val)
print(ll)           # 1 -> 2 -> 3 -> 4 -> 5
ll.reverse()
print(ll)           # 5 -> 4 -> 3 -> 2 -> 1
ll.delete(3)
print(ll.find(3))   # False
''',

    # --- Doubly Linked List ---
    '''
# Doubly linked list implementation
class DNode:
    """A node in a doubly linked list."""
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly linked list with forward and backward traversal."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        """Add a node to the end."""
        new_node = DNode(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, data):
        """Add a node to the beginning."""
        new_node = DNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def delete(self, data):
        """Delete the first node with the given data."""
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.size -= 1
                return True
            current = current.next
        return False

    def forward(self):
        """Traverse the list forward."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def backward(self):
        """Traverse the list backward."""
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result


# Usage
dll = DoublyLinkedList()
for val in [10, 20, 30, 40, 50]:
    dll.append(val)
print("Forward:", dll.forward())    # [10, 20, 30, 40, 50]
print("Backward:", dll.backward())  # [50, 40, 30, 20, 10]
dll.delete(30)
print("After delete:", dll.forward())  # [10, 20, 40, 50]
''',

    # --- Queue ---
    '''
# Queue implementation using a list
class Queue:
    """A FIFO queue data structure."""
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.pop(0)

    def peek(self):
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return f"Queue({self._items})"


# Usage
q = Queue()
q.enqueue("first")
q.enqueue("second")
q.enqueue("third")
print(q.dequeue())  # first
print(q.peek())     # second
print(q.size())     # 2
''',

    # --- Binary Search Tree ---
    '''
# Binary search tree implementation
class BSTNode:
    """A node in a binary search tree."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary search tree with insert, search, delete, and traversals."""
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert a key into the BST."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        """Search for a key in the BST. Returns True if found."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def delete(self, key):
        """Delete a key from the BST."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node found
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Node has two children: find inorder successor
            successor = self._min_node(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)
        return node

    def _min_node(self, node):
        """Find the node with the minimum key."""
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        """Return keys in sorted order (inorder traversal)."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder(self):
        """Return keys in preorder traversal."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        """Return keys in postorder traversal."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    def height(self):
        """Return the height of the BST."""
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))


# Usage
bst = BinarySearchTree()
for val in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(val)

print("Inorder:", bst.inorder())     # [20, 30, 40, 50, 60, 70, 80]
print("Preorder:", bst.preorder())   # [50, 30, 20, 40, 70, 60, 80]
print("Postorder:", bst.postorder()) # [20, 40, 30, 60, 80, 70, 50]
print("Height:", bst.height())       # 2
print("Search 40:", bst.search(40))  # True
bst.delete(30)
print("After delete 30:", bst.inorder())  # [20, 40, 50, 60, 70, 80]
''',

    # --- Heap / Priority Queue ---
    '''
# Min-heap implementation from scratch
class MinHeap:
    """A min-heap (priority queue) implementation."""
    def __init__(self):
        self._heap = []

    def push(self, val):
        """Insert a value into the heap."""
        self._heap.append(val)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        """Remove and return the smallest value."""
        if not self._heap:
            raise IndexError("Heap is empty")
        self._swap(0, len(self._heap) - 1)
        val = self._heap.pop()
        if self._heap:
            self._sift_down(0)
        return val

    def peek(self):
        """Return the smallest value without removing it."""
        if not self._heap:
            raise IndexError("Heap is empty")
        return self._heap[0]

    def _sift_up(self, idx):
        """Move a node up to maintain heap property."""
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx] < self._heap[parent]:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx):
        """Move a node down to maintain heap property."""
        size = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < size and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < size and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def size(self):
        return len(self._heap)

    def __str__(self):
        return f"MinHeap({self._heap})"


# Usage
heap = MinHeap()
for val in [5, 3, 8, 1, 2, 7]:
    heap.push(val)

print("Min:", heap.peek())  # 1
while heap.size() > 0:
    print(heap.pop(), end=" ")  # 1 2 3 5 7 8
print()
''',

    # --- Hash Map ---
    '''
# Hash map (hash table) implementation
class HashMap:
    """A simple hash map using chaining for collision resolution."""
    def __init__(self, capacity=16):
        self._capacity = capacity
        self._size = 0
        self._buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        """Compute the bucket index for a key."""
        return hash(key) % self._capacity

    def put(self, key, value):
        """Insert or update a key-value pair."""
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key, default=None):
        """Retrieve the value for a key, or default if not found."""
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return default

    def remove(self, key):
        """Remove a key-value pair. Returns True if found."""
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def contains(self, key):
        """Check if a key exists in the map."""
        return self.get(key) is not None

    def keys(self):
        """Return all keys."""
        result = []
        for bucket in self._buckets:
            for k, v in bucket:
                result.append(k)
        return result

    def values(self):
        """Return all values."""
        result = []
        for bucket in self._buckets:
            for k, v in bucket:
                result.append(v)
        return result

    def __len__(self):
        return self._size


# Usage
hm = HashMap()
hm.put("name", "Alice")
hm.put("age", 30)
hm.put("city", "New York")
print(hm.get("name"))     # Alice
print(hm.contains("age")) # True
hm.remove("city")
print(hm.keys())          # ['name', 'age']
''',

    # --- Graph (Adjacency List) ---
    '''
# Graph implementation with BFS and DFS
from collections import deque


class Graph:
    """An undirected graph using adjacency list representation."""
    def __init__(self):
        self._adj = {}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self._adj:
            self._adj[vertex] = []

    def add_edge(self, u, v):
        """Add an undirected edge between u and v."""
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u].append(v)
        self._adj[v].append(u)

    def bfs(self, start):
        """Breadth-first search from a starting vertex."""
        visited = set()
        queue = deque([start])
        visited.add(start)
        order = []
        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self._adj.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start):
        """Depth-first search from a starting vertex."""
        visited = set()
        order = []
        self._dfs_helper(start, visited, order)
        return order

    def _dfs_helper(self, vertex, visited, order):
        visited.add(vertex)
        order.append(vertex)
        for neighbor in self._adj.get(vertex, []):
            if neighbor not in visited:
                self._dfs_helper(neighbor, visited, order)

    def has_path(self, start, end):
        """Check if a path exists between start and end using BFS."""
        if start == end:
            return True
        visited = set()
        queue = deque([start])
        visited.add(start)
        while queue:
            vertex = queue.popleft()
            for neighbor in self._adj.get(vertex, []):
                if neighbor == end:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False

    def shortest_path(self, start, end):
        """Find the shortest path between start and end using BFS."""
        if start == end:
            return [start]
        visited = {start}
        queue = deque([(start, [start])])
        while queue:
            vertex, path = queue.popleft()
            for neighbor in self._adj.get(vertex, []):
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []  # No path found

    def vertices(self):
        return list(self._adj.keys())

    def edges(self):
        seen = set()
        result = []
        for u in self._adj:
            for v in self._adj[u]:
                edge = tuple(sorted([u, v]))
                if edge not in seen:
                    seen.add(edge)
                    result.append(edge)
        return result


# Usage
g = Graph()
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.add_edge("C", "D")
g.add_edge("D", "E")

print("BFS from A:", g.bfs("A"))           # ['A', 'B', 'C', 'D', 'E']
print("DFS from A:", g.dfs("A"))           # ['A', 'B', 'D', 'C', 'E']
print("Path A->E:", g.shortest_path("A", "E"))  # ['A', 'B', 'D', 'E']
print("Has path A->E:", g.has_path("A", "E"))   # True
''',

    # --- Directed Graph with Topological Sort ---
    '''
# Directed graph with topological sort and cycle detection
from collections import deque


class DirectedGraph:
    """A directed graph with topological sort using Kahn's algorithm."""
    def __init__(self):
        self._adj = {}
        self._in_degree = {}

    def add_vertex(self, vertex):
        if vertex not in self._adj:
            self._adj[vertex] = []
            self._in_degree[vertex] = 0

    def add_edge(self, u, v):
        """Add a directed edge from u to v."""
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u].append(v)
        self._in_degree[v] += 1

    def topological_sort(self):
        """Return vertices in topological order using Kahn's algorithm.
        Raises ValueError if the graph has a cycle."""
        in_degree = dict(self._in_degree)
        queue = deque([v for v in in_degree if in_degree[v] == 0])
        order = []

        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self._adj[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self._adj):
            raise ValueError("Graph has a cycle, topological sort not possible")
        return order

    def has_cycle(self):
        """Detect if the directed graph has a cycle using DFS."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in self._adj}

        def dfs(v):
            color[v] = GRAY
            for neighbor in self._adj[v]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[v] = BLACK
            return False

        return any(dfs(v) for v in self._adj if color[v] == WHITE)


# Usage — course prerequisites
dg = DirectedGraph()
dg.add_edge("Math 101", "Math 201")
dg.add_edge("Math 101", "Physics 101")
dg.add_edge("Math 201", "Math 301")
dg.add_edge("Physics 101", "Physics 201")

print("Topological order:", dg.topological_sort())
print("Has cycle:", dg.has_cycle())  # False
''',

    # --- Sorting Algorithms ---
    '''
# Merge sort implementation
def merge_sort(arr):
    """Sort a list using merge sort algorithm. Time: O(n log n), Space: O(n)."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Usage
numbers = [38, 27, 43, 3, 9, 82, 10]
print("Original:", numbers)
print("Sorted:", merge_sort(numbers))
''',

    '''
# Quick sort implementation
def quick_sort(arr):
    """Sort a list using quick sort algorithm. Time: O(n log n) avg, Space: O(log n)."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# In-place quick sort (more efficient)
def quick_sort_inplace(arr, low=0, high=None):
    """In-place quick sort using Lomuto partition scheme."""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)


def partition(arr, low, high):
    """Partition the array around the pivot (last element)."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Usage
numbers = [38, 27, 43, 3, 9, 82, 10]
print("Quick sort:", quick_sort(numbers))

numbers2 = [38, 27, 43, 3, 9, 82, 10]
quick_sort_inplace(numbers2)
print("In-place:", numbers2)
''',

    '''
# Insertion sort implementation
def insertion_sort(arr):
    """Sort a list using insertion sort. Time: O(n^2), Space: O(1).
    Good for small or nearly sorted arrays."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# Usage
numbers = [12, 11, 13, 5, 6]
print("Sorted:", insertion_sort(numbers))
''',

    '''
# Selection sort implementation
def selection_sort(arr):
    """Sort a list using selection sort. Time: O(n^2), Space: O(1)."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# Usage
numbers = [64, 25, 12, 22, 11]
print("Sorted:", selection_sort(numbers))
''',

    '''
# Counting sort implementation
def counting_sort(arr):
    """Sort a list of non-negative integers using counting sort.
    Time: O(n + k), Space: O(k) where k is the max value."""
    if not arr:
        return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)

    # Count occurrences
    for num in arr:
        count[num] += 1

    # Build sorted array
    result = []
    for val, cnt in enumerate(count):
        result.extend([val] * cnt)
    return result


# Usage
numbers = [4, 2, 2, 8, 3, 3, 1]
print("Sorted:", counting_sort(numbers))
''',

    '''
# Heap sort implementation
def heap_sort(arr):
    """Sort a list using heap sort. Time: O(n log n), Space: O(1)."""
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


def heapify(arr, n, i):
    """Maintain the max-heap property."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


# Usage
numbers = [12, 11, 13, 5, 6, 7]
print("Sorted:", heap_sort(numbers))
''',

    # --- Dynamic Programming ---
    '''
# Longest common subsequence (LCS) using dynamic programming
def lcs(text1, text2):
    """Find the length of the longest common subsequence.
    Time: O(m*n), Space: O(m*n)."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to find the actual subsequence
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            result.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], "".join(reversed(result))


# Usage
s1 = "ABCBDAB"
s2 = "BDCAB"
length, subseq = lcs(s1, s2)
print(f"LCS length: {length}")  # 4
print(f"LCS: {subseq}")         # BCAB
''',

    '''
# 0/1 Knapsack problem using dynamic programming
def knapsack(weights, values, capacity):
    """Solve the 0/1 knapsack problem.
    Time: O(n * capacity), Space: O(n * capacity)."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i - 1][w]
            # Take item i if it fits
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])

    # Backtrack to find which items were selected
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]

    return dp[n][capacity], list(reversed(selected))


# Usage
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 8
max_value, items = knapsack(weights, values, capacity)
print(f"Max value: {max_value}")  # 10
print(f"Selected items: {items}")
''',

    '''
# Coin change problem using dynamic programming
def coin_change(coins, amount):
    """Find the minimum number of coins to make the given amount.
    Returns -1 if not possible. Time: O(amount * len(coins))."""
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1

    return dp[amount] if dp[amount] != float("inf") else -1


def coin_change_combinations(coins, amount):
    """Count the number of ways to make the given amount.
    Time: O(amount * len(coins))."""
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]


# Usage
coins = [1, 5, 10, 25]
amount = 36
print(f"Min coins for {amount}: {coin_change(coins, amount)}")
print(f"Ways to make {amount}: {coin_change_combinations(coins, amount)}")
''',

    '''
# Longest increasing subsequence using dynamic programming
def lis(arr):
    """Find the length of the longest increasing subsequence.
    Time: O(n^2), Space: O(n)."""
    if not arr:
        return 0, []

    n = len(arr)
    dp = [1] * n
    parent = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

    # Find the maximum length and backtrack
    max_len = max(dp)
    idx = dp.index(max_len)

    # Reconstruct the subsequence
    result = []
    while idx != -1:
        result.append(arr[idx])
        idx = parent[idx]

    return max_len, list(reversed(result))


# Usage
arr = [10, 9, 2, 5, 3, 7, 101, 18]
length, subseq = lis(arr)
print(f"LIS length: {length}")  # 4
print(f"LIS: {subseq}")         # [2, 3, 7, 18] or [2, 5, 7, 18]
''',

    '''
# Edit distance (Levenshtein distance) using dynamic programming
def edit_distance(word1, word2):
    """Calculate the minimum edit distance between two strings.
    Operations: insert, delete, replace. Time: O(m*n)."""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete
                    dp[i][j - 1],      # insert
                    dp[i - 1][j - 1],  # replace
                )

    return dp[m][n]


# Usage
print(edit_distance("kitten", "sitting"))  # 3
print(edit_distance("sunday", "saturday")) # 3
''',

    '''
# Matrix chain multiplication using dynamic programming
def matrix_chain_order(dimensions):
    """Find the optimal way to multiply a chain of matrices.
    dimensions[i] is the row count of matrix i, dimensions[-1] is the
    column count of the last matrix. Time: O(n^3)."""
    n = len(dimensions) - 1  # number of matrices
    # dp[i][j] = minimum multiplications for matrices i..j
    dp = [[0] * n for _ in range(n)]
    # split[i][j] = where to split for optimal result
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):  # chain length
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = (dp[i][k] + dp[k + 1][j]
                        + dimensions[i] * dimensions[k + 1] * dimensions[j + 1])
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    def build_solution(i, j):
        if i == j:
            return f"M{i + 1}"
        k = split[i][j]
        left = build_solution(i, k)
        right = build_solution(k + 1, j)
        return f"({left} x {right})"

    return dp[0][n - 1], build_solution(0, n - 1)


# Usage: 4 matrices with dimensions 10x30, 30x5, 5x60, 60x10
dims = [10, 30, 5, 60, 10]
min_ops, order = matrix_chain_order(dims)
print(f"Minimum multiplications: {min_ops}")
print(f"Optimal order: {order}")
''',

    # --- Trie ---
    '''
# Trie (prefix tree) implementation
class TrieNode:
    """A node in a trie."""
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """A trie for efficient string prefix operations."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """Check if a word exists in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """Check if any word starts with the given prefix."""
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix):
        """Return all words that start with the given prefix."""
        node = self._find_node(prefix)
        if node is None:
            return []
        results = []
        self._collect_words(node, prefix, results)
        return results

    def _find_node(self, prefix):
        """Find the node corresponding to the last character of prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node, prefix, results):
        """Collect all words from this node downward."""
        if node.is_end:
            results.append(prefix)
        for char, child in sorted(node.children.items()):
            self._collect_words(child, prefix + char, results)


# Usage
trie = Trie()
words = ["apple", "app", "application", "apply", "banana", "band"]
for word in words:
    trie.insert(word)

print(trie.search("app"))          # True
print(trie.search("apt"))          # False
print(trie.starts_with("app"))     # True
print(trie.autocomplete("app"))    # ['app', 'apple', 'application', 'apply']
print(trie.autocomplete("ban"))    # ['banana', 'band']
''',

    # --- Dijkstra's Shortest Path ---
    '''
# Dijkstra's shortest path algorithm
import heapq


def dijkstra(graph, start):
    """Find shortest paths from start to all other vertices.
    graph: dict of {vertex: [(neighbor, weight), ...]}
    Returns: (distances, predecessors) dictionaries."""
    distances = {vertex: float("inf") for vertex in graph}
    distances[start] = 0
    predecessors = {vertex: None for vertex in graph}
    # Priority queue: (distance, vertex)
    pq = [(0, start)]

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current_dist > distances[current]:
            continue

        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))

    return distances, predecessors


def reconstruct_path(predecessors, start, end):
    """Reconstruct the shortest path from start to end."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    if path[0] != start:
        return []  # No path exists
    return path


# Usage
graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("A", 4), ("C", 1), ("D", 5)],
    "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
    "D": [("B", 5), ("C", 8), ("E", 2)],
    "E": [("C", 10), ("D", 2)],
}

distances, predecessors = dijkstra(graph, "A")
print("Distances from A:", distances)
print("Path A -> E:", reconstruct_path(predecessors, "A", "E"))
''',

    # --- Two Pointer Technique ---
    '''
# Two pointer technique examples

def two_sum_sorted(arr, target):
    """Find two numbers in a sorted array that sum to target.
    Time: O(n), Space: O(1)."""
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []


def remove_duplicates(arr):
    """Remove duplicates from a sorted array in place.
    Returns the new length. Time: O(n), Space: O(1)."""
    if not arr:
        return 0
    write = 1
    for read in range(1, len(arr)):
        if arr[read] != arr[read - 1]:
            arr[write] = arr[read]
            write += 1
    return write


def is_palindrome(s):
    """Check if a string is a palindrome using two pointers.
    Ignores non-alphanumeric characters and case."""
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def container_with_most_water(heights):
    """Find two lines that form a container holding the most water.
    Time: O(n), Space: O(1)."""
    left, right = 0, len(heights) - 1
    max_area = 0
    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        max_area = max(max_area, width * height)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return max_area


# Usage
print(two_sum_sorted([1, 2, 3, 4, 6], 6))  # [1, 3]
print(is_palindrome("A man, a plan, a canal: Panama"))  # True
print(container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
''',

    # --- Sliding Window ---
    '''
# Sliding window technique examples

def max_sum_subarray(arr, k):
    """Find the maximum sum of a subarray of size k.
    Time: O(n), Space: O(1)."""
    if len(arr) < k:
        return 0

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum


def longest_substring_no_repeat(s):
    """Find the length of the longest substring without repeating characters.
    Time: O(n), Space: O(min(n, alphabet_size))."""
    char_index = {}
    max_length = 0
    start = 0

    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = end
        max_length = max(max_length, end - start + 1)

    return max_length


def min_window_substring(s, t):
    """Find the minimum window in s that contains all characters of t.
    Time: O(n), Space: O(n)."""
    from collections import Counter

    if not s or not t:
        return ""

    need = Counter(t)
    have = {}
    formed = 0
    required = len(need)
    best = (float("inf"), 0, 0)  # (length, left, right)
    left = 0

    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        if char in need and have[char] == need[char]:
            formed += 1

        while formed == required:
            length = right - left + 1
            if length < best[0]:
                best = (length, left, right)
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]


# Usage
print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3))  # 9
print(longest_substring_no_repeat("abcabcbb"))    # 3
print(min_window_substring("ADOBECODEBANC", "ABC"))  # "BANC"
''',

    # --- Backtracking ---
    '''
# Backtracking examples

def permutations(nums):
    """Generate all permutations of a list."""
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i + 1:])
            current.pop()

    backtrack([], nums)
    return result


def combinations(nums, k):
    """Generate all combinations of size k from a list."""
    result = []

    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result


def subsets(nums):
    """Generate all subsets (power set) of a list."""
    result = []

    def backtrack(start, current):
        result.append(current[:])
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result


def n_queens(n):
    """Solve the N-Queens problem. Returns all valid board configurations."""
    result = []
    board = [["." for _ in range(n)] for _ in range(n)]

    def is_safe(row, col):
        # Check column
        for r in range(row):
            if board[r][col] == "Q":
                return False
        # Check upper-left diagonal
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] == "Q":
                return False
            r -= 1
            c -= 1
        # Check upper-right diagonal
        r, c = row - 1, col + 1
        while r >= 0 and c < n:
            if board[r][c] == "Q":
                return False
            r -= 1
            c += 1
        return True

    def backtrack(row):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = "Q"
                backtrack(row + 1)
                board[row][col] = "."

    backtrack(0)
    return result


# Usage
print("Permutations of [1,2,3]:", permutations([1, 2, 3]))
print("Combinations C(4,2):", combinations([1, 2, 3, 4], 2))
print("Subsets of [1,2]:", subsets([1, 2]))
print(f"4-Queens solutions: {len(n_queens(4))}")  # 2
''',
]
