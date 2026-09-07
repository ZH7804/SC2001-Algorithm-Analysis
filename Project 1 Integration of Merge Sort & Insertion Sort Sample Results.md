# Hybrid Merge Sort Empirical Analysis & Benchmark Report

An empirical performance analysis comparing **Hybrid Merge Sort** (Merge Sort combined with Insertion Sort for small sub-array thresholds $S$) against **Classic Merge Sort**.

---

## Executive Summary & Key Findings

1. **Optimal Threshold ($S = 16$):** Switching from recursion to Insertion Sort when sub-array sizes reach $S = 16$ provides the best real-world CPU performance across large datasets ($n \ge 100,000$).
2. **Comparisons vs. Execution Time Trade-off:** While increasing $S$ strictly increases the number of key comparisons, it significantly reduces CPU execution time up to $S = 16$ by eliminating thousands of recursive function calls, stack allocations, and memory pointer overheads.
3. **Hybrid vs. Classic Merge Sort:** For $n = 10,000,000$, Hybrid Merge Sort ($S = 16$) runs **~5 seconds faster** (a **9.1% speedup**) than Classic Merge Sort, despite performing ~6.3 million more comparisons.

---

## Benchmark Results

### Part (c)(i): Input Size Scaling ($S = 16$, Varying $n$)

Evaluates how algorithm performance scales as array size $n$ grows by powers of 10 while maintaining a fixed threshold $S = 16$.

| Input Size ($n$) | Key Comparisons | CPU Time (s) | Scaling Factor (Time) | Theoretical $O(n \log n)$ |
| :--- | :--- | :--- | :--- | :--- |
| **1,000** | 10,453 | 0.000s | Baseline | Linearithmic |
| **10,000** | 127,132 | 0.031s | ~$31	imes$ | Linearithmic |
| **100,000** | 1,639,667 | 0.281s | ~$9.1	imes$ | Linearithmic |
| **1,000,000** | 20,219,827 | 3.500s | ~$12.5	imes$ | Linearithmic |
| **10,000,000** | 226,422,815 | 49.578s | ~$14.2	imes$ | Linearithmic |

* **Analysis:** Comparisons scale cleanly in line with $O(n \log n)$. Execution time exhibits expected super-linear growth, with slight cache-miss penalties visible as dataset size increases

---

### Part (c)(ii): Threshold Optimization ($n = 1,000,000$, Varying $S$)

Analyzes the effect of varying threshold $S$ on a fixed array size of 1,000,000 elements.

| Threshold ($S$) | Key Comparisons | CPU Time (s) | Relative Time-Taken vs $S=2$ | Performance Trajectory |
| :--- | :--- | :--- | :--- | :--- |
| **2** | 18,675,091 | 3.766s | 100.0% | Recursion Overhead Dominated |
| **5** | 18,727,658 | 3.531s | 93.8% | Transitioning |
| **16** | **20,220,552** | **3.469s** | **92.1%** | **Optimal Sweet Spot** |
| **64** | 29,907,159 | 4.266s | 113.3% | Insertion $O(S^2)$ Creep |
| **128** | 44,247,653 | 5.703s | 151.4% | Algorithmic Bottleneck |
| **500** | 133,834,667 | 14.734s | 391.2% | Severely Degraded ($O(S^2)$) |

### Part (c)(iii): Optimal Threshold across Variable $n$

Identifies the fastest threshold value $S$ across different problem scales.

| Array Size ($n$) | Best $S$ Found | CPU Time (s) | Key Comparisons |
| :--- | :--- | :--- | :--- |
| **10,000** | 2 | 0.0156s | 120,459 |
| **100,000** | 16 | 0.2344s | 1,639,837 |
| **1,000,000** | 16 | 3.3750s | 20,223,754 |

* **Observation:** For small arrays ($n \le 10,000$), call-stack depth is shallow enough that smaller threshold values perform well. For larger input sizes ($n \ge 100,000$), $S = 16$ consistently emerges as the global optimal threshold.

---

### Part (d): Head-to-Head Comparison ($n = 10,000,000$)

Comparing **Hybrid Merge Sort ($S = 16$)** directly against **Classic Merge Sort** on a 10-million element array.

| Algorithm | Key Comparisons | CPU Time (s) | Performance Delta |
| :--- | :--- | :--- | :--- |
| **Hybrid Sort ($S = 16$)** | 226,416,552 | **49.422s** | **~9.1% Faster** |
| **Classic Merge Sort** | **220,102,660** | 54.375s | Baseline (+4.953s) |

```
Key Comparisons vs. CPU Time
========================================================================
Classic Sort : [----------------------------- 220.1M] -> 54.38s CPU time
Hybrid Sort  : [--------------------------------- 226.4M] -> 49.42s CPU time
                                                               (4.95s FAST)
========================================================================
```

---

## Mathematical & System Overhead Breakdown

### 1. Theoretical Model
The overall time complexity model for Hybrid Merge Sort is given by:

$$	ext{Time}(n, S) = c_{	ext{merge}} \cdot n \log_2\left(rac{n}{S}
ight) + c_{	ext{insertion}} \cdot n S$$

Where:
* $c_{	ext{merge}}$ represents recursion overhead, stack allocation, array slicing, and merge operations per level.
* $c_{	ext{insertion}}$ represents the cycle cost per element swap/shift in Insertion Sort.

### 2. Why $S = 16$ Outperforms $S = 2$ and Classic Sort
* **Function Call Stack Elimination:** Bypassing the bottom $\log_2(16) = 4$ layers of recursion removes $2^4 = 16 times$ sub-problem stack overheads across the entire array.
* **L1 Cache Locality:** Sub-arrays of size $S \le 16$ fit entirely within L1 data cache lines (~64 bytes), allowing Insertion Sort's inner loops to run almost exclusively in registers and cache.
* **Instruction Efficiency:** Lower instruction count per element shifting operation in Insertion Sort offsets the theoretical $O(S^2)$ increase in comparisons.

---

## Console Output Log

```text
--- Part (c)(i): S fixed at 16, varying n ---
  n =     1,000 -> comparisons =        10,453   time =   0.000s
  n =    10,000 -> comparisons =       127,132   time =   0.031s
  n =   100,000 -> comparisons =     1,639,667   time =   0.281s
  n = 1,000,000 -> comparisons =    20,219,827   time =   3.500s
  n =10,000,000 -> comparisons =   226,422,815   time =  49.578s

--- Part (c)(ii): n fixed at 1,000,000, varying S ---
  S =     2 -> comparisons =    18,675,091   time =   3.766s
  S =     5 -> comparisons =    18,727,658   time =   3.531s
  S =    16 -> comparisons =    20,220,552   time =   3.469s
  S =    64 -> comparisons =    29,907,159   time =   4.266s
  S =   128 -> comparisons =    44,247,653   time =   5.703s
  S =   500 -> comparisons =   133,834,467   time =  14.734s

--- Part (c)(iii): searching for a good S across different n (best = fastest runtime) ---
  n =    10,000 -> best S found = 2 (time = 0.0156s, comparisons = 120,459)
  n =   100,000 -> best S found = 16 (time = 0.2344s, comparisons = 1,639,837)
  n = 1,000,000 -> best S found = 16 (time = 3.3750s, comparisons = 20,223,754)

--- Part (d): hybrid (S = 16) vs classic merge sort, n = 10,000,000 ---
  hybrid sort :    226,416,552 comparisons        49.422s CPU time
  classic sort:    220,102,660 comparisons        54.375s CPU time
```
