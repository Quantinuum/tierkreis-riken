#!/usr/bin/env bash


# Currently we want the file name as output not passing the contents
#cp -pr FCIDUMP $output_value_file
TRK_BASE_DIR=~/.tierkreis/checkpoints

worker_call_args_file=$1

function_name=$(jq -r ".function_name" $TRK_BASE_DIR/$worker_call_args_file)
done_path=$(jq -r ".done_path" $TRK_BASE_DIR/$worker_call_args_file)
logs_path=$(jq -r ".logs_path" $TRK_BASE_DIR/$worker_call_args_file)
output_dir=$(jq -r ".output_dir" $TRK_BASE_DIR/$worker_call_args_file)

output_value_file=$(jq -r ".outputs.value" $TRK_BASE_DIR/$worker_call_args_file)
#source ./cnt.sh
echo "$(pwd)/FCIDUMP" >> $TRK_BASE_DIR/$output_value_file

touch $TRK_BASE_DIR/$done_path
