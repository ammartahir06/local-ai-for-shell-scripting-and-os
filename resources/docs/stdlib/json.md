# json — JSON Encoder and Decoder

The `json` module provides functions for working with JSON data.

## Common Functions

### json.dumps(obj)
Serializes a Python object to a JSON-formatted string.

```python
import json
data = {"name": "Alice", "age": 30}
text = json.dumps(data, indent=2)
```

### json.loads(s)
Deserializes a JSON string to a Python object.

```python
import json
text = '{"name": "Alice", "age": 30}'
data = json.loads(text)
```

### json.dump(obj, fp)
Writes a Python object as JSON to a file.

```python
import json
with open('data.json', 'w') as f:
    json.dump({"key": "value"}, f)
```

### json.load(fp)
Reads JSON from a file into a Python object.

```python
import json
with open('data.json') as f:
    data = json.load(f)
```
