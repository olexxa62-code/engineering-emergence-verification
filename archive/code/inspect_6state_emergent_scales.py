#!/usr/bin/env python3
"""Інспекція emergent scales в 6-state системі"""
import sys
import pickle
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ce2_core import calculate_cp
from algorithm1_brute_force import run_algorithm1

sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))
from six_state_two_cycle import create_two_cycle_tpm

def main():
    print("\n" + "="*70)
    print("EMERGENT SCALES ІНСПЕКЦІЯ: 6-state Two 3-Cycles")
    print("="*70)
    
    # Створюємо TPM для baseline
    tpm = create_two_cycle_tpm(p_self=0.20)
    results = run_algorithm1(tpm)
    
    # Виключаємо microscale
    microscale = tuple((i,) for i in range(6))
    emergent = [p for p in results['emergent'] if p != microscale]
    
    print(f"\nTotal emergent scales (excl. microscale): {len(emergent)}\n")
    
    # Показуємо кожен emergent scale
    for i, partition in enumerate(emergent, 1):
        cp = results['cp_dict'][partition]
        delta_cp = results['delta_cp_dict'][partition]
        dimensionality = len(partition)
        
        print(f"Scale {i}:")
        print(f"  Partition: {partition}")
        print(f"  Dimensionality: {dimensionality}")
        print(f"  CP: {cp:.4f}")
        print(f"  ΔCP: {delta_cp:.4f}")
        print()
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
