import time
import random
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys

# --- חלק א': מימוש אלגוריתמי מיון [cite: 16-22] ---

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

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


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# --- פונקציות עזר ---

def generate_base_array(size, noise_percentage):
    if noise_percentage == 0:
        return [random.randint(0, 1000000) for _ in range(size)]

    base_array = list(range(size))
    num_swaps = int((noise_percentage / 100) * size // 2)

    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        base_array[i], base_array[j] = base_array[j], base_array[i]

    return base_array


# מיפוי אלגוריתמים לפי דרישות המטלה [cite: 71-76]
ALG_MAP = {
    3: ("Insertion Sort", insertion_sort),
    4: ("Merge Sort", merge_sort),
    5: ("Quick Sort", quick_sort)
}


def compare_algorithms(selected_ids, sizes, epochs, noise):
    raw_results = {ALG_MAP[i][0]: {size: [] for size in sizes} for i in selected_ids}
    sys.setrecursionlimit(2000000)

    for epoch in range(epochs):
        print(f"\n--- Epoch {epoch + 1}/{epochs} ---")

        for size in sizes:
            base_array = generate_base_array(size, noise)
            for alg_id in selected_ids:
                name, func = ALG_MAP[alg_id]

                # תנאי דילוג: מיון הכנסה מעל 50,000 איברים
                if name == "Insertion Sort" and size > 10000:
                    continue

                test_arr = base_array.copy()
                start = time.time()
                test_arr = func(test_arr)
                elapsed = time.time() - start

                raw_results[name][size].append(elapsed)

    return raw_results


def show_results(raw_results, sizes, filename):
    plt.figure(figsize=(12, 7))

    # הדפסת דוח תוצאות מפורט [cite: 31-33]
    print(f"\n{'Algorithm':<15} | {'Size':<10} | {'Mean (s)':<12} | {'Std Dev':<10}")
    print("-" * 60)

    for alg_name, size_dict in raw_results.items():
        means, stds, valid_sizes = [], [], []

        for size in sizes:
            times = size_dict[size]
            if times:
                m = np.mean(times)
                s = np.std(times)

                means.append(m)
                stds.append(s)
                valid_sizes.append(size)

                print(f"{alg_name:<15} | {size:<10} | {m:<12.5f} | {s:<10.5f}")

        if valid_sizes:
            plt.errorbar(valid_sizes, means, yerr=stds,
                         label=alg_name, marker='o', capsize=5)

    plt.xlabel('Array Size (n)')
    plt.ylabel('Time (seconds)')
    plt.title(f'Sorting Performance Comparison ({filename})')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.savefig(f"{filename}.png")
    print(f"\nSaved: {filename}.png")
    plt.show()


# --- ממשק שורת פקודה (CLI) [cite: 61-70] ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sorting Experiment CLI")

    parser.add_argument(
        "-a", "--algorithms",
        nargs='+',
        type=int,
        default=[3, 4, 5],
        help="3: Insertion, 4: Merge, 5: Quick"
    )

    parser.add_argument(
        "-s", "--sizes",
        nargs='+',
        type=int,
        default=[100, 1000, 5000, 10000, 50000, 250000, 100000]
    )

    parser.add_argument(
        "-e", "--experiment",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="0: Random, 1: 5% Noise, 2: 20% Noise"
    )

    parser.add_argument(
        "-r", "--repetitions",
        type=int,
        default=5
    )

    args = parser.parse_args()

    noise_val = {0: 0, 1: 5, 2: 20}[args.experiment]
    out_file = {0: "result1", 1: "result2", 2: "result2"}[args.experiment]

    results = compare_algorithms(
        args.algorithms,
        args.sizes,
        args.repetitions,
        noise_val
    )

    show_results(results, args.sizes, out_file)