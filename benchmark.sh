#!/bin/bash

echo "Compiling Rust implementation..."
cargo build --release

echo "n,Python Merge Sort (s),Rust Bogo Sort (s)"

run_sort_with_timeout() {
    local cmd="$1"
    local numbers="$2"
    local timeout=10  # 10 seconds timeout
    local warmup_runs=3
    local timed_runs=5
    
    # Warmup runs
    for ((i=0; i<warmup_runs; i++)); do
        timeout $timeout bash -c "echo \"$numbers\" | $cmd" >/dev/null 2>&1
        if [ $? -eq 124 ]; then
            echo "timeout"
            return
        fi
    done
    
    # Timed runs
    local total_time=0
    for ((i=0; i<timed_runs; i++)); do
        local start_time=$(date +%s.%N)
        timeout $timeout bash -c "echo \"$numbers\" | $cmd" >/dev/null 2>&1
        local timeout_status=$?
        local end_time=$(date +%s.%N)
        if [ $timeout_status -eq 124 ]; then
            echo "timeout"
            return
        fi
        local elapsed=$(echo "$end_time - $start_time" | bc)
        total_time=$(echo "$total_time + $elapsed" | bc)
    done
    
    echo "scale=6; $total_time / $timed_runs" | bc
}

for n in {1..30}; do
    # Generate random numbers
    numbers=$(python -c "import random; print(' '.join(str(random.randint(0, 1000)) for _ in range($n)))")
    
    # Run Python merge sort
    python_time=$(run_sort_with_timeout "python src/merge_sort.py $n" "$numbers")
    
    # Run Rust bogo sort
    rust_time=$(run_sort_with_timeout "./target/release/bogo_sort" "$numbers")
    
    echo "$n,$python_time,$rust_time"
    
    # Break if Rust bogo sort times out
    if [ "$rust_time" == "timeout" ]; then
        echo "Rust bogo sort timed out at n=$n. Stopping benchmark."
        break
    fi
done
