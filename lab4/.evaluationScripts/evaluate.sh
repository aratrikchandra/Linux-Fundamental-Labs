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


# Check and remove Terraform-related files
if [ -f lowercase.txt ]; then
    rm lowercase.txt
fi

if [ -f no_digits.txt ]; then
    rm no_digits.txt
fi

if [ -f replace_colons.txt]; then
    rm replace_colons.txt
fi

if [ -f squeeze_spaces.txt ]; then
    rm squeeze_spaces.txt
fi


cd "$ptcd"
