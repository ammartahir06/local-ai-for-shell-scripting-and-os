# File I/O in Python

## Reading a File

```python
# Read entire file content
with open('example.txt', 'r') as f:
    content = f.read()
```

## Writing to a File

```python
# Write text to a file (creates or overwrites)
with open('output.txt', 'w') as f:
    f.write('Hello, world!\n')
```

## Appending to a File

```python
# Append text without overwriting
with open('log.txt', 'a') as f:
    f.write('New log entry\n')
```

## Reading Line by Line

```python
with open('data.txt') as f:
    for line in f:
        print(line.strip())
```
