#!/bin/bash
set -euo pipefail

cp "$( dirname -- "${BASH_SOURCE[0]}" )"/../data/result.json $output_value_file
