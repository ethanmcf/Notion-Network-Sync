#!/bin/bash

PYTHON_SCRIPT=$1
SERVICE_NAME=$2

python3 src/common/ran_previously_check.py "$SERVICE_NAME"
exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo "Run recently $PYTHON_SCRIPT. Skipping."
else
  echo "Running $PYTHON_SCRIPT..."
  python "$PYTHON_SCRIPT"
fi