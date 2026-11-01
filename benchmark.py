"""Reproducible time/memory benchmark for MSCS-532 Assignment 2.

Timing and memory are measured in SEPARATE runs: tracemalloc slows execution.
Execute: python benchmark.py
"""
import csv
import platform
import random
import statistics
import time
import tracemalloc
from pathlib import Path

from sorting_algorithms import quick_sort, merge_sort

SIZES = (500, 2000, 4000)
REPEATS = 3
SEED = 532
ROOT = Path(__file__).resolve().parent


def create_input(n, order):
    if order == 'sorted':
        return list(range(n))
    if order == 'reverse sorted':
        return list(range(n - 1, -1, -1))
    if order == 'random':
        return random.Random(SEED + n).sample(range(n * 10), n)
    raise ValueError(order)


def measure(algorithm, source):
    expected = sorted(source)
    measurements = []
    for _ in range(REPEATS):
        values = source.copy()  # Input copying is excluded from timed region.
        start = time.perf_counter()
        algorithm(values)
        measurements.append((time.perf_counter() - start) * 1000)
        assert values == expected, 'Sorted output did not match Python sorted()'

    # Peak Python allocations during sorting; input copy is made before tracing.
    values = source.copy()
    tracemalloc.start()
    tracemalloc.reset_peak()
    algorithm(values)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert values == expected
    return round(statistics.median(measurements), 3), round(peak / 1024, 2)


def run():
    rows = []
    for n in SIZES:
        for order in ('sorted', 'reverse sorted', 'random'):
            source = create_input(n, order)
            for algorithm in (quick_sort, merge_sort):
                duration, peak = measure(algorithm, source)
                rows.append({
                    'size': n,
                    'dataset': order,
                    'algorithm': algorithm.__name__,
                    'median_time_ms': duration,
                    'peak_traced_KiB': peak,
                })
                print(f'n={n:>4} {order:<14} {algorithm.__name__:<10} '
                      f'{duration:>9.3f} ms   {peak:>8.2f} KiB')

    path = ROOT / 'benchmark_results.csv'
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / 'environment.txt').write_text(
        f'Python: {platform.python_version()}\n'
        f'Platform: {platform.system()} {platform.machine()}\n'
        f'Sizes: {SIZES}\nRepeats: {REPEATS}\nRandom seed: {SEED}\n'
        'Times: median of repeats in milliseconds; input copying excluded.\n'
        'Memory: tracemalloc peak of traced Python allocations during sorting, '
        'excluding preexisting input array; not total process RAM.\n',
        encoding='utf-8',
    )
    print('\nResults saved:', path)


if __name__ == '__main__':
    run()
