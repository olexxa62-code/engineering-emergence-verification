"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
ВИПРАВЛЕНИЙ Algorithm 2 & 3: Branching Greedy
"""
import numpy as np
from itertools import combinations
from ce2_core import calculate_cp, coarse_grain_tpm

def greedy_completion(tpm, start_partition):
    """Algorithm 2: GreedyCompletion"""
    current = start_partition
    path = [current]
    cp_list = [calculate_cp(coarse_grain_tpm(tpm, current))]
    
    while len(current) > 1:
        k = len(current)
        best_cp = -np.inf
        best_partition = None
        
        for i, j in combinations(range(k), 2):
            new_partition = []
            merged_block = tuple(sorted(current[i] + current[j]))
            
            for idx in range(k):
                if idx == i:
                    new_partition.append(merged_block)
                elif idx != j:
                    new_partition.append(current[idx])
            
            new_partition = tuple(sorted(new_partition, key=lambda x: x[0]))
            
            tpm_coarse = coarse_grain_tpm(tpm, new_partition)
            cp = calculate_cp(tpm_coarse)
            
            if cp > best_cp:
                best_cp = cp
                best_partition = new_partition
        
        current = best_partition
        path.append(current)
        cp_list.append(best_cp)
    
    return path, cp_list

def run_greedy_algorithm(tpm, n_paths=100, verbose=True):
    """Algorithm 3: Branching Greedy з паралельними шляхами"""
    n = tpm.shape[0]
    
    if verbose:
        print(f"Starting Branching Greedy for n={n} states...")
        print(f"Number of parallel paths: {n_paths}")
    
    microscale = tuple((i,) for i in range(n))
    cp_dict = {microscale: calculate_cp(tpm)}
    
    current = microscale
    path_count = 0
    
    while len(current) > 1:
        k = len(current)
        candidates = []
        
        for i, j in combinations(range(k), 2):
            new_partition = []
            merged_block = tuple(sorted(current[i] + current[j]))
            
            for idx in range(k):
                if idx == i:
                    new_partition.append(merged_block)
                elif idx != j:
                    new_partition.append(current[idx])
            
            new_partition = tuple(sorted(new_partition, key=lambda x: x[0]))
            
            tpm_coarse = coarse_grain_tpm(tpm, new_partition)
            cp = calculate_cp(tpm_coarse)
            
            candidates.append((cp, new_partition))
            
            if new_partition not in cp_dict:
                cp_dict[new_partition] = cp
        
        candidates.sort(reverse=True, key=lambda x: x[0])
        top_n = min(n_paths, len(candidates))
        selected = [c[1] for c in candidates[:top_n]]
        
        for start_partition in selected:
            if path_count >= n_paths:
                break
                
            path, cp_list = greedy_completion(tpm, start_partition)
            path_count += 1
            
            for partition, cp in zip(path, cp_list):
                if partition not in cp_dict:
                    cp_dict[partition] = cp
        
        current = selected[0] if selected else current
        
        if verbose and len(current) % 2 == 0:
            print(f"  Progress: dimensionality {len(current)}, sampled {len(cp_dict)} partitions")
    
    if verbose:
        print(f"Completed: {len(cp_dict)} unique partitions sampled")
    
    # ВИПРАВЛЕНИЙ обчислення ΔCP
    delta_cp_dict = {}
    
    for partition in cp_dict.keys():
        max_ancestor_cp = 0.0
        
        for other in cp_dict.keys():
            # ВИКЛЮЧАЄМО себе!
            if other == partition:
                continue
                
            if is_refinement(partition, other):
                max_ancestor_cp = max(max_ancestor_cp, cp_dict[other])
        
        delta_cp_dict[partition] = cp_dict[partition] - max_ancestor_cp
    
    threshold = 1e-10
    emergent = [p for p in cp_dict.keys() if delta_cp_dict[p] > threshold]
    
    if verbose:
        print(f"Found {len(emergent)} emergent scales (ΔCP > {threshold})")
    
    return {
        'cp_dict': cp_dict,
        'delta_cp_dict': delta_cp_dict,
        'emergent': emergent,
        'n_sampled': len(cp_dict)
    }

def is_refinement(partition_a, partition_b):
    """
    Перевіряє чи partition_b є refinement partition_a
    (тобто partition_b більш дрібна, тобто ancestor)
    """
    for block_b in partition_b:
        found = False
        for block_a in partition_a:
            if set(block_b).issubset(set(block_a)):
                found = True
                break
        if not found:
            return False
    
    return len(partition_b) >= len(partition_a)

if __name__ == "__main__":
    print("FIXED Branching Greedy Algorithm module loaded")
