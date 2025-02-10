#!/bin/bash

SQL_DIR="/home/pgsql_explain/sql_files/output/pgsql_queries_explain/cleansed_json_files"
OUTPUT_DIR="/home/pgsql_explain/sql_files/output/parsed_join_json_files"

mkdir -p "$OUTPUT_DIR"

for json_file in "$SQL_DIR"/*format_json_cleansed
do
  echo "$json_file"

done

