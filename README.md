# Python Merge Sort vs Rust Bogo Sort Comparison

This project compares the performance of merge sort implemented in Python against bogo sort implemented in Rust. The goal is to find the array length at which Python's merge sort becomes faster than Rust's bogo sort.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/henri123lemoine/sorting-comparison.git
   cd sorting-comparison
   ```

2. Build the Rust library:
   ```bash
   cargo build --release
   cd ../..
   ```

## Running the Benchmark

To run the benchmark and find the crossover point:

```bash
./benchmark.sh
```

This script will test various array lengths and report the point at which Python's merge sort becomes faster than Rust's bogo sort.

## Project Structure

- `src/merge_sort.py`: Implementation of merge sort in Python
- `src/lib.rs`: Rust file containing the bogo sort implementation
- `benchmark.sh`: Bash script to run the benchmark and compare the algorithms
- `pyproject.toml`: Python project configuration
- `Cargo.toml`: Rust project configuration

## Results

Not counting Python start times:

![Sorting Comparison](assets/sorting_comparison.png)

Crossover point: ~4

Counting Python start times:

```bash
~/Documents/Programming/PersonalProjects/sorting-comparison (main*) » ./benchmark.sh      henrilemoine@Henris-MacBook-Pro
Compiling Rust implementation...
   Compiling sorting-comparison v0.1.0 (/Users/henrilemoine/Documents/Programming/PersonalProjects/sorting-comparison)
    Finished `release` profile [optimized] target(s) in 0.33s
n,Python Merge Sort (s),Rust Bogo Sort (s)
1,0.082,0.004
2,0.025,0.003
3,0.024,0.003
4,0.023,0.002
5,0.023,0.003
6,0.023,0.004
7,0.022,0.003
8,0.024,0.007
9,0.022,0.026
10,0.024,1.515
11,0.024,2.453
12,0.023,61.772
```

Crossover point: ~9
