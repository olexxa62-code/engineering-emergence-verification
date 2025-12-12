"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
ВИПРАВЛЕНИЙ Sensitivity Analysis для 6-state System
З правильним виключенням microscale
"""
import sys
import numpy as np
import pickle
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ce2_core import calculate_cp, calculate_determinism, calculate_degeneracy, coarse_grain_tpm
from algorithm1_brute_force import run_algorithm1

sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))
from six_state_two_cycle import create_two_cycle_tpm

def analyze_single_p_self(p_self):
    """Аналізує 6-state систему для заданого p_self"""
    # Створюємо TPM
    tpm = create_two_cycle_tpm(p_self=p_self)
    
    # CP для microscale
    det_micro = calculate_determinism(tpm)
    deg_micro = calculate_degeneracy(tpm)
    cp_micro = calculate_cp(tpm)
    
    # Optimal macroscale ((0,1,2), (3,4,5))
    optimal_partition = ((0,1,2), (3,4,5))
    tpm_macro = coarse_grain_tpm(tpm, optimal_partition)
    det_macro = calculate_determinism(tpm_macro)
    deg_macro = calculate_degeneracy(tpm_macro)
    cp_macro = calculate_cp(tpm_macro)
    
    delta_cp = cp_macro - cp_micro
    
    # Algorithm 1 з правильним виключенням microscale
    algo_results = run_algorithm1(tpm)
    
    # ВИКЛЮЧАЄМО MICROSCALE!
    microscale = tuple((i,) for i in range(6))
    emergent_corrected = [p for p in algo_results['emergent'] if p != microscale]
    n_emergent_corrected = len(emergent_corrected)
    
    return {
        'p_self': p_self,
        'cp_micro': cp_micro,
        'det_micro': det_micro,
        'deg_micro': deg_micro,
        'cp_macro': cp_macro,
        'det_macro': det_macro,
        'deg_macro': deg_macro,
        'delta_cp': delta_cp,
        'n_emergent_raw': len(algo_results['emergent']),
        'n_emergent_corrected': n_emergent_corrected,
        'emergent_partitions': emergent_corrected
    }

def main():
    print("="*70)
    print("CORRECTED SENSITIVITY ANALYSIS: 6-state Two 3-Cycles")
    print("З правильним виключенням microscale")
    print("="*70)
    
    p_self_values = np.arange(0.0, 0.55, 0.05)
    all_results = []
    
    for p_self in p_self_values:
        print(f"\nАналізую p_self = {p_self:.2f}...")
        results = analyze_single_p_self(p_self)
        all_results.append(results)
        
        print(f"  CP(micro)={results['cp_micro']:.4f} | "
              f"CP(macro)={results['cp_macro']:.4f} | "
              f"ΔCP={results['delta_cp']:.4f}")
        print(f"  Emergent: RAW={results['n_emergent_raw']}, "
              f"CORRECTED={results['n_emergent_corrected']}")
    
    # Зберігаємо
    output_file = Path("results/sensitivity_analysis_6state_corrected.pkl")
    with open(output_file, 'wb') as f:
        pickle.dump(all_results, f)
    
    print(f"\n{'='*70}")
    print(f"Збережено: {output_file}")
    print(f"Total configurations: {len(all_results)}")
    print(f"{'='*70}\n")
    
    return all_results

if __name__ == "__main__":
    main()
