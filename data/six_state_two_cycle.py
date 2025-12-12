"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

"""
6-state two-cycle system from Hoel's Figure 2
Two 3-cycles with noise (self-loop probability)
"""

import numpy as np

def create_two_cycle_tpm(p_self=0.2, seed=42):
    """
    Create 6-state TPM with two 3-cycles.
    
    States 0,1,2 form cycle: 0→1→2→0
    States 3,4,5 form cycle: 3→4→5→3
    
    Args:
        p_self: probability of self-loop (noise)
        seed: random seed
    
    Returns:
        6×6 TPM
    """
    np.random.seed(seed)
    T = np.zeros((6, 6))
    
    # Cycle 1: 0→1→2→0
    T[0, 1] = 1.0 - p_self
    T[0, 0] = p_self
    
    T[1, 2] = 1.0 - p_self
    T[1, 1] = p_self
    
    T[2, 0] = 1.0 - p_self
    T[2, 2] = p_self
    
    # Cycle 2: 3→4→5→3
    T[3, 4] = 1.0 - p_self
    T[3, 3] = p_self
    
    T[4, 5] = 1.0 - p_self
    T[4, 4] = p_self
    
    T[5, 3] = 1.0 - p_self
    T[5, 5] = p_self
    
    return T

def get_expected_values():
    """
    Expected values from Hoel's paper Figure 2.
    
    Returns:
        dict with expected CP values
    """
    return {
        'microscale': {
            'partition': tuple((i,) for i in range(6)),
            'CP': 0.721,  # approximate from figure
        },
        'optimal_macroscale': {
            'partition': ((0, 1, 2), (3, 4, 5)),
            'CP': 1.000,  # perfect determinism
            'delta_CP': 0.279,  # approximate 1.0 - 0.721
        }
    }

if __name__ == '__main__':
    # Test
    T = create_two_cycle_tpm(p_self=0.2)
    print("6-state two-cycle TPM:")
    print(T)
    print(f"\nExpected values:")
    expected = get_expected_values()
    print(f"  Microscale CP: {expected['microscale']['CP']}")
    print(f"  Macroscale CP: {expected['optimal_macroscale']['CP']}")
    print(f"  ΔCP: {expected['optimal_macroscale']['delta_CP']}")
