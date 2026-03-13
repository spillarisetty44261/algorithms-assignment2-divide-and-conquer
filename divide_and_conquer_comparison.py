import random
import time
import tracemalloc
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10000)

# Merge Sort implementation
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Quick Sort implementation
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)

# Function to measure execution time and memory usage
def measure_performance(sort_function, data):
    tracemalloc.start()

    start_time = time.perf_counter()
    sort_function(data.copy())
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time
    memory_usage_kb = peak / 1024

    return execution_time, memory_usage_kb

# Dataset generation
size = 2000
sorted_data = list(range(size))
reverse_sorted_data = list(range(size, 0, -1))
random_data = random.sample(range(size * 2), size)

datasets = {
    "Sorted": sorted_data,
    "Reverse Sorted": reverse_sorted_data,
    "Random": random_data
}

results = []

for dataset_name, dataset in datasets.items():
    merge_time, merge_memory = measure_performance(merge_sort, dataset)
    quick_time, quick_memory = measure_performance(quick_sort, dataset)

    results.append([dataset_name, "Merge Sort", merge_time, merge_memory])
    results.append([dataset_name, "Quick Sort", quick_time, quick_memory])

# Print results
print("Dataset Type | Algorithm   | Execution Time (s) | Memory Usage (KB)")
print("-" * 65)
for row in results:
    print(f"{row[0]:13} | {row[1]:11} | {row[2]:18.6f} | {row[3]:16.2f}")

# Prepare data for graph
dataset_labels = list(datasets.keys())
merge_times = [row[2] for row in results if row[1] == "Merge Sort"]
quick_times = [row[2] for row in results if row[1] == "Quick Sort"]

x = range(len(dataset_labels))

plt.figure(figsize=(8, 5))
plt.plot(x, merge_times, marker='o', label='Merge Sort')
plt.plot(x, quick_times, marker='o', label='Quick Sort')
plt.xticks(x, dataset_labels)
plt.xlabel("Dataset Type")
plt.ylabel("Execution Time (seconds)")
plt.title("Merge Sort vs Quick Sort Execution Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("execution_time_graph.png")
plt.show()