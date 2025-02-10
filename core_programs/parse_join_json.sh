#!/bin/bash

# Input and output directories

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
SQL_DIR="$PARENT_DIR/cleansed_json_files"
OUTPUT_DIR="$PARENT_DIR/parsed_join_json_files"
LOG_FILE="$PARENT_DIR/logs/parse_join_json_logs"

echo "$SCRIPT_DIR"
echo "$PARENT_DIR"
echo "$SQL_DIR"
echo "$OUTPUT_DIR"

# Ensure the output directory exists
#mkdir -p "$OUTPUT_DIR"

# Loop through JSON files
for json_file in "$SQL_DIR"/*format_json_cleansed; do
    # Extract filename without path
    base_name=$(basename "$json_file")

    # Extract the part before the first underscore "_"
    prefix="${base_name%%_*}"

    # Define output file path
    output_file="$OUTPUT_DIR/${prefix}_join.json"

    echo "Processing: $json_file -> $output_file" | tee -a "$LOG_FILE"

    # Execute Python script and save output to the correct file
    python3 "$SCRIPT_DIR/parse_explain_json_dev.py" "$json_file" > "$output_file" 2>&1 | tee -a "$LOG_FILE"
#    echo "$SCRIPT_DIR/parse_explain_json_dev.py"
#    echo "$json_file"
#    exit
done

echo "All JSON files have been processed." | tee -a "$LOG_FILE"