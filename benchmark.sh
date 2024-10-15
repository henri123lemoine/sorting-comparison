#!/bin/bash

echo "Compiling Rust implementation..."
cargo build --release

echo "n,Python Merge Sort (s),Rust Bogo Sort (s)"

for n in {1..12}; do
    # Generate random numbers
    numbers=$(python -c "import random; print(' '.join(str(random.randint(0, 1000)) for _ in range($n)))")
    
    # Run Python merge sort
    python_time=$(TIMEFORMAT='%R'; { time echo "$numbers" | uv run src/merge_sort.py $n > /dev/null; } 2>&1)
    
    # Run Rust bogo sort
    rust_time=$(TIMEFORMAT='%R'; { time echo "$numbers" | ./target/release/bogo_sort > /dev/null; } 2>&1)
    
    echo "$n,$python_time,$rust_time"
    
    # Break if Rust bogo sort takes more than 5 seconds
    if (( $(echo "$rust_time > 5" | bc -l) )); then
        break
    fi
done
