#!/bin/bash

# Database credentials
DB_USER="postgresdb"
DB_NAME="postgresdb"
DB_PASSWORD="postgresdb"

# Directories for SQL files and output
SQL_DIR="/home/pgsql_explain/sql_files"
OUTPUT_DIR="/home/pgsql_explain/sql_files/output/pgsql_queries_explain/cleansed_json_files"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Loop through all .sql files in the SQL directory
for sql_file in "$SQL_DIR"/*.sql; do
    # Extract the base filename without path and extension
    base_name=$(basename "$sql_file" .sql)
    output_file="$OUTPUT_DIR/${base_name}_explain_verbose_analyze_format_json_cleansed"

    # Check if the SQL file is empty and skip it
    if [[ ! -s "$sql_file" ]]; then
        continue
    fi

    echo "Processing: $sql_file -> $output_file"

    # Execute EXPLAIN and save the JSON result to a file (Suppress all output)
    PGPASSWORD="$DB_PASSWORD" psql -U "$DB_USER" -d "$DB_NAME" -q <<EOF > /dev/null
\pset format unaligned
\pset tuples_only on
EXPLAIN (VERBOSE, ANALYZE, FORMAT JSON) $(cat "$sql_file")
\g $output_file
EOF

done
