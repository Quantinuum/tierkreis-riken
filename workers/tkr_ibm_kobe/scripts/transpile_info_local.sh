#!/bin/bash
set -xeuo pipefail

cp $(dirname $0)/../data/config.json $1
cp $(dirname $0)/../data/props.json $2

