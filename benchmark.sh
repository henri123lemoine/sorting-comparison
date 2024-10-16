#!/bin/bash

set -e

NUM_RUNS=5  # Number of runs to average

# Function to run benchmarks
run_benchmark() {
    local include_compile_time=$1
    local include_start_time=$2
    local output_file=$3

    echo "Running benchmark: include_compile_time=$include_compile_time, include_start_time=$include_start_time"
    echo "Output file: $output_file"

    echo "n,Python Merge Sort (s),Rust Bogo Sort (s)" > "$output_file"

    if [ "$include_compile_time" = true ]; then
        echo "Compiling Rust implementation..."
        cargo clean > /dev/null 2>&1
        compile_time=$(TIMEFORMAT='%R'; { time cargo build --release > /dev/null 2>&1; } 2>&1)
        echo "Compile time: $compile_time seconds"
    fi

    for n in {1..11}; do
        echo "Processing n=$n"
        python_total=0
        rust_total=0

        for run in $(seq 1 $NUM_RUNS); do
            # Generate random numbers
            numbers=$(uv run python -c "import random; print(' '.join(str(random.randint(0, 1000)) for _ in range($n)))")
            
            # Run Python merge sort
            if [ "$include_start_time" = true ]; then
                python_time=$(TIMEFORMAT='%R'; { time uv run src/merge_sort.py $n <<< "$numbers" > /dev/null; } 2>&1)
            else
                python_time=$(uv run python -c "
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

            python_total=$(awk -v pt="$python_total" -v ct="$python_time" 'BEGIN {print pt + ct}')
            rust_total=$(awk -v rt="$rust_total" -v ct="$rust_time" 'BEGIN {print rt + ct}')
        done

        # Calculate averages
        python_avg=$(awk -v total="$python_total" -v runs="$NUM_RUNS" 'BEGIN {printf "%.6f", total / runs}')
        rust_avg=$(awk -v total="$rust_total" -v runs="$NUM_RUNS" 'BEGIN {printf "%.6f", total / runs}')
        
        echo "$n,$python_avg,$rust_avg" >> "$output_file"
        
        # Break if average Rust bogo sort takes more than 30 seconds
        if (( $(awk -v rt="$rust_avg" 'BEGIN {print (rt > 30)}') )); then
            echo "Breaking loop: Average Rust bogo sort took more than 30 seconds"
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
