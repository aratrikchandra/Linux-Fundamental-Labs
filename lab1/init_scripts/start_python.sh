#!/bin/bash

# Create Python processes
for i in {1..2}; do
    python3 -c "import time; time.sleep(86400)" &
done
