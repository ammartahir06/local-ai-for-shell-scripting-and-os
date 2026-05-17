# Bash Shell Scripting Reference

## Script Structure

Every bash script starts with a shebang line and should have proper error handling:

```bash
#!/bin/bash
set -euo pipefail
```

## Variables

```bash
name="value"          # No spaces around =
readonly CONST="val"  # Read-only variable
echo "$name"          # Use quotes to prevent word splitting
echo "${name}_suffix" # Braces for clarity
```

## Conditionals

```bash
if [ condition ]; then
    commands
elif [ condition ]; then
    commands
else
    commands
fi
```

### Test Operators

| Operator | Description |
|----------|-------------|
| -f file  | File exists and is regular |
| -d dir   | Directory exists |
| -r file  | File is readable |
| -w file  | File is writable |
| -x file  | File is executable |
| -z str   | String is empty |
| -n str   | String is not empty |
| -eq      | Integer equal |
| -ne      | Integer not equal |
| -gt      | Integer greater than |
| -lt      | Integer less than |

## Loops

```bash
# For loop
for item in list; do
    commands
done

# While loop
while [ condition ]; do
    commands
done

# C-style for loop
for ((i=0; i<10; i++)); do
    commands
done
```

## Functions

```bash
function_name() {
    local var=$1    # Local variable
    echo "$var"
    return 0        # Return status (0 = success)
}
result=$(function_name "arg")
```

## Common Commands

| Command | Purpose |
|---------|---------|
| grep    | Search text patterns |
| awk     | Text processing |
| sed     | Stream editing |
| find    | Search files |
| xargs   | Build commands from input |
| cut     | Extract columns |
| sort    | Sort lines |
| uniq    | Remove duplicates |
| wc      | Count lines/words/chars |
| tee     | Split output to file and stdout |
