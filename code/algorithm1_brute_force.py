"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

"""
Algorithm 1: Calculating ΔCP(T) - Brute Force
Full enumeration of all partitions
"""

import numpy as np
import networkx as nx
from typing import List, Tuple, Dict
from ce2_core import (
    generate_all_partitions,
    coarse_grain_tpm,
    calculate_cp
)

def build_refinement_graph(partitions: List[Tuple[Tuple[int, ...], ...]]) -> nx.DiGraph:
    """
    Build Hasse diagram (refinement lattice).
    Edge from πa to πb if πa refines πb (πa ≤ πb).
    """
    G = nx.DiGraph()
    
    for p in partitions:
        G.add_node(p)
    
    # Check refinement relation
    for i, pa in enumerate(partitions):
        for j, pb in enumerate(partitions):
            if i == j:
                continue
            # Check if pa ≤ pb (pa refines pb)
            if is_refinement(pa, pb):
                G.add_edge(pa, pb)
    
    # Transitive reduction to get Hasse diagram
    G = nx.transitive_reduction(G)
    
    return G

def is_refinement(pa: Tuple, pb: Tuple) -> bool:
    """
    Check if pa refines pb: ∀b ∈ pb : ∃a ∈ pa s.t. a ⊆ b
    """
    for block_b in pb:
        found = False
        for block_a in pa:
            if set(block_a).issubset(set(block_b)):
                found = True
                break
        if not found:
            return False
    return True

def calculate_delta_cp(
    T: np.ndarray,
    partitions: List[Tuple],
    cp_dict: Dict[Tuple, float],
    G: nx.DiGraph
) -> Dict[Tuple, float]:
    """
    Calculate ΔCP for each partition relative to its ancestors.
    """
    delta_cp_dict = {}
    
    for p in partitions:
        # Get all ancestors (all nodes reachable from p going backwards)
        ancestors = list(nx.ancestors(G, p))
        
        if len(ancestors) == 0:
            baseline = 0.0
        else:
            baseline = max([cp_dict[a] for a in ancestors])
        
        delta_cp_dict[p] = cp_dict[p] - baseline
    
    return delta_cp_dict

def run_algorithm1(T: np.ndarray, epsilon: float = 1e-10) -> Dict:
    """
    Run Algorithm 1: Full brute force calculation of emergent hierarchy.
    
    Returns dict with:
        - partitions: all partitions
        - cp_dict: CP values
        - delta_cp_dict: ΔCP values
        - emergent: partitions with ΔCP > epsilon
        - graph: refinement graph
    """
    n = T.shape[0]
    print(f"Starting Algorithm 1 for n={n} states...")
    
    # Step 1: Generate all partitions
    print("Step 1: Generating all partitions...")
    partitions = generate_all_partitions(n)
    print(f"  Generated {len(partitions)} partitions (Bell number B({n}))")
    
    # Step 2: Compute CP for each partition
    print("Step 2: Computing CP for all partitions...")
    cp_dict = {}
    for p in partitions:
        T_coarse = coarse_grain_tpm(T, p)
        cp_dict[p] = calculate_cp(T_coarse)
    print(f"  Computed CP for {len(cp_dict)} partitions")
    
    # Step 3: Build refinement graph
    print("Step 3: Building refinement lattice...")
    G = build_refinement_graph(partitions)
    print(f"  Built graph with {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Step 4: Calculate ΔCP
    print("Step 4: Computing ΔCP relative to ancestors...")
    delta_cp_dict = calculate_delta_cp(T, partitions, cp_dict, G)
    
    # Step 5: Emergent set
    print("Step 5: Extracting emergent hierarchy...")
    emergent = [p for p in partitions if delta_cp_dict[p] > epsilon]
    print(f"  Found {len(emergent)} emergent scales (ΔCP > {epsilon})")
    
    return {
        'partitions': partitions,
        'cp_dict': cp_dict,
        'delta_cp_dict': delta_cp_dict,
        'emergent': emergent,
        'graph': G,
        'n': n
    }

print("Algorithm 1 module loaded")
