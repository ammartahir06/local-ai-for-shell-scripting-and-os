# 🎯 EXAM PRACTICE QUESTIONS — Test Your Knowledge
### Solve these without looking at the guides!

---

## 💻 PART 1: BASH SCRIPTING

**Q1. File Organizer**
Write a script that takes a directory name as an argument. Inside that directory, create two folders: `images/` and `documents/`. Move all `.jpg` and `.png` files into `images/`, and all `.txt` and `.pdf` files into `documents/`.
> *Hint: Use `for file in "$dir"/*` and `case` or `if` with `[[ $file == *.jpg ]]`.*

**Q2. Odd/Even Summer**
Write a script that asks the user for a number `N`. Then calculate and print two sums:
1. The sum of all even numbers from 1 to N.
2. The sum of all odd numbers from 1 to N.
> *Hint: Use a `for ((i=1; i<=N; i++))` loop and modulo `% 2`.*

**Q3. File Existence Checker**
Write a script that reads filenames from a text file called `files_to_check.txt` (one per line). For each file, check if it exists in the current directory. If it exists, print its size. If it doesn't, print "File not found".
> *Hint: Use `while IFS= read -r file; do ... done < files_to_check.txt` and `[ -f "$file" ]`.*

**Q4. Simple Number Guesser**
Write a script that generates a random number between 1 and 10 (use `$((RANDOM % 10 + 1))`). Ask the user to guess it. Keep looping until they guess correctly. Give "too high" or "too low" hints.

---

## 🍴 PART 2: FORK & PROCESSES

**Q5. The `fork()` Loop**
What is the exact output of this code? How many times is "Hello" printed?
```c
int main() {
    for (int i = 0; i < 3; i++) {
        fork();
        printf("Hello\n");
    }
    return 0;
}
```
> *Answer: 14 times. (2 + 4 + 8 = 14).*

**Q6. Build a specific tree**
Write code to create this exact process tree (using `wait()` to ensure parent waits for both):
```
    P
   / \
  C1 C2
```
> *Hint: Call `fork()` twice from the parent, store both PIDs, and don't let C1 call `fork()` again.*

---

## 🚰 PART 3: PIPES & IPC

**Q7. The Ping-Pong Pipe**
Write a C program where a parent process creates a child process. The parent sends the string "PING" through a pipe to the child. The child reads it, prints it, and then sends "PONG" back to the parent through a SECOND pipe. The parent reads it and prints it.
> *Hint: You need `int pipe1[2]` and `int pipe2[2]`.*

**Q8. Message Queue Struct**
Find the **TWO critical errors** in this struct intended for a message queue:
```c
struct my_msg {
    int pid;
    char text[100];
    long type;
};
```
> *Answer: 1. The `type` field MUST be named something like `mtype` (convention) but more importantly it MUST be a `long` and it MUST be the very FIRST field in the struct. 2. The type value used with msgsnd/rcv must be > 0.*

**Q9. dup2() Simulation**
Write C code that redirects the output of `ls -la` to a file called `output.txt` instead of the terminal.

---

## 🧵 PART 4: THREADS & MAKEFILES

**Q10. Thread Function Signature**
Write the correct prototype for a C function that can be passed to `pthread_create()`.
> *Answer: `void *myFunction(void *arg)`*

**Q11. Make this Makefile**
You have three files: `server.c`, `client.c`, and `common.h`. `server.c` and `client.c` both include `common.h`. Write a Makefile that builds two executables: `server` and `client`. Ensure they recompile if `common.h` changes. Include a clean rule.

```makefile
# Your answer here:
all: server client

server: server.c common.h
	gcc -o server server.c

client: client.c common.h
	gcc -o client client.c

clean:
	rm -f server client
```

---

## ⏱️ PART 5: THE FINAL BOSS (Similar to LT2)

**Q12. The Grand Integration Test**
1. Write a parent process that creates a Message Queue.
2. The parent `fork()`s TWO child processes.
3. Child 1 reads a string from the user, counts the vowels, and sends the count via the Message Queue (using `mtype = 1`).
4. Child 2 reads a string from the user, counts the consonants, and sends the count via the Message Queue (using `mtype = 2`).
5. The parent waits for both messages to arrive (using `msgrcv`), prints the final total, cleans up the queue, and exits.

---
*Good luck tomorrow! Get some sleep, you've got this.*
