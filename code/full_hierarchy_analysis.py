"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

"""
Complete analysis of emergent hierarchy for 6-state two-cycle system
"""

import sys
sys.path.insert(0, './stage1_hoel_verification/code')
sys.path.insert(0, './stage1_hoel_verification/data')
sys.path.insert(0, './code')

import numpy as np
import pickle
from algorithm1_brute_force import run_algorithm1
from six_state_two_cycle import create_two_cycle_tpm

def main():
    print("="*70)
    print("FULL EMERGENT HIERARCHY ANALYSIS")
    print("6-state two-cycle system")
    print("="*70)
    
    # Create system
    T = create_two_cycle_tpm(p_self=0.2)
    
    # Run complete analysis
    print("\nRunning Algorithm 1 (brute force)...")
    results = run_algorithm1(T)
    
    # Save results
    output_file = 'stage1_hoel_verification/results/six_state_hierarchy.pkl'
    with open(output_file, 'wb') as f:
        pickle.dump({
            'T': T,
            'results': results,
            'description': '6-state two-cycle with p_self=0.2'
        }, f)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*70)
    print("EMERGENT HIERARCHY SUMMARY")
    print("="*70)
    print(f"Total partitions: {len(results['partitions'])}")
    print(f"Emergent scales: {len(results['emergent'])}")
    
    # Top 10 by ΔCP
    print("\nTop 10 partitions by ΔCP:")
    sorted_delta = sorted(results['delta_cp_dict'].items(), 
                         key=lambda x: x[1], reverse=True)
    for i, (partition, delta_cp) in enumerate(sorted_delta[:10]):
        cp = results['cp_dict'][partition]
        print(f"  {i+1:2d}. dim={len(partition)}: "
              f"CP={cp:.4f}, ΔCP={delta_cp:.4f}")
        if i < 3:  # Show partition for top 3
            print(f"      {partition}")
    
    # Verify expected optimal partition
    optimal = ((0, 1, 2), (3, 4, 5))
    if optimal in results['delta_cp_dict']:
        print(f"\n✓ Expected optimal partition {optimal} found:")
        print(f"  CP = {results['cp_dict'][optimal]:.4f}")
        print(f"  ΔCP = {results['delta_cp_dict'][optimal]:.4f}")
    else:
        print(f"\n✗ Expected optimal partition NOT in emergent set")

if __name__ == '__main__':
    main()
