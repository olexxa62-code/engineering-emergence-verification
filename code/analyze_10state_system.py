"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
Аналіз 10-state two 5-cycles системи
Тестуємо гіпотезу про вплив довжини циклу
"""
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ce2_core import calculate_cp, calculate_determinism, calculate_degeneracy, coarse_grain_tpm
from algorithm1_brute_force import run_algorithm1

sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))
from ten_state_two_five_cycles import create_two_five_cycle_tpm, get_optimal_partition

def main():
    print("\n" + "="*70)
    print("АНАЛІЗ: 10-state Two 5-Cycles")
    print("="*70)
    
    # Створюємо TPM
    p_self = 0.20
    print(f"\nПараметри: p_self = {p_self}")
    tpm = create_two_five_cycle_tpm(p_self=p_self)
    
    # Microscale метрики
    print("\nMICROSCALE метрики:")
    cp_micro = calculate_cp(tpm)
    det_micro = calculate_determinism(tpm)
    deg_micro = calculate_degeneracy(tpm)
    spec_micro = 1 - deg_micro
    
    print(f"  CP(micro)   = {cp_micro:.4f}")
    print(f"  Determinism = {det_micro:.4f}")
    print(f"  Specificity = {spec_micro:.4f}")
    
    # Optimal macroscale
    optimal_partition = get_optimal_partition()
    tpm_macro = coarse_grain_tpm(tpm, optimal_partition)
    
    print("\nOPTIMAL MACROSCALE метрики:")
    cp_macro = calculate_cp(tpm_macro)
    det_macro = calculate_determinism(tpm_macro)
    deg_macro = calculate_degeneracy(tpm_macro)
    spec_macro = 1 - deg_macro
    
    print(f"  Partition   = {optimal_partition}")
    print(f"  CP(macro)   = {cp_macro:.4f}")
    print(f"  Determinism = {det_macro:.4f}")
    print(f"  Specificity = {spec_macro:.4f}")
    print(f"  ΔCP         = {cp_macro - cp_micro:.4f}")
    
    # Algorithm 1 (це займе час!)
    print("\n" + "-"*70)
    print("Запускаю Algorithm 1...")
    print("ПОПЕРЕДЖЕННЯ: 10 states = 115,975 партицій, це займе ~5-10 хвилин")
    print("-"*70)
    
    algo_results = run_algorithm1(tpm)
    
    # Виключаємо microscale
    microscale = tuple((i,) for i in range(10))
    emergent_corrected = [p for p in algo_results['emergent'] if p != microscale]
    n_emergent = len(emergent_corrected)
    
    print("\n" + "="*70)
    print("РЕЗУЛЬТАТИ:")
    print("="*70)
    print(f"Total partitions analyzed: {len(algo_results['cp_dict'])}")
    print(f"Emergent scales (RAW):     {len(algo_results['emergent'])}")
    print(f"Emergent scales (CORR):    {n_emergent}")
    print()
    
    # Показуємо детально emergent scales
    print("EMERGENT HIERARCHY STRUCTURE:")
    print("-"*70)
    for i, partition in enumerate(emergent_corrected, 1):
        cp = algo_results['cp_dict'][partition]
        delta_cp = algo_results['delta_cp_dict'][partition]
        dim = len(partition)
        
        print(f"Scale {i}:")
        print(f"  Partition: {partition}")
        print(f"  Dimensionality: {dim}")
        print(f"  CP:    {cp:.4f}")
        print(f"  ΔCP:   {delta_cp:.4f}")
        print()
    
    print("="*70)
    
    # Порівняння з іншими системами
    print("\nПОРІВНЯННЯ З ІНШИМИ СИСТЕМАМИ:")
    print("-"*70)
    print("System               | Cycle length | Emergent scales | Hierarchy type")
    print("-"*70)
    print("6-state (3-cycles)   |      3       |        3        | Complex")
    print("8-state (4-cycles)   |      4       |        1        | Balloon")
    print(f"10-state (5-cycles)  |      5       |        {n_emergent}        | {'Balloon' if n_emergent == 1 else 'Complex'}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
