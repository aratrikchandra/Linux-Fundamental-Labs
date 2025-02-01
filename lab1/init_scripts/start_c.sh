#!/bin/bash

# Create a simple C program
echo '#include <unistd.h>' > simple.c
echo 'int main() { sleep(86400); return 0; }' >> simple.c
gcc simple.c -o simple

# Run the C processes
for i in {1..3}; do
    ./simple &
done
