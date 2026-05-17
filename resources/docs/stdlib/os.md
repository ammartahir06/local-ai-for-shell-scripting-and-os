# os — Operating System Interface

The `os` module provides functions for interacting with the operating system.

## Common Functions

### os.getcwd()
Returns the current working directory as a string.

```python
import os
print(os.getcwd())
```

### os.listdir(path='.')
Returns a list of entries in the given directory.

```python
import os
for entry in os.listdir('.'):
    print(entry)
```

### os.path.join(*paths)
Joins path components intelligently.

```python
import os
full_path = os.path.join('home', 'user', 'documents')
```

### os.makedirs(name, exist_ok=False)
Creates a directory and any missing parent directories.

```python
import os
os.makedirs('output/reports', exist_ok=True)
```
