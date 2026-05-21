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

    # --- System V Semaphores (Lab 8 style) ---
    '''
// System V Semaphore - semget semctl semop - setup, producer, consumer
// Donut shop model: semaphore tracks available resources
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <errno.h>

#define SEMKEY 456
#define PLAIN 0
#define CHOC  1
#define SHUG  2

// Must define this union yourself on Linux
union semun {
    int              val;
    struct semid_ds *buf;
    unsigned short  *array;
    struct seminfo  *__buf;
};

// Setup: create and initialize semaphore set
void sem_setup() {
    int sem_id;
    union semun arg;
    unsigned short dcount[3];

    // Create set of 3 semaphores
    sem_id = semget(SEMKEY, 3, IPC_CREAT | IPC_EXCL | 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    // Set initial values (available resources)
    dcount[PLAIN] = 2;    // 2 plain donuts
    dcount[CHOC]  = 3;    // 3 chocolate donuts
    dcount[SHUG]  = 4;    // 4 sugar donuts
    arg.array = dcount;

    // SETALL = set all semaphores at once
    if (semctl(sem_id, 0, SETALL, arg) == -1) {
        perror("semctl SETALL"); exit(1);
    }
    printf("Semaphore set created. ID=%d\\n", sem_id);
    printf("Initial: Plain=%d, Choc=%d, Sugar=%d\\n",
           dcount[PLAIN], dcount[CHOC], dcount[SHUG]);
}

// Producer: add resources (V operation = positive sem_op)
void producer() {
    struct sembuf sops[3];
    union semun arg;
    unsigned short dcount[3];

    int sem_id = semget(SEMKEY, 3, 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    // Read current values
    arg.array = dcount;
    semctl(sem_id, 0, GETALL, arg);
    printf("Before produce: Plain=%d, Choc=%d, Sugar=%d\\n",
           dcount[PLAIN], dcount[CHOC], dcount[SHUG]);

    // V operation: POSITIVE sem_op = release/produce
    sops[0].sem_num = PLAIN; sops[0].sem_op = 2; sops[0].sem_flg = 0;
    sops[1].sem_num = CHOC;  sops[1].sem_op = 3; sops[1].sem_flg = 0;
    sops[2].sem_num = SHUG;  sops[2].sem_op = 4; sops[2].sem_flg = 0;

    if (semop(sem_id, sops, 3) == -1) { perror("semop"); exit(1); }
    printf("Produced donuts!\\n");
}

// Consumer: take resources (P operation = negative sem_op)
void consumer() {
    struct sembuf sops[3];
    union semun arg;
    unsigned short dcount[3];

    int sem_id = semget(SEMKEY, 3, 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    // Read current values
    arg.array = dcount;
    semctl(sem_id, 0, GETALL, arg);
    printf("Available: Plain=%d, Choc=%d, Sugar=%d\\n",
           dcount[PLAIN], dcount[CHOC], dcount[SHUG]);

    // P operation: NEGATIVE sem_op = acquire/consume
    // Blocks if not enough resources available
    sops[0].sem_num = PLAIN; sops[0].sem_op = -1; sops[0].sem_flg = 0;
    sops[1].sem_num = CHOC;  sops[1].sem_op = -1; sops[1].sem_flg = 0;
    sops[2].sem_num = SHUG;  sops[2].sem_op = -1; sops[2].sem_flg = 0;

    printf("Waiting for resources (blocks if not enough)...\\n");
    if (semop(sem_id, sops, 3) == -1) { perror("semop"); exit(1); }
    printf("Got my donuts!\\n");
}

// Cleanup: delete semaphore set
void sem_cleanup() {
    int sem_id = semget(SEMKEY, 3, 0666);
    semctl(sem_id, 0, IPC_RMID);
    printf("Semaphore set deleted.\\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s [setup|produce|consume|cleanup]\\n", argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "setup") == 0)   sem_setup();
    else if (strcmp(argv[1], "produce") == 0) producer();
    else if (strcmp(argv[1], "consume") == 0) consumer();
    else if (strcmp(argv[1], "cleanup") == 0) sem_cleanup();
    return 0;
}
// Compile: gcc -o donut donut.c
// Run: ./donut setup && ./donut produce && ./donut consume && ./donut cleanup
''',
    '''
// System V Shared Memory - shmget shmat shmdt shmctl - writer and reader
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include <sys/time.h>

#define PERM (S_IRUSR | S_IWUSR | IPC_CREAT)

// Writer: creates shared memory and writes data
void writer() {
    key_t key = ftok("/etc/passwd", 5);
    int id = shmget(key, 100, PERM);
    if (id == -1) { perror("shmget"); exit(1); }

    // Attach shared memory - get pointer
    char *cptr = (char *)shmat(id, NULL, 0);
    if (cptr == (char *)-1) { perror("shmat"); exit(1); }

    struct timeval tv;
    for (int i = 0; i < 5; i++) {
        gettimeofday(&tv, NULL);
        sprintf(cptr, "Time: %ld.%06ld (write #%d)",
                tv.tv_sec, tv.tv_usec, i + 1);
        printf("Writer wrote: %s\\n", cptr);
        sleep(3);
    }

    // Detach and delete
    shmdt(cptr);
    shmctl(id, IPC_RMID, NULL);
    printf("Shared memory deleted.\\n");
}

// Reader: attaches to existing shared memory and reads
void reader() {
    key_t key = ftok("/etc/passwd", 5);  // SAME key = SAME segment
    int id = shmget(key, 100, PERM);
    if (id == -1) { perror("shmget"); exit(1); }

    char *cptr = (char *)shmat(id, NULL, 0);
    if (cptr == (char *)-1) { perror("shmat"); exit(1); }

    for (int i = 0; i < 5; i++) {
        printf("Reader read: %s\\n", cptr);
        sleep(3);
    }

    shmdt(cptr);  // Detach only, don't delete (writer does that)
}

int main(int argc, char *argv[]) {
    if (argc > 1 && strcmp(argv[1], "read") == 0)
        reader();
    else
        writer();
    return 0;
}
// Compile: gcc -o shmem shmem.c
// Run in two terminals: ./shmem write  AND  ./shmem read
''',
    '''
// System V Message Queue - msgget msgsnd msgrcv msgctl - complete example
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/wait.h>

// Message struct: mtype MUST be first field and MUST be > 0
struct msg {
    long type;      // MUST be first, MUST be > 0
    int  pid;       // sender's PID
    int  sum;       // data payload
};

int main(void) {
    // Create message queue (IPC_PRIVATE = unique key)
    int msgid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    if (msgid == -1) { perror("msgget"); return 1; }
    printf("Message queue created: ID=%d\\n", msgid);

    pid_t pid = fork();

    if (pid == 0) {
        // CHILD: send a message
        struct msg m;
        m.type = 1;              // type must be > 0
        m.pid  = getpid();
        m.sum  = 42;

        // msgsnd: size = total struct size MINUS the long mtype
        msgsnd(msgid, &m, sizeof(m) - sizeof(long), 0);
        printf("Child %d sent: sum=%d\\n", m.pid, m.sum);
        exit(0);
    }

    // PARENT: wait for child, then receive message
    wait(NULL);

    struct msg m;
    // msgrcv: type=1 means receive messages with mtype==1
    // type=0 means receive ANY message
    msgrcv(msgid, &m, sizeof(m) - sizeof(long), 1, 0);
    printf("Parent received from PID %d: sum=%d\\n", m.pid, m.sum);

    // CLEANUP: always delete the queue when done
    msgctl(msgid, IPC_RMID, NULL);
    printf("Message queue deleted.\\n");
    return 0;
}
// Compile: gcc -o msgq msgq.c
''',
    '''
// LT2 Complete Solution - pipe + fork 4 children + message queue
// Parent writes 40 random numbers to pipe, forks 4 children
// Each child reads 10 numbers, computes sum, sends via message queue
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
    printf("Parent PID %ld writing 40 numbers to pipe:\\n", (long)getpid());
    for (int i = 0; i < 40; i++) {
        numbers[i] = rand() % 100;
        total_sum += numbers[i];
        printf("%d ", numbers[i]);
    }
    printf("\\nTotal sum = %d\\n", total_sum);

    // 3. Write all 40 numbers to pipe
    write(pipefd[1], numbers, sizeof(numbers));
    close(pipefd[1]);  // close write end

    // 4. Fork 4 children
    for (int i = 0; i < 4; i++) {
        if (fork() == 0) {
            // CHILD: read 10 numbers from pipe
            int arr[10];
            read(pipefd[0], arr, sizeof(arr));

            int sum = 0;
            for (int j = 0; j < 10; j++) sum += arr[j];

            // Send result via message queue
            struct msg m;
            m.type = 1;
            m.pid  = getpid();
            m.sum  = sum;
            msgsnd(msgid, &m, sizeof(m) - sizeof(long), 0);
            printf("Child %d: sum of my 10 numbers = %d\\n", getpid(), sum);
            exit(0);
        }
    }
    close(pipefd[0]);  // parent done reading

    // 5. Receive 4 messages from children
    printf("\\nParent receiving messages:\\n");
    for (int i = 0; i < 4; i++) {
        struct msg m;
        msgrcv(msgid, &m, sizeof(m) - sizeof(long), 1, 0);
        printf("  From PID %d: sum = %d\\n", m.pid, m.sum);
    }

    // 6. Wait for all children
    for (int i = 0; i < 4; i++) wait(NULL);

    // 7. Cleanup
    msgctl(msgid, IPC_RMID, NULL);
    printf("All children done. Queue cleaned up.\\n");
    return 0;
}
// Compile: gcc -o lt2 lt2.c
''',
    '''
// dup2 - Redirect stdout to a file in C
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

#define FLAGS (O_WRONLY | O_CREAT | O_APPEND)
#define MODE  (S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)

int main(void) {
    // Open file for writing
    int fd = open("output.txt", FLAGS, MODE);
    if (fd == -1) { perror("open"); return 1; }

    // dup2: make STDOUT point to the file
    // After this, anything written to STDOUT goes to output.txt
    dup2(fd, STDOUT_FILENO);
    close(fd);  // close raw fd (STDOUT already wired to file)

    // These now write to output.txt, NOT the terminal
    printf("This goes to the file!\\n");
    write(STDOUT_FILENO, "So does this\\n", 13);

    return 0;
}
// Compile: gcc -o redirect redirect.c
// Run: ./redirect && cat output.txt
''',
    '''
// fork fan topology - one parent creates multiple children
// Child breaks out of loop, parent continues forking
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    int n = 4;  // number of children
    pid_t childpid = 0;

    // Fan: child breaks, parent continues loop
    for (int i = 1; i < n; i++) {
        if ((childpid = fork()) <= 0)
            break;  // child (0) or error (-1) breaks out
    }

    if (childpid == 0) {
        // I am a CHILD
        printf("Child: PID=%ld, Parent=%ld\\n", (long)getpid(), (long)getppid());
    } else {
        // I am the PARENT (finished forking all children)
        printf("Parent: PID=%ld, created %d children\\n", (long)getpid(), n - 1);
        // Wait for all children
        for (int i = 1; i < n; i++)
            wait(NULL);
        printf("Parent: All children finished\\n");
    }
    return 0;
}
''',
    '''
// fork chain topology - each process creates the next
// Parent breaks out of loop, child continues
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    int n = 4;  // chain length
    pid_t childpid;

    // Chain: parent breaks, child continues loop
    for (int i = 1; i < n; i++) {
        if ((childpid = fork()))
            break;  // parent (non-zero) breaks out
        // child (0) continues the loop, becoming next parent
    }

    printf("Process %ld (parent %ld) in chain\\n",
           (long)getpid(), (long)getppid());

    if (childpid > 0) {
        // I forked a child, wait for it
        wait(NULL);
    }
    return 0;
}
''',
    '''
// FIFO named pipe - mkfifo parent child communication
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>

#define FIFO_PERM (S_IRUSR | S_IWUSR)

int main(int argc, char *argv[]) {
    char *fifo_name = "myfifo";

    // Create FIFO (named pipe) on filesystem
    if (mkfifo(fifo_name, FIFO_PERM) == -1 && errno != EEXIST) {
        perror("mkfifo"); return 1;
    }

    pid_t pid = fork();
    if (pid == -1) { perror("fork"); return 1; }

    if (pid == 0) {
        // CHILD: write to FIFO
        int fd;
        // Retry open if interrupted by signal
        while ((fd = open(fifo_name, O_WRONLY)) == -1 && errno == EINTR);
        char buf[256];
        snprintf(buf, sizeof(buf), "[PID %ld]: Hello from child!\\n", (long)getpid());
        write(fd, buf, strlen(buf) + 1);
        close(fd);
        return 0;
    } else {
        // PARENT: read from FIFO
        int fd;
        while ((fd = open(fifo_name, O_RDONLY)) == -1 && errno == EINTR);
        char buf[256];
        read(fd, buf, sizeof(buf));
        printf("Parent read: %s\\n", buf);
        close(fd);
        wait(NULL);
        unlink(fifo_name);  // Remove FIFO from filesystem
    }
    return 0;
}
// Compile: gcc -o fifo_demo fifo_demo.c
''',
    '''
// Concurrent socket server - fork per client pattern
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/wait.h>

int main(void) {
    int listenfd, connfd;
    struct sockaddr_in serv_addr;

    // 1. Create TCP socket
    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd < 0) { perror("socket"); return 1; }

    // 2. Setup address
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(5000);

    // 3. Bind
    if (bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("bind"); return 1;
    }

    // 4. Listen (queue up to 10 pending connections)
    listen(listenfd, 10);
    printf("Server listening on port 5000...\\n");

    while (1) {
        // 5. Accept (blocks until client connects)
        connfd = accept(listenfd, NULL, NULL);
        printf("New client connected!\\n");

        // 6. Fork child to handle this client
        pid_t pid = fork();
        if (pid == 0) {
            // CHILD: handle client
            close(listenfd);  // child doesn't need listener

            char buffer[1024] = {0};
            read(connfd, buffer, sizeof(buffer));
            printf("Client says: %s\\n", buffer);

            char *reply = "Hello from server!";
            write(connfd, reply, strlen(reply));

            close(connfd);
            exit(0);  // child exits after serving
        }

        // PARENT: close client fd (child handles it)
        close(connfd);
        // Reap zombie children
        waitpid(-1, NULL, WNOHANG);
    }
    return 0;
}
// Compile: gcc -o server server.c
''',
]
