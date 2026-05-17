"""C programming OS concepts training corpus.

Contains categorized C code snippets covering operating system concepts
including process management (fork, exec, wait), threading (pthreads),
IPC (pipes, shared memory, message queues), signals, sockets, and
memory management.
"""

C_OS_CORPUS = [
    # --- Fork and Process Creation ---
    '''
// fork() - Create a child process
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        // Fork failed
        perror("fork failed");
        exit(1);
    } else if (pid == 0) {
        // Child process
        printf("Child process: PID = %d, Parent PID = %d\\n", getpid(), getppid());
        printf("Child doing some work...\\n");
        sleep(2);
        printf("Child finished.\\n");
        exit(0);
    } else {
        // Parent process
        printf("Parent process: PID = %d, Child PID = %d\\n", getpid(), pid);
        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) {
            printf("Child exited with status %d\\n", WEXITSTATUS(status));
        }
    }

    return 0;
}
''',
    '''
// Multiple fork() calls - creating multiple child processes
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define NUM_CHILDREN 3

int main() {
    pid_t pids[NUM_CHILDREN];

    // Create multiple children
    for (int i = 0; i < NUM_CHILDREN; i++) {
        pids[i] = fork();

        if (pids[i] < 0) {
            perror("fork failed");
            exit(1);
        } else if (pids[i] == 0) {
            // Child process
            printf("Child %d: PID = %d\\n", i, getpid());
            sleep(i + 1);  // Each child sleeps different time
            printf("Child %d finished\\n", i);
            exit(i);  // Exit with child number as status
        }
    }

    // Parent waits for all children
    for (int i = 0; i < NUM_CHILDREN; i++) {
        int status;
        pid_t finished = waitpid(pids[i], &status, 0);
        if (WIFEXITED(status)) {
            printf("Child PID %d exited with status %d\\n",
                   finished, WEXITSTATUS(status));
        }
    }

    printf("All children finished. Parent exiting.\\n");
    return 0;
}
''',
    '''
// fork() and exec() - Replace child process image
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(1);
    } else if (pid == 0) {
        // Child: replace with ls command
        printf("Child: About to exec ls -la\\n");

        // execvp replaces the current process image
        char *args[] = {"ls", "-la", "/tmp", NULL};
        execvp("ls", args);

        // If exec returns, it failed
        perror("execvp failed");
        exit(1);
    } else {
        // Parent waits for child
        int status;
        waitpid(pid, &status, 0);
        printf("Parent: Child finished with status %d\\n", WEXITSTATUS(status));
    }

    return 0;
}
''',

    '''
// Zombie and Orphan processes demonstration
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

// Zombie: child exits but parent doesn't call wait()
void create_zombie() {
    pid_t pid = fork();
    if (pid == 0) {
        // Child exits immediately
        printf("Child (zombie-to-be) PID: %d exiting\\n", getpid());
        exit(0);
    } else {
        // Parent sleeps without calling wait - child becomes zombie
        printf("Parent sleeping... child %d is now a zombie\\n", pid);
        sleep(10);
        // After sleep, reap the zombie
        wait(NULL);
        printf("Zombie reaped\\n");
    }
}

// Orphan: parent exits before child
void create_orphan() {
    pid_t pid = fork();
    if (pid == 0) {
        // Child sleeps - will become orphan when parent exits
        printf("Child PID: %d, Parent PID: %d\\n", getpid(), getppid());
        sleep(5);
        // After parent exits, init (PID 1) adopts the orphan
        printf("Orphan child: new Parent PID: %d (adopted by init)\\n", getppid());
        exit(0);
    } else {
        // Parent exits immediately
        printf("Parent PID: %d exiting, leaving child %d as orphan\\n", getpid(), pid);
        exit(0);
    }
}

int main() {
    printf("=== Zombie Process Demo ===\\n");
    create_zombie();
    return 0;
}
''',

    # --- Pipes ---
    '''
// Pipe - Inter-process communication between parent and child
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int pipefd[2];  // pipefd[0] = read end, pipefd[1] = write end
    char buffer[256];

    if (pipe(pipefd) == -1) {
        perror("pipe failed");
        exit(1);
    }

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(1);
    } else if (pid == 0) {
        // Child: reads from pipe
        close(pipefd[1]);  // Close write end

        int bytes_read = read(pipefd[0], buffer, sizeof(buffer) - 1);
        buffer[bytes_read] = '\\0';
        printf("Child received: %s\\n", buffer);

        close(pipefd[0]);
        exit(0);
    } else {
        // Parent: writes to pipe
        close(pipefd[0]);  // Close read end

        const char *message = "Hello from parent!";
        write(pipefd[1], message, strlen(message));
        printf("Parent sent: %s\\n", message);

        close(pipefd[1]);
        waitpid(pid, NULL, 0);
    }

    return 0;
}
''',
    '''
// Two-way pipe communication (bidirectional)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int pipe1[2];  // Parent -> Child
    int pipe2[2];  // Child -> Parent
    char buffer[256];

    if (pipe(pipe1) == -1 || pipe(pipe2) == -1) {
        perror("pipe failed");
        exit(1);
    }

    pid_t pid = fork();

    if (pid == 0) {
        // Child
        close(pipe1[1]);  // Close write end of pipe1
        close(pipe2[0]);  // Close read end of pipe2

        // Read from parent
        int n = read(pipe1[0], buffer, sizeof(buffer) - 1);
        buffer[n] = '\\0';
        printf("Child received: %s\\n", buffer);

        // Send response to parent
        const char *response = "Hello from child!";
        write(pipe2[1], response, strlen(response));

        close(pipe1[0]);
        close(pipe2[1]);
        exit(0);
    } else {
        // Parent
        close(pipe1[0]);  // Close read end of pipe1
        close(pipe2[1]);  // Close write end of pipe2

        // Send to child
        const char *message = "Hello from parent!";
        write(pipe1[1], message, strlen(message));

        // Read response from child
        int n = read(pipe2[0], buffer, sizeof(buffer) - 1);
        buffer[n] = '\\0';
        printf("Parent received: %s\\n", buffer);

        close(pipe1[1]);
        close(pipe2[0]);
        waitpid(pid, NULL, 0);
    }

    return 0;
}
''',
    '''
// dup2 - Redirect stdout to pipe (simulate shell pipe: cmd1 | cmd2)
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

// Simulates: ls -la | grep ".c"
int main() {
    int pipefd[2];

    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(1);
    }

    pid_t pid1 = fork();
    if (pid1 == 0) {
        // First child: runs "ls -la"
        close(pipefd[0]);           // Close read end
        dup2(pipefd[1], STDOUT_FILENO);  // Redirect stdout to pipe
        close(pipefd[1]);

        execlp("ls", "ls", "-la", NULL);
        perror("execlp ls");
        exit(1);
    }

    pid_t pid2 = fork();
    if (pid2 == 0) {
        // Second child: runs "grep .c"
        close(pipefd[1]);           // Close write end
        dup2(pipefd[0], STDIN_FILENO);   // Redirect stdin from pipe
        close(pipefd[0]);

        execlp("grep", "grep", ".c", NULL);
        perror("execlp grep");
        exit(1);
    }

    // Parent closes both ends and waits
    close(pipefd[0]);
    close(pipefd[1]);
    waitpid(pid1, NULL, 0);
    waitpid(pid2, NULL, 0);

    return 0;
}
''',

    # --- Pthreads (Threading) ---
    '''
// Basic pthread - creating and joining threads
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 5

void *thread_function(void *arg) {
    int thread_id = *(int *)arg;
    printf("Thread %d: Hello from thread! (TID: %lu)\\n",
           thread_id, pthread_self());
    sleep(1);
    printf("Thread %d: Done.\\n", thread_id);
    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i;
        int rc = pthread_create(&threads[i], NULL, thread_function, &thread_ids[i]);
        if (rc != 0) {
            fprintf(stderr, "Error creating thread %d: %d\\n", i, rc);
            exit(1);
        }
    }

    // Wait for all threads to finish
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
        printf("Main: Thread %d joined.\\n", i);
    }

    printf("Main: All threads completed.\\n");
    return 0;
}
// Compile: gcc -o threads threads.c -lpthread
''',
    '''
// Mutex - protecting shared data from race conditions
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 10
#define ITERATIONS 100000

int shared_counter = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void *increment_counter(void *arg) {
    int thread_id = *(int *)arg;

    for (int i = 0; i < ITERATIONS; i++) {
        pthread_mutex_lock(&mutex);
        shared_counter++;  // Critical section
        pthread_mutex_unlock(&mutex);
    }

    printf("Thread %d finished\\n", thread_id);
    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, increment_counter, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Expected: %d\\n", NUM_THREADS * ITERATIONS);
    printf("Actual:   %d\\n", shared_counter);

    pthread_mutex_destroy(&mutex);
    return 0;
}
// Compile: gcc -o mutex mutex.c -lpthread
''',
    '''
// Producer-Consumer problem using mutex and condition variables
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define BUFFER_SIZE 5
#define NUM_ITEMS 20

int buffer[BUFFER_SIZE];
int count = 0;  // Number of items in buffer
int in = 0;     // Next position to produce
int out = 0;    // Next position to consume

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;
pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;

void *producer(void *arg) {
    for (int i = 0; i < NUM_ITEMS; i++) {
        pthread_mutex_lock(&mutex);

        // Wait while buffer is full
        while (count == BUFFER_SIZE) {
            pthread_cond_wait(&not_full, &mutex);
        }

        // Produce item
        buffer[in] = i;
        printf("Produced: %d (buffer[%d])\\n", i, in);
        in = (in + 1) % BUFFER_SIZE;
        count++;

        pthread_cond_signal(&not_empty);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void *consumer(void *arg) {
    for (int i = 0; i < NUM_ITEMS; i++) {
        pthread_mutex_lock(&mutex);

        // Wait while buffer is empty
        while (count == 0) {
            pthread_cond_wait(&not_empty, &mutex);
        }

        // Consume item
        int item = buffer[out];
        printf("Consumed: %d (buffer[%d])\\n", item, out);
        out = (out + 1) % BUFFER_SIZE;
        count--;

        pthread_cond_signal(&not_full);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t prod_thread, cons_thread;

    pthread_create(&prod_thread, NULL, producer, NULL);
    pthread_create(&cons_thread, NULL, consumer, NULL);

    pthread_join(prod_thread, NULL);
    pthread_join(cons_thread, NULL);

    printf("Producer-Consumer completed.\\n");
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&not_full);
    pthread_cond_destroy(&not_empty);
    return 0;
}
// Compile: gcc -o prodcons prodcons.c -lpthread
''',

    '''
// Semaphore - controlling access to shared resources
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_THREADS 5

sem_t semaphore;

void *worker(void *arg) {
    int id = *(int *)arg;

    printf("Thread %d: Waiting to enter critical section...\\n", id);
    sem_wait(&semaphore);  // Decrement (wait/P operation)

    // Critical section - only N threads can be here at once
    printf("Thread %d: Entered critical section\\n", id);
    sleep(2);  // Simulate work
    printf("Thread %d: Leaving critical section\\n", id);

    sem_post(&semaphore);  // Increment (signal/V operation)
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    // Initialize semaphore with value 2 (allow 2 threads at a time)
    sem_init(&semaphore, 0, 2);

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    sem_destroy(&semaphore);
    printf("All threads completed.\\n");
    return 0;
}
// Compile: gcc -o semaphore semaphore.c -lpthread
''',
    '''
// Reader-Writer problem using rwlock
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_READERS 5
#define NUM_WRITERS 2

int shared_data = 0;
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

void *reader(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < 3; i++) {
        pthread_rwlock_rdlock(&rwlock);
        printf("Reader %d: read value = %d\\n", id, shared_data);
        pthread_rwlock_unlock(&rwlock);
        usleep(100000);  // 100ms
    }
    return NULL;
}

void *writer(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < 3; i++) {
        pthread_rwlock_wrlock(&rwlock);
        shared_data++;
        printf("Writer %d: wrote value = %d\\n", id, shared_data);
        pthread_rwlock_unlock(&rwlock);
        usleep(200000);  // 200ms
    }
    return NULL;
}

int main() {
    pthread_t readers[NUM_READERS], writers[NUM_WRITERS];
    int reader_ids[NUM_READERS], writer_ids[NUM_WRITERS];

    for (int i = 0; i < NUM_READERS; i++) {
        reader_ids[i] = i;
        pthread_create(&readers[i], NULL, reader, &reader_ids[i]);
    }
    for (int i = 0; i < NUM_WRITERS; i++) {
        writer_ids[i] = i;
        pthread_create(&writers[i], NULL, writer, &writer_ids[i]);
    }

    for (int i = 0; i < NUM_READERS; i++)
        pthread_join(readers[i], NULL);
    for (int i = 0; i < NUM_WRITERS; i++)
        pthread_join(writers[i], NULL);

    pthread_rwlock_destroy(&rwlock);
    printf("Final value: %d\\n", shared_data);
    return 0;
}
// Compile: gcc -o rwlock rwlock.c -lpthread
''',
    '''
// Dining Philosophers problem - deadlock avoidance
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_PHILOSOPHERS 5

pthread_mutex_t forks[NUM_PHILOSOPHERS];

void think(int id) {
    printf("Philosopher %d is thinking...\\n", id);
    usleep(rand() % 500000);
}

void eat(int id) {
    printf("Philosopher %d is eating...\\n", id);
    usleep(rand() % 500000);
}

void *philosopher(void *arg) {
    int id = *(int *)arg;
    int left = id;
    int right = (id + 1) % NUM_PHILOSOPHERS;

    for (int i = 0; i < 3; i++) {
        think(id);

        // Deadlock avoidance: always pick up lower-numbered fork first
        int first = (left < right) ? left : right;
        int second = (left < right) ? right : left;

        pthread_mutex_lock(&forks[first]);
        pthread_mutex_lock(&forks[second]);

        eat(id);

        pthread_mutex_unlock(&forks[second]);
        pthread_mutex_unlock(&forks[first]);
    }

    printf("Philosopher %d is done.\\n", id);
    return NULL;
}

int main() {
    pthread_t threads[NUM_PHILOSOPHERS];
    int ids[NUM_PHILOSOPHERS];

    srand(time(NULL));

    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        pthread_mutex_init(&forks[i], NULL);
    }

    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, philosopher, &ids[i]);
    }

    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        pthread_join(threads[i], NULL);
    }

    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        pthread_mutex_destroy(&forks[i]);
    }

    printf("Dinner is over.\\n");
    return 0;
}
// Compile: gcc -o dining dining.c -lpthread
''',

    # --- Signals ---
    '''
// Signal handling in C
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// Simple signal handler
void sigint_handler(int signum) {
    printf("\\nCaught SIGINT (Ctrl+C)! Signal number: %d\\n", signum);
    printf("Cleaning up and exiting...\\n");
    exit(0);
}

void sigterm_handler(int signum) {
    printf("\\nCaught SIGTERM! Graceful shutdown...\\n");
    exit(0);
}

int main() {
    // Register signal handlers
    signal(SIGINT, sigint_handler);
    signal(SIGTERM, sigterm_handler);

    printf("Process PID: %d\\n", getpid());
    printf("Running... Press Ctrl+C to interrupt or send SIGTERM.\\n");

    // Infinite loop - waiting for signals
    while (1) {
        printf("Working...\\n");
        sleep(2);
    }

    return 0;
}
''',
    '''
// sigaction - more robust signal handling
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>

volatile sig_atomic_t got_signal = 0;

void handler(int signum, siginfo_t *info, void *context) {
    got_signal = signum;
    // Note: printf is not async-signal-safe, but used here for demo
    printf("\\nReceived signal %d from PID %d\\n", signum, info->si_pid);
}

int main() {
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;  // Use sa_sigaction instead of sa_handler
    sigemptyset(&sa.sa_mask);

    // Register for multiple signals
    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGUSR1, &sa, NULL);
    sigaction(SIGUSR2, &sa, NULL);

    printf("PID: %d\\n", getpid());
    printf("Send signals with: kill -SIGUSR1 %d\\n", getpid());

    while (1) {
        pause();  // Wait for a signal
        printf("Woke up from signal %d\\n", got_signal);
        got_signal = 0;
    }

    return 0;
}
''',
    '''
// Sending signals between processes
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <sys/wait.h>

void child_handler(int signum) {
    printf("Child received signal %d\\n", signum);
}

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        signal(SIGUSR1, child_handler);
        printf("Child PID: %d, waiting for signal...\\n", getpid());

        // Wait for signal from parent
        pause();

        printf("Child: Continuing after signal\\n");
        exit(0);
    } else {
        // Parent process
        sleep(1);  // Give child time to set up handler

        printf("Parent: Sending SIGUSR1 to child %d\\n", pid);
        kill(pid, SIGUSR1);

        waitpid(pid, NULL, 0);
        printf("Parent: Child finished\\n");
    }

    return 0;
}
''',

    # --- Shared Memory ---
    '''
// POSIX shared memory between processes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <fcntl.h>

#define SHM_NAME "/my_shared_mem"
#define SHM_SIZE 4096

typedef struct {
    int counter;
    char message[256];
} SharedData;

int main() {
    // Create shared memory object
    int fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (fd == -1) {
        perror("shm_open");
        exit(1);
    }

    // Set size
    ftruncate(fd, SHM_SIZE);

    // Map into address space
    SharedData *data = (SharedData *)mmap(NULL, SHM_SIZE,
                                          PROT_READ | PROT_WRITE,
                                          MAP_SHARED, fd, 0);
    if (data == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    // Initialize
    data->counter = 0;
    strcpy(data->message, "Hello from shared memory!");

    pid_t pid = fork();

    if (pid == 0) {
        // Child reads and modifies shared memory
        printf("Child: counter = %d, message = %s\\n",
               data->counter, data->message);
        data->counter = 42;
        strcpy(data->message, "Modified by child!");
        exit(0);
    } else {
        waitpid(pid, NULL, 0);
        // Parent reads modified data
        printf("Parent: counter = %d, message = %s\\n",
               data->counter, data->message);
    }

    // Cleanup
    munmap(data, SHM_SIZE);
    shm_unlink(SHM_NAME);
    return 0;
}
// Compile: gcc -o shm shm.c -lrt
''',

    # --- Socket Programming ---
    '''
// TCP Server in C - accepts connections and echoes messages
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];

    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket failed");
        exit(1);
    }

    // Allow port reuse
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // Bind to address
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed");
        exit(1);
    }

    // Listen for connections
    if (listen(server_fd, 5) < 0) {
        perror("listen failed");
        exit(1);
    }

    printf("Server listening on port %d...\\n", PORT);

    // Accept a connection
    client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
    if (client_fd < 0) {
        perror("accept failed");
        exit(1);
    }

    printf("Client connected: %s:%d\\n",
           inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

    // Echo loop
    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        int bytes_read = read(client_fd, buffer, BUFFER_SIZE - 1);
        if (bytes_read <= 0) break;

        printf("Received: %s", buffer);
        write(client_fd, buffer, bytes_read);  // Echo back
    }

    close(client_fd);
    close(server_fd);
    return 0;
}
''',
    '''
// TCP Client in C - connects to server and sends messages
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int sock_fd;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];

    // Create socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("socket failed");
        exit(1);
    }

    // Server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    // Connect to server
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect failed");
        exit(1);
    }

    printf("Connected to server. Type messages (Ctrl+D to quit):\\n");

    // Send messages
    while (fgets(buffer, BUFFER_SIZE, stdin) != NULL) {
        write(sock_fd, buffer, strlen(buffer));

        // Read echo response
        memset(buffer, 0, BUFFER_SIZE);
        int bytes_read = read(sock_fd, buffer, BUFFER_SIZE - 1);
        if (bytes_read > 0) {
            printf("Server echo: %s", buffer);
        }
    }

    close(sock_fd);
    return 0;
}
''',
    '''
// UDP Server and Client in C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9090
#define BUFFER_SIZE 1024

// UDP Server
void udp_server() {
    int sock_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];

    sock_fd = socket(AF_INET, SOCK_DGRAM, 0);

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    bind(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    printf("UDP Server listening on port %d...\\n", PORT);

    while (1) {
        int n = recvfrom(sock_fd, buffer, BUFFER_SIZE - 1, 0,
                         (struct sockaddr *)&client_addr, &client_len);
        buffer[n] = '\\0';
        printf("Received from %s:%d: %s\\n",
               inet_ntoa(client_addr.sin_addr),
               ntohs(client_addr.sin_port), buffer);

        // Send response
        sendto(sock_fd, buffer, n, 0,
               (struct sockaddr *)&client_addr, client_len);
    }

    close(sock_fd);
}

// UDP Client
void udp_client() {
    int sock_fd;
    struct sockaddr_in server_addr;
    socklen_t server_len = sizeof(server_addr);
    char buffer[BUFFER_SIZE];

    sock_fd = socket(AF_INET, SOCK_DGRAM, 0);

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    const char *message = "Hello UDP Server!";
    sendto(sock_fd, message, strlen(message), 0,
           (struct sockaddr *)&server_addr, sizeof(server_addr));

    int n = recvfrom(sock_fd, buffer, BUFFER_SIZE - 1, 0,
                     (struct sockaddr *)&server_addr, &server_len);
    buffer[n] = '\\0';
    printf("Server response: %s\\n", buffer);

    close(sock_fd);
}

int main(int argc, char *argv[]) {
    if (argc > 1 && strcmp(argv[1], "client") == 0) {
        udp_client();
    } else {
        udp_server();
    }
    return 0;
}
''',

    # --- Memory Management ---
    '''
// Dynamic memory allocation in C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    // malloc - allocate uninitialized memory
    int *arr = (int *)malloc(5 * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "malloc failed\\n");
        exit(1);
    }

    // Initialize and use
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
    }

    printf("malloc array: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");

    // realloc - resize allocated memory
    arr = (int *)realloc(arr, 10 * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "realloc failed\\n");
        exit(1);
    }

    for (int i = 5; i < 10; i++) {
        arr[i] = i * 10;
    }

    printf("realloc array: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");

    free(arr);  // Always free allocated memory

    // calloc - allocate zero-initialized memory
    int *zeros = (int *)calloc(5, sizeof(int));
    printf("calloc array: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", zeros[i]);  // All zeros
    }
    printf("\\n");
    free(zeros);

    // Dynamic string
    char *str = (char *)malloc(50 * sizeof(char));
    strcpy(str, "Hello, dynamic memory!");
    printf("String: %s\\n", str);
    free(str);

    return 0;
}
''',
    '''
// Linked list with dynamic memory in C
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node *create_node(int data) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (new_node == NULL) {
        fprintf(stderr, "Memory allocation failed\\n");
        exit(1);
    }
    new_node->data = data;
    new_node->next = NULL;
    return new_node;
}

void append(Node **head, int data) {
    Node *new_node = create_node(data);
    if (*head == NULL) {
        *head = new_node;
        return;
    }
    Node *current = *head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
}

void print_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\\n");
}

void free_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        Node *temp = current;
        current = current->next;
        free(temp);
    }
}

int main() {
    Node *head = NULL;

    append(&head, 10);
    append(&head, 20);
    append(&head, 30);
    append(&head, 40);

    printf("Linked list: ");
    print_list(head);

    free_list(head);  // Prevent memory leak
    return 0;
}
''',

    # --- File I/O in C ---
    '''
// File operations using file descriptors (low-level I/O)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>

int main() {
    // Open file for writing (create if not exists)
    int fd = open("test_output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open for write");
        exit(1);
    }

    // Write to file
    const char *text = "Hello from low-level I/O!\\nLine 2\\nLine 3\\n";
    ssize_t bytes_written = write(fd, text, strlen(text));
    printf("Wrote %zd bytes\\n", bytes_written);
    close(fd);

    // Open file for reading
    fd = open("test_output.txt", O_RDONLY);
    if (fd < 0) {
        perror("open for read");
        exit(1);
    }

    // Read from file
    char buffer[256];
    ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
    buffer[bytes_read] = '\\0';
    printf("Read %zd bytes:\\n%s", bytes_read, buffer);

    // Get file info with stat
    struct stat file_stat;
    fstat(fd, &file_stat);
    printf("File size: %ld bytes\\n", file_stat.st_size);
    printf("Permissions: %o\\n", file_stat.st_mode & 0777);

    // Seek to beginning
    lseek(fd, 0, SEEK_SET);

    close(fd);
    return 0;
}
''',

    # --- Named Pipe (FIFO) ---
    '''
// Named pipe (FIFO) for IPC between unrelated processes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/wait.h>

#define FIFO_PATH "/tmp/my_fifo"
#define BUFFER_SIZE 256

int main() {
    // Create named pipe (FIFO)
    mkfifo(FIFO_PATH, 0666);

    pid_t pid = fork();

    if (pid == 0) {
        // Child: Writer
        int fd = open(FIFO_PATH, O_WRONLY);
        const char *messages[] = {
            "Message 1 from writer",
            "Message 2 from writer",
            "DONE"
        };

        for (int i = 0; i < 3; i++) {
            write(fd, messages[i], strlen(messages[i]) + 1);
            printf("Writer sent: %s\\n", messages[i]);
            sleep(1);
        }

        close(fd);
        exit(0);
    } else {
        // Parent: Reader
        int fd = open(FIFO_PATH, O_RDONLY);
        char buffer[BUFFER_SIZE];

        while (1) {
            int n = read(fd, buffer, BUFFER_SIZE);
            if (n <= 0) break;
            printf("Reader received: %s\\n", buffer);
            if (strcmp(buffer, "DONE") == 0) break;
        }

        close(fd);
        waitpid(pid, NULL, 0);
        unlink(FIFO_PATH);  // Remove the FIFO
    }

    return 0;
}
''',

    # --- Makefile ---
    '''
// Makefile for C projects with multiple source files
// Save this as "Makefile" (no extension)
//
// CC = gcc
// CFLAGS = -Wall -Wextra -g -pthread
// LDFLAGS = -lpthread -lrt
//
// # Source files
// SRCS = main.c utils.c network.c
// OBJS = $(SRCS:.c=.o)
// TARGET = myprogram
//
// # Default target
// all: $(TARGET)
//
// # Link object files
// $(TARGET): $(OBJS)
// 	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)
//
// # Compile source files
// %.o: %.c
// 	$(CC) $(CFLAGS) -c $< -o $@
//
// # Clean build files
// clean:
// 	rm -f $(OBJS) $(TARGET)
//
// # Run the program
// run: $(TARGET)
// 	./$(TARGET)
//
// .PHONY: all clean run

// Example compilation commands:
// gcc -Wall -o program main.c              # Single file
// gcc -Wall -o program main.c utils.c      # Multiple files
// gcc -Wall -c main.c                      # Compile only (no link)
// gcc -Wall -o program main.o utils.o      # Link object files
// gcc -Wall -o threads threads.c -lpthread # With pthread library
// gcc -Wall -g -o debug program.c          # With debug symbols
''',

    # --- Thread Barrier ---
    '''
// Barrier - synchronize multiple threads at a point
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_THREADS 4

pthread_barrier_t barrier;

void *worker(void *arg) {
    int id = *(int *)arg;

    // Phase 1: Each thread does independent work
    printf("Thread %d: Phase 1 - doing independent work\\n", id);
    sleep(rand() % 3 + 1);
    printf("Thread %d: Phase 1 complete, waiting at barrier\\n", id);

    // All threads wait here until everyone arrives
    pthread_barrier_wait(&barrier);

    // Phase 2: All threads proceed together
    printf("Thread %d: Phase 2 - all threads synchronized!\\n", id);

    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    srand(time(NULL));

    // Initialize barrier for NUM_THREADS threads
    pthread_barrier_init(&barrier, NULL, NUM_THREADS);

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_barrier_destroy(&barrier);
    printf("All phases complete.\\n");
    return 0;
}
// Compile: gcc -o barrier barrier.c -lpthread
''',
]
