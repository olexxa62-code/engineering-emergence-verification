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
    print(f"  CP(micro) = {cp_micro:.4f}")
    
    # Optimal macroscale
    optimal = get_optimal_partition()
    tpm_macro = coarse_grain_tpm(tpm, optimal)
    cp_macro = calculate_cp(tpm_macro)
    delta_cp = cp_macro - cp_micro
    
    print("\nOPTIMAL MACROSCALE:")
    print(f"  Partition = {optimal}")
    print(f"  CP(macro) = {cp_macro:.4f}")
    print(f"  ΔCP       = {delta_cp:.4f}")
    
    # Greedy algorithm (швидко!)
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
    for i, part in enumerate(emergent[:5], 1):  # top 5
        cp = results['cp_dict'][part]
        dcp = results['delta_cp_dict'][part]
        print(f"  {i}. dim={len(part)}, CP={cp:.4f}, ΔCP={dcp:.4f}")
    
    if len(emergent) > 5:
        print(f"  ... та ще {len(emergent)-5} scales")
    
    print("\n" + "="*70)
    print("ПОРІВНЯННЯ:")
    print("-"*70)
    print("System              | Length | Emergent | Type")
    print("-"*70)
    print("6-state (3-cycles)  |   3    |    3     | Complex")
    print("8-state (4-cycles)  |   4    |    1     | Balloon")
    print(f"10-state (5-cycles) |   5    |    {len(emergent)}     | {'Balloon' if len(emergent)==1 else 'Complex'}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
