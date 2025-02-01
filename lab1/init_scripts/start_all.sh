#!/bin/bash

# Run Python, C, and master processes as root
/home/labuser/init_scripts/start_python.sh
/home/labuser/init_scripts/start_c.sh
python3 /home/labuser/init_scripts/master.py &