"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
10-state system: Two independent 5-cycles
Intermediate length between 3-cycle and 4-cycle
"""
import numpy as np

def create_two_five_cycle_tpm(p_self=0.2):
    """
    Creates TPM for two independent 5-cycles
    
    States 0-4: first 5-cycle (0→1→2→3→4→0)
    States 5-9: second 5-cycle (5→6→7→8→9→5)
    
    Parameters:
    -----------
    p_self : float
        Probability of staying in current state
    
    Returns:
    --------
    tpm : ndarray (10, 10)
        Transition probability matrix
    """
    n = 10
    tpm = np.zeros((n, n))
    
    # First 5-cycle: states 0-4
    for i in range(5):
        next_state = (i + 1) % 5
        tpm[i, i] = p_self           # stay
        tpm[i, next_state] = 1 - p_self  # transition
    
    # Second 5-cycle: states 5-9
    for i in range(5, 10):
        next_state = 5 + ((i - 5 + 1) % 5)
        tpm[i, i] = p_self           # stay
        tpm[i, next_state] = 1 - p_self  # transition
    
    return tpm

def get_optimal_partition():
    """Returns optimal macroscale partition"""
    return ((0, 1, 2, 3, 4), (5, 6, 7, 8, 9))

def get_system_description():
    """System description"""
    return {
        'name': '10-state two 5-cycles',
        'n_states': 10,
        'structure': 'Two independent 5-cycles',
        'cycles': [(0,1,2,3,4), (5,6,7,8,9)],
        'optimal_partition': ((0,1,2,3,4), (5,6,7,8,9)),
        'expected_hierarchy': 'Unknown (testing hypothesis)'
    }

if __name__ == "__main__":
    print("\n" + "="*70)
    print("10-STATE TWO 5-CYCLES SYSTEM")
    print("="*70)
    
    desc = get_system_description()
    for key, value in desc.items():
        print(f"{key}: {value}")
    
    print("\nTPM structure (p_self=0.2):")
    tpm = create_two_five_cycle_tpm(p_self=0.2)
    print(f"Shape: {tpm.shape}")
    print(f"Row sums (should be 1.0): {tpm.sum(axis=1)}")
    print(f"Non-zero entries per row: {(tpm > 0).sum(axis=1)}")
    print("="*70 + "\n")
