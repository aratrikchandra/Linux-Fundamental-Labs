#! /bin/bash

LAB_DIRECTORY="labDirectory"

if [ -d "$LAB_DIRECTORY" ]; then
  list_of_files="$(ls $LAB_DIRECTORY | grep '\.sh$')"
  echo $list_of_files
else
  echo "Directory $LAB_DIRECTORY does not exist."
fi
