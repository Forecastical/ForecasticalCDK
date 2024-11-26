#!/bin/bash

# Create a temporary file to store all Python contents
temp_file=$(mktemp)

# Find all .py files recursively starting from current directory
find . -name "*.py" -type f | while read -r file; do
    echo -e "\n### File: $file ###\n" >> "$temp_file"
    cat "$file" >> "$temp_file"
    echo -e "\n\n" >> "$temp_file"
done

# Copy the contents to clipboard
cat "$temp_file" | pbcopy

# Clean up
rm "$temp_file"

echo "All Python files have been copied to your clipboard!"
echo "Found Python files:"
find . -name "*.py" -type f
