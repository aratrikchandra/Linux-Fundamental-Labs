#!/bin/bash

# Create dummy processes
for i in {1..5}; do
    sleep 86400 &
done
