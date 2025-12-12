"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

"""
8-state Two Length-4 Cycles System

Reference: Hoel et al. "Engineering Emergence" v2, Figure 3(ii), page 12
Quote: "system with two length-4 cycles (explored in more detail in Figure 6)"

Structure:
- Cycle 1: states {0,1,2,3} → 0→1→2→3→0
- Cycle 2: states {4,5,6,7} → 4→5→6→7→4

Parameters (extrapolated from Figure 2):
- p_self = 0.2 (probability of staying in current state)
- p_next = 0.8 (probability of transitioning to next state in cycle)

Expected results (from Figure 3):
- Emergent hierarchy: "balloon" shape - single dominant emergent scale
- Spath: 0.00
- Srow: 0.00
- n_emergent: 1 (pinpoint emergence at macroscale)
"""

import numpy as np
from typing import Tuple

PAPER_REFERENCE = {
    'version': 'v2',
    'page': 12,
    'figure': 'Figure 3(ii)',
    'quote': 'system with two length-4 cycles',
    'n_states': 8,
    'verified': False,  # Will be True after validation
    'expected': {
        'Spath': 0.00,
        'Srow': 0.00,
        'hierarchy_shape': 'balloon',
        'n_emergent_scales': 1
    }
}


def create_tpm(p_self: float = 0.2) -> np.ndarray:
    """
    Create TPM for 8-state two length-4 cycles system.
    
    Parameters:
    -----------
    p_self : float
        Probability of staying in current state (default 0.2 from Figure 2)
    
    Returns:
    --------
    T : np.ndarray (8x8)
        Transition probability matrix
    """
    assert 0 <= p_self <= 1, "p_self must be in [0, 1]"
    
    p_next = 1.0 - p_self
    n = 8
    T = np.zeros((n, n))
    
    # Cycle 1: 0→1→2→3→0
    cycle1_states = [0, 1, 2, 3]
    for i, state in enumerate(cycle1_states):
        next_state = cycle1_states[(i + 1) % 4]
        T[state, state] = p_self      # Self-loop
        T[state, next_state] = p_next  # Transition to next
    
    # Cycle 2: 4→5→6→7→4
    cycle2_states = [4, 5, 6, 7]
    for i, state in enumerate(cycle2_states):
        next_state = cycle2_states[(i + 1) % 4]
        T[state, state] = p_self      # Self-loop
        T[state, next_state] = p_next  # Transition to next
    
    return T


def get_optimal_partition() -> Tuple[Tuple[int, ...], ...]:
    """
    Get the expected optimal partition that groups two cycles.
    
    Returns:
    --------
    partition : tuple of tuples
        ((0,1,2,3), (4,5,6,7)) - two 4-cycles as macrostates
    """
    return ((0, 1, 2, 3), (4, 5, 6, 7))


def verify_tpm(T: np.ndarray) -> bool:
    """
    Verify TPM properties.
    
    Properties to check:
    1. Row-stochastic (rows sum to 1)
    2. Two disconnected 4-cycles
    3. Correct size (8x8)
    """
    n = T.shape[0]
    
    # Check 1: Size
    if n != 8:
        print(f"❌ Wrong size: {n} (expected 8)")
        return False
    
    # Check 2: Row-stochastic
    row_sums = T.sum(axis=1)
    if not np.allclose(row_sums, 1.0):
        print(f"❌ Not row-stochastic: {row_sums}")
        return False
    
    # Check 3: Two disconnected cycles
    # States 0-3 should only connect to 0-3
    cycle1_to_cycle2 = T[0:4, 4:8].sum()
    if not np.isclose(cycle1_to_cycle2, 0.0):
        print(f"❌ Cycle 1 leaks to Cycle 2: {cycle1_to_cycle2}")
        return False
    
    # States 4-7 should only connect to 4-7
    cycle2_to_cycle1 = T[4:8, 0:4].sum()
    if not np.isclose(cycle2_to_cycle1, 0.0):
        print(f"❌ Cycle 2 leaks to Cycle 1: {cycle2_to_cycle1}")
        return False
    
    print("✅ TPM verification passed")
    return True


def print_tpm_info(T: np.ndarray, p_self: float):
    """Print TPM information and structure."""
    print("\n" + "="*60)
    print("8-STATE TWO LENGTH-4 CYCLES SYSTEM")
    print("="*60)
    print(f"\nReference: {PAPER_REFERENCE['figure']}, page {PAPER_REFERENCE['page']}")
    print(f"Quote: \"{PAPER_REFERENCE['quote']}\"")
    print(f"\nParameters:")
    print(f"  n_states: {T.shape[0]}")
    print(f"  p_self: {p_self}")
    print(f"  p_next: {1.0 - p_self}")
    
    print(f"\nStructure:")
    print(f"  Cycle 1: 0→1→2→3→0 (states {{0,1,2,3}})")
    print(f"  Cycle 2: 4→5→6→7→4 (states {{4,5,6,7}})")
    
    print(f"\nExpected results:")
    print(f"  Hierarchy shape: {PAPER_REFERENCE['expected']['hierarchy_shape']}")
    print(f"  Spath: {PAPER_REFERENCE['expected']['Spath']}")
    print(f"  Srow: {PAPER_REFERENCE['expected']['Srow']}")
    print(f"  Emergent scales: {PAPER_REFERENCE['expected']['n_emergent_scales']}")
    
    print(f"\nOptimal partition: {get_optimal_partition()}")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Create TPM with default parameters
    p_self = 0.2
    T = create_tpm(p_self)
    
    # Print info
    print_tpm_info(T, p_self)
    
    # Verify
    verify_tpm(T)
    
    # Display TPM
    print("\nTransition Probability Matrix (8x8):")
    print("     ", end="")
    for j in range(8):
        print(f"  {j}  ", end="")
    print()
    print("    " + "-"*44)
    
    for i in range(8):
        print(f" {i} | ", end="")
        for j in range(8):
            if T[i, j] > 0:
                print(f"{T[i, j]:.2f} ", end="")
            else:
                print("  .  ", end="")
        print()
    
    print("\nCycle structures:")
    print("  Cycle 1 submatrix (states 0-3):")
    print(T[0:4, 0:4])
    print("\n  Cycle 2 submatrix (states 4-7):")
    print(T[4:8, 4:8])
