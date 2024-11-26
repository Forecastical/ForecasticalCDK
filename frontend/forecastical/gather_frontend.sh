#!/bin/bash

# Create a temporary file to store all contents
temp_file=$(mktemp)

echo "=== Frontend Contents Report ===" > "$temp_file"
echo "Generated on $(date)" >> "$temp_file"
echo "" >> "$temp_file"

# Function to add file contents with header
add_file_contents() {
    local file=$1
    echo "======================================" >> "$temp_file"
    echo "File: $file" >> "$temp_file"
    echo "======================================" >> "$temp_file"
    echo "" >> "$temp_file"
    cat "$file" >> "$temp_file"
    echo "" >> "$temp_file"
    echo "" >> "$temp_file"
}

# Find and process Vue components
echo "Processing Vue components..."
find . -name "*.vue" -type f | while read -r file; do
    add_file_contents "$file"
done

# Find and process JavaScript files
echo "Processing JavaScript files..."
find . -name "*.js" -type f ! -path "./node_modules/*" | while read -r file; do
    add_file_contents "$file"
done


# Copy to clipboard using pbcopy
cat "$temp_file" | pbcopy

# Clean up
rm "$temp_file"

echo "Contents have been copied to clipboard!"
echo "Files processed:"
echo "- Vue components: $(find . -name "*.vue" -type f | wc -l)"
echo "- JavaScript files: $(find . -name "*.js" -type f ! -path "./node_modules/*" | wc -l)"
