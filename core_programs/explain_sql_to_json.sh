#!/bin/bash

# PostgreSQL configuration
DB_NAME="postgresdb"
DB_USER="postgresdb"
SQL_DIR="/home/pgsql_explain/sql_files"
OUTPUT_DIR="/home/pgsql_explain/sql_files/output"
DB_PASSWORD="postgresdb"

export PGPASSWORD=$DB_PASSWORD

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Loop through all SQL files in the directory
for sql_file in "$SQL_DIR"/*.sql
do
  # Get base name of SQL file
  base_name=$(basename "$sql_file" .sql)

  # Define output file path
  output_file="$OUTPUT_DIR/${base_name}_explain.json"

  echo "Processing $sql_file and saving result to $output_file..."

  # Run EXPLAIN and save output
  psql -U "$DB_USER" -d "$DB_NAME" -c "EXPLAIN (VERBOSE, ANALYZE, FORMAT JSON) $(cat $sql_file)" > $output_file

  if [ $? -eq 0 ]; then
    echo "Successfully processed $sql_file."
  else
    echo "Failed to process $sql_file."
  fi
done
