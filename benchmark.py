import time
from typing import List, Tuple, Callable

import matplotlib.pyplot as plt

from src.merge_sort import merge_sort, generate_random_array
from sorting_comparison import bogo_sort


def time_sort(sort_func: Callable, arr: List[int], max_time: float = 0.1) -> Tuple[float, bool]:
    """Time a sorting function with a maximum time limit."""
    start_time = time.perf_counter()
    try:
        sorted_arr = sort_func(arr.copy())
        duration = time.perf_counter() - start_time
        if duration > max_time or sorted_arr != sorted(arr):
            return duration, False
        return duration, True
    except Exception:
        return max_time, False


def quick_benchmark(sort_func: Callable, size: int, runs: int = 3, max_time: float = 0.1) -> float:
    """Run a quick benchmark for a sorting function."""
    total_time = 0
    for _ in range(runs):
        duration, success = time_sort(sort_func, generate_random_array(size), max_time)
        if not success:
            return max_time
        total_time += duration
    return total_time / runs


def benchmark_sorting(max_size: int = 20, step: int = 1) -> Tuple[List[int], List[float], List[float]]:
    """Benchmark merge sort and bogo sort."""
    sizes = list(range(1, max_size + 1, step))
    merge_times, bogo_times = [], []

    print("Benchmarking...")
    for size in sizes:
        merge_time = quick_benchmark(merge_sort, size)
        bogo_time = quick_benchmark(bogo_sort, size)
        
        merge_times.append(merge_time)
        bogo_times.append(bogo_time)
        
        print(f"Size {size}: Merge Sort: {merge_time:.6f}s, Bogo Sort: {bogo_time:.6f}s")
        
        if bogo_time >= 0.1:
            print("Bogo Sort reached time limit. Stopping Bogo Sort benchmarking.")
            break

    return sizes[:len(bogo_times)], merge_times[:len(bogo_times)], bogo_times


def plot_results(sizes: List[int], merge_times: List[float], bogo_times: List[float]):
    """Plot the benchmark results."""
    plt.figure(figsize=(12, 8))
    plt.loglog(sizes, merge_times, label="Python Merge Sort", marker="o")
    plt.loglog(sizes, bogo_times, label="Rust Bogo Sort", marker="s")
    plt.xlabel("Array Size")
    plt.ylabel("Time (seconds)")
    plt.title("Python Merge Sort vs Rust Bogo Sort (Quick Benchmark)")
    plt.legend()
    plt.grid(True)
    plt.savefig("assets/sorting_comparison.png")
    plt.show()


if __name__ == "__main__":
    sizes, merge_times, bogo_times = benchmark_sorting()
    plot_results(sizes, merge_times, bogo_times)
