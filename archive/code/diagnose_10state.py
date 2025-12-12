#!/usr/bin/env python3
"""
Діагностика: чому greedy algorithm не знаходить emergent scales
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ce2_core import calculate_cp, coarse_grain_tpm
from algorithm2_greedy import run_greedy_algorithm

sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))
from ten_state_two_five_cycles import create_two_five_cycle_tpm, get_optimal_partition

def main():
    print("\n" + "="*70)
    print("ДІАГНОСТИКА: 10-state Greedy Algorithm")
    print("="*70)
    
    tpm = create_two_five_cycle_tpm(p_self=0.2)
    optimal = get_optimal_partition()
    
    print(f"\nOptimal partition: {optimal}")
    
    # Запускаємо greedy
    results = run_greedy_algorithm(tpm, n_paths=100, verbose=False)
    
    print(f"\nTotal sampled: {results['n_sampled']}")
    print(f"Emergent (raw): {len(results['emergent'])}")
    
    # Перевіряємо чи optimal є в cp_dict
    if optimal in results['cp_dict']:
        cp = results['cp_dict'][optimal]
        delta_cp = results['delta_cp_dict'][optimal]
        print(f"\nOptimal partition ЗНАЙДЕНО:")
        print(f"  CP = {cp:.4f}")
        print(f"  ΔCP = {delta_cp:.4f}")
    else:
        print(f"\nOptimal partition НЕ ЗНАЙДЕНО в sampled partitions!")
    
    # Перевіряємо microscale
    microscale = tuple((i,) for i in range(10))
    if microscale in results['cp_dict']:
        cp_micro = results['cp_dict'][microscale]
        delta_micro = results['delta_cp_dict'][microscale]
        print(f"\nMicroscale:")
        print(f"  CP = {cp_micro:.4f}")
        print(f"  ΔCP = {delta_micro:.4f}")
    
    # Топ-5 за ΔCP
    print("\n" + "-"*70)
    print("TOP 5 партицій за ΔCP:")
    print("-"*70)
    
    sorted_by_delta = sorted(results['delta_cp_dict'].items(), 
                             key=lambda x: x[1], reverse=True)
    
    for i, (part, dcp) in enumerate(sorted_by_delta[:5], 1):
        cp = results['cp_dict'][part]
        print(f"{i}. dim={len(part)}, CP={cp:.4f}, ΔCP={dcp:.4f}")
        if len(part) <= 3:
            print(f"   {part}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
