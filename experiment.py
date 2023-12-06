from dynamic_programming_optimized import find_partition_dynamic_programming
from branch_and_bound import bnb_final

import random
import time
import tracemalloc
import os

import matplotlib.pyplot as plt
import gc

import sys

sys.setrecursionlimit(10**9) 


def generate_and_save_dataset(size, file_name):
    dataset = [random.randint(1, 80) for _ in range(size)]
    with open(file_name, 'w') as f:
        f.write('\n'.join(map(str, dataset)))
    return dataset

def measure_time_and_memory(func, *args):
    gc.collect()  
    tracemalloc.start()  

    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()  
    tracemalloc.stop() 

    time_taken = (end_time - start_time) * 1000  # in milliseconds
    memory_taken = peak   # in bytes

    return time_taken, memory_taken, result

def analyze_subset_sum_algorithms(sizes, data_folder):
    results = {'Dynamic Programming': {'time': {}, 'memory': {}},
               'Branch and Bound': {'time': {}, 'memory': {}}}

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    for size in sizes:
        file_name = f'{data_folder}/dataset_{size}.txt'
        dataset = generate_and_save_dataset(size, file_name)
        print(f"Dataset size: {size}")

        # Measure Dynamic Programming
        dataset_dp = dataset.copy()
        time_dp, mem_dp, _ = measure_time_and_memory(find_partition_dynamic_programming, dataset_dp, size)
        print(f"Dynamic Programming - Time: {time_dp} ms, Memory: {mem_dp} bytes")

        results['Dynamic Programming']['time'][size] = time_dp
        results['Dynamic Programming']['memory'][size] = mem_dp

        # Measure Branch and Bound
        dataset_bb = dataset.copy()
        time_bb, mem_bb, _ = measure_time_and_memory(bnb_final, dataset_bb)
        print(f"Branch and Bound - Time: {time_bb} ms, Memory: {mem_bb} bytes")

        results['Branch and Bound']['time'][size] = time_bb
        results['Branch and Bound']['memory'][size] = mem_bb

        print()

    plot_results(sizes, results)
    
    
def plot_results(sizes, results, file_name='subset_sum_performance_results.png'):
    fig, axs = plt.subplots(2)

    axs[0].set_title('Execution Time Comparison')
    axs[0].set_xlabel('Dataset Size')
    axs[0].set_ylabel('Time (ms)')

    axs[1].set_title('Memory Consumption Comparison')
    axs[1].set_xlabel('Dataset Size')
    axs[1].set_ylabel('Memory (bytes)')

    for algo_name, algo_results in results.items():
        time_values = [algo_results['time'][size] for size in sizes]
        memory_values = [algo_results['memory'][size] for size in sizes]

        axs[0].plot(sizes, time_values, label=algo_name)
        axs[1].plot(sizes, memory_values, label=algo_name)

    axs[0].legend()
    axs[1].legend()

    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()

    
if __name__ == "__main__":
    sizes = [10, 40, 80]
    data_folder = 'datasets'
    
    analyze_subset_sum_algorithms(sizes, data_folder)
