# 🟡 MAKEFILE & THREADS (pthreads) — Exam Guide
### Priority #3 — Both came in today's other section

---

## PART 1: MAKEFILE

### 1.1 What is a Makefile?

A Makefile is a build automation script. Instead of typing long `gcc` commands, you type `make` and it builds everything.

### 1.2 Rule Syntax — THE CORE CONCEPT

```makefile
target: dependency1 dependency2
[TAB]   command to build target
```

> ⚠️ **CRITICAL:** The command line MUST start with a **real TAB character**, NOT spaces. This is the #1 Makefile error.

### 1.3 Your Lab 1 Makefile — Line by Line

```makefile
# Goal: build "test" executable from main.o + static lib + shared lib
test: main.o libmystaticlib.a libmysharedlib.so
	gcc -o test main.o -L. -lmystaticlib -Wl,-rpath=/home/nadeem/SP26/code -lmysharedlib
#       -o test           → output file name
#       main.o            → compiled main.c
#       -L.               → look for libraries in current directory (.)
#       -lmystaticlib     → link libmystaticlib.a (lib prefix + .a auto-added)
#       -lmysharedlib     → link libmysharedlib.so
#       -Wl,-rpath=...    → tell linker where to find .so at runtime

# Compile main.c → main.o
main.o: main.c myheader.h
	gcc -c main.c
#       -c    → compile only, produce .o (don't link)

# Compile f1.c → f1.o (for static library)
f1.o: f1.c
	gcc -c f1.c

# Compile f2.c → f2.o (for shared library)
f2.o: f2.c
	gcc -c -fpic f2.c
#       -fpic → Position Independent Code (REQUIRED for shared libs)

# Create SHARED library (.so) from f2.o
libmysharedlib.so: f2.o
	gcc -shared -o libmysharedlib.so f2.o
#       -shared → create a .so (shared/dynamic library)

# Create STATIC library (.a) from f1.o
libmystaticlib.a: f1.o
	ar cr libmystaticlib.a f1.o
#       ar    → archive tool
#       c     → create archive
#       r     → replace if exists

# Clean rule — not a file, just a command
clean:
	rm *.o libmystaticlib.a libmysharedlib.so test
```

### 1.4 Your Lab 3 Makefile — Multiple Executables

```makefile
all: msgreader.exe msgwriter.exe shmem_writer.exe shmem_reader.exe

msgreader.exe: msgreader.c msgqueue.h
	gcc -o msgreader.exe msgreader.c

msgwriter.exe: msgwriter.c msgqueue.h
	gcc -o msgwriter.exe msgwriter.c

shmem_writer.exe: shmem_writer.c
	gcc -o shmem_writer.exe shmem_writer.c

shmem_reader.exe: shmem_reader.c
	gcc -o shmem_reader.exe shmem_reader.c

clean:
	rm *.exe
```

### 1.5 Static vs Shared Library — Know the Difference

| Feature | Static Library `.a` | Shared Library `.so` |
|---------|--------------------|--------------------|
| **Analogy** | Photocopy — embedded in your exe | Library card — borrowed at runtime |
| **Created with** | `ar cr libname.a obj.o` | `gcc -shared -o libname.so obj.o` |
| **Linked when** | At compile time | At runtime |
| **Executable size** | Larger (code copied inside) | Smaller |
| **To update** | Must recompile everything | Just replace the .so file |
| **Compile flag** | `-c` only | `-c -fpic` (Position Independent Code) |

### 1.6 Key GCC Flags — Memorize

| Flag | Meaning |
|------|---------|
| `-c` | Compile only (produce .o, don't link) |
| `-o name` | Name the output file |
| `-fpic` or `-fPIC` | Position Independent Code (for .so) |
| `-shared` | Create a shared library |
| `-L.` | Look for libraries in current directory |
| `-lname` | Link `libname.so` or `libname.a` |
| `-lpthread` | Link pthread library |
| `-Wall` | Show all warnings |

### 1.7 Makefile Variables (May Be Asked)

```makefile
CC = gcc
CFLAGS = -Wall -g
LDFLAGS = -L. -lmylib

# Use variables with $(VAR_NAME)
myprogram: main.o
	$(CC) $(CFLAGS) -o myprogram main.o $(LDFLAGS)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c
```

### 1.8 Common Make Commands

```bash
make              # build the FIRST target (default)
make clean        # run the "clean" rule
make target_name  # build a specific target
make -n           # dry run: show what would be done without doing it
```

### 1.9 How to Write a Makefile From Scratch (Exam Pattern)

**Given:** `main.c` includes `utils.h`, uses functions from `utils.c`. Build an executable called `myprogram`.

```makefile
myprogram: main.o utils.o
	gcc -o myprogram main.o utils.o

main.o: main.c utils.h
	gcc -c main.c

utils.o: utils.c utils.h
	gcc -c utils.c

clean:
	rm -f *.o myprogram
```

**Given:** Same but also create a shared library from `utils.c`:

```makefile
myprogram: main.o libutils.so
	gcc -o myprogram main.o -L. -lutils

main.o: main.c utils.h
	gcc -c main.c

utils.o: utils.c utils.h
	gcc -c -fpic utils.c

libutils.so: utils.o
	gcc -shared -o libutils.so utils.o

clean:
	rm -f *.o *.so myprogram
```

---

## PART 2: POSIX THREADS (pthreads) in C

### 2.1 Process vs Thread — Know This Table

| Feature | Process (fork) | Thread (pthread) |
|---------|---------------|-----------------|
| Memory | Separate copy | **Shared** |
| Creation cost | High | Low |
| Communication | Needs IPC | Just use shared variables |
| Crash effect | Others unaffected | **Kills whole process** |
| PID | Each has own PID | Share parent's PID |

### 2.2 Thread Function Signature — NEVER CHANGE

```c
void *myFunction(void *arg) {
    // Must return void*
    // Must accept void*
    // Cast arg inside to your type
    return NULL;
}
```

### 2.3 Creating and Joining Threads

```c
#include <stdio.h>
#include <pthread.h>

void *myWork(void *arg) {
    int id = *(int *)arg;     // cast void* → int*, then dereference
    printf("Thread %d running\n", id);
    return NULL;
}

int main(void) {
    pthread_t tid[3];
    int ids[3] = {0, 1, 2};

    // Create 3 threads
    for (int i = 0; i < 3; i++) {
        pthread_create(&tid[i], NULL, myWork, &ids[i]);
        //             ^thread_id  ^default  ^function  ^argument
    }

    // Wait for all to finish (like wait() for processes)
    for (int i = 0; i < 3; i++) {
        pthread_join(tid[i], NULL);
    }

    printf("All threads done\n");
    return 0;
}
// Compile: gcc -o mythreads mythreads.c -lpthread
```

### 2.4 PrintAB Example (from your lab7/PrintThread.c)

```c
#include <stdio.h>
#include <pthread.h>

pthread_t tid[2];

void *printA(void *arg) {
    for (int i = 0; i < 40; i++)
        printf("A");
    return NULL;
}

void *printB(void *arg) {
    for (int i = 0; i < 40; i++)
        printf("B");
    return NULL;
}

int main(void) {
    pthread_create(&tid[0], NULL, printA, NULL);
    pthread_create(&tid[1], NULL, printB, NULL);
    pthread_join(tid[0], NULL);
    pthread_join(tid[1], NULL);
    return 0;
}
// Output: AABBABABBAABB... (random interleaving = concurrency!)
```

### 2.5 Matrix Squaring with Threads (from your lab7/Matrixsquare.c)

```c
#include <stdio.h>
#include <pthread.h>

pthread_t thread_id[3];

void *square(void *row) {
    int *trow = (int *)row;       // cast void* to int*
    for (int i = 0; i < 3; i++)
        trow[i] = trow[i] * trow[i];
    return NULL;
}

int main() {
    int a[3][3] = {
        {1, 2, 3},
        {3, 4, 5},
        {5, 6, 7}
    };

    // Each thread squares one ROW
    for (int i = 0; i < 3; i++)
        pthread_create(&thread_id[i], NULL, square, a[i]);
        //                                          ^^^^
        //                             a[i] is already a pointer to row i

    for (int i = 0; i < 3; i++)
        pthread_join(thread_id[i], NULL);

    // Print result
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++)
            printf("%d ", a[i][j]);
        printf("\n");
    }
    // Output: 1 4 9 / 9 16 25 / 25 36 49
}
```

### 2.6 Thread Timer Example (from your lab7/thread1.c)

```c
#include <stdio.h>
#include <pthread.h>
#include <time.h>

void *doSomeThing(void *arg) {
    struct timespec start, end;
    int tnum = *(int *)arg;

    // Get CPU time for THIS thread
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &start);

    // Simulate work
    for (unsigned long i = 0; i < 0xFFFFFFFF; ++i);

    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &end);

    double elapsed = (end.tv_sec - start.tv_sec)
                   + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Thread %d ran for %.6f seconds\n", tnum, elapsed);
    return NULL;
}

int main(void) {
    pthread_t tid[2];
    int tnum[2] = {0, 1};

    for (int i = 0; i < 2; i++)
        pthread_create(&tid[i], NULL, doSomeThing, &tnum[i]);

    for (int i = 0; i < 2; i++)
        pthread_join(tid[i], NULL);

    return 0;
}
```

### 2.7 Common Thread Exam Questions

**Q: What's the signature of a thread function?**
> `void *functionName(void *arg)` — cannot change these types.

**Q: How to pass an int to a thread?**
> Pass `&myint` as arg, inside thread: `int val = *(int *)arg;`

**Q: How to compile pthread program?**
> `gcc -o out source.c -lpthread` — forgetting `-lpthread` = linker error.

**Q: What's the difference between `pthread_self()` and `getpid()`?**
> `pthread_self()` = thread ID (unique per thread). `getpid()` = process ID (same for all threads in a process).

**Q: What happens if you don't join?**
> Thread resources aren't cleaned up (like zombie processes). Main might exit before threads finish.

**Q: What is `CLOCK_THREAD_CPUTIME_ID`?**
> Measures CPU time used by THIS specific thread only, not wall-clock time.

---

## QUICK MAKEFILE CHEAT SHEET

```
STRUCTURE:
  target: dependencies
  [TAB] command

STATIC LIB:   ar cr libname.a obj.o
SHARED LIB:   gcc -shared -o libname.so obj.o  (need -fpic when compiling .o)
LINK LIB:     gcc -o prog prog.o -L. -lname
COMPILE ONLY: gcc -c source.c
CLEAN:        rm -f *.o *.a *.so executable
```

## QUICK PTHREAD CHEAT SHEET

```
INCLUDE:       #include <pthread.h>
FUNCTION:      void *myFunc(void *arg) { ... return NULL; }
CREATE:        pthread_create(&tid, NULL, myFunc, &arg);
JOIN:          pthread_join(tid, NULL);
SELF:          pthread_t myid = pthread_self();
COMPILE:       gcc -o out source.c -lpthread
CAST ARG:      int val = *(int *)arg;
```
