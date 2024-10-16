#!/bin/bash

set -e

echo "Compiling Rust implementation..."
cargo build --release > /dev/null 2>&1
compile_time=$(TIMEFORMAT='%R'; { time cargo build --release > /dev/null 2>&1; } 2>&1)
echo "Compile time: $compile_time seconds"

# Function to run benchmarks
run_benchmark() {
    local include_compile_time=$1
    local include_start_time=$2
    local output_file=$3

    echo "Running benchmark: include_compile_time=$include_compile_time, include_start_time=$include_start_time"
    echo "Output file: $output_file"

    echo "n,Python Merge Sort (s),Rust Bogo Sort (s)" > "$output_file"

    for n in {1..7}; do
        echo "Processing n=$n"
        # Generate random numbers
        numbers=$(python -c "import random; print(' '.join(str(random.randint(0, 1000)) for _ in range($n)))")
        
        # Run Python merge sort
        if [ "$include_start_time" = true ]; then
            python_time=$(TIMEFORMAT='%R'; { time python src/merge_sort.py $n <<< "$numbers" > /dev/null; } 2>&1)
        else
            python_time=$(python -c "
import time
from src.merge_sort import merge_sort
numbers = [int(x) for x in '$numbers'.split()]
start = time.time()
merge_sort(numbers)
end = time.time()
print(f'{end - start:.6f}')
")
        fi
        
        # Run Rust bogo sort
        rust_time=$(TIMEFORMAT='%R'; { time ./target/release/bogo_sort <<< "$numbers" > /dev/null; } 2>&1)
        
        if [ "$include_compile_time" = true ]; then
            rust_time=$(awk -v rt="$rust_time" -v ct="$compile_time" 'BEGIN {print rt + ct}')
        fi
        
        echo "$n,$python_time,$rust_time" >> "$output_file"
        
        # Break if Rust bogo sort takes more than 5 seconds
        if (( $(awk -v rt="$rust_time" 'BEGIN {print (rt > 5)}') )); then
            echo "Breaking loop: Rust bogo sort took more than 5 seconds"
            break
        fi
    done

    echo "Benchmark results saved to $output_file"
}

# Run benchmarks for all scenarios
run_benchmark false false "assets/benchmark_no_compile_no_start.csv"
run_benchmark false true "assets/benchmark_no_compile_with_start.csv"
run_benchmark true false "assets/benchmark_with_compile_no_start.csv"
run_benchmark true true "assets/benchmark_with_compile_with_start.csv"

echo "All benchmarks completed"
