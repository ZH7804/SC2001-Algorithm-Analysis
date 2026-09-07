import os
import random
import time

import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt

QUICK_TEST = False

TIMING_REPEATS = 1


class SortingStats: #creates a counter for the comps which we will be using later

    def __init__(self):
        self.comparisons = 0


def generate_random_dataset(size, upper_bound=None): #generating the dataset using random
    if upper_bound is None:
        upper_bound = size
    return random.choices(range(1, upper_bound + 1), k=size)


def insertion_sort(array_to_sort, starting_index, ending_index, stats): #typical insertion sort implementation
    for current_index in range(starting_index + 1, ending_index + 1):
        key_value = array_to_sort[current_index]
        walker = current_index - 1

        while walker >= starting_index:
            stats.comparisons += 1
            if array_to_sort[walker] > key_value:
                array_to_sort[walker + 1] = array_to_sort[walker]
                walker -= 1
            else:
                break

        array_to_sort[walker + 1] = key_value


def merge_two_halves(array_to_sort, starting_index, middle_index, ending_index, stats):
    left_half = array_to_sort[starting_index:middle_index + 1]
    right_half = array_to_sort[middle_index + 1:ending_index + 1]

    left_pos = 0
    right_pos = 0
    write_pos = starting_index

    while left_pos < len(left_half) and right_pos < len(right_half):
        stats.comparisons += 1
        if left_half[left_pos] <= right_half[right_pos]:
            array_to_sort[write_pos] = left_half[left_pos]
            left_pos += 1
        else:
            array_to_sort[write_pos] = right_half[right_pos]
            right_pos += 1
        write_pos += 1

    while left_pos < len(left_half):
        array_to_sort[write_pos] = left_half[left_pos]
        left_pos += 1
        write_pos += 1

    while right_pos < len(right_half):
        array_to_sort[write_pos] = right_half[right_pos]
        right_pos += 1
        write_pos += 1


def hybrid_sort(array_to_sort, starting_index, ending_index, threshold_size, stats):
    if starting_index >= ending_index:
        return

    subarray_length = ending_index - starting_index + 1
    if subarray_length <= threshold_size:
        insertion_sort(array_to_sort, starting_index, ending_index, stats)
        return

    middle_index = (starting_index + ending_index) // 2
    hybrid_sort(array_to_sort, starting_index, middle_index, threshold_size, stats)
    hybrid_sort(array_to_sort, middle_index + 1, ending_index, threshold_size, stats)
    merge_two_halves(array_to_sort, starting_index, middle_index, ending_index, stats)


def classic_merge_sort(array_to_sort, starting_index, ending_index, stats):
    if starting_index >= ending_index:
        return

    middle_index = (starting_index + ending_index) // 2
    classic_merge_sort(array_to_sort, starting_index, middle_index, stats)
    classic_merge_sort(array_to_sort, middle_index + 1, ending_index, stats)
    merge_two_halves(array_to_sort, starting_index, middle_index, ending_index, stats)

def save_plot(figure, output_dir, filename): #just a helper to save our plots generated
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)
    figure.savefig(full_path, dpi=150, bbox_inches="tight")
    plt.close(figure)
    print(f"  saved plot -> {full_path}")


def experiment_fixed_threshold(input_sizes, threshold_size, output_dir): #this is for fixed s, comparison + time vs n, i.e. for c(i)
    print(f"\n--- Part (c)(i): S fixed at {threshold_size}, varying n ---")

    comparison_counts = []
    run_times = []
    for n in input_sizes:
        dataset = generate_random_dataset(n)
        stats = SortingStats()
        start_time = time.process_time()
        hybrid_sort(dataset, 0, n - 1, threshold_size, stats)
        elapsed = time.process_time() - start_time
        comparison_counts.append(stats.comparisons)
        run_times.append(elapsed)
        print(f"  n = {n:>10,}  ->  comparisons = {stats.comparisons:>15,}   time = {elapsed:>8.3f}s")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(input_sizes, comparison_counts, marker="o")
    ax1.set_xlabel("Input size n")
    ax1.set_ylabel("Key comparisons")
    ax1.set_title("Comparisons")
    ax1.grid(True, alpha=0.3)

    ax2.plot(input_sizes, run_times, marker="o", color="crimson")
    ax2.set_xlabel("Input size n")
    ax2.set_ylabel("CPU time (s)")
    ax2.set_title("Runtime")
    ax2.grid(True, alpha=0.3)

    fig.suptitle(f"Comparisons and runtime vs n (S = {threshold_size})")
    save_plot(fig, output_dir, "part_c1_comparisons_and_time_vs_n.png")


def experiment_fixed_size(fixed_n, threshold_values, output_dir): #for fixed n, comparison + time vs s, i.e. for c(ii)
    print(f"\n--- Part (c)(ii): n fixed at {fixed_n:,}, varying S ---")
    base_dataset = generate_random_dataset(fixed_n)

    comparison_counts = []
    run_times = []
    for s in threshold_values:
        dataset_copy = base_dataset[:]
        stats = SortingStats()
        start_time = time.process_time()
        hybrid_sort(dataset_copy, 0, fixed_n - 1, s, stats)
        elapsed = time.process_time() - start_time
        comparison_counts.append(stats.comparisons)
        run_times.append(elapsed)
        print(f"  S = {s:>5}  ->  comparisons = {stats.comparisons:>15,}   time = {elapsed:>8.3f}s")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(threshold_values, comparison_counts, marker="o", color="darkorange")
    ax1.set_xlabel("Threshold S")
    ax1.set_ylabel("Key comparisons")
    ax1.set_title("Comparisons")
    ax1.grid(True, alpha=0.3)

    ax2.plot(threshold_values, run_times, marker="o", color="crimson")
    ax2.set_xlabel("Threshold S")
    ax2.set_ylabel("CPU time (s)")
    ax2.set_title("Runtime")
    ax2.grid(True, alpha=0.3)

    fig.suptitle(f"Comparisons and runtime vs S (n = {fixed_n:,})")
    save_plot(fig, output_dir, "part_c2_comparisons_and_time_vs_S.png")

def experiment_find_optimal_threshold(sizes_to_check, threshold_values, output_dir): #searching for best S, chosen by runtime
    print("\n--- Part (c)(iii): searching for a good S across different n (best = fastest runtime) ---")

    fig_comparisons, ax_comparisons = plt.subplots(figsize=(9, 6))
    fig_time, ax_time = plt.subplots(figsize=(9, 6))
    best_threshold_per_size = {}

    for n in sizes_to_check:
        dataset = generate_random_dataset(n)
        comparisons_for_this_n = []
        times_for_this_n = []

        for s in threshold_values:
            best_time_for_this_s = None
            comparisons_for_this_s = None
            for _ in range(TIMING_REPEATS):
                dataset_copy = dataset[:]
                stats = SortingStats()
                start_time = time.process_time()
                hybrid_sort(dataset_copy, 0, n - 1, s, stats)
                elapsed = time.process_time() - start_time
                comparisons_for_this_s = stats.comparisons
                if best_time_for_this_s is None or elapsed < best_time_for_this_s:
                    best_time_for_this_s = elapsed

            comparisons_for_this_n.append(comparisons_for_this_s)
            times_for_this_n.append(best_time_for_this_s)

        best_index = times_for_this_n.index(min(times_for_this_n))
        best_s = threshold_values[best_index]
        best_threshold_per_size[n] = best_s

        print(f"  n = {n:>9,}  ->  best S found = {best_s} "
              f"(time = {times_for_this_n[best_index]:.4f}s, "
              f"comparisons = {comparisons_for_this_n[best_index]:,})")

        ax_comparisons.plot(threshold_values, comparisons_for_this_n, marker="o", label=f"n = {n:,}")
        ax_time.plot(threshold_values, times_for_this_n, marker="o", label=f"n = {n:,}")

    ax_comparisons.set_xlabel("Threshold S")
    ax_comparisons.set_ylabel("Key comparisons")
    ax_comparisons.set_title("Key comparisons vs S for a few different input sizes")
    ax_comparisons.legend()
    ax_comparisons.grid(True, alpha=0.3)
    save_plot(fig_comparisons, output_dir, "part_c3_comparisons_vs_S.png")

    ax_time.set_xlabel("Threshold S")
    ax_time.set_ylabel("CPU time (s), best of repeats")
    ax_time.set_title("Runtime vs S for a few different input sizes")
    ax_time.legend()
    ax_time.grid(True, alpha=0.3)
    save_plot(fig_time, output_dir, "part_c3_time_vs_S.png")

    return best_threshold_per_size

def experiment_hybrid_vs_classic(n, threshold_size, output_dir): #for part d, making comp between hybrid and classic merge sort
    print(f"\n--- Part (d): hybrid (S = {threshold_size}) vs classic merge sort, n = {n:,} ---")

    shared_dataset = generate_random_dataset(n)

    hybrid_copy = shared_dataset[:]
    hybrid_stats = SortingStats()
    hybrid_start = time.process_time()
    hybrid_sort(hybrid_copy, 0, n - 1, threshold_size, hybrid_stats)
    hybrid_cpu_time = time.process_time() - hybrid_start

    classic_copy = shared_dataset[:]
    classic_stats = SortingStats()
    classic_start = time.process_time()
    classic_merge_sort(classic_copy, 0, n - 1, classic_stats)
    classic_cpu_time = time.process_time() - classic_start


    print(f"  hybrid sort  : {hybrid_stats.comparisons:>15,} comparisons   {hybrid_cpu_time:>8.3f}s CPU time")
    print(f"  classic sort : {classic_stats.comparisons:>15,} comparisons   {classic_cpu_time:>8.3f}s CPU time")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    labels = ["Hybrid", "Classic Merge Sort"]

    ax1.bar(labels, [hybrid_stats.comparisons, classic_stats.comparisons],
            color=["seagreen", "steelblue"])
    ax1.set_ylabel("Key comparisons")
    ax1.set_title("Comparisons")

    ax2.bar(labels, [hybrid_cpu_time, classic_cpu_time],
            color=["seagreen", "steelblue"])
    ax2.set_ylabel("CPU time (s)")
    ax2.set_title("CPU time")

    fig.suptitle(f"Hybrid vs Classic Merge Sort on n = {n:,}")
    save_plot(fig, output_dir, "part_d_hybrid_vs_classic.png")

def main():
    output_dir = "project1_output_plots"

    if QUICK_TEST:
        sizes_for_c1 = [200, 500, 1000, 2000, 5000]
        fixed_n_for_c2 = 5000
        threshold_values_for_c2 = [2, 5, 10, 20]
        sizes_for_c3 = [1000, 5000]
        threshold_values_for_c3 = [2, 5, 10, 20]
        n_for_part_d = 100000
    else:
        sizes_for_c1 = [1000, 10000, 100000, 1000000, 10000000]
        fixed_n_for_c2 = 1000000
        threshold_values_for_c2 = [2, 5, 16, 64, 128, 500]
        sizes_for_c3 = [10000, 100000, 1000000]
        threshold_values_for_c3 = [2, 5, 16, 64, 128, 500]
        n_for_part_d = 10000000  

    threshold_for_c1 = 16 

    experiment_fixed_threshold(sizes_for_c1, threshold_for_c1, output_dir)
    experiment_fixed_size(fixed_n_for_c2, threshold_values_for_c2, output_dir)
    best_thresholds = experiment_find_optimal_threshold(sizes_for_c3, threshold_values_for_c3, output_dir)

    threshold_for_part_d = best_thresholds[max(best_thresholds.keys())] if best_thresholds else threshold_for_c1
    experiment_hybrid_vs_classic(n_for_part_d, threshold_for_part_d, output_dir)

    print("\nAll done. Plots are in:", os.path.abspath(output_dir))


if __name__ == "__main__":
    main()
