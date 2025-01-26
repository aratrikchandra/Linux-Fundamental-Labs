#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    for (int i = 0; i < 3; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            // This is the child process
            // printf("Child process %d with PID %d\n", i + 1, getpid());
            sleep(86400);  // Keep the child process alive for 24 hours
            return 0;
        } else if (pid > 0) {
            // This is the parent process
            // printf("Created child process %d with PID %d\n", i + 1, pid);
        } else {
            // Fork failed
            // fprintf(stderr, "Fork failed\n");
            return 1;
        }
    }

    // Wait for all child processes to finish
    for (int i = 0; i < 3; i++) {
        wait(NULL);
    }

    return 0;
}
