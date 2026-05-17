"""Shell scripting and Ubuntu administration training corpus.

Contains categorized Bash/Shell code snippets covering common topics
for students learning Linux system administration and shell scripting.
"""

SHELL_CORPUS = [
    # --- Complete Shell Scripts (multi-requirement solutions) ---
    '''
#!/bin/bash
# Script with sum_of_digits and multiplication_table functions using read input

# Function 1: Calculate the sum of the digits
sum_of_digits() {
    local num=$1
    local sum=0

    # Loop until the number becomes 0
    while [ "$num" -gt 0 ]; do
        # Get the last digit using modulo 10
        digit=$((num % 10))
        # Add the digit to the running total
        sum=$((sum + digit))
        # Remove the last digit by dividing by 10
        num=$((num / 10))
    done

    echo "Sum of digits: $sum"
}

# Function 2: Generate the multiplication table
multiplication_table() {
    local num=$1
    echo "Multiplication Table for $num:"

    # Loop from 1 to 10
    for i in {1..10}; do
        result=$((num * i))
        echo "$num x $i = $result"
    done
}

# Prompt the user to enter a number
read -p "Please enter a positive number: " user_input

# Basic validation to ensure the user actually entered a number
if ! [[ "$user_input" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid input. Please enter numbers only."
    exit 1
fi

echo "==============================="
# Call the first function and pass the user input to it
sum_of_digits "$user_input"
echo "==============================="
# Call the second function and pass the user input to it
multiplication_table "$user_input"
echo "==============================="
''',
    '''
#!/bin/bash
# Bash script with functions for factorial and fibonacci using user input

# Function to calculate factorial recursively
factorial() {
    local n=$1
    if [ "$n" -le 1 ]; then
        echo 1
    else
        local prev=$(factorial $((n - 1)))
        echo $((n * prev))
    fi
}

# Function to generate fibonacci sequence
fibonacci() {
    local n=$1
    local a=0
    local b=1

    echo "Fibonacci sequence (first $n terms):"
    for ((i=0; i<n; i++)); do
        echo -n "$a "
        local temp=$((a + b))
        a=$b
        b=$temp
    done
    echo ""
}

# Function to check if number is prime
is_prime() {
    local num=$1
    if [ "$num" -lt 2 ]; then
        echo "$num is not prime"
        return
    fi
    for ((i=2; i*i<=num; i++)); do
        if [ $((num % i)) -eq 0 ]; then
            echo "$num is not prime"
            return
        fi
    done
    echo "$num is prime"
}

# Prompt user for input
read -p "Enter a number: " number

# Validate input
if ! [[ "$number" =~ ^[0-9]+$ ]]; then
    echo "Error: Please enter a valid positive integer."
    exit 1
fi

echo "--- Results for $number ---"
echo "Factorial: $(factorial $number)"
fibonacci "$number"
is_prime "$number"
''',
    '''
#!/bin/bash
# Calculator script with menu - demonstrates functions, case, and read
# Supports addition, subtraction, multiplication, division, and modulo

add() { echo "$1 + $2 = $(($1 + $2))"; }
subtract() { echo "$1 - $2 = $(($1 - $2))"; }
multiply() { echo "$1 * $2 = $(($1 * $2))"; }

divide() {
    if [ "$2" -eq 0 ]; then
        echo "Error: Division by zero!"
    else
        echo "$1 / $2 = $(($1 / $2)) (remainder: $(($1 % $2)))"
    fi
}

power() {
    local base=$1
    local exp=$2
    local result=1
    for ((i=0; i<exp; i++)); do
        result=$((result * base))
    done
    echo "$base ^ $exp = $result"
}

# Main loop
while true; do
    echo ""
    echo "=== Calculator Menu ==="
    echo "1) Addition"
    echo "2) Subtraction"
    echo "3) Multiplication"
    echo "4) Division"
    echo "5) Power"
    echo "6) Exit"
    read -p "Choose operation (1-6): " choice

    if [ "$choice" -eq 6 ]; then
        echo "Goodbye!"
        break
    fi

    read -p "Enter first number: " num1
    read -p "Enter second number: " num2

    case $choice in
        1) add $num1 $num2 ;;
        2) subtract $num1 $num2 ;;
        3) multiply $num1 $num2 ;;
        4) divide $num1 $num2 ;;
        5) power $num1 $num2 ;;
        *) echo "Invalid choice" ;;
    esac
done
''',
    '''
#!/bin/bash
# Number analysis script - check even/odd, reverse digits, count digits
# Demonstrates multiple functions with arithmetic operations

# Function to check if number is even or odd
check_even_odd() {
    local num=$1
    if [ $((num % 2)) -eq 0 ]; then
        echo "$num is even"
    else
        echo "$num is odd"
    fi
}

# Function to reverse the digits of a number
reverse_number() {
    local num=$1
    local reversed=0

    while [ "$num" -gt 0 ]; do
        digit=$((num % 10))
        reversed=$((reversed * 10 + digit))
        num=$((num / 10))
    done

    echo "Reversed: $reversed"
}

# Function to count the digits
count_digits() {
    local num=$1
    local count=0

    while [ "$num" -gt 0 ]; do
        num=$((num / 10))
        ((count++))
    done

    echo "Number of digits: $count"
}

# Function to check if palindrome
is_palindrome() {
    local num=$1
    local original=$num
    local reversed=0

    while [ "$num" -gt 0 ]; do
        digit=$((num % 10))
        reversed=$((reversed * 10 + digit))
        num=$((num / 10))
    done

    if [ "$original" -eq "$reversed" ]; then
        echo "$original is a palindrome"
    else
        echo "$original is not a palindrome"
    fi
}

# Get user input
read -p "Enter a positive integer: " number

if ! [[ "$number" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid input"
    exit 1
fi

echo "=== Analysis of $number ==="
check_even_odd "$number"
count_digits "$number"
reverse_number "$number"
is_palindrome "$number"
''',
    '''
#!/bin/bash
# String processing script with functions - word count, char count, reverse
# Demonstrates string manipulation functions with user input

# Function to count words in a string
word_count() {
    local str="$1"
    local count=$(echo "$str" | wc -w)
    echo "Word count: $count"
}

# Function to count characters
char_count() {
    local str="$1"
    local count=${#str}
    echo "Character count: $count"
}

# Function to reverse a string
reverse_string() {
    local str="$1"
    echo "Reversed: $(echo "$str" | rev)"
}

# Function to convert to uppercase
to_uppercase() {
    local str="$1"
    echo "Uppercase: ${str^^}"
}

# Function to convert to lowercase
to_lowercase() {
    local str="$1"
    echo "Lowercase: ${str,,}"
}

# Function to count vowels
count_vowels() {
    local str="$1"
    local vowels=$(echo "$str" | grep -oi '[aeiou]' | wc -l)
    echo "Vowel count: $vowels"
}

# Get user input
read -p "Enter a string: " user_string

echo "=== String Analysis ==="
word_count "$user_string"
char_count "$user_string"
reverse_string "$user_string"
to_uppercase "$user_string"
to_lowercase "$user_string"
count_vowels "$user_string"
''',
    '''
#!/bin/bash
# Array operations script with functions - demonstrates array manipulation

# Function to find maximum element
find_max() {
    local -a arr=("$@")
    local max=${arr[0]}
    for elem in "${arr[@]}"; do
        if [ "$elem" -gt "$max" ]; then
            max=$elem
        fi
    done
    echo "Maximum: $max"
}

# Function to find minimum element
find_min() {
    local -a arr=("$@")
    local min=${arr[0]}
    for elem in "${arr[@]}"; do
        if [ "$elem" -lt "$min" ]; then
            min=$elem
        fi
    done
    echo "Minimum: $min"
}

# Function to calculate sum of array
array_sum() {
    local -a arr=("$@")
    local sum=0
    for elem in "${arr[@]}"; do
        sum=$((sum + elem))
    done
    echo "Sum: $sum"
}

# Function to calculate average
array_average() {
    local -a arr=("$@")
    local sum=0
    local count=${#arr[@]}
    for elem in "${arr[@]}"; do
        sum=$((sum + elem))
    done
    echo "Average: $((sum / count))"
}

# Function to sort array (bubble sort)
sort_array() {
    local -a arr=("$@")
    local n=${#arr[@]}
    for ((i=0; i<n-1; i++)); do
        for ((j=0; j<n-i-1; j++)); do
            if [ "${arr[$j]}" -gt "${arr[$((j+1))]}" ]; then
                local temp=${arr[$j]}
                arr[$j]=${arr[$((j+1))]}
                arr[$((j+1))]=$temp
            fi
        done
    done
    echo "Sorted: ${arr[*]}"
}

# Read array from user
read -p "Enter numbers separated by spaces: " -a numbers

echo "=== Array Analysis ==="
echo "Array: ${numbers[*]}"
echo "Length: ${#numbers[@]}"
find_max "${numbers[@]}"
find_min "${numbers[@]}"
array_sum "${numbers[@]}"
array_average "${numbers[@]}"
sort_array "${numbers[@]}"
''',
    '''
#!/bin/bash
# Process .txt files by word count - move to short/medium/long directories with summary
# Initialize counters for the summary
total_files=0
short_count=0
medium_count=0
long_count=0

# Create the required subdirectories if they don't exist
# The -p flag ensures no error is thrown if they already exist
mkdir -p short medium long

# Loop through all .txt files in the current directory
for file in *.txt; do
    # Safety check: skip if no .txt files are found in the directory
    if [ ! -f "$file" ]; then
        echo "No .txt files found to process."
        continue
    fi

    # Count the words. Using '<' feeds the file content directly to wc,
    # outputting ONLY the number (avoiding the need to use 'cut' on the filename)
    word_count=$(wc -w < "$file")

    # Increment the total processed files counter
    ((total_files++))

    # Sort the files based on word count
    if [ "$word_count" -lt 100 ]; then
        mv "$file" short/
        ((short_count++))
    elif [ "$word_count" -le 500 ]; then
        mv "$file" medium/
        ((medium_count++))
    else
        mv "$file" long/
        ((long_count++))
    fi
done

# Print the final summary
echo "--- Processing Summary ---"
echo "Total files processed: $total_files"
echo "Moved to short/ (< 100 words): $short_count"
echo "Moved to medium/ (100 - 500 words): $medium_count"
echo "Moved to long/ (> 500 words): $long_count"
''',
    '''
#!/bin/bash
# Organize files by extension into subdirectories with summary report
total=0
declare -A ext_counts

# Loop through all files in current directory
for file in *; do
    # Skip directories
    [ -f "$file" ] || continue

    # Extract extension
    ext="${file##*.}"

    # Skip files without extension
    if [ "$ext" = "$file" ]; then
        ext="no_extension"
    fi

    # Create directory for this extension if needed
    mkdir -p "$ext"

    # Move file to its extension directory
    mv "$file" "$ext/"
    ((total++))

    # Track count per extension
    ext_counts[$ext]=$(( ${ext_counts[$ext]:-0} + 1 ))
done

# Print summary
echo "=== File Organization Summary ==="
echo "Total files processed: $total"
echo ""
echo "Files per category:"
for ext in "${!ext_counts[@]}"; do
    echo "  $ext/: ${ext_counts[$ext]} files"
done
''',
    '''
#!/bin/bash
# Batch rename files - add prefix/suffix, replace patterns, with dry-run option
# Usage: ./rename.sh [-d] [-p prefix] [-s suffix] [-r old:new] pattern
dry_run=false
prefix=""
suffix=""
replace_old=""
replace_new=""

usage() {
    echo "Usage: $0 [-d] [-p prefix] [-s suffix] [-r old:new] file_pattern"
    echo "  -d          Dry run (show what would happen)"
    echo "  -p prefix   Add prefix to filenames"
    echo "  -s suffix   Add suffix before extension"
    echo "  -r old:new  Replace 'old' with 'new' in filenames"
    exit 1
}

while getopts "dp:s:r:h" opt; do
    case $opt in
        d) dry_run=true ;;
        p) prefix="$OPTARG" ;;
        s) suffix="$OPTARG" ;;
        r) replace_old="${OPTARG%%:*}"; replace_new="${OPTARG#*:}" ;;
        h|?) usage ;;
    esac
done
shift $((OPTIND - 1))

pattern="${1:-*}"
count=0

for file in $pattern; do
    [ -f "$file" ] || continue

    # Get name and extension
    name="${file%.*}"
    ext="${file##*.}"
    [ "$ext" = "$file" ] && ext=""

    # Build new name
    new_name="${prefix}${name}${suffix}"

    # Apply replacement if specified
    if [ -n "$replace_old" ]; then
        new_name="${new_name//$replace_old/$replace_new}"
    fi

    # Add extension back
    [ -n "$ext" ] && new_name="${new_name}.${ext}"

    # Skip if name unchanged
    [ "$new_name" = "$file" ] && continue

    if [ "$dry_run" = true ]; then
        echo "[DRY RUN] $file -> $new_name"
    else
        mv "$file" "$new_name"
        echo "Renamed: $file -> $new_name"
    fi
    ((count++))
done

echo "Total: $count files ${dry_run:+would be }renamed."
''',
    '''
#!/bin/bash
# Monitor disk usage and alert if any partition exceeds threshold
THRESHOLD=80
ALERT_LOG="/var/log/disk_alerts.log"

echo "=== Disk Usage Report ($(date)) ==="
echo ""

alert_count=0
total_partitions=0

# Parse df output, skip header
df -h | tail -n +2 | while read -r filesystem size used avail percent mountpoint; do
    # Remove % sign for comparison
    usage=${percent%\\%}
    ((total_partitions++))

    if [ "$usage" -ge "$THRESHOLD" ]; then
        echo "[WARNING] $mountpoint is ${percent} full ($used/$size)"
        echo "$(date): WARNING - $mountpoint at ${percent}" >> "$ALERT_LOG"
        ((alert_count++))
    else
        echo "[OK] $mountpoint: ${percent} used"
    fi
done

echo ""
echo "--- Summary ---"
echo "Partitions checked: $total_partitions"
echo "Alerts triggered: $alert_count"
echo "Threshold: ${THRESHOLD}%"
''',
    '''
#!/bin/bash
# Log file analyzer - parse log files and generate statistics
LOG_FILE="${1:-/var/log/syslog}"

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

echo "=== Log Analysis Report ==="
echo "File: $LOG_FILE"
echo "Date: $(date)"
echo ""

# Total lines
total_lines=$(wc -l < "$LOG_FILE")
echo "Total log entries: $total_lines"

# Count by severity
errors=$(grep -ci "error" "$LOG_FILE")
warnings=$(grep -ci "warning" "$LOG_FILE")
critical=$(grep -ci "critical\\|fatal" "$LOG_FILE")
info=$(grep -ci "info" "$LOG_FILE")

echo ""
echo "--- By Severity ---"
echo "Critical/Fatal: $critical"
echo "Errors:         $errors"
echo "Warnings:       $warnings"
echo "Info:           $info"

# Top 5 most frequent messages
echo ""
echo "--- Top 5 Most Frequent Patterns ---"
cut -d' ' -f5- "$LOG_FILE" | sort | uniq -c | sort -rn | head -5

# Activity by hour
echo ""
echo "--- Activity by Hour ---"
cut -d' ' -f3 "$LOG_FILE" | cut -d: -f1 | sort | uniq -c | sort -rn | head -5
''',
    '''
#!/bin/bash
# Automated backup script with rotation, compression, and logging
SOURCE_DIR="${1:-/home}"
BACKUP_DIR="${2:-/backup}"
MAX_BACKUPS=7
LOG_FILE="/var/log/backup.log"
DATE=$(date +%Y%m%d_%H%M%S)
ARCHIVE="${BACKUP_DIR}/backup_${DATE}.tar.gz"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Create backup directory if needed
mkdir -p "$BACKUP_DIR"

log "Starting backup of $SOURCE_DIR"

# Create compressed archive
if tar -czf "$ARCHIVE" "$SOURCE_DIR" 2>/dev/null; then
    size=$(du -sh "$ARCHIVE" | cut -f1)
    log "Backup successful: $ARCHIVE ($size)"
else
    log "ERROR: Backup failed!"
    exit 1
fi

# Rotate old backups - keep only MAX_BACKUPS most recent
backup_count=$(ls -1 "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null | wc -l)
if [ "$backup_count" -gt "$MAX_BACKUPS" ]; then
    remove_count=$((backup_count - MAX_BACKUPS))
    ls -1t "$BACKUP_DIR"/backup_*.tar.gz | tail -n "$remove_count" | while read -r old; do
        rm -f "$old"
        log "Removed old backup: $old"
    done
fi

log "Backup rotation complete. Current backups: $(ls -1 "$BACKUP_DIR"/backup_*.tar.gz | wc -l)"
''',
    '''
#!/bin/bash
# System health check script with comprehensive reporting
echo "============================================"
echo "       SYSTEM HEALTH CHECK REPORT"
echo "       $(date)"
echo "============================================"
echo ""

# System info
echo "--- System Information ---"
echo "Hostname: $(hostname)"
echo "Kernel:   $(uname -r)"
echo "Uptime:   $(uptime -p)"
echo ""

# CPU usage
echo "--- CPU Usage ---"
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
echo "CPU Usage: ${cpu_usage}%"
echo ""

# Memory usage
echo "--- Memory Usage ---"
free -h | awk '/^Mem:/ {printf "Total: %s, Used: %s, Free: %s, Usage: %.1f%%\\n", $2, $3, $4, ($3/$2)*100}'
echo ""

# Disk usage
echo "--- Disk Usage ---"
df -h | awk 'NR==1 || /^\\/dev/' | while read -r line; do
    echo "  $line"
done
echo ""

# Top 5 processes by CPU
echo "--- Top 5 Processes (CPU) ---"
ps aux --sort=-%cpu | head -6 | awk '{printf "  %-10s %5s%% %s\\n", $1, $3, $11}'
echo ""

# Top 5 processes by Memory
echo "--- Top 5 Processes (Memory) ---"
ps aux --sort=-%mem | head -6 | awk '{printf "  %-10s %5s%% %s\\n", $1, $4, $11}'
echo ""

# Network connections
echo "--- Active Network Connections ---"
ss -tuln | grep LISTEN | wc -l | xargs -I{} echo "  Listening ports: {}"
echo ""

# Recent failed login attempts
echo "--- Security ---"
if [ -f /var/log/auth.log ]; then
    failed=$(grep -c "Failed password" /var/log/auth.log 2>/dev/null || echo 0)
    echo "  Failed login attempts: $failed"
fi

echo ""
echo "============================================"
echo "         END OF REPORT"
echo "============================================"
''',

    # --- Bash Basics ---
    '''
#!/bin/bash
# Hello World script - basic bash script structure
echo "Hello, World!"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Today's date: $(date)"
''',
    '''
#!/bin/bash
# Variables in bash - declaring and using variables
name="Alice"
age=25
echo "Name: $name"
echo "Age: $age"

# Read-only variable
readonly PI=3.14159
echo "PI = $PI"

# Command substitution
current_dir=$(pwd)
file_count=$(ls | wc -l)
echo "Current directory: $current_dir"
echo "Files in directory: $file_count"
''',
    '''
#!/bin/bash
# String operations in bash
str="Hello, World!"

# String length
echo "Length: ${#str}"

# Substring extraction
echo "Substring: ${str:0:5}"    # Hello

# String replacement
echo "Replace: ${str/World/Bash}"

# Uppercase and lowercase
echo "Upper: ${str^^}"
echo "Lower: ${str,,}"

# Check if string contains substring
if [[ "$str" == *"World"* ]]; then
    echo "Contains 'World'"
fi
''',
    '''
#!/bin/bash
# Arrays in bash
fruits=("apple" "banana" "cherry" "date" "elderberry")

# Access elements
echo "First: ${fruits[0]}"
echo "Third: ${fruits[2]}"

# All elements
echo "All: ${fruits[@]}"

# Array length
echo "Length: ${#fruits[@]}"

# Loop through array
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# Add element
fruits+=("fig")

# Remove element
unset fruits[1]

# Associative array (dictionary)
declare -A colors
colors[red]="#FF0000"
colors[green]="#00FF00"
colors[blue]="#0000FF"

for key in "${!colors[@]}"; do
    echo "$key = ${colors[$key]}"
done
''',

    # --- Bash Loops ---
    '''
#!/bin/bash
# For loop in bash - iterate over a range
for i in {1..10}; do
    echo "Number: $i"
done

# C-style for loop
for ((i=0; i<5; i++)); do
    echo "Index: $i"
done

# Loop over files in a directory
for file in *.txt; do
    echo "Processing: $file"
    wc -l "$file"
done

# Loop over command output
for user in $(cut -d: -f1 /etc/passwd); do
    echo "User: $user"
done
''',
    '''
#!/bin/bash
# While loop in bash
count=1
while [ $count -le 10 ]; do
    echo "Count: $count"
    ((count++))
done

# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < "input.txt"

# Infinite loop with break
while true; do
    read -p "Enter command (quit to exit): " cmd
    if [ "$cmd" = "quit" ]; then
        break
    fi
    echo "You entered: $cmd"
done
''',
    '''
#!/bin/bash
# Until loop in bash - runs until condition is true
count=1
until [ $count -gt 5 ]; do
    echo "Count: $count"
    ((count++))
done

# Select menu loop
echo "Choose a color:"
select color in "Red" "Green" "Blue" "Quit"; do
    case $color in
        "Red")   echo "You chose red!" ;;
        "Green") echo "You chose green!" ;;
        "Blue")  echo "You chose blue!" ;;
        "Quit")  break ;;
        *)       echo "Invalid option" ;;
    esac
done
''',

    # --- Bash Conditionals ---
    '''
#!/bin/bash
# If-else statements in bash
read -p "Enter a number: " num

if [ $num -gt 0 ]; then
    echo "$num is positive"
elif [ $num -lt 0 ]; then
    echo "$num is negative"
else
    echo "$num is zero"
fi

# File test operators
file="test.txt"
if [ -f "$file" ]; then
    echo "$file exists and is a regular file"
elif [ -d "$file" ]; then
    echo "$file is a directory"
else
    echo "$file does not exist"
fi

# String comparison
str1="hello"
str2="world"
if [ "$str1" = "$str2" ]; then
    echo "Strings are equal"
else
    echo "Strings are different"
fi

# Multiple conditions with AND/OR
age=25
if [ $age -ge 18 ] && [ $age -le 65 ]; then
    echo "Working age"
fi
''',
    '''
#!/bin/bash
# Case statement in bash - pattern matching
read -p "Enter a file extension: " ext

case "$ext" in
    txt|doc)
        echo "Text document"
        ;;
    jpg|png|gif)
        echo "Image file"
        ;;
    mp3|wav|flac)
        echo "Audio file"
        ;;
    mp4|avi|mkv)
        echo "Video file"
        ;;
    sh|bash)
        echo "Shell script"
        ;;
    c|h)
        echo "C source/header file"
        ;;
    *)
        echo "Unknown file type"
        ;;
esac
''',

    # --- Bash Functions ---
    '''
#!/bin/bash
# Functions in bash
greet() {
    local name=$1
    local greeting=${2:-"Hello"}
    echo "$greeting, $name!"
}

greet "Alice"
greet "Bob" "Hi"

# Function with return value
is_even() {
    local num=$1
    if (( num % 2 == 0 )); then
        return 0  # true
    else
        return 1  # false
    fi
}

for i in {1..5}; do
    if is_even $i; then
        echo "$i is even"
    else
        echo "$i is odd"
    fi
done

# Function that outputs a value (capture with $())
factorial() {
    local n=$1
    if [ $n -le 1 ]; then
        echo 1
    else
        local prev=$(factorial $((n - 1)))
        echo $((n * prev))
    fi
}

result=$(factorial 5)
echo "5! = $result"
''',

    # --- Text Processing (grep, awk, sed) ---
    '''
#!/bin/bash
# grep - search for patterns in files
# Search for a word in a file
grep "error" /var/log/syslog

# Case-insensitive search
grep -i "warning" logfile.txt

# Recursive search in directories
grep -r "TODO" ./src/

# Show line numbers
grep -n "function" script.sh

# Count matches
grep -c "error" logfile.txt

# Invert match (lines NOT containing pattern)
grep -v "debug" logfile.txt

# Extended regex
grep -E "error|warning|critical" logfile.txt

# Show only matching part
grep -o "[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+" access.log
''',
    '''
#!/bin/bash
# awk - text processing and data extraction
# Print specific columns
awk '{print $1, $3}' data.txt

# Print with custom separator
awk -F',' '{print $1, $2}' data.csv

# Filter rows by condition
awk '$3 > 50 {print $1, $3}' scores.txt

# Sum a column
awk '{sum += $2} END {print "Total:", sum}' sales.txt

# Count lines matching a pattern
awk '/error/ {count++} END {print "Errors:", count}' log.txt

# Print line numbers
awk '{print NR, $0}' file.txt

# Format output
awk '{printf "%-10s %5d\\n", $1, $2}' data.txt

# Process /etc/passwd
awk -F: '{print $1, $6}' /etc/passwd
''',
    '''
#!/bin/bash
# sed - stream editor for text transformation
# Replace first occurrence on each line
sed 's/old/new/' file.txt

# Replace all occurrences (global)
sed 's/old/new/g' file.txt

# Replace in-place (modify file directly)
sed -i 's/old/new/g' file.txt

# Delete lines matching a pattern
sed '/^#/d' config.txt       # Delete comment lines
sed '/^$/d' file.txt         # Delete empty lines

# Print specific lines
sed -n '5,10p' file.txt      # Print lines 5-10

# Insert text before/after a line
sed '3i\\New line before line 3' file.txt
sed '3a\\New line after line 3' file.txt

# Multiple operations
sed -e 's/foo/bar/g' -e 's/baz/qux/g' file.txt

# Replace between line ranges
sed '10,20s/old/new/g' file.txt
''',

    # --- File Operations and Permissions ---
    '''
#!/bin/bash
# File permissions with chmod
# Numeric mode
chmod 755 script.sh    # rwxr-xr-x (owner: rwx, group: rx, others: rx)
chmod 644 file.txt     # rw-r--r-- (owner: rw, group: r, others: r)
chmod 700 private.sh   # rwx------ (owner only)

# Symbolic mode
chmod u+x script.sh    # Add execute for user/owner
chmod g+w file.txt     # Add write for group
chmod o-r file.txt     # Remove read for others
chmod a+r file.txt     # Add read for all

# Change ownership
chown user:group file.txt
chown -R user:group directory/

# Find files by permission
find . -perm 777 -type f
find . -perm /u+x -type f    # Files with user execute

# Set default permissions with umask
umask 022    # New files: 644, new dirs: 755
umask 077    # New files: 600, new dirs: 700
''',
    '''
#!/bin/bash
# Find command - search for files and directories
# Find by name
find /home -name "*.txt"
find . -iname "*.PDF"          # Case-insensitive

# Find by type
find . -type f                  # Regular files only
find . -type d                  # Directories only
find . -type l                  # Symbolic links

# Find by size
find . -size +100M              # Larger than 100MB
find . -size -1k               # Smaller than 1KB

# Find by modification time
find . -mtime -7               # Modified in last 7 days
find . -mtime +30              # Modified more than 30 days ago

# Find and execute command
find . -name "*.log" -exec rm {} \\;
find . -name "*.c" -exec grep -l "main" {} \\;

# Find with xargs (more efficient)
find . -name "*.txt" | xargs grep "pattern"
find . -name "*.tmp" -print0 | xargs -0 rm

# Find and delete
find /tmp -type f -mtime +7 -delete
''',

    # --- Pipes and Redirection ---
    '''
#!/bin/bash
# Pipes and redirection in bash
# Output redirection
echo "Hello" > output.txt       # Overwrite
echo "World" >> output.txt      # Append

# Input redirection
sort < unsorted.txt

# Pipe - send output of one command to another
cat file.txt | grep "error" | sort | uniq -c | sort -rn

# Redirect stderr
command 2> error.log            # Redirect stderr to file
command 2>&1                    # Redirect stderr to stdout
command > output.txt 2>&1       # Both stdout and stderr to file
command &> all_output.txt       # Shorthand for above

# Pipe to multiple commands with tee
ls -la | tee listing.txt | grep ".sh"

# Here document
cat << EOF > config.txt
server=localhost
port=8080
debug=true
EOF

# Process substitution
diff <(sort file1.txt) <(sort file2.txt)
''',

    # --- Process Management ---
    '''
#!/bin/bash
# Process management in Ubuntu/Linux
# View running processes
ps aux                          # All processes
ps aux | grep nginx             # Find specific process
ps -ef --forest                 # Process tree

# Top/htop for real-time monitoring
top -bn1 | head -20             # Non-interactive, first 20 lines

# Background and foreground
long_command &                  # Run in background
jobs                            # List background jobs
fg %1                           # Bring job 1 to foreground
bg %1                           # Resume job 1 in background

# Kill processes
kill PID                        # Send SIGTERM
kill -9 PID                     # Send SIGKILL (force)
kill -STOP PID                  # Pause process
kill -CONT PID                  # Resume process
killall process_name            # Kill by name
pkill -f "pattern"              # Kill by pattern

# Nice and renice (priority)
nice -n 10 ./heavy_task.sh      # Start with lower priority
renice -n 5 -p PID             # Change priority of running process

# nohup - keep running after logout
nohup ./server.sh &
nohup ./script.sh > output.log 2>&1 &
''',

    # --- Cron Jobs ---
    '''
#!/bin/bash
# Cron jobs - scheduled task execution
# Edit crontab
# crontab -e

# Crontab format: minute hour day month weekday command
# *     *     *     *     *     command
# 0-59  0-23  1-31  1-12  0-7

# Examples:
# Run every minute
# * * * * * /path/to/script.sh

# Run at 2:30 AM daily
# 30 2 * * * /path/to/backup.sh

# Run every Monday at 9 AM
# 0 9 * * 1 /path/to/report.sh

# Run every 5 minutes
# */5 * * * * /path/to/check.sh

# Run at midnight on the 1st of every month
# 0 0 1 * * /path/to/monthly.sh

# Backup script example
backup_dir="/backup/$(date +%Y%m%d)"
mkdir -p "$backup_dir"
tar -czf "$backup_dir/home.tar.gz" /home/
find /backup -type d -mtime +30 -exec rm -rf {} \\;
echo "Backup completed: $(date)" >> /var/log/backup.log
''',

    # --- Ubuntu System Administration ---
    '''
#!/bin/bash
# Package management with apt (Ubuntu/Debian)
# Update package list
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install a package
sudo apt install nginx -y

# Remove a package
sudo apt remove nginx
sudo apt purge nginx            # Remove with config files
sudo apt autoremove             # Remove unused dependencies

# Search for packages
apt search "web server"
apt show nginx                  # Package details

# List installed packages
dpkg -l | grep nginx
apt list --installed

# Hold a package (prevent updates)
sudo apt-mark hold package_name
sudo apt-mark unhold package_name
''',
    '''
#!/bin/bash
# Systemd service management
# Start/stop/restart services
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx     # Reload config without restart

# Enable/disable at boot
sudo systemctl enable nginx
sudo systemctl disable nginx

# Check status
systemctl status nginx
systemctl is-active nginx
systemctl is-enabled nginx

# List all services
systemctl list-units --type=service
systemctl list-units --type=service --state=running

# View service logs
journalctl -u nginx
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx -f          # Follow (like tail -f)

# Create a custom service
# /etc/systemd/system/myapp.service
# [Unit]
# Description=My Application
# After=network.target
#
# [Service]
# Type=simple
# User=www-data
# ExecStart=/usr/bin/python3 /opt/myapp/app.py
# Restart=always
# RestartSec=5
#
# [Install]
# WantedBy=multi-user.target

# After creating: sudo systemctl daemon-reload
''',
    '''
#!/bin/bash
# User and group management in Ubuntu
# Create a new user
sudo useradd -m -s /bin/bash newuser
sudo passwd newuser

# Create user with specific options
sudo useradd -m -s /bin/bash -G sudo,docker -c "John Doe" john

# Modify user
sudo usermod -aG docker username    # Add to group
sudo usermod -s /bin/zsh username   # Change shell
sudo usermod -L username            # Lock account
sudo usermod -U username            # Unlock account

# Delete user
sudo userdel -r username            # Remove with home directory

# Group management
sudo groupadd developers
sudo groupdel developers
sudo gpasswd -a user group          # Add user to group
sudo gpasswd -d user group          # Remove user from group

# View user info
id username
groups username
cat /etc/passwd | grep username
getent passwd username
''',

    # --- Networking ---
    '''
#!/bin/bash
# Network configuration and tools in Ubuntu
# View network interfaces
ip addr show
ip link show
ifconfig                        # Legacy but still common

# Configure IP address
sudo ip addr add 192.168.1.100/24 dev eth0
sudo ip route add default via 192.168.1.1

# DNS configuration
cat /etc/resolv.conf
nslookup google.com
dig google.com

# Check connectivity
ping -c 4 google.com
traceroute google.com
mtr google.com

# Port scanning and connections
ss -tuln                        # Show listening ports
netstat -tuln                   # Legacy alternative
lsof -i :80                    # What's using port 80

# Firewall with UFW
sudo ufw enable
sudo ufw status verbose
sudo ufw allow 22/tcp           # Allow SSH
sudo ufw allow 80/tcp           # Allow HTTP
sudo ufw allow 443/tcp          # Allow HTTPS
sudo ufw deny 3306              # Deny MySQL from outside
sudo ufw allow from 192.168.1.0/24 to any port 22

# SSH operations
ssh user@remote_host
ssh -i ~/.ssh/key.pem user@host
ssh -L 8080:localhost:80 user@remote    # Local port forwarding

# SCP - secure copy
scp file.txt user@remote:/path/
scp -r directory/ user@remote:/path/
scp user@remote:/path/file.txt ./
''',

    # --- Disk and Storage ---
    '''
#!/bin/bash
# Disk usage and storage management
# Check disk space
df -h                           # Human-readable
df -h /home                     # Specific mount point

# Check directory sizes
du -sh /var/log                 # Summary of directory
du -sh /home/*                  # Each subdirectory
du -h --max-depth=1 /          # Top-level directories

# Find large files
find / -type f -size +100M -exec ls -lh {} \\;
find /var/log -name "*.log" -size +50M

# Disk partitions
lsblk                           # List block devices
fdisk -l                        # Partition table
blkid                           # UUID of partitions

# Mount/unmount
sudo mount /dev/sdb1 /mnt/usb
sudo umount /mnt/usb

# Archive and compress
tar -czf archive.tar.gz directory/     # Create gzip archive
tar -xzf archive.tar.gz               # Extract gzip archive
tar -cjf archive.tar.bz2 directory/   # Create bzip2 archive
tar -xjf archive.tar.bz2              # Extract bzip2 archive

# Rsync for backup/sync
rsync -avz /source/ /destination/
rsync -avz --delete /source/ user@remote:/backup/
rsync -avz --exclude="*.log" /source/ /dest/
''',

    # --- Script Error Handling ---
    '''
#!/bin/bash
# Error handling and debugging in bash scripts
set -e          # Exit on any error
set -u          # Exit on undefined variable
set -o pipefail # Exit on pipe failure
set -x          # Debug mode (print each command)

# Trap for cleanup on exit
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/myapp_*
    echo "Done."
}
trap cleanup EXIT
trap 'echo "Error on line $LINENO"; exit 1' ERR

# Function with error checking
safe_cd() {
    local dir=$1
    if [ ! -d "$dir" ]; then
        echo "Error: Directory '$dir' does not exist" >&2
        return 1
    fi
    cd "$dir" || return 1
}

# Check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if ! command_exists "docker"; then
    echo "Error: docker is not installed" >&2
    exit 1
fi

# Retry logic
retry() {
    local max_attempts=$1
    local delay=$2
    shift 2
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if "$@"; then
            return 0
        fi
        echo "Attempt $attempt failed. Retrying in ${delay}s..."
        sleep $delay
        ((attempt++))
    done
    echo "All $max_attempts attempts failed."
    return 1
}

retry 3 5 curl -f http://example.com/health
''',

    # --- Script with getopts ---
    '''
#!/bin/bash
# Command-line argument parsing with getopts
usage() {
    echo "Usage: $0 [-v] [-o output_file] [-n count] input_file"
    echo "  -v              Verbose mode"
    echo "  -o output_file  Specify output file"
    echo "  -n count        Number of iterations"
    echo "  -h              Show this help"
    exit 1
}

verbose=false
output_file="output.txt"
count=1

while getopts "vo:n:h" opt; do
    case $opt in
        v) verbose=true ;;
        o) output_file="$OPTARG" ;;
        n) count="$OPTARG" ;;
        h) usage ;;
        ?) usage ;;
    esac
done

shift $((OPTIND - 1))

if [ $# -eq 0 ]; then
    echo "Error: Input file required"
    usage
fi

input_file="$1"

if [ "$verbose" = true ]; then
    echo "Input: $input_file"
    echo "Output: $output_file"
    echo "Count: $count"
fi

# Process the file
for ((i=1; i<=count; i++)); do
    if [ "$verbose" = true ]; then
        echo "Iteration $i..."
    fi
    cat "$input_file" >> "$output_file"
done

echo "Done. Output written to $output_file"
''',
]


# --- Additional practical scripts ---
SHELL_CORPUS += [
    '''
#!/bin/bash
# Read .txt files and move files with more than 500 words to big_files directory
# Creates the big_files directory if it does not exist

TARGET_DIR="big_files"
WORD_LIMIT=500

# Create target directory if needed
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
    echo "Created directory: $TARGET_DIR"
fi

# Loop through all .txt files in current directory
for file in *.txt; do
    # Skip if no .txt files found (glob didn't match)
    [ -f "$file" ] || continue

    # Count words in the file
    word_count=$(wc -w < "$file")

    echo "File: $file - Words: $word_count"

    # Move file if word count exceeds limit
    if [ "$word_count" -gt "$WORD_LIMIT" ]; then
        mv "$file" "$TARGET_DIR/"
        echo "  -> Moved to $TARGET_DIR/"
    fi
done

echo "Done. Files with more than $WORD_LIMIT words moved to $TARGET_DIR/"
''',
    '''
#!/bin/bash
# Check word count of text files and categorize them by size
# Moves large files (>500 words) to a separate folder

set -euo pipefail

SOURCE_DIR="${1:-.}"
BIG_DIR="$SOURCE_DIR/big_files"
THRESHOLD=500

# Create big_files directory if it doesn't exist
mkdir -p "$BIG_DIR"

count_moved=0
count_skipped=0

# Find all .txt files recursively
find "$SOURCE_DIR" -maxdepth 1 -name "*.txt" -type f | while read -r file; do
    words=$(wc -w < "$file")

    if [ "$words" -gt "$THRESHOLD" ]; then
        mv "$file" "$BIG_DIR/"
        echo "[MOVED] $file ($words words)"
        ((count_moved++))
    else
        echo "[KEPT]  $file ($words words)"
        ((count_skipped++))
    fi
done

echo ""
echo "Summary: Moved files with >$THRESHOLD words to $BIG_DIR/"
''',
]
