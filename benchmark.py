import signal
import time

import matplotlib.pyplot as plt

from src.merge_sort import merge_sort, generate_random_array
from sorting_comparison import bogo_sort


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


def time_sort_with_timeout(sort_func, arr, timeout=5):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        start_time = time.time()
        sort_func(arr)
        end_time = time.time()
        signal.alarm(0)  # Reset the alarm
        return end_time - start_time
    except TimeoutException:
        return float("inf")


def find_crossover_point(max_size=20, step=1, runs=5, bogo_max_size=10):
    sizes = list(range(1, max_size + 1, step))
    merge_times = []
    bogo_times = []
    crossover_found = False

    for size in sizes:
        print(f"\nTesting array size: {size}")
        merge_time = 0
        bogo_time = 0
        for run in range(runs):
            arr = generate_random_array(size)
            arr_copy = arr.copy()

            # Time and verify Merge Sort
            merge_start = time.time()
            merge_sorted = merge_sort(arr)
            merge_end = time.time()
            merge_run_time = merge_end - merge_start
            merge_time += merge_run_time
            print(f"  Merge Sort Run {run+1}: {merge_run_time:.6f} seconds")
            assert merge_sorted == sorted(arr), "Merge Sort failed to sort correctly"

            # Time and verify Bogo Sort (only for small sizes)
            if size <= bogo_max_size:
                bogo_start = time.time()
                bogo_sorted = bogo_sort(arr_copy)
                bogo_end = time.time()
                bogo_run_time = bogo_end - bogo_start
                bogo_time += bogo_run_time
                print(f"  Bogo Sort Run {run+1}: {bogo_run_time:.6f} seconds")
                assert bogo_sorted == sorted(
                    arr_copy
                ), "Bogo Sort failed to sort correctly"

        merge_times.append(merge_time / runs)
        if size <= bogo_max_size:
            bogo_times.append(bogo_time / runs)
            if not crossover_found and merge_times[-1] < bogo_times[-1]:
                print(f"Crossover point found at array size: {size}")
                crossover_found = True

        print(f"Average Merge Sort time: {merge_times[-1]:.6f} seconds")
        if size <= bogo_max_size:
            print(f"Average Bogo Sort time: {bogo_times[-1]:.6f} seconds")

    # Pad bogo_times with infinity for the sizes we didn't test
    bogo_times.extend([float("inf")] * (len(sizes) - len(bogo_times)))

    plot_results(sizes, merge_times, bogo_times)


def plot_results(sizes, merge_times, bogo_times):
    plt.figure(figsize=(12, 8))
    plt.loglog(sizes, merge_times, label="Python Merge Sort", marker="o")
    plt.loglog(
        sizes[: len([t for t in bogo_times if t != float("inf")])],
        [t for t in bogo_times if t != float("inf")],
        label="Rust Bogo Sort",
        marker="s",
    )
    plt.xlabel("Array Size")
    plt.ylabel("Time (seconds)")
    plt.title("Python Merge Sort vs Rust Bogo Sort")
    plt.legend()
    plt.grid(True)
    plt.savefig("assets/sorting_comparison.png")
    plt.show()


if __name__ == "__main__":
    find_crossover_point()
