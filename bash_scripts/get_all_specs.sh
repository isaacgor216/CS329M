#!/bin/bash

# This script parses the riegeli files in the 
# provided dataset to extract the problem specs

# Directory containing the files
input_directory="/home/isaacgor216/CS329M/dm-code_contests"

# Directory where output files will be stored
output_directory="/home/isaacgor216/CS329M/code_contests/problem_specs"

# Ensure output directory exists
mkdir -p "$output_directory"

for file in "$input_directory"/*.riegeli-*
do
    # Extract the base name without the path
    base_name=$(basename "$file")

    # Extract the digits from the file name
    # This assumes the format is always '.riegeli-xxxxx-of-00128'
    digits=$(echo "$base_name" | grep -oP '(?<=.riegeli-)\d+(?=-of-\d+)')

    # Construct the output filename using the extracted digits
    output_file="$output_directory/${base_name%%.riegeli-*}_specs_${digits}.txt"

    # Store problem name and descriptions in output_file
    bazel run -c opt   :print_names_and_descriptions "$input_directory/$base_name" > "$output_file"
done

