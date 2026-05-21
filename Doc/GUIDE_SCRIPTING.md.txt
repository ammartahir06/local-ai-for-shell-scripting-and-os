# 🔴 BASH SHELL SCRIPTING — Complete Exam Guide
### Priority #1 — This WILL come in your exam

> **Why this is #1:** Scripting came in today's other section. LT3 was scripting. Your slides cover it. It's the easiest topic to test in a lab exam.

---

## 1. THE ABSOLUTE BASICS — MEMORIZE THESE

### 1.1 Every Script Starts With This
```bash
#!/bin/bash
# This is called a "shebang" — tells the OS which interpreter to use
```

### 1.2 Running a Script
```bash
# Method 1: Run with bash directly
bash myscript.sh

# Method 2: Make executable and run
chmod +x myscript.sh    # give execute permission
./myscript.sh            # run it
```

### 1.3 Variables — NO SPACES around `=`
```bash
# ✅ CORRECT:
name="Ahad"
age=21
count=0

# ❌ WRONG (will error):
name = "Ahad"      # bash thinks "name" is a command
```

### 1.4 Reading Variables
```bash
echo $name           # prints: Ahad
echo "Hello $name"   # prints: Hello Ahad  (double quotes expand variables)
echo 'Hello $name'   # prints: Hello $name (single quotes = literal)
echo "Age is ${age}" # ${} is safer when followed by other text
```

### 1.5 Command-Line Arguments
```bash
#!/bin/bash
echo "Script name: $0"      # ./myscript.sh
echo "First argument: $1"   # first arg
echo "Second argument: $2"  # second arg
echo "All arguments: $@"    # all args as separate words
echo "Number of args: $#"   # count of arguments
```

### 1.6 Reading User Input
```bash
#!/bin/bash
echo "Enter a number:"
read num                    # reads into variable $num
echo "You entered: $num"

# Or on same line:
read -p "Enter your name: " name
echo "Hello $name"
```

---

## 2. ARITHMETIC — How to Do Math in Bash

```bash
# Method 1: $(( expression )) — MOST COMMON
a=10
b=3
sum=$((a + b))          # 13
diff=$((a - b))         # 7
product=$((a * b))      # 30
quotient=$((a / b))     # 3 (integer division!)
remainder=$((a % b))    # 1 (modulo)

echo "Sum = $sum"

# Method 2: expr (older style, spaces required)
result=$(expr $a + $b)

# Method 3: let
let "sum = a + b"

# Method 4: bc for decimals
echo "scale=2; 10/3" | bc    # 3.33
```

---

## 3. CONDITIONALS — if/elif/else/fi

### 3.1 Basic if Statement
```bash
#!/bin/bash
num=15

if [ $num -gt 10 ]; then
    echo "$num is greater than 10"
elif [ $num -eq 10 ]; then
    echo "$num is equal to 10"
else
    echo "$num is less than 10"
fi
```

### 3.2 Comparison Operators — MEMORIZE THIS TABLE

**For NUMBERS (use inside `[ ]` or `[[ ]]`):**

| Operator | Meaning | Example |
|----------|---------|---------|
| `-eq` | Equal | `[ $a -eq $b ]` |
| `-ne` | Not equal | `[ $a -ne $b ]` |
| `-gt` | Greater than | `[ $a -gt $b ]` |
| `-lt` | Less than | `[ $a -lt $b ]` |
| `-ge` | Greater or equal | `[ $a -ge $b ]` |
| `-le` | Less or equal | `[ $a -le $b ]` |

**For STRINGS:**

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` or `==` | Equal | `[ "$a" = "$b" ]` |
| `!=` | Not equal | `[ "$a" != "$b" ]` |
| `-z` | Is empty | `[ -z "$a" ]` |
| `-n` | Is not empty | `[ -n "$a" ]` |

**For FILES:**

| Operator | Meaning | Example |
|----------|---------|---------|
| `-f` | Is a regular file | `[ -f "$file" ]` |
| `-d` | Is a directory | `[ -d "$dir" ]` |
| `-e` | Exists (file or dir) | `[ -e "$path" ]` |
| `-r` | Is readable | `[ -r "$file" ]` |
| `-w` | Is writable | `[ -w "$file" ]` |
| `-x` | Is executable | `[ -x "$file" ]` |
| `-s` | Exists and not empty | `[ -s "$file" ]` |

### 3.3 Logical Operators
```bash
# AND
if [ $a -gt 0 ] && [ $a -lt 100 ]; then
    echo "Between 0 and 100"
fi

# OR
if [ $a -eq 0 ] || [ $a -eq 100 ]; then
    echo "Is 0 or 100"
fi

# NOT
if [ ! -f "myfile.txt" ]; then
    echo "File does not exist"
fi
```

---

## 4. LOOPS — for, while, until

### 4.1 for Loop — Different Styles
```bash
# Style 1: List of items
for fruit in apple banana cherry; do
    echo "I like $fruit"
done

# Style 2: Range
for i in {1..5}; do
    echo "Number: $i"
done

# Style 3: C-style (for arithmetic)
for ((i=1; i<=10; i++)); do
    echo "$i x 5 = $((i * 5))"
done

# Style 4: Files in directory
for file in *.txt; do
    echo "Found file: $file"
done

# Style 5: Command output
for user in $(cat /etc/passwd | cut -d: -f1); do
    echo "User: $user"
done
```

### 4.2 while Loop
```bash
#!/bin/bash
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

### 4.3 Reading a File Line by Line
```bash
#!/bin/bash
while IFS= read -r line; do
    echo "Line: $line"
done < "input.txt"
```

---

## 5. FUNCTIONS — Know This for Exam

```bash
#!/bin/bash

# Define a function
my_function() {
    echo "Hello from function!"
    echo "Argument 1: $1"
    echo "Argument 2: $2"
    return 0     # return value (0 = success)
}

# Call the function
my_function "arg1" "arg2"

# Get return value
echo "Return status: $?"    # $? = last command's exit status
```

### Function with Return Value via echo
```bash
add_numbers() {
    local sum=$(($1 + $2))   # local = function-scoped variable
    echo $sum                  # "return" via echo
}

# Capture output
result=$(add_numbers 5 3)
echo "Sum is: $result"        # Sum is: 8
```

---

## 6. USEFUL COMMANDS YOU MUST KNOW

```bash
# Word count
wc -w file.txt        # count words
wc -l file.txt        # count lines
wc -c file.txt        # count bytes/characters

# Cut — extract fields
echo "hello:world:foo" | cut -d: -f2     # world (field 2, delimiter :)

# Sort
sort file.txt          # sort alphabetically
sort -n file.txt       # sort numerically
sort -r file.txt       # reverse sort

# Grep — search for patterns
grep "hello" file.txt        # lines containing "hello"
grep -c "hello" file.txt     # count matching lines
grep -i "hello" file.txt     # case insensitive
grep -r "hello" /dir/        # recursive search in directory

# Sed — stream editor
sed 's/old/new/g' file.txt   # replace all "old" with "new"

# Awk — pattern processing
awk '{print $1}' file.txt    # print first field of each line

# basename / dirname
basename /path/to/file.txt   # file.txt
dirname /path/to/file.txt    # /path/to

# test command (same as [ ])
test -f "file.txt" && echo "exists"
```

---

## 7. 🎯 LT3 SOLUTION WALKTHROUGH — Study This Carefully

### LT3 Part A: Organize Files by Word Count

```bash
#!/bin/bash
# Q1a.sh — Organize .txt files by word count

# Initialize counters
short_count=0
medium_count=0
long_count=0
total=0

# Create directories if they don't exist
# test -d checks if directory exists, ! means "not"
if [ ! -d "short" ]; then
    mkdir short
fi
if [ ! -d "medium" ]; then
    mkdir medium
fi
if [ ! -d "long" ]; then
    mkdir long
fi

echo "--- File Organization Started ---"

# Loop through all .txt files in current directory
for file in *.txt; do
    # Skip if no .txt files found (glob returns literal *.txt)
    if [ ! -f "$file" ]; then
        continue
    fi

    # Count words using wc -w, cut to get just the number
    words=$(wc -w < "$file")
    # Alternative: words=$(wc -w "$file" | cut -d' ' -f1)

    total=$((total + 1))

    if [ $words -lt 100 ]; then
        mv "$file" short/
        echo "Processed $file (Words: $words) -> Moved to short/"
        short_count=$((short_count + 1))
    elif [ $words -le 500 ]; then
        mv "$file" medium/
        echo "Processed $file (Words: $words) -> Moved to medium/"
        medium_count=$((medium_count + 1))
    else
        mv "$file" long/
        echo "Processed $file (Words: $words) -> Moved to long/"
        long_count=$((long_count + 1))
    fi
done

echo "--- Organization Summary ---"
echo "Total .txt files processed: $total"
echo "Files moved to 'short/': $short_count (< 100 words)"
echo "Files moved to 'medium/': $medium_count (100 - 500 words)"
echo "Files moved to 'long/': $long_count (> 500 words)"
echo "Process finished."
```

### LT3 Part B: sum_of_digits and multiplication_table

```bash
#!/bin/bash
# Q1b.sh — Sum of digits + Multiplication table

# Function: sum_of_digits
sum_of_digits() {
    local num=$1
    local sum=0

    # Loop through each digit
    while [ $num -gt 0 ]; do
        digit=$((num % 10))       # get last digit
        sum=$((sum + digit))      # add to sum
        num=$((num / 10))         # remove last digit
    done

    echo "Sum of digits: $sum"
}

# Function: multiplication_table
multiplication_table() {
    local num=$1
    echo "Multiplication table of $num is:"

    for ((i=1; i<=10; i++)); do
        result=$((num * i))
        printf "%d x %2d = %d\n" $num $i $result
    done
}

# Main script
read -p "Enter a number: " number

sum_of_digits $number
multiplication_table $number
```

---

## 8. MORE PRACTICE SCRIPTS — Likely Exam Patterns

### 8.1 Check if a Number is Prime
```bash
#!/bin/bash
read -p "Enter a number: " num

if [ $num -le 1 ]; then
    echo "$num is not prime"
    exit 0
fi

is_prime=1
for ((i=2; i*i<=num; i++)); do
    if [ $((num % i)) -eq 0 ]; then
        is_prime=0
        break
    fi
done

if [ $is_prime -eq 1 ]; then
    echo "$num is prime"
else
    echo "$num is not prime"
fi
```

### 8.2 Fibonacci Series
```bash
#!/bin/bash
read -p "How many terms? " n

a=0
b=1
echo "Fibonacci series:"
for ((i=0; i<n; i++)); do
    echo -n "$a "
    temp=$((a + b))
    a=$b
    b=$temp
done
echo
```

### 8.3 Factorial
```bash
#!/bin/bash
read -p "Enter a number: " num

fact=1
for ((i=1; i<=num; i++)); do
    fact=$((fact * i))
done
echo "Factorial of $num is $fact"
```

### 8.4 Reverse a String
```bash
#!/bin/bash
read -p "Enter a string: " str
echo "$str" | rev
# Or manually:
len=${#str}
reversed=""
for ((i=len-1; i>=0; i--)); do
    reversed="$reversed${str:$i:1}"
done
echo "Reversed: $reversed"
```

### 8.5 Count Files by Extension in a Directory
```bash
#!/bin/bash
dir=${1:-.}    # default to current directory if no arg

echo "File counts in $dir:"
for ext in $(ls "$dir" | grep -o '\.[^.]*$' | sort -u); do
    count=$(ls "$dir"/*"$ext" 2>/dev/null | wc -l)
    echo "  $ext: $count files"
done
```

### 8.6 Simple Calculator Script
```bash
#!/bin/bash
read -p "Enter first number: " a
read -p "Enter operator (+, -, *, /): " op
read -p "Enter second number: " b

case $op in
    +) result=$((a + b)) ;;
    -) result=$((a - b)) ;;
    \*) result=$((a * b)) ;;
    /) 
        if [ $b -eq 0 ]; then
            echo "Error: Division by zero"
            exit 1
        fi
        result=$((a / b)) ;;
    *) echo "Invalid operator"; exit 1 ;;
esac

echo "$a $op $b = $result"
```

### 8.7 Rename All Files — Add Prefix
```bash
#!/bin/bash
prefix=$1
for file in *; do
    if [ -f "$file" ]; then
        mv "$file" "${prefix}_${file}"
        echo "Renamed: $file -> ${prefix}_${file}"
    fi
done
```

### 8.8 Find Largest File in Directory
```bash
#!/bin/bash
dir=${1:-.}
largest=""
max_size=0

for file in "$dir"/*; do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        if [ $size -gt $max_size ]; then
            max_size=$size
            largest=$file
        fi
    fi
done

echo "Largest file: $largest ($max_size bytes)"
```

### 8.9 Backup Script with Date
```bash
#!/bin/bash
src=$1
dest=$2
date_str=$(date +%Y%m%d_%H%M%S)
backup_name="${dest}/backup_${date_str}.tar.gz"

tar -czf "$backup_name" "$src"
echo "Backup created: $backup_name"
```

### 8.10 Check Disk Usage and Alert
```bash
#!/bin/bash
threshold=80
usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $usage -gt $threshold ]; then
    echo "WARNING: Disk usage is ${usage}% (above ${threshold}%)"
else
    echo "OK: Disk usage is ${usage}%"
fi
```

---

## 9. SCRIPTING CHEAT SHEET — Print This Page

```
VARIABLES:        var=value    echo $var    read var
ARGUMENTS:        $0=script  $1=first  $#=count  $@=all
ARITHMETIC:       $((a + b))  $((a % b))  $((a / b))
STRINGS:          ${#str}=length  ${str:0:3}=substring
IF:               if [ cond ]; then ... elif ... else ... fi
FOR:              for i in list; do ... done
FOR C-STYLE:      for ((i=0; i<n; i++)); do ... done
WHILE:            while [ cond ]; do ... done
FUNCTION:         fname() { ... }    fname arg1 arg2
CASE:             case $var in pat1) ... ;; pat2) ... ;; esac
FILE TEST:        -f=file  -d=dir  -e=exists  -s=notempty
NUM COMPARE:      -eq -ne -gt -lt -ge -le
STR COMPARE:      = != -z(empty) -n(notempty)
REDIRECT:         > overwrite  >> append  < input  2> stderr
PIPE:             cmd1 | cmd2
EXIT STATUS:      $? (0=success, non-zero=error)
```

---

> 🧠 **KEY INSIGHT:** In the exam, you'll likely write a script from scratch. Practice by typing these scripts yourself (not copy-paste). The muscle memory of writing `#!/bin/bash`, `for`, `if [ ]`, `done`, `fi` is what saves you under pressure.
