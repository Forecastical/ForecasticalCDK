
capture_output() {
    echo "Directory Structure:"
    tree -L 2

    echo -e "\nFile Contents:"

    find . -type f \( -name "*.py" -o -name "*.txt" -o -name "*.lock" -o -name "*.nix" -o -name "Makefile" \) | while read file; do
        echo -e "\n--- $file ---"
        echo "Location: $(dirname "$file")"
        echo "Contents:"
        cat "$file"
        echo -e "--- End of $file ---\n"
    done
}

# Capture the output and copy it to clipboard
capture_output | tee >(pbcopy)

echo "Output has been copied to clipboard. You can now paste it anywhere."
