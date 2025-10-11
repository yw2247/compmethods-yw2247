# 2a. Modify alg2 for Keyed Sorting 
def mergesort_keyed(data, key):

    # Base case: 0 or 1 item -> already sorted
    if len(data) <= 1:
        return data[:]

    # Recursive divide
    mid = len(data) // 2
    left  = mergesort_keyed(data[:mid], key)
    right = mergesort_keyed(data[mid:], key)

    # Merge step: combine two sorted halves
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1

    # Add leftovers
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Examples
if __name__ == "__main__":
    patients = [
        {"patient_id": 3, "name": "Charlie", "age": 40},
        {"patient_id": 1, "name": "Alice", "age": 22},
        {"patient_id": 2, "name": "Bob", "age": 31},
        {"patient_id": 2, "name": "Bella", "age": 29},  
        {"patient_id": 9, "name": "Tommy", "age": 1}
    ]

    print("Original data:")
    for p in patients:
        print(p)

    sorted_patients = mergesort_keyed(patients, key="patient_id")

    print("\nSorted data (by patient_id):")
    for p in sorted_patients:
        print(p)


# 2b Parallelize the Algorithm
# Parallel chunk sort (Pool.map), serial pairwise merges.

import sys, time, random
from multiprocessing import Pool, cpu_count, set_start_method
import matplotlib.pyplot as plt

def merge(a, b, key):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        if a[i][key] <= b[j][key]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

# parallel sort (only)
def _sort_chunk(args):
    chunk, key = args
    return sorted(chunk, key=lambda d: d[key])

def parallel_sort_then_serial_merge(data, key, chunk_size=None):
    n = len(data)
    cores = max(1, cpu_count() or 4)

    if chunk_size is None:
        chunk_size = max(n // 8, 200_000)

    if n <= chunk_size:
        return mergesort_keyed(data, key)

    chunks = [data[i:i+chunk_size] for i in range(0, n, chunk_size)]

    # Parallel sort each chunk
    with Pool(processes=cores) as pool:
        sorted_chunks = pool.map(_sort_chunk, [(ch, key) for ch in chunks])

    # Serial pairwise merges 
    while len(sorted_chunks) > 1:
        merged = []
        it = iter(sorted_chunks)
        for a in it:
            b = next(it, None)
            merged.append(a if b is None else merge(a, b, key))
        sorted_chunks = merged

    return sorted_chunks[0]

# generate data + quick check
def make_data(n):
    random.seed(0)
    return [{"patient_id": random.randint(1, max(2, n//2)),
             "name": f"P{i}",
             "age": random.randint(0, 90)} for i in range(n)]

def is_sorted_by_key(lst, key):
    k = [x[key] for x in lst]
    return all(k[i] <= k[i+1] for i in range(len(k)-1))

# benchmark + plot
if __name__ == "__main__":
    if sys.platform != "win32":
        try:
            set_start_method("fork", force=True)
        except RuntimeError:
            pass

    sizes = [400_000, 800_000, 1_200_000, 1_600_000]
    serial_t, parallel_t = [], []

    for n in sizes:
        data = make_data(n)
        data2 = list(data)

        t0 = time.perf_counter()
        out_s = mergesort_keyed(data, "patient_id")
        t1 = time.perf_counter()

        t2 = time.perf_counter()
        out_p = parallel_sort_then_serial_merge(
            data2, "patient_id",
            chunk_size=max(n // 8, 200_000)                    
        )
        t3 = time.perf_counter()

        ts = t1 - t0
        tp = t3 - t2
        serial_t.append(ts); parallel_t.append(tp)

        assert is_sorted_by_key(out_s, "patient_id")
        assert out_s == out_p

        print(f"n={n:8} | serial={ts:7.3f}s | parallel={tp:7.3f}s | speedup={ts/tp:4.2f}x ")

    # log–log plot 
    plt.figure(figsize=(6,4))
    plt.loglog(sizes, serial_t, marker="o", label="Serial")
    plt.loglog(sizes, parallel_t, marker="s", label="Parallel (parallel-sort, serial-merge)")
    plt.xlabel("n (log scale)"); plt.ylabel("Time (s, log scale)")
    plt.title("Merge Sort: Serial vs Parallel (sort-only)")
    plt.legend(); plt.tight_layout()
    plt.savefig("ps2b_sort_only_loglog.png", dpi=180)

