# Dijkstra's Algorithm: Adjacency Matrix + Array vs. Adjacency List + Min-Heap

An empirical performance analysis comparing two implementations of **Dijkstra's Algorithm**: a straightforward version using an **Adjacency Matrix** with an **array-based priority queue**, against a faster version using an **Array of Adjacency Lists** with a **self-implemented binary Min-Heap**.

---

## Executive Summary & Key Findings

1. **Theoretical complexity confirmed:** the Adjacency Matrix + Array implementation runs in **O(V²)**, while the Adjacency List + Min-Heap implementation runs in **O((V + E) log V)**. The benchmark results below track these curves closely.
2. **Vertex scaling dominates the matrix version:** as |V| grows from 50 to 800 (a 16x increase), the Matrix+Array runtime grows by roughly **~230x** (0.000359s → 0.083964s), consistent with a quadratic O(V²) blow-up. The List+Heap version grows by only **~21x** (0.000398s → 0.008314s) over the same range.
3. **At V = 800, the heap version is ~10x faster** than the matrix version (0.083964s vs. 0.008314s), even though the test graphs are relatively sparse.
4. **Edge count barely affects the matrix version:** with |V| fixed at 300, growing extra edges from 200 to 30,000 (150x more edges) only increases Matrix+Array runtime by **~15%** (0.012128s → 0.013907s), because its cost is dominated by the V² term regardless of |E|.
5. **Edge count clearly affects the heap version:** over the same range, List+Heap runtime grows by **~5.5x** (0.001507s → 0.008316s), reflecting its dependence on |E| through the (V + E) term.

---

## Implementation Overview

| Part | Graph Representation | Priority Queue | Time Complexity |
| ---- | --------------------- | -------------- | ---------------- |
| **(a)** | Adjacency Matrix | Plain array (linear scan for minimum) | O(V²) |
| **(b)** | Array of Adjacency Lists | Self-implemented binary Min-Heap | O((V + E) log V) |

- `dijkstraWithMatrixAndArray` — for every vertex, scans the full distance array to find the closest unvisited vertex, then relaxes all its neighbours by reading a row of the adjacency matrix.
- `dijkstraWithAdjacencyListAndHeap` — uses a hand-built `MinimisingHeap` class (push / bubble-up, pop / bubble-down) instead of Python's built-in `heapq`, so the closest unvisited vertex is retrieved in O(log V) instead of O(V).
- `generateRandomConnectedGraph` — builds a random weighted, undirected, connected graph and returns it in both representations at once, so both algorithms are timed on identical inputs.

---

## Benchmark Results

### Part (a): Vertex Scaling (|E| ≈ proportional to |V|)

Growing the number of vertices while keeping the graph's "shape" (extra edges ≈ 2×|V|) roughly constant.

| Vertices \|V\| | Edges (approx) \|E\| | Matrix + Array (s) | List + Heap (s) | Speedup (Heap vs. Matrix) |
| -------------: | ---------------------: | ------------------: | ----------------: | --------------------------: |
| **50**         | 149                     | 0.000359             | 0.000398           | 0.9x                        |
| **100**        | 299                     | 0.001291             | 0.000574           | 2.2x                        |
| **200**        | 599                     | 0.004892             | 0.001397           | 3.5x                        |
| **400**        | 1,199                   | 0.021713             | 0.003578           | 6.1x                        |
| **800**        | 2,399                   | 0.083964             | 0.008314            | 10.1x                       |

- **Analysis:** Matrix+Array runtime roughly quadruples each time |V| doubles — the textbook signature of O(V²). List+Heap grows far more gently, and the speed gap between the two widens steadily as |V| increases, exactly as the O((V+E) log V) vs. O(V²) comparison predicts.

### Part (b): Edge Scaling (|V| fixed at 300)

Fixing the number of vertices at 300 and growing the number of extra random edges.

| Vertices \|V\| | Extra Edges | Matrix + Array (s) | List + Heap (s) | Speedup (Heap vs. Matrix) |
| --------------: | -----------: | ------------------: | ----------------: | --------------------------: |
| **300**         | 200           | 0.012128             | 0.001507           | 8.0x                        |
| **300**         | 1,000         | 0.011432             | 0.002768           | 4.1x                        |
| **300**         | 5,000         | 0.011358             | 0.005929           | 1.9x                        |
| **300**         | 15,000        | 0.012839             | 0.006888            | 1.9x                        |
| **300**         | 30,000        | 0.013907             | 0.008316            | 1.7x                        |

- **Analysis:** Matrix+Array is almost flat here, since its cost is dominated by V² and barely notices |E|. List+Heap does grow with |E| (as expected from the (V+E) term), so the speed advantage of the heap version narrows as the graph gets denser — though it never falls behind the matrix version in this range.

---

## Part (c): Which Implementation Is Better, and When?

- **Sparse graphs (|E| ≈ O(V)):** the Adjacency List + Min-Heap version wins clearly and by a growing margin as |V| increases. Most real-world graphs (road networks, social graphs, dependency graphs) are sparse, so this is usually the better default choice.
- **Dense graphs (|E| close to V²):** the gap narrows, because the heap version's cost grows with |E| while the matrix version's cost stays roughly fixed at O(V²) either way. For sufficiently dense graphs, the two approaches converge, and the simpler Matrix+Array version may even become competitive since it avoids heap bookkeeping overhead.
- **Small graphs:** the difference barely matters in absolute terms (fractions of a millisecond), so implementation simplicity may be a better deciding factor than raw speed.
- **Large, sparse graphs:** this is where the Adjacency List + Min-Heap implementation is unambiguously the right choice — the benchmark shows a 10x speed advantage at just 800 vertices, and this gap only grows for larger graphs.

---

## Mathematical Overhead Breakdown

### Why Matrix + Array Struggles as |V| Grows

- **Linear scan per extraction:** finding the closest unvisited vertex requires checking every vertex, an O(V) operation, repeated V times → O(V²) overall, independent of how many edges actually exist.
- **Dense relaxation step:** relaxing "neighbours" means scanning a full row of the adjacency matrix (length V), even for vertices with very few actual neighbours.

### Why List + Heap Scales Better

- **Log-time extraction:** the self-implemented `MinimizingHeap` retrieves the closest unvisited vertex in O(log V) via `bubbleDown`, instead of scanning every vertex.
- **Sparse relaxation step:** relaxing neighbours only touches the actual adjacency list of the current vertex, which costs O(degree of vertex) rather than O(V).
- **Trade-off:** every relaxation that improves a distance pushes a new entry onto the heap (an O(log V) operation) rather than updating in place, so total heap operations are bounded by O((V + E) log V).

---

## Console Output Log

```
timing experiment: growing the number of vertices |V|
------------------------------------------------------------
  vertices   edges (approx)   matrix+array (s)    list+heap (s)
        50              149            0.000359         0.000398
       100              299            0.001291         0.000574
       200              599            0.004892         0.001397
       400             1199            0.021713         0.003578
       800             2399            0.083964         0.008314

timing experiment: fixed |V|, growing the number of edges |E|
------------------------------------------------------------
  vertices  extra edges   matrix+array (s)    list+heap (s)
       300          200            0.012128         0.001507
       300         1000            0.011432         0.002768
       300         5000            0.011358         0.005929
       300        15000            0.012839         0.006888
       300        30000            0.013907         0.008316
```
