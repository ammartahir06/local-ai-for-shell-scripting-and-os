# 🟢 SEMAPHORES, SHARED MEMORY & FIFO — Exam Guide
### Priority #5-7 — Know the patterns, less likely but possible

---

## PART 1: SEMAPHORES (Lab 8 — Donut Shop)

### 1.1 What is a Semaphore?

**Analogy:** A parking lot counter. Shows "3 spaces free". Car enters → counter decrements to 2. Car leaves → counter increments to 3. If counter is 0, the gate blocks until a space opens.

### 1.2 P and V Operations — The Two Core Actions

| Name | Also called | `sem_op` value | What it does |
|------|------------|----------------|-------------|
| **P** | Wait / Acquire / Down | **Negative** (-N) | Subtract N. If result would be < 0, **BLOCK** |
| **V** | Signal / Release / Up | **Positive** (+N) | Add N. Wake up blocked processes |

> 🧠 **P** = **P**lease let me in (blocks). **V** = **V**acate (release spot).

### 1.3 The Four Files (from your lab8)

#### `myheader.h` — Shared Definitions
```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <errno.h>

#define PLAIN 0     // semaphore[0] = plain donuts
#define CHOC  1     // semaphore[1] = chocolate donuts
#define SHUG  2     // semaphore[2] = sugar donuts
#define SEMKEY 456  // shared key for all programs

// MUST define this yourself on Linux:
union semun {
    int              val;
    struct semid_ds *buf;
    unsigned short  *array;    // used for GETALL/SETALL
    struct seminfo  *__buf;
};
```

#### `sem_setup.c` — Create and Initialize
```c
#include "myheader.h"

int main(void) {
    int sem_id;
    union semun arg;
    unsigned short dcount[3];

    // Create set of 3 semaphores
    sem_id = semget(SEMKEY, 3, IPC_CREAT | IPC_EXCL | 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    // Set initial values
    dcount[PLAIN] = 2;    // 2 plain donuts
    dcount[CHOC]  = 3;    // 3 chocolate donuts
    dcount[SHUG]  = 4;    // 4 sugar donuts
    arg.array = dcount;

    // SETALL = set all semaphores at once
    if (semctl(sem_id, 0, SETALL, arg) == -1) {
        perror("semctl"); exit(1);
    }
    printf("Semaphore set created. ID=%d\n", sem_id);
    return 0;
}
```

#### `producer.c` — Add Resources (V operation, positive sem_op)
```c
#include "myheader.h"

int main(void) {
    struct sembuf sops[3];
    union semun arg;
    unsigned short dcount[3];

    int sem_id = semget(SEMKEY, 3, 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    // Read current values
    arg.array = dcount;
    semctl(sem_id, 0, GETALL, arg);
    printf("Current: Plain=%d, Choc=%d, Sugar=%d\n",
           dcount[PLAIN], dcount[CHOC], dcount[SHUG]);

    // POSITIVE sem_op = ADD (V operation = produce/release)
    sops[0].sem_num = PLAIN; sops[0].sem_op = dcount[PLAIN]; sops[0].sem_flg = 0;
    sops[1].sem_num = CHOC;  sops[1].sem_op = dcount[CHOC];  sops[1].sem_flg = 0;
    sops[2].sem_num = SHUG;  sops[2].sem_op = dcount[SHUG];  sops[2].sem_flg = 0;

    // Execute atomically
    if (semop(sem_id, sops, 3) == -1) { perror("semop"); exit(1); }
    printf("Production done!\n");
    return 0;
}
```

#### `consumer.c` — Take Resources (P operation, negative sem_op)
```c
#include "myheader.h"

int main(void) {
    struct sembuf sops[3];
    union semun arg;
    unsigned short dcount[3];

    int sem_id = semget(SEMKEY, 3, 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    arg.array = dcount;
    semctl(sem_id, 0, GETALL, arg);
    printf("Available: Plain=%d, Choc=%d, Sugar=%d\n",
           dcount[PLAIN], dcount[CHOC], dcount[SHUG]);

    printf("Enter how many Plain, Choc, Sugar: ");
    scanf("%hu %hu %hu", &dcount[PLAIN], &dcount[CHOC], &dcount[SHUG]);

    // NEGATIVE sem_op = SUBTRACT (P operation = consume/acquire)
    sops[0].sem_num = PLAIN; sops[0].sem_op = 0 - dcount[PLAIN]; sops[0].sem_flg = 0;
    sops[1].sem_num = CHOC;  sops[1].sem_op = 0 - dcount[CHOC];  sops[1].sem_flg = 0;
    sops[2].sem_num = SHUG;  sops[2].sem_op = 0 - dcount[SHUG];  sops[2].sem_flg = 0;

    printf("Waiting for resources...\n");
    // ATOMIC: all 3 must succeed or we block
    if (semop(sem_id, sops, 3) == -1) { perror("semop"); exit(1); }
    printf("Got my donuts!\n");
    return 0;
}
```

### 1.4 The Atomicity Guarantee — Key Concept

```
State: Plain=2, Choc=3, Sugar=4
Consumer wants: Plain=2, Choc=1, Sugar=6

semop checks ALL at once:
  Plain: 2 - 2 = 0   ✓
  Choc:  3 - 1 = 2   ✓
  Sugar: 4 - 6 = -2  ✗ (would go negative!)

Result: NONE taken. Process BLOCKS.
→ No partial consumption → prevents deadlock
→ When producer adds more sugar, all operations succeed at once
```

### 1.5 Running the Donut Shop
```bash
gcc -o sem_setup sem_setup.c
gcc -o producer  producer.c
gcc -o consumer  consumer.c

./sem_setup     # Create semaphores (run FIRST)
./producer      # Add donuts
./consumer      # Buy donuts (blocks if not enough)

ipcs -s         # List semaphore sets
ipcrm -s <id>   # Delete semaphore set
```

---

## PART 2: SHARED MEMORY (Lab 3)

### 2.1 What is Shared Memory?

**Analogy:** One whiteboard in the center of a room. Every process that attaches can read/write directly. No copying, no messages. **Fastest IPC method.**

**Risk:** Two processes writing simultaneously = corruption. Use semaphores to coordinate.

### 2.2 The Four Steps

```c
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/stat.h>

// 1. Generate key (same key = same segment for any process)
key_t key = ftok("/etc/passwd", 5);

// 2. Create/get shared memory segment
int shm_id = shmget(key, 100, S_IRUSR | S_IWUSR | IPC_CREAT);
//                        ^size  ^permissions

// 3. Attach — get a pointer to use
char *ptr = (char *)shmat(shm_id, NULL, 0);
//                                ^OS picks address

// 4. USE IT like normal memory
sprintf(ptr, "Hello from PID %ld", (long)getpid());  // write
printf("Read: %s\n", ptr);                             // read

// 5. Detach (done using it)
shmdt(ptr);

// 6. Delete segment (only once, from one process)
shmctl(shm_id, IPC_RMID, NULL);
```

### 2.3 Writer Program (from your lab3)

```c
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <stdio.h>
#include <unistd.h>

#define PERM (S_IRUSR | S_IWUSR | IPC_CREAT)

int main(void) {
    key_t key = ftok("/etc/passwd", 5);
    int id = shmget(key, 100, PERM);
    char *cptr = (char *)shmat(id, NULL, 0);

    struct timeval tv;
    for (int i = 0; i < 5; i++) {
        gettimeofday(&tv, NULL);
        sprintf(cptr, "Time: %ld.%06ld", tv.tv_sec, tv.tv_usec);
        printf("Wrote: %s\n", cptr);
        sleep(5);
    }

    shmdt(cptr);
    shmctl(id, IPC_RMID, NULL);
    return 0;
}
```

### 2.4 Reader Program (from your lab3)

```c
// Same setup, but only reads:
key_t key = ftok("/etc/passwd", 5);    // SAME key = SAME segment
int id = shmget(key, 100, PERM);
char *cptr = (char *)shmat(id, NULL, 0);

for (int i = 0; i < 5; i++) {
    printf("Read: %s\n", cptr);
    sleep(5);
}
shmdt(cptr);
```

---

## PART 3: FIFO / NAMED PIPES (Lab 6)

### 3.1 Pipe vs FIFO

| Feature | Anonymous Pipe | FIFO (Named Pipe) |
|---------|---------------|-------------------|
| Name on filesystem | No | Yes (e.g., `"myfifo"`) |
| Who can use | Only parent-child | Any process that knows the name |
| Created with | `pipe(fd)` | `mkfifo(name, perms)` |
| Lifetime | Dies with processes | File persists on disk |

### 3.2 Creating and Using a FIFO

```c
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

// Create the FIFO
if (mkfifo("myfifo", S_IRUSR | S_IWUSR) == -1) {
    if (errno != EEXIST) {    // OK if it already exists
        perror("mkfifo");
        return 1;
    }
}
```

### 3.3 The Blocking Rendezvous

When opening a FIFO:
- `open("myfifo", O_RDONLY)` → **BLOCKS** until someone opens for writing
- `open("myfifo", O_WRONLY)` → **BLOCKS** until someone opens for reading

Both sides must "pick up the phone" before communication starts.

### 3.4 Complete FIFO Example (from your lab6)

```c
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>

#define FIFO_PERM (S_IRUSR | S_IWUSR)

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s pipename\n", argv[0]);
        return 1;
    }

    // Create FIFO
    if (mkfifo(argv[1], FIFO_PERM) == -1 && errno != EEXIST) {
        perror("mkfifo"); return 1;
    }

    pid_t pid = fork();
    if (pid == -1) { perror("fork"); return 1; }

    if (pid == 0) {
        // CHILD: write to FIFO
        int fd;
        while ((fd = open(argv[1], O_WRONLY)) == -1 && errno == EINTR);
        //       ^^^^^^ retry if interrupted by signal (EINTR)
        char buf[256];
        snprintf(buf, sizeof(buf), "[%ld]: Hello from child!\n", (long)getpid());
        write(fd, buf, strlen(buf) + 1);
        close(fd);
        return 0;
    } else {
        // PARENT: read from FIFO
        int fd;
        while ((fd = open(argv[1], O_RDONLY)) == -1 && errno == EINTR);
        char buf[256];
        read(fd, buf, sizeof(buf));
        printf("Parent read: %s\n", buf);
        close(fd);
        wait(NULL);
    }
    return 0;
}
```

Run: `./fifo_demo myfifo`

---

## QUICK REFERENCE — All IPC Methods

| Method | Create | Send/Write | Receive/Read | Cleanup |
|--------|--------|-----------|-------------|---------|
| **Pipe** | `pipe(fd)` | `write(fd[1], ...)` | `read(fd[0], ...)` | `close()` |
| **FIFO** | `mkfifo(name, perm)` | `write(fd, ...)` | `read(fd, ...)` | `close()`, `rm fifo` |
| **Msg Queue** | `msgget(key, flags)` | `msgsnd(id, &msg, sz, 0)` | `msgrcv(id, &msg, sz, type, 0)` | `msgctl(id, IPC_RMID, NULL)` |
| **Shared Mem** | `shmget(key, size, flags)` | `sprintf(ptr, ...)` | `printf("%s", ptr)` | `shmdt(ptr)` + `shmctl(id, IPC_RMID, NULL)` |
| **Semaphore** | `semget(key, n, flags)` | `semop(id, sops, n)` | (same) | `semctl(id, 0, IPC_RMID)` |

```bash
# Terminal commands to manage IPC:
ipcs                # show all IPC resources
ipcs -q / -m / -s   # show queues / shared mem / semaphores
ipcrm -q <id>       # delete queue
ipcrm -m <id>       # delete shared memory
ipcrm -s <id>       # delete semaphore set
```
