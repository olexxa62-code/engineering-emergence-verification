"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
Аналіз 10-state системи через BRANCHING GREEDY
(brute force НЕ підходить для n≥10)
"""
import sys
import pickle
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ce2_core import calculate_cp, calculate_determinism, calculate_degeneracy, coarse_grain_tpm
from algorithm2_greedy import run_greedy_algorithm

sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))
from ten_state_two_five_cycles import create_two_five_cycle_tpm, get_optimal_partition

def main():
    print("\n" + "="*70)
    print("АНАЛІЗ: 10-state Two 5-Cycles (BRANCHING GREEDY)")
    print("="*70)
    
    p_self = 0.20
    print(f"\nПараметри: p_self = {p_self}")
    tpm = create_two_five_cycle_tpm(p_self=p_self)
    
    # Microscale
    print("\nMICROSCALE:")
    cp_micro = calculate_cp(tpm)
    det_micro = calculate_determinism(tpm)
    deg_micro = calculate_degeneracy(tpm)
    print(f"  CP(micro) = {cp_micro:.4f}")
    
    # Optimal macroscale
    optimal = get_optimal_partition()
    tpm_macro = coarse_grain_tpm(tpm, optimal)
    cp_macro = calculate_cp(tpm_macro)
    det_macro = calculate_determinism(tpm_macro)
    deg_macro = calculate_degeneracy(tpm_macro)
    delta_cp = cp_macro - cp_micro
    
    print("\nOPTIMAL MACROSCALE:")
    print(f"  Partition = {optimal}")
    print(f"  CP(macro) = {cp_macro:.4f}")
    print(f"  ΔCP       = {delta_cp:.4f}")
    
    # Greedy algorithm
    print("\n" + "-"*70)
    print("Запускаю Branching Greedy Algorithm (n_paths=100)...")
    print("-"*70)
    
    results = run_greedy_algorithm(tpm, n_paths=100)
    
    # Виключаємо microscale
    microscale = tuple((i,) for i in range(10))
    emergent = [p for p in results['emergent'] if p != microscale]
    
    print("\n" + "="*70)
    print("РЕЗУЛЬТАТИ:")
    print("="*70)
    print(f"Partitions sampled:      {len(results['cp_dict'])}")
    print(f"Emergent scales (RAW):   {len(results['emergent'])}")
    print(f"Emergent scales (CORR):  {len(emergent)}")
    print()
    
    # Показуємо emergent scales
    print("EMERGENT SCALES:")
    for i, part in enumerate(emergent[:5], 1):
        cp = results['cp_dict'][part]
        dcp = results['delta_cp_dict'][part]
        print(f"  {i}. dim={len(part)}, CP={cp:.4f}, ΔCP={dcp:.4f}")
    
    if len(emergent) > 5:
        print(f"  ... та ще {len(emergent)-5} scales")
    
    # Збираємо дані для збереження
    output_data = {
        'n_states': 10,
        'cycle_length': 5,
        'p_self': p_self,
        'cp_micro': cp_micro,
        'det_micro': det_micro,
        'deg_micro': deg_micro,
        'cp_optimal': cp_macro,
        'det_optimal': det_macro,
        'deg_optimal': deg_macro,
        'delta_cp': delta_cp,
        'optimal_partition': optimal,
        'n_emergent_raw': len(results['emergent']),
        'n_emergent': len(emergent),
        'emergent_partitions': emergent,
        'hierarchy_type': 'Balloon' if len(emergent) == 1 else 'Complex',
        'n_partitions_sampled': len(results['cp_dict'])
    }
    
    # Зберігаємо результати
    output_file = Path("results/results_10state_two_5cycles.pkl")
    with open(output_file, 'wb') as f:
        pickle.dump(output_data, f)
    
    print(f"\n✓ Збережено: {output_file}")
    
    print("\n" + "="*70)
    print("ПОРІВНЯННЯ:")
    print("-"*70)
    print("System              | Length | Emergent | Type")
    print("-"*70)
    print("6-state (3-cycles)  |   3    |    3     | Complex")
    print("8-state (4-cycles)  |   4    |    1     | Balloon")
    print(f"10-state (5-cycles) |   5    |    {len(emergent)}     | {output_data['hierarchy_type']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
