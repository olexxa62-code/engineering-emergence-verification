"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

"""
Causal Emergence 2.0 - Core Implementation
Based on: Engineering Emergence (Jansma & Hoel, 2025)
"""

import numpy as np
from itertools import combinations
from typing import List, Tuple, Dict, Set
import networkx as nx

def generate_all_partitions(n: int) -> List[Tuple[Tuple[int, ...], ...]]:
    """
    Generate all partitions of set {0, 1, ..., n-1}.
    Returns list of partitions, each partition is tuple of tuples.
    """
    def partition_helper(items):
        if len(items) == 0:
            yield tuple()
            return
        
        first = items[0]
        rest = items[1:]
        
        for smaller_partition in partition_helper(rest):
            # Add first to existing block
            for i, block in enumerate(smaller_partition):
                new_partition = list(smaller_partition)
                new_partition[i] = tuple(sorted(block + (first,)))
                yield tuple(sorted(new_partition))
            # Create new block
            yield tuple(sorted(smaller_partition + ((first,),)))
    
    items = list(range(n))
    unique_partitions = set(partition_helper(items))
    return sorted(list(unique_partitions))


def coarse_grain_tpm(T: np.ndarray, partition: Tuple[Tuple[int, ...], ...]) -> np.ndarray:
    """
    Coarse-grain TPM T according to partition.
    T: n×n transition probability matrix
    partition: tuple of tuples, each inner tuple is a macrostate
    Returns: k×k coarse-grained TPM where k = len(partition)
    """
    n = T.shape[0]
    k = len(partition)
    T_macro = np.zeros((k, k))
    
    # Build mapping from microstate to macrostate index
    micro_to_macro = {}
    for macro_idx, block in enumerate(partition):
        for micro_idx in block:
            micro_to_macro[micro_idx] = macro_idx
    
    # Coarse-grain: sum probabilities
    for i in range(n):
        for j in range(n):
            macro_i = micro_to_macro[i]
            macro_j = micro_to_macro[j]
            T_macro[macro_i, macro_j] += T[i, j]
    
    # Normalize rows
    for i in range(k):
        row_sum = T_macro[i, :].sum()
        if row_sum > 0:
            T_macro[i, :] /= row_sum
    
    return T_macro

def calculate_determinism(T: np.ndarray) -> float:
    """
    Calculate determinism of TPM T.
    determinism = 1 - H(E|C) / log2(n)
    """
    n = T.shape[0]
    if n == 1:
        return 1.0
    
    H_E_given_C = 0.0
    for i in range(n):
        for j in range(n):
            if T[i, j] > 0:
                H_E_given_C -= T[i, j] * np.log2(T[i, j])
    
    H_E_given_C /= n  # Average over uniform p(C)
    determinism = 1.0 - H_E_given_C / np.log2(n)
    
    return determinism

def calculate_degeneracy(T: np.ndarray) -> float:
    """
    Calculate degeneracy of TPM T.
    degeneracy = 1 - H(E) / log2(n)
    """
    n = T.shape[0]
    if n == 1:
        return 1.0
    
    # Marginal distribution over effects (uniform prior over causes)
    T_e = T.mean(axis=0)
    
    H_E = 0.0
    for prob in T_e:
        if prob > 0:
            H_E -= prob * np.log2(prob)
    
    degeneracy = 1.0 - H_E / np.log2(n)
    
    return degeneracy

def calculate_cp(T: np.ndarray) -> float:
    """
    Calculate causal primitives (CP) of TPM T.
    CP = determinism + specificity - 1
       = determinism + (1 - degeneracy) - 1
       = determinism - degeneracy
    """
    det = calculate_determinism(T)
    deg = calculate_degeneracy(T)
    specificity = 1.0 - deg
    cp = det + specificity - 1.0
    
    return cp

