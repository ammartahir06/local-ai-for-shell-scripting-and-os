# 🔵 SOCKET PROGRAMMING (Lab 9) — Quick Exam Guide
### Priority #8 — (Unlikely to be the main focus, but good to know)

---

## 1. THE SOCKET WORKFLOW

Socket programming allows two unrelated processes (even on different computers) to communicate over a network using IP addresses and ports.

**The Server (The Restaurant):**
1. `socket()` — Build the restaurant.
2. `bind()` — Assign the restaurant an address (Port number).
3. `listen()` — Open the doors and wait for customers.
4. `accept()` — A customer arrives, give them a dedicated waiter (a new file descriptor).
5. `read()` / `write()` — Take their order and serve food.

**The Client (The Customer):**
1. `socket()` — Get a phone.
2. `connect()` — Dial the restaurant's address and port.
3. `write()` / `read()` — Place order and receive food.

---

## 2. KEY STRUCTURES TO REMEMBER

To use sockets, you must include these headers:
```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
```

The Address Structure (You must fill this out to bind or connect):
```c
struct sockaddr_in serv_addr;
serv_addr.sin_family = AF_INET;                     // Always AF_INET for IPv4
serv_addr.sin_port = htons(8080);                   // Port (htons = host to network short)
serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // IP Address (Localhost)
```

---

## 3. THE CONCURRENT SERVER PATTERN (Lab 9 focus)

In a concurrent server, the main server loop just waits for clients to connect. When a client connects, it `fork()`s a child process to handle that specific client, while the parent goes back to waiting for the next client.

### Concurrent Server Code (server2.c style)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void) {
    int listenfd, connfd;
    struct sockaddr_in serv_addr;

    // 1. Create Socket (TCP)
    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd < 0) { perror("Socket failed"); return 1; }

    // 2. Setup Address Structure
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); // Accept connections on any IP
    serv_addr.sin_port = htons(5000);              // Port 5000

    // 3. Bind the socket to the port
    if (bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Bind failed"); return 1;
    }

    // 4. Listen for incoming connections (max queue size 10)
    listen(listenfd, 10);
    printf("Server listening on port 5000...\n");

    while(1) {
        // 5. Accept a connection (BLOCKS until a client connects)
        connfd = accept(listenfd, (struct sockaddr*)NULL, NULL);
        printf("New client connected!\n");

        // 6. Fork a child to handle the client
        pid_t pid = fork();

        if (pid == 0) {
            // --- CHILD PROCESS ---
            close(listenfd); // Child doesn't need to listen for new clients
            
            char buffer[1024] = {0};
            // Read message from client
            read(connfd, buffer, sizeof(buffer));
            printf("Client says: %s\n", buffer);
            
            // Send response
            char *msg = "Hello from concurrent server!";
            write(connfd, msg, strlen(msg));
            
            close(connfd); // Close connection for this client
            exit(0);       // Child dies after serving the client
        }
        
        // --- PARENT PROCESS ---
        close(connfd); // Parent doesn't talk to the client, the child is doing it
        // Loop goes back up to accept() the next client
    }
    
    return 0;
}
```

---

## 4. THE CLIENT CODE

```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void) {
    int sockfd;
    struct sockaddr_in serv_addr;

    // 1. Create Socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    // 2. Setup the server address you want to connect TO
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(5000);
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // Localhost

    // 3. Connect to the server
    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed"); return 1;
    }

    // 4. Talk to server
    char *hello = "Hello from client";
    write(sockfd, hello, strlen(hello));
    
    char buffer[1024] = {0};
    read(sockfd, buffer, sizeof(buffer));
    printf("Server replied: %s\n", buffer);

    close(sockfd);
    return 0;
}
```

## Quick Cheat Sheet

**Server Side:** `socket()` → `bind()` → `listen()` → `accept()` → `read()/write()`
**Client Side:** `socket()` → `connect()` → `write()/read()`

**Important functions to remember:**
*   `htons(PORT)`: "Host TO Network Short" - converts your port number to the network's byte order.
*   `inet_addr("IP_STRING")`: Converts a string IP like "127.0.0.1" into the binary format the struct expects.
