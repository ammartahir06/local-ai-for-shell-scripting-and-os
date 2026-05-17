# C Operating System Concepts Reference

## Process Management

### fork() - Create Child Process

```c
#include <unistd.h>
#include <sys/wait.h>

pid_t pid = fork();
if (pid == 0) {
    // Child process
} else if (pid > 0) {
    // Parent process
    wait(NULL);  // Wait for child
}
```

### exec() Family - Replace Process Image

```c
// execvp - search PATH for program
char *args[] = {"ls", "-la", NULL};
execvp("ls", args);

// Other variants: execl, execle, execlp, execv, execve
```

### wait() / waitpid() - Wait for Child

```c
int status;
pid_t child = waitpid(pid, &status, 0);
if (WIFEXITED(status)) {
    int exit_code = WEXITSTATUS(status);
}
```

## Threading (POSIX Threads)

### Create and Join Threads

```c
#include <pthread.h>

void *thread_func(void *arg) {
    // Thread work
    pthread_exit(NULL);
}

pthread_t thread;
pthread_create(&thread, NULL, thread_func, arg);
pthread_join(thread, NULL);
```

### Mutex (Mutual Exclusion)

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_lock(&mutex);
// Critical section
pthread_mutex_unlock(&mutex);
```

### Condition Variables

```c
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// Wait
pthread_mutex_lock(&mutex);
while (!condition)
    pthread_cond_wait(&cond, &mutex);
pthread_mutex_unlock(&mutex);

// Signal
pthread_mutex_lock(&mutex);
condition = true;
pthread_cond_signal(&cond);
pthread_mutex_unlock(&mutex);
```

### Semaphores

```c
#include <semaphore.h>

sem_t sem;
sem_init(&sem, 0, initial_value);
sem_wait(&sem);   // P operation (decrement)
sem_post(&sem);   // V operation (increment)
sem_destroy(&sem);
```

## Inter-Process Communication (IPC)

### Pipes

```c
int pipefd[2];
pipe(pipefd);
// pipefd[0] = read end
// pipefd[1] = write end
```

### Shared Memory (POSIX)

```c
#include <sys/mman.h>
#include <fcntl.h>

int fd = shm_open("/name", O_CREAT | O_RDWR, 0666);
ftruncate(fd, size);
void *ptr = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
// Use shared memory...
munmap(ptr, size);
shm_unlink("/name");
```

## Signal Handling

```c
#include <signal.h>

void handler(int signum) {
    // Handle signal
}

// Simple
signal(SIGINT, handler);

// Robust (preferred)
struct sigaction sa;
sa.sa_handler = handler;
sigemptyset(&sa.sa_mask);
sa.sa_flags = 0;
sigaction(SIGINT, &sa, NULL);
```

## Socket Programming

```c
#include <sys/socket.h>
#include <arpa/inet.h>

// TCP Server steps:
int fd = socket(AF_INET, SOCK_STREAM, 0);
bind(fd, addr, sizeof(addr));
listen(fd, backlog);
int client = accept(fd, NULL, NULL);
read(client, buffer, size);
write(client, data, len);
close(client);
close(fd);
```

## Compilation

```bash
gcc -Wall -o output source.c           # Basic
gcc -Wall -g -o debug source.c         # With debug
gcc -Wall -o threads threads.c -lpthread  # With pthreads
gcc -Wall -o shm shm.c -lrt           # With shared memory
```
