#!/bin/bash

# This script iterates over every spec in the training set
# (stored in $source_directory) and runs the llm_pipeline 
# program to generate the test cases for each file, storing them 
# in $output_directory

# Directory containing the problem spec files in appropriate format
# TODO: make this yours
source_directory="/home/isaacgor216/CS329M/code_contests/problem_specs"

# Path to your Python script
generation_script="/home/isaacgor216/CS329M/code_contests/llm_pipeline.py"

# Directory where the generated test cases will be stored
# TODO: make this yours
output_directory="/home/isaacgor216/CS329M/code_contests/llm_generation"

# Loop through each file in the directory
for file in "$source_directory"/code_contests_*_specs_*.txt;
do
    # Check if file is a regular file (and not a directory)
    if [ -f "$file" ]
    then
		filename=$(basename "$file")
		
		regex="code_contests_([^_]+)_specs_([^\.]+)\.txt"

		if [[ $filename =~ $regex ]]; then
	
			category="${BASH_REMATCH[1]}"
			num="${BASH_REMATCH[2]}"

			# Create new filename (train_num.txt)
			new_filename="${category}_${num}.txt"

			# Path for the new file
			new_file_path="${output_directory}/${new_filename}"

			if [ -f $new_file_path ]; then
				echo "Skipping $new_file_path: File already exists"
				continue
			fi

			echo "$filename > $new_file_path"
			python3 "$generation_script" "$file" "$new_file_path"
		fi
    fi
done



