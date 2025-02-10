#!/bin/bash

# Input and output directories
SQL_DIR="/home/pgsql_explain/sql_files/output/pgsql_queries_explain/cleansed_json_files"
OUTPUT_DIR="/home/pgsql_explain/sql_files/output/pgsql_queries_explain/parsed_join_json_files"
SCRIPT_DIR="/home/pgsql_explain/sql_files/output/pgsql_queries_explain/core_programs"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Loop through JSON files
for json_file in "$SQL_DIR"/*format_json_cleansed; do
    # Extract filename without path
    base_name=$(basename "$json_file")

    # Extract the part before the first underscore "_"
    prefix="${base_name%%_*}"

    # Define output file path
    output_file="$OUTPUT_DIR/${prefix}_join.json"

    echo "Processing: $json_file -> $output_file"

    # Execute Python script and save output to the correct file
    python "$SCRIPT_DIR/parse_explain_json_dev.py" "$json_file" > "$output_file"

done

echo "All JSON files have been processed."