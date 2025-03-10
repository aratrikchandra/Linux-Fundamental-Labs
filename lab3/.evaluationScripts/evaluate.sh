#! /bin/bash

# For Testing
INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
# INSTRUCTOR_SCRIPTS="."
LAB_DIRECTORY="../labDirectory"


ptcd=$(pwd)

cd $INSTRUCTOR_SCRIPTS
# echo $ptcd

list_of_files="$(ls $LAB_DIRECTORY)"


cp -r $LAB_DIRECTORY/* autograder/

cd ./autograder/

chmod -R 777 $list_of_files

./grader.sh

rm -r $list_of_files

generated_files=("part1.txt" "part2.txt" "part3.txt" "employees1.txt" "employees2.txt" "employees3.txt" "combined.txt" "deduped.txt" "output.txt")

for item in "${generated_files[@]}"; do
  if [ -e "$item" ]; then
    rm -r "$item"
    echo "Deleted $item"
  fi

cd "$ptcd"
