"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)
Author: Oleksii Onasenko
Developer: SubstanceNet
"""
"""
Verify CP calculations against Hoel's expected values
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))

import numpy as np
from ce2_core import coarse_grain_tpm, calculate_cp, calculate_determinism, calculate_degeneracy
from six_state_two_cycle import create_two_cycle_tpm

def verify_microscale(T):
    """Verify microscale CP calculation"""
    cp_micro = calculate_cp(T)
    det = calculate_determinism(T)
    deg = calculate_degeneracy(T)
    spec = 1.0 - deg
    
    print("="*60)
    print("MICROSCALE VERIFICATION")
    print("="*60)
    print(f"Partition: individual states {tuple((i,) for i in range(6))}")
    print(f"Determinism: {det:.6f}")
    print(f"Degeneracy: {deg:.6f}")
    print(f"Specificity: {spec:.6f}")
    print(f"CP = Det + Spec - 1 = {det:.4f} + {spec:.4f} - 1 = {cp_micro:.6f}")
    print()
    return cp_micro

def verify_macroscale(T):
    """Verify optimal macroscale CP calculation"""
    optimal_partition = ((0,1,2), (3,4,5))
    T_macro = coarse_grain_tpm(T, optimal_partition)
    cp_macro = calculate_cp(T_macro)
    det = calculate_determinism(T_macro)
    deg = calculate_degeneracy(T_macro)
    spec = 1.0 - deg
    
    print("="*60)
    print("OPTIMAL MACROSCALE VERIFICATION")
    print("="*60)
    print(f"Partition: {optimal_partition}")
    print(f"Coarse-grained TPM:")
    print(T_macro)
    print(f"Determinism: {det:.6f}")
    print(f"Degeneracy: {deg:.6f}")
    print(f"Specificity: {spec:.6f}")
    print(f"CP = Det + Spec - 1 = {det:.4f} + {spec:.4f} - 1 = {cp_macro:.6f}")
    print()
    return cp_macro

def main():
    print("\n" + "="*60)
    print("CP VALUES VERIFICATION")
    print("="*60 + "\n")
    
    # Create TPM
    T = create_two_cycle_tpm(p_self=0.2)
    print("6-state Two 3-Cycles System (p_self=0.2)")
    print()
    
    cp_micro = verify_microscale(T)
    cp_macro = verify_macroscale(T)
    
    delta_cp = cp_macro - cp_micro
    
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print(f"CP(microscale): {cp_micro:.6f}")
    print(f"CP(macroscale): {cp_macro:.6f}")
    print(f"ΔCP: {delta_cp:.6f}")
    print()
    
    # Expected values from paper
    print("Expected (from Hoel's Figure 2):")
    print("  CP(micro) ≈ 0.72")
    print("  CP(optimal) = 1.00")
    print()
    
    if abs(cp_micro - 0.7207) < 0.01 and abs(cp_macro - 1.0) < 0.01:
        print("[VERIFIED] Values match expected!")
    else:
        print("[WARNING] Values differ from expected")

if __name__ == "__main__":
    main()
