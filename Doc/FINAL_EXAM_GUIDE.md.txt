# 🎯 OS LAB FINAL EXAM — ULTIMATE SURVIVAL GUIDE
### Your One-Night Cram Plan — Everything You Need to Pass (and Score High)

> **⏰ Exam: Tomorrow (May 21, 2026)**
> **Strategy: 80/20 Pareto Principle — Focus on what gets asked MOST**

---

## 🔥 PARETO ANALYSIS: What to Study FIRST

Based on your past papers (FA23 v01 & v02), lab tasks (LT1, LT2, LT3), and the fact that scripting came up in today's other section:

| Priority | Topic | Why | Time to Spend |
|----------|-------|-----|---------------|
| 🔴 **#1** | **Bash Shell Scripting** | Came in other section TODAY. LT3 was scripting. WILL come. | 2-3 hours |
| 🔴 **#2** | **fork() + Pipes + Message Queues** | LT2 was exactly this. Core of every past paper. | 2 hours |
| 🟡 **#3** | **Makefile** | Came in other section today. LT1 was Makefile. | 1 hour |
| 🟡 **#4** | **Threads (pthreads in C)** | Came in other section. Lab 7 code. | 1 hour |
| 🟢 **#5** | **Semaphores** | Lab 8. Producer-Consumer. | 45 min |
| 🟢 **#6** | **Shared Memory + Message Queues (IPC)** | Lab 3. Paired with semaphores. | 30 min |
| 🔵 **#7** | **FIFO (Named Pipes)** | Lab 6. Less likely but possible. | 20 min |
| 🔵 **#8** | **Sockets (Client-Server)** | Lab 9. Unlikely for final but know basics. | 15 min |
| ⚪ **#9** | **Java Threads** | Lab 5. Very unlikely in lab exam. | Skip unless time |

---

## 📚 TABLE OF CONTENTS

| File | What's Inside |
|------|--------------|
| **This file** | Strategy, Lab breakdown, Quick reference |
| [GUIDE_SCRIPTING.md](./GUIDE_SCRIPTING.md) | 🔴 Bash Scripting — COMPLETE guide with practice |
| [GUIDE_FORK_PIPES_MQ.md](./GUIDE_FORK_PIPES_MQ.md) | 🔴 fork, pipes, message queues, dup2, exec |
| [GUIDE_MAKEFILE_THREADS.md](./GUIDE_MAKEFILE_THREADS.md) | 🟡 Makefile + pthreads in C |
| [GUIDE_SEM_SHM_FIFO.md](./GUIDE_SEM_SHM_FIFO.md) | 🟢 Semaphores, Shared Memory, FIFO |
| [PRACTICE_QUESTIONS.md](./PRACTICE_QUESTIONS.md) | 🎯 50+ practice questions with solutions |

---

## 🏫 YOUR LABS — PROPER NAMES & WHAT THEY COVERED

| Lab # | Proper Name | Key Files | Core Concepts |
|-------|-------------|-----------|---------------|
| **Lab 1** | **C Basics, Structs/Unions & Makefile** | `main.c`, `f1.c`, `f2.c`, `myheader.h`, `makefile` | struct vs union memory layout, static & shared libraries, multi-file compilation |
| **Lab 2+4** | **Processes, Pipes & I/O Redirection** | `twoprocs.c`, `simplefan.c`, `simplechain.c`, `redirect.c`, `simpleredirect.c`, `parentwritepipe.c`, `execls.c`, `outputPID.c` | fork(), fan/chain topology, dup2(), pipe(), exec(), `ls -l \| wc` pipeline |
| **Lab 3** | **IPC: Message Queues & Shared Memory** | `msgqueue.h`, `msgwriter.c`, `msgreader.c`, `shmem_writer.c`, `shmem_reader.c`, `makefile` | ftok(), msgget/msgsnd/msgrcv, shmget/shmat/shmdt, gettimeofday() |
| **Lab 5** | **Java Threads & Concurrency** | `MatrixThread.java`, `MatrixSquare.java`, `MMWithThreadExecService.java`, `SquareMatrix.java`, `WDist.java` | Runnable, Thread.start/join, ExecutorService, ForkJoinPool |
| **Lab 6** | **Named Pipes (FIFO)** | `parentchildfifo.c` | mkfifo(), blocking open, EINTR retry, parent-child FIFO communication |
| **Lab 7** | **POSIX Threads (pthreads) in C** | `PrintThread.c`, `thread1.c`, `Matrixsquare.c` | pthread_create/join, void* args, clock_gettime, matrix squaring with threads |
| **Lab 8** | **Semaphores (Producer-Consumer)** | `myheader.h`, `sem_setup.c`, `producer.c`, `consumer.c` | semget/semctl/semop, union semun, P/V operations, donut shop model |
| **Lab 9** | **Socket Programming (Client-Server)** | `server.c`, `server2.c`, `client.c` | socket(), bind(), listen(), accept(), connect(), fork-per-client |

---

## 🧠 YOUR PAST LAB TASKS — WHAT WAS ASKED

### LT1 — Simpletron Machine (Makefile Focus)
- Build a virtual machine simulator using multiple `.c` files + `.h` header + **Makefile**
- Makefile must build `simple.exe` with static AND shared libraries
- Key: `ar cr`, `gcc -shared`, `-fpic`, `-L. -lname`

### LT2 — Pipe + Message Queue (fork + IPC Focus)
- Parent writes 40 random numbers to pipe
- Fork 4 children, each reads 10 numbers, computes sum
- Children send results via **message queue** (PID + sum)
- Parent reads 4 messages, prints, waits, cleans up

### LT3 — Shell Scripting (MOST LIKELY TO COME)
**Part A:** Organize `.txt` files by word count into `short/`, `medium/`, `long/` directories
**Part B:** Script with two functions: `sum_of_digits` and `multiplication_table`

---

## ⚡ QUICK REFERENCE — ALL SYSTEM CALLS

```c
/* ── PROCESS ── */
pid_t fork();                          // 0=child, >0=parent, -1=error
pid_t getpid();  pid_t getppid();
pid_t wait(NULL);                      // wait for ANY child
void exit(int status);
int execl(path, arg0, ..., NULL);      // replace process

/* ── FILE DESCRIPTORS ── */
int open(path, flags, mode);           // O_RDONLY, O_WRONLY, O_CREAT, O_APPEND
int close(fd);
ssize_t read(fd, buf, count);
ssize_t write(fd, buf, count);
int dup2(oldfd, newfd);                // rewire newfd → oldfd's target

/* ── PIPES ── */
int pipe(int fd[2]);                   // fd[0]=read, fd[1]=write

/* ── FIFO ── */
int mkfifo(path, mode);               // S_IRUSR | S_IWUSR

/* ── MESSAGE QUEUES ── */
key_t ftok(path, id);                  // generate IPC key
int msgget(key, flags);                // IPC_PRIVATE or ftok key
int msgsnd(id, &msg, sizeof(msg)-sizeof(long), 0);
ssize_t msgrcv(id, &msg, sizeof(msg)-sizeof(long), type, 0);
int msgctl(id, IPC_RMID, NULL);        // DELETE queue

/* ── SHARED MEMORY ── */
int shmget(key, size, flags);
void* shmat(id, NULL, 0);             // attach, returns pointer
int shmdt(ptr);                        // detach
int shmctl(id, IPC_RMID, NULL);        // delete

/* ── SEMAPHORES ── */
int semget(key, nsems, flags);
int semctl(id, semnum, cmd, arg);      // SETALL, GETALL, IPC_RMID
int semop(id, struct sembuf*, nsops);  // +N=release, -N=acquire

/* ── THREADS ── */
int pthread_create(&tid, NULL, fn, arg);
int pthread_join(tid, NULL);
pthread_t pthread_self();
// Compile: gcc -o out file.c -lpthread
```

---

## 🚨 TOP 10 MISTAKES THAT LOSE MARKS

| # | Mistake | Fix |
|---|---------|-----|
| 1 | Forgetting `#!/bin/bash` in scripts | ALWAYS first line |
| 2 | `sizeof(msg)` in msgsnd/msgrcv | Use `sizeof(msg) - sizeof(long)` |
| 3 | Forgetting `wait(NULL)` after fork | One wait() per child |
| 4 | Not closing unused pipe ends | Close fd[0] in writer, fd[1] in reader |
| 5 | Forgetting `-lpthread` when compiling | `gcc file.c -lpthread` |
| 6 | Using spaces around `=` in bash | `var=value` NOT `var = value` |
| 7 | `long mtype` not first in msg struct | MUST be first field, MUST be > 0 |
| 8 | Missing `chmod +x script.sh` | Or run with `bash script.sh` |
| 9 | Forgetting `msgctl(id, IPC_RMID, NULL)` | Always cleanup IPC resources |
| 10 | Using TABs in Makefile — spaces won't work | Makefile rules MUST use TAB character |

---

## 📖 STUDY ORDER (Tonight)

```
6:00 PM - 8:00 PM  → GUIDE_SCRIPTING.md (read + practice scripts)
8:00 PM - 9:30 PM  → GUIDE_FORK_PIPES_MQ.md (fork patterns + LT2 style)
9:30 PM - 10:15 PM → GUIDE_MAKEFILE_THREADS.md (Makefile rules + pthreads)
10:15 PM - 10:45 PM → GUIDE_SEM_SHM_FIFO.md (semaphores + shared mem)
10:45 PM - 11:30 PM → PRACTICE_QUESTIONS.md (solve without looking)
11:30 PM - 12:00 AM → Re-read Quick Reference above, sleep!
```

> 💡 **Sleep is more important than one more hour of studying. Your brain consolidates memory during sleep.**

---

*Now go read the individual guide files. Start with GUIDE_SCRIPTING.md — it's the most likely to appear.*
