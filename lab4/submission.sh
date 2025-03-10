#!/bin/bash

# Input file
input_file="data.txt"

# Task 1: Convert all uppercase letters to lowercase
tr '[:upper:]' '[:lower:]' < "$input_file" > lowercase.txt

# Task 2: Delete all digits
tr -d '[:digit:]' < "$input_file" > no_digits.txt

# Task 3: Replace all colons with hyphens
tr ':' '-' < "$input_file" > replace_colons.txt

# Task 4: Squeeze consecutive spaces into a single space
tr -s ' ' < "$input_file" > squeeze_spaces.txt