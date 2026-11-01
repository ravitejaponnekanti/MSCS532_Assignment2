# MSCS532 Assignment 2: Divide-and-Conquer Sorting

Implementations: in-place stack-based Quick Sort (last-element pivot) and stable top-down Merge Sort, both ascending.

## Run (Python 3.8+)

```bash
python sorting_algorithms.py
python -m unittest -v
python benchmark.py
```

`benchmark.py` writes `benchmark_results.csv` and `environment.txt`. Runs test sorted, reverse-sorted, and seeded random unique integers of sizes 500, 2,000 and 4,000, with 3 timed trials per case. Time is the median in milliseconds. Peak additional **traced Python allocations** are measured separately with `tracemalloc` and are **not** total physical RAM; copied input lists are excluded.

## Why choose the last element as pivot?

This pivot rule intentionally demonstrates Quick Sort's worst case on pre-sorted inputs. A production system would normally randomize or improve pivot selection; benchmark results should not be read as a comparison of highly optimized production sorting libraries.

## GitHub

Create a **public** repository named `MSCS532_Assignment2`, push these source files, and replace the repository URL placeholder in your written report before submitting.

Suggested commits:

```bash
git init -b main
git add README.md sorting_algorithms.py
git commit -m "Implement divide-and-conquer sorting algorithms"
git add test_sorting.py
git commit -m "Add sorting correctness and stability tests"
git add benchmark.py benchmark_results.csv environment.txt
git commit -m "Add reproducible performance benchmarks"
```

Use your own machine's measurements if the assignment requires a local execution environment.
