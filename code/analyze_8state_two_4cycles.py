"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
Sensitivity Analysis: 8-state Two Length-4 Cycles
Параметр: p_self (probability of staying in current state)
Діапазон: [0.0, 0.5] з кроком 0.05

Reference: Engineering Emergence, Hoel & Jansma (2025), Figure 3(ii)
"""

import numpy as np
import sys
import os
from pathlib import Path
import pickle

# Додаємо шлях до модулів
sys.path.insert(0, str(Path(__file__).parent))

from ce2_core import calculate_cp, calculate_determinism, calculate_degeneracy, coarse_grain_tpm
from algorithm1_brute_force import run_algorithm1

def create_two_cycle_tpm(n_states=8, p_self=0.2):
    """
    Створює TPM для системи з двома length-4 циклами.
    
    Cycle 1: 0→1→2→3→0 (states {0,1,2,3})
    Cycle 2: 4→5→6→7→4 (states {4,5,6,7})
    
    Parameters:
    -----------
    n_states : int
        Number of states (повинно бути 8)
    p_self : float
        Probability of staying in current state
        
    Returns:
    --------
    tpm : ndarray
        Transition probability matrix (8x8)
    """
    if n_states != 8:
        raise ValueError("This system requires exactly 8 states")
    
    p_next = 1.0 - p_self
    tpm = np.zeros((n_states, n_states))
    
    # Cycle 1: 0→1→2→3→0
    cycle1_transitions = [(0,1), (1,2), (2,3), (3,0)]
    for current, next_state in cycle1_transitions:
        tpm[next_state, current] = p_next
        tpm[current, current] = p_self
    
    # Cycle 2: 4→5→6→7→4
    cycle2_transitions = [(4,5), (5,6), (6,7), (7,4)]
    for current, next_state in cycle2_transitions:
        tpm[next_state, current] = p_next
        tpm[current, current] = p_self
    
    return tpm

def analyze_single_p_self(p_self, verbose=True):
    """
    Аналізує систему для заданого p_self.
    
    Returns:
    --------
    results : dict
        Містить CP metrics та emergent hierarchy info
    """
    # Створюємо TPM
    tpm = create_two_cycle_tpm(n_states=8, p_self=p_self)
    
    # Обчислюємо CP для microscale
    det_micro = calculate_determinism(tpm); deg_micro = calculate_degeneracy(tpm); cp_micro = calculate_cp(tpm)
    
    # Coarse-grain до оптимального макромасштабу ((0,1,2,3), (4,5,6,7))
    optimal_partition = ((0,1,2,3), (4,5,6,7))
    tpm_macro = coarse_grain_tpm(tpm, optimal_partition)
    det_macro = calculate_determinism(tpm_macro); deg_macro = calculate_degeneracy(tpm_macro); cp_macro = calculate_cp(tpm_macro)
    
    delta_cp = cp_macro - cp_micro
    
    # Запускаємо Algorithm 1 для повного аналізу
    if verbose:
        print(f"\n{'='*60}")
        print(f"p_self = {p_self:.2f}")
        print(f"{'='*60}")
    
    algo_results = run_algorithm1(tpm)
    
    # Виключаємо microscale з emergent scales
    microscale = tuple((i,) for i in range(8))
    emergent_corrected = [p for p in algo_results['emergent'] 
                         if p != microscale]
    n_emergent_corrected = len(emergent_corrected)
    
    results = {
        'p_self': p_self,
        'cp_micro': cp_micro,
        'det_micro': det_micro,
        'deg_micro': deg_micro,
        'cp_macro': cp_macro,
        'det_macro': det_macro,
        'deg_macro': deg_macro,
        'delta_cp': delta_cp,
        'n_emergent': len(algo_results['emergent']),
        'n_emergent_corrected': n_emergent_corrected,
        'emergent_partitions': emergent_corrected,
        'tpm': tpm,
        'tpm_macro': tpm_macro
    }
    
    if verbose:
        print(f"\nMICROSCALE:")
        print(f"  Determinism: {det_micro:.4f}")
        print(f"  Degeneracy:  {deg_micro:.4f}")
        print(f"  CP:          {cp_micro:.4f}")
        print(f"\nMACROSCALE (optimal):")
        print(f"  Determinism: {det_macro:.4f}")
        print(f"  Degeneracy:  {deg_macro:.4f}")
        print(f"  CP:          {cp_macro:.4f}")
        print(f"\nΔCP: {delta_cp:.4f}")
        print(f"Emergent scales (corrected): {n_emergent_corrected}")
    
    return results

def run_sensitivity_analysis():
    """
    Запускає повний sensitivity analysis.
    """
    print("="*70)
    print("SENSITIVITY ANALYSIS: 8-state Two Length-4 Cycles")
    print("Parameter: p_self (probability of staying in current state)")
    print("="*70)
    
    # Діапазон значень p_self
    p_self_values = np.arange(0.0, 0.55, 0.05)
    
    all_results = []
    
    for p_self in p_self_values:
        results = analyze_single_p_self(p_self, verbose=False)
        all_results.append(results)
        
        # Короткий вивід
        print(f"p_self={p_self:.2f} | "
              f"CP(micro)={results['cp_micro']:.4f} | "
              f"CP(macro)={results['cp_macro']:.4f} | "
              f"ΔCP={results['delta_cp']:.4f} | "
              f"Emergent={results['n_emergent_corrected']}")
    
    # Зберігаємо результати
    output_dir = Path(__file__).parent.parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "sensitivity_analysis_8state.pkl"
    with open(output_file, 'wb') as f:
        pickle.dump(all_results, f)
    
    print(f"\n{'='*70}")
    print(f"Результати збережено: {output_file}")
    print(f"Total configurations analyzed: {len(all_results)}")
    print(f"{'='*70}")
    
    return all_results

if __name__ == "__main__":
    results = run_sensitivity_analysis()
