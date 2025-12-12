"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

"""
Verify CP calculations against Hoel's expected values
"""

import sys
sys.path.insert(0, './stage1_hoel_verification/code')
sys.path.insert(0, './stage1_hoel_verification/data')

import numpy as np
from ce2_core import coarse_grain_tpm, calculate_cp, calculate_determinism, calculate_degeneracy
from six_state_two_cycle import create_two_cycle_tpm, get_expected_values

def verify_microscale(T, expected):
    """Verify microscale CP calculation"""
    cp_micro = calculate_cp(T)
    det = calculate_determinism(T)
    deg = calculate_degeneracy(T)
    spec = 1.0 - deg
    
    print("="*60)
    print("MICROSCALE VERIFICATION")
    print("="*60)
    print(f"Partition: individual states {tuple((i,) for i in range(6))}")
    print(f"\nCalculated:")
    print(f"  Determinism: {det:.4f}")
    print(f"  Degeneracy:  {deg:.4f}")
    print(f"  Specificity: {spec:.4f}")
    print(f"  CP = det + spec - 1 = {cp_micro:.4f}")
    print(f"\nExpected (from Hoel):")
    print(f"  CP ≈ {expected['microscale']['CP']:.3f}")
    print(f"\nDifference: {abs(cp_micro - expected['microscale']['CP']):.4f}")
    
    return cp_micro

def verify_macroscale(T, expected):
    """Verify macroscale CP calculation"""
    partition = expected['optimal_macroscale']['partition']
    T_macro = coarse_grain_tpm(T, partition)
    cp_macro = calculate_cp(T_macro)
    det = calculate_determinism(T_macro)
    deg = calculate_degeneracy(T_macro)
    spec = 1.0 - deg
    
    print("\n" + "="*60)
    print("MACROSCALE VERIFICATION")
    print("="*60)
    print(f"Partition: {partition}")
    print(f"\nCoarse-grained TPM:")
    print(T_macro)
    print(f"\nCalculated:")
    print(f"  Determinism: {det:.4f}")
    print(f"  Degeneracy:  {deg:.4f}")
    print(f"  Specificity: {spec:.4f}")
    print(f"  CP = det + spec - 1 = {cp_macro:.4f}")
    print(f"\nExpected (from Hoel):")
    print(f"  CP = {expected['optimal_macroscale']['CP']:.3f}")
    print(f"\nDifference: {abs(cp_macro - expected['optimal_macroscale']['CP']):.4f}")
    
    return cp_macro

def main():
    # Create system
    T = create_two_cycle_tpm(p_self=0.2)
    expected = get_expected_values()
    
    # Verify calculations
    cp_micro = verify_microscale(T, expected)
    cp_macro = verify_macroscale(T, expected)
    
    # Calculate ΔCP
    delta_cp = cp_macro - cp_micro
    expected_delta = expected['optimal_macroscale']['delta_CP']
    
    print("\n" + "="*60)
    print("ΔCP VERIFICATION")
    print("="*60)
    print(f"Calculated ΔCP: {delta_cp:.4f}")
    print(f"Expected ΔCP:   {expected_delta:.3f}")
    print(f"Difference:     {abs(delta_cp - expected_delta):.4f}")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    if abs(cp_micro - expected['microscale']['CP']) < 0.05:
        print("✓ Microscale CP matches expected value")
    else:
        print("✗ Microscale CP does NOT match")
        
    if abs(cp_macro - expected['optimal_macroscale']['CP']) < 0.05:
        print("✓ Macroscale CP matches expected value")
    else:
        print("✗ Macroscale CP does NOT match")
        
    if abs(delta_cp - expected_delta) < 0.05:
        print("✓ ΔCP matches expected value")
    else:
        print("✗ ΔCP does NOT match")

if __name__ == '__main__':
    main()
