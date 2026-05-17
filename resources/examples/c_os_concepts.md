# C OS Concepts Examples

## Fork and Wait

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();
    if (pid == 0) {
        printf("Child: PID=%d, Parent=%d\n", getpid(), getppid());
        return 42;
    } else {
        int status;
        waitpid(pid, &status, 0);
        printf("Parent: Child exited with %d\n", WEXITSTATUS(status));
    }
    return 0;
}
```

## Thread with Mutex

```c
#include <stdio.h>
#include <pthread.h>

int counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *increment(void *arg) {
    for (int i = 0; i < 100000; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("Counter: %d (expected 200000)\n", counter);
    pthread_mutex_destroy(&lock);
    return 0;
}
```

## Pipe Between Processes

```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int fd[2];
    pipe(fd);

    if (fork() == 0) {
        close(fd[1]);
        char buf[100];
        read(fd[0], buf, sizeof(buf));
        printf("Child got: %s\n", buf);
        close(fd[0]);
    } else {
        close(fd[0]);
        write(fd[1], "Hello pipe!", 12);
        close(fd[1]);
        wait(NULL);
    }
    return 0;
}
```

## Signal Handler

```c
#include <stdio.h>
#include <signal.h>
#include <unistd.h>

void handler(int sig) {
    printf("\nCaught signal %d\n", sig);
}

int main() {
    signal(SIGINT, handler);
    printf("PID: %d. Press Ctrl+C...\n", getpid());
    while(1) pause();
    return 0;
}
```
