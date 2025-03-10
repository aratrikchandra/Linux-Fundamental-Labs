#!/bin/bash

# Step 3: Create a new tar archive with fold1, fold2, and readme.txt using different compression methods
tar -czf file.tgz fold1 fold2 readme.txt

tar -cjf file.tar.bz2 fold1 fold2 readme.txt

tar -cJf file.tar.xz fold1 fold2 readme.txt