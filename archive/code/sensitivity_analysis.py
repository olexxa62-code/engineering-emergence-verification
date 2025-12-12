"""
Sensitivity analysis: how does emergence change with noise?
"""

import sys
sys.path.insert(0, './stage1_hoel_verification/code')
sys.path.insert(0, './stage1_hoel_verification/data')
sys.path.insert(0, './code')

import numpy as np
import pickle
from algorithm1_brute_force import run_algorithm1
from six_state_two_cycle import create_two_cycle_tpm
import matplotlib.pyplot as plt

def run_sensitivity(p_self_values):
    """Run CE 2.0 analysis for different noise levels"""
    results = []
    
    for i, p_self in enumerate(p_self_values):
        print(f"\n[{i+1}/{len(p_self_values)}] Analyzing p_self = {p_self:.2f}...")
        T = create_two_cycle_tpm(p_self=p_self, seed=42)
        res = run_algorithm1(T)
        
        # Extract key metrics
        optimal = ((0, 1, 2), (3, 4, 5))
        micro = tuple((i,) for i in range(6))
        
        results.append({
            'p_self': p_self,
            'cp_micro': res['cp_dict'][micro],
            'cp_optimal': res['cp_dict'][optimal],
            'delta_cp_optimal': res['delta_cp_dict'][optimal],
            'n_emergent': len(res['emergent']),
            'max_cp': max(res['cp_dict'].values()),
            'max_delta_cp': max(res['delta_cp_dict'].values())
        })
    
    return results

def plot_sensitivity(results, output_path):
    """Visualize sensitivity analysis"""
    p_self = [r['p_self'] for r in results]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # CP values
    ax = axes[0, 0]
    ax.plot(p_self, [r['cp_micro'] for r in results], 
            'o-', label='Microscale', linewidth=2, markersize=8)
    ax.plot(p_self, [r['cp_optimal'] for r in results], 
            's-', label='Optimal macro', linewidth=2, markersize=8, color='red')
    ax.set_xlabel('Noise (p_self)', fontsize=12)
    ax.set_ylabel('CP', fontsize=12)
    ax.set_title('CP vs Noise Level', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # ΔCP
    ax = axes[0, 1]
    ax.plot(p_self, [r['delta_cp_optimal'] for r in results], 
            'ro-', linewidth=2, markersize=8)
    ax.set_xlabel('Noise (p_self)', fontsize=12)
    ax.set_ylabel('ΔCP', fontsize=12)
    ax.set_title('Causal Emergence vs Noise', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    
    # Number of emergent scales
    ax = axes[1, 0]
    ax.plot(p_self, [r['n_emergent'] for r in results], 
            'go-', linewidth=2, markersize=8)
    ax.set_xlabel('Noise (p_self)', fontsize=12)
    ax.set_ylabel('Number of emergent scales', fontsize=12)
    ax.set_title('Emergent Hierarchy Size', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Maximum values
    ax = axes[1, 1]
    ax.plot(p_self, [r['max_cp'] for r in results], 
            'o-', label='max(CP)', linewidth=2, markersize=8)
    ax.plot(p_self, [r['max_delta_cp'] for r in results], 
            's-', label='max(ΔCP)', linewidth=2, markersize=8)
    ax.set_xlabel('Noise (p_self)', fontsize=12)
    ax.set_ylabel('Maximum value', fontsize=12)
    ax.set_title('Maximum CP and ΔCP', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nSaved sensitivity plot: {output_path}")
    plt.close()

def main():
    print("="*70)
    print("SENSITIVITY ANALYSIS: Noise variation")
    print("="*70)
    
    # Test range: from deterministic to very noisy
    p_self_values = np.linspace(0.0, 0.5, 11)
    
    # Run analysis
    results = run_sensitivity(p_self_values)
    
    # Save results
    output_file = 'stage1_hoel_verification/results/sensitivity_analysis.pkl'
    with open(output_file, 'wb') as f:
        pickle.dump(results, f)
    print(f"\nResults saved: {output_file}")
    
    # Visualize
    plot_sensitivity(results, 
        'stage1_hoel_verification/figures/sensitivity_analysis.png')
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for r in results:
        print(f"p_self={r['p_self']:.2f}: "
              f"CP(micro)={r['cp_micro']:.3f}, "
              f"CP(optimal)={r['cp_optimal']:.3f}, "
              f"ΔCP={r['delta_cp_optimal']:.3f}, "
              f"n_emergent={r['n_emergent']}")

if __name__ == '__main__':
    main()
