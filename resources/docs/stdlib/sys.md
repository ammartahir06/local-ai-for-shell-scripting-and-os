# sys — System-Specific Parameters and Functions

The `sys` module provides access to variables and functions related to the Python interpreter.

## Common Attributes

### sys.argv
A list of command-line arguments passed to the script.

```python
import sys
print(sys.argv)  # ['script.py', 'arg1', 'arg2']
```

### sys.version
A string containing the Python version number.

```python
import sys
print(sys.version)
```

### sys.path
A list of directories where Python looks for modules.

```python
import sys
for p in sys.path:
    print(p)
```

### sys.exit(code=0)
Exits the program with the given status code.

```python
import sys
if error_occurred:
    sys.exit(1)
```
