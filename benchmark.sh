#!/bin/bash

echo "Compiling Rust script..."
rustc bogo_sort.rs

echo "Running benchmarks..."
echo "n,Python Merge Sort (s),Rust Bogo Sort (s)"

for i in {1..10}; do
    python_time=$(TIMEFORMAT='%3R'; { time uv run src/merge_sort.py $i > /dev/null; } 2>&1)
    rust_time=$(TIMEFORMAT='%3R'; { time ./bogo_sort $i > /dev/null; } 2>&1)
    echo "$i,$python_time,$rust_time"
done
