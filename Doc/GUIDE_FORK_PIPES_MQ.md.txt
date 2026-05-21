# 🔴 FORK, PIPES & MESSAGE QUEUES — Complete Exam Guide
### Priority #2 — The backbone of every OS lab exam

---

## 1. FORK() — THE FOUNDATION

### 1.1 The Golden Rule — Memorize This

```
fork() is called ONCE but returns TWICE:
  → In PARENT: returns CHILD's PID (positive number)
  → In CHILD:  returns 0
  → On ERROR:  returns -1
```

### 1.2 Basic fork() Pattern — Write This In Your Sleep

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t childpid = fork();

    if (childpid == -1) {
        perror("fork failed");
        return 1;
    }

    if (childpid == 0) {
        // ═══ CHILD CODE ═══
        printf("CHILD: My PID=%ld, Parent=%ld\n",
               (long)getpid(), (long)getppid());
        return 0;
    }

    // ═══ PARENT CODE ═══
    printf("PARENT: My PID=%ld, Child=%ld\n",
           (long)getpid(), (long)childpid);
    wait(NULL);   // MUST wait for child
    printf("PARENT: Child has finished\n");
    return 0;
}
```

### 1.3 Memory Isolation — Key Concept

```c
int x = 0;
pid_t pid = fork();

if (pid == 0) {
    x = 5;    // child changes x to 5
    printf("Child x = %d\n", x);   // prints 5
} else {
    x = 10;   // parent changes x to 10
    wait(NULL);
    printf("Parent x = %d\n", x);  // prints 10 (NOT 5!)
}
// Each process has its OWN copy of x — changes don't affect each other
```

### 1.4 Fan Topology — One Parent, Many Children

```
        Parent
       /  |  |  \
      C1  C2  C3  C4
```

**The trick: CHILD breaks out of loop**

```c
// From your lab2+4/simplefan.c
pid_t childpid = 0;
int n = atoi(argv[1]);  // e.g., 4

for (int i = 1; i < n; i++) {
    if ((childpid = fork()) <= 0)
        break;   // child (0) breaks, parent continues
}

// After loop:
// childpid == 0 → I am a child
// childpid > 0  → I am the parent (finished forking)
```

### 1.5 Chain Topology — Each Creates Next

```
P0 → P1 → P2 → P3
```

**The trick: PARENT breaks out of loop**

```c
// From your lab2+4/simplechain.c
for (int i = 1; i < n; i++) {
    if (childpid = fork())   // if non-zero (parent) → break
        break;               // child (0) continues the loop
}
```

> 🧠 **Memory Trick:**
> - **Fan** = child **f**alls out (breaks) → `fork() <= 0` break
> - **Chain** = parent **c**hops out (breaks) → `if(fork())` break

---

## 2. EXEC() — REPLACING A PROCESS

```c
// exec replaces current process with new program
// If it succeeds, code after exec is NEVER reached

pid_t pid = fork();
if (pid == 0) {
    // Child becomes "ls -l"
    execl("/bin/ls", "ls", "-l", NULL);  // NULL sentinel REQUIRED
    perror("exec failed");  // only reached if exec fails
    exit(1);
}
// Parent continues here
wait(NULL);
```

**`execl()` argument format:**
```c
execl("/full/path/to/program", "program_name", "arg1", "arg2", ..., NULL);
//    ^path                     ^argv[0]        ^argv[1] ^argv[2]  ^end
```

---

## 3. PIPES — Parent-Child Communication

### 3.1 Creating and Using a Pipe

```c
int fd[2];          // fd[0] = READ end, fd[1] = WRITE end
pipe(fd);           // MUST happen BEFORE fork()

pid_t pid = fork();

if (pid == 0) {
    // CHILD reads from pipe
    close(fd[1]);   // close write end (child won't write)
    char buf[100];
    int n = read(fd[0], buf, sizeof(buf));
    printf("Child received: %s\n", buf);
    close(fd[0]);
    return 0;
} else {
    // PARENT writes to pipe
    close(fd[0]);   // close read end (parent won't read)
    char *msg = "Hello child!";
    write(fd[1], msg, strlen(msg) + 1);
    close(fd[1]);
    wait(NULL);
}
```

> 🧠 **Remember:**
> - `fd[0]` = Read (0 looks like an open mouth 👄)
> - `fd[1]` = Write (1 looks like a pencil ✏️)

### 3.2 Why Close Unused Pipe Ends?

If parent doesn't close `fd[0]` and child doesn't close `fd[1]`:
- The pipe's write end is still "open" even after writing is done
- Reader never gets EOF
- **Reader blocks forever**

**RULE: Always close the end you're not using!**

---

## 4. DUP2() — I/O Redirection

### 4.1 How dup2 Works

```c
dup2(oldfd, newfd);
// Makes newfd point to the same place as oldfd
// Typical use: redirect STDOUT to a file or pipe
```

### 4.2 Redirect STDOUT to a File (from your lab2+4/redirect.c)

```c
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

#define FLAGS (O_WRONLY | O_CREAT | O_APPEND)
#define MODE  (S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)

int main(void) {
    int fd = open("my.file", FLAGS, MODE);
    if (fd == -1) { perror("open"); return 1; }

    dup2(fd, STDOUT_FILENO);    // STDOUT now → my.file
    close(fd);                   // close raw fd (STDOUT already wired)

    write(STDOUT_FILENO, "OK", 2);  // goes to my.file, not terminal!
    return 0;
}
```

### 4.3 Building `ls -l | wc` in C (from your lab2+4/simpleredirect.c)

```c
#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void) {
    pid_t childpid;
    int fd[2];

    // Create pipe AND fork
    if ((pipe(fd) == -1) || ((childpid = fork()) == -1)) {
        perror("Failed to setup pipeline");
        return 1;
    }

    if (childpid == 0) {
        // ═══ CHILD runs "ls -l" ═══
        dup2(fd[1], STDOUT_FILENO);   // ls output → pipe write end
        close(fd[0]);                  // close unused read end
        close(fd[1]);                  // close raw write (already wired)
        execl("/bin/ls", "ls", "-l", NULL);
        perror("exec ls failed");
        return 1;
    }

    // ═══ PARENT runs "wc" ═══
    dup2(fd[0], STDIN_FILENO);    // wc input ← pipe read end
    close(fd[0]);                  // close raw read (already wired)
    close(fd[1]);                  // close unused write end
    execl("/usr/bin/wc", "wc", NULL);
    perror("exec wc failed");
    return 1;
}
```

**Visual:**
```
CHILD (ls -l)           PIPE            PARENT (wc)
  STDOUT ──────────► fd[1] ──► fd[0] ──────► STDIN
  (dup2 rewired)                            (dup2 rewired)
```

---

## 5. MESSAGE QUEUES — Sending Structured Data

### 5.1 The Message Struct — CRITICAL RULES

```c
struct mymsg {
    long mtype;      // ← MUST be FIRST field
                     // ← MUST be > 0
    // Your data goes after:
    int  pid;
    int  sum;
};
```

### 5.2 Complete Message Queue Example

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/wait.h>

struct msg {
    long type;
    int  pid;
    int  sum;
};

int main(void) {
    // Create message queue
    int msgid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    if (msgid == -1) { perror("msgget"); return 1; }

    pid_t pid = fork();

    if (pid == 0) {
        // CHILD: send a message
        struct msg m;
        m.type = 1;              // must be > 0
        m.pid  = getpid();
        m.sum  = 42;
        msgsnd(msgid, &m, sizeof(m) - sizeof(long), 0);
        //                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        //                data size = total - mtype size
        return 0;
    }

    // PARENT: receive the message
    wait(NULL);
    struct msg m;
    msgrcv(msgid, &m, sizeof(m) - sizeof(long), 1, 0);
    //                                           ^
    //                                 type=1: receive msgs with mtype==1
    //                                 type=0: receive any type
    printf("From PID %d: sum = %d\n", m.pid, m.sum);

    // CLEANUP — always delete!
    msgctl(msgid, IPC_RMID, NULL);
    return 0;
}
```

### 5.3 ftok() — For Unrelated Processes

```c
// Both programs use the SAME file and id → get SAME key
key_t key = ftok("/etc/passwd", 5);
int msgid = msgget(key, 0666 | IPC_CREAT);
```

### 5.4 Check/Delete IPC resources from terminal

```bash
ipcs -q            # list message queues
ipcs -m            # list shared memory
ipcs -s            # list semaphores
ipcrm -q <msgid>   # delete a message queue
```

---

## 6. 🎯 LT2 COMPLETE SOLUTION — The Most Important Program

This is the most likely type of question. Study this until you can write it from memory.

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/msg.h>

struct msg {
    long type;
    int  pid;
    int  sum;
};

int main(void) {
    int pipefd[2];
    int numbers[40];
    int total_sum = 0;

    // 1. Create pipe and message queue
    if (pipe(pipefd) == -1) { perror("pipe"); return 1; }
    int msgid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    if (msgid == -1) { perror("msgget"); return 1; }

    // 2. Generate 40 random numbers
    printf("I am parent process %ld and I am going to write following 40 numbers in pipe\n",
           (long)getpid());
    for (int i = 0; i < 40; i++) {
        numbers[i] = rand() % 100;
        total_sum += numbers[i];
        printf("%d ", numbers[i]);
    }
    printf("\nSum of the above numbers is %d\n", total_sum);

    // 3. Write all 40 numbers to pipe
    write(pipefd[1], numbers, sizeof(numbers));
    close(pipefd[1]);  // close write end — children will read

    // 4. Fork 4 children
    printf("Now I am going to fork four child processes\n");
    for (int i = 0; i < 4; i++) {
        if (fork() == 0) {
            // ═══ CHILD ═══
            int arr[10];
            read(pipefd[0], arr, sizeof(arr));  // each child reads 10 ints

            int sum = 0;
            for (int j = 0; j < 10; j++) sum += arr[j];

            // Send result via message queue
            struct msg m;
            m.type = 1;
            m.pid  = getpid();
            m.sum  = sum;
            msgsnd(msgid, &m, sizeof(m) - sizeof(long), 0);
            exit(0);
        }
    }

    close(pipefd[0]);  // parent done reading

    // 5. Receive 4 messages
    for (int i = 0; i < 4; i++) {
        struct msg m;
        msgrcv(msgid, &m, sizeof(m) - sizeof(long), 1, 0);
        printf("Message read is: I am process %d and sum of my 10 numbers is %d\n",
               m.pid, m.sum);
    }

    // 6. Wait for all children
    for (int i = 0; i < 4; i++) wait(NULL);
    printf("I am so sad, all of my children are dead now\n");

    // 7. Cleanup
    msgctl(msgid, IPC_RMID, NULL);
    return 0;
}
```

**Compile:** `gcc -o LT2.exe LT2.c`

---

## 7. KEY Q&A — What Examiner Asks

**Q: What does fork() return?**
> Child gets 0. Parent gets child's PID. Error returns -1.

**Q: What happens if you forget wait()?**
> Child becomes a **zombie** — it finished but exit status wasn't collected. Wastes kernel resources.

**Q: Fan vs Chain?**
> Fan: child breaks (`fork() <= 0`). Chain: parent breaks (`if(fork())`).

**Q: Why `sizeof(msg) - sizeof(long)`?**
> `mtype` is the header — OS handles it. You only tell msgsnd/msgrcv the payload size.

**Q: Pipe vs Message Queue?**
> Pipe: unstructured byte stream, parent-child only, FIFO order.
> MQ: structured messages with types, can be selective, any process with key.

**Q: What does exec() do?**
> Replaces current process's code with new program. Same PID, same open files. If it succeeds, code after exec is never reached.

**Q: Why close both pipe ends after dup2?**
> If write end stays open in any process, reader never gets EOF and hangs forever.
