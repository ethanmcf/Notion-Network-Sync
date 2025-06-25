#!/bin/bash

FLAG_FILE=$1
PYTHON_SCRIPT=$2
NOW=$(date +%s)
TWO_DAYS=$((2 * 24 * 60 * 60))  # seconds in 2 days

if [ -f "$FLAG_FILE" ]; then
    LAST_RUN=$(cat "$FLAG_FILE")
    DIFF=$((NOW - LAST_RUN))

    if [ $DIFF -lt $TWO_DAYS ]; then
        echo "Run recently $PYTHON_SCRIPT. Skipping."
        exit 0
    fi
fi

echo "Running $PYTHON_SCRIPT..."
python "$PYTHON_SCRIPT"

# Update timestamp
date +%s > "$FLAG_FILE"