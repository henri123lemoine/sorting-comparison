import time

import matplotlib.pyplot as plt

from sorting_comparison import bogo_sort
from src.merge_sort import merge_sort, generate_random_array


def time_sort(sort_func, arr):
    start_time = time.time()
    sort_func(arr)
    end_time = time.time()
    return end_time - start_time


def find_crossover_point(max_size=20, step=1, runs=5):
    sizes = range(1, max_size + 1, step)
    merge_times = []
    bogo_times = []

    for size in sizes:
        merge_time = 0
        bogo_time = 0
        for _ in range(runs):
            arr = generate_random_array(size)
            merge_time += time_sort(merge_sort, arr.copy())
            bogo_time += time_sort(bogo_sort, arr)
        
        merge_times.append(merge_time / runs)
        bogo_times.append(bogo_time / runs)

        if merge_times[-1] < bogo_times[-1]:
            print(f"Crossover point found at array size: {size}")
            break

    plot_results(sizes, merge_times, bogo_times)


def plot_results(sizes, merge_times, bogo_times):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, merge_times, label='Python Merge Sort')
    plt.plot(sizes, bogo_times, label='Rust Bogo Sort')
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.title('Python Merge Sort vs Rust Bogo Sort')
    plt.legend()
    plt.yscale('log')
    plt.grid(True)
    plt.savefig('sorting_comparison.png')
    plt.show()


if __name__ == "__main__":
    find_crossover_point()
