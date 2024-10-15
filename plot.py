import matplotlib.pyplot as plt
import csv
import os

def read_csv(filename):
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
        return headers, data
    except FileNotFoundError:
        print(f"Warning: File {filename} not found. Skipping this scenario.")
        return None, None

def plot_results(filename, title):
    headers, data = read_csv(filename)
    if headers is None or data is None:
        return

    n = [int(row[0]) for row in data]
    python_times = [float(row[1]) for row in data]
    rust_times = [float(row[2]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(n, python_times, marker='o', label='Python Merge Sort')
    plt.plot(n, rust_times, marker='o', label='Rust Bogo Sort')

    plt.xlabel('Array Size (n)')
    plt.ylabel('Time (seconds)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.yscale('log')

    # Add horizontal line at y=0.1 seconds for reference
    plt.axhline(y=0.1, color='r', linestyle='--', alpha=0.5)
    plt.text(max(n), 0.1, '0.1s', va='bottom', ha='right', color='r', alpha=0.5)

    # Find and annotate crossover point
    crossover_point = next((i for i, (p, r) in enumerate(zip(python_times, rust_times)) if p < r), None)
    if crossover_point is not None:
        plt.annotate(f'Crossover: n={n[crossover_point]}',
                     xy=(n[crossover_point], python_times[crossover_point]),
                     xytext=(0, 30), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    plt.tight_layout()
    plt.savefig(f'{os.path.splitext(filename)[0]}_plot.png')
    plt.close()
    print(f"Plot saved as {os.path.splitext(filename)[0]}_plot.png")

# Plot results for all scenarios
scenarios = [
    ('benchmark_no_compile_no_start.csv', 'Python Merge Sort vs Rust Bogo Sort\n(No Compile Time, No Start Time)'),
    ('benchmark_no_compile_with_start.csv', 'Python Merge Sort vs Rust Bogo Sort\n(No Compile Time, With Start Time)'),
    ('benchmark_with_compile_no_start.csv', 'Python Merge Sort vs Rust Bogo Sort\n(With Compile Time, No Start Time)'),
    ('benchmark_with_compile_with_start.csv', 'Python Merge Sort vs Rust Bogo Sort\n(With Compile Time, With Start Time)')
]

for filename, title in scenarios:
    plot_results(filename, title)

print("All plots have been generated.")
