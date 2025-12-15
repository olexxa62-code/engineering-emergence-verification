"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
Final visualization: Cycle Length Effect
Comparison of 6-state, 8-state, 10-state systems
"""
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ce2_core import calculate_cp, coarse_grain_tpm
from algorithm2_greedy import run_greedy_algorithm

sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))
from ten_state_two_five_cycles import create_two_five_cycle_tpm, get_optimal_partition

def load_results(filepath):
    """Loads pickle results"""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def get_10state_data():
    """Gets data for 10-state (baseline p_self=0.2)"""
    tpm = create_two_five_cycle_tpm(p_self=0.2)
    optimal = get_optimal_partition()
    
    cp_micro = calculate_cp(tpm)
    tpm_macro = coarse_grain_tpm(tpm, optimal)
    cp_macro = calculate_cp(tpm_macro)
    delta_cp = cp_macro - cp_micro
    
    # Greedy for emergent scales
    results = run_greedy_algorithm(tpm, n_paths=100, verbose=False)
    microscale = tuple((i,) for i in range(10))
    emergent = [p for p in results['emergent'] if p != microscale]
    
    return {
        'cp_micro': cp_micro,
        'cp_macro': cp_macro,
        'delta_cp': delta_cp,
        'n_emergent': len(emergent)
    }

def create_final_visualization():
    """Creates final visualization"""
    print("\nLoading data...")
    
    # Load 6-state and 8-state (baseline p_self=0.2, index=4)
    results_6 = load_results('results/sensitivity_analysis_6state_corrected.pkl')
    results_8 = load_results('results/sensitivity_analysis_8state.pkl')
    
    data_6 = results_6[4]  # p_self=0.2
    data_8 = results_8[4]
    
    print("Computing 10-state...")
    data_10 = get_10state_data()
    
    # Data for visualization
    cycle_lengths = [3, 4, 5]
    cp_micros = [data_6['cp_micro'], data_8['cp_micro'], data_10['cp_micro']]
    cp_macros = [data_6['cp_macro'], data_8['cp_macro'], data_10['cp_macro']]
    delta_cps = [data_6['delta_cp'], data_8['delta_cp'], data_10['delta_cp']]
    emergent_scales = [data_6['n_emergent_corrected'], 
                       data_8['n_emergent_corrected'], 
                       data_10['n_emergent']]
    
    print("\nCreating visualization...")
    
    # Create figure
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    fig.suptitle('Cycle Length Effect on Emergent Hierarchy Structure', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Panel 1: CP values
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(cycle_lengths, cp_micros, 'o-', linewidth=3, markersize=12, 
             color='#2E86AB', label='CP(microscale)')
    ax1.plot(cycle_lengths, cp_macros, 's-', linewidth=3, markersize=12, 
             color='#A23B72', label='CP(macroscale)')
    ax1.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax1.set_xlabel('Cycle Length', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Causal Power (CP)', fontsize=13, fontweight='bold')
    ax1.set_title('Causal Power by Scale', fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(cycle_lengths)
    ax1.set_ylim([0.65, 1.05])
    
    # Panel 2: ΔCP
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(cycle_lengths, delta_cps, 'D-', linewidth=3, markersize=12, 
             color='#F18F01', label='ΔCP (emergence gain)')
    ax2.set_xlabel('Cycle Length', fontsize=13, fontweight='bold')
    ax2.set_ylabel('ΔCP', fontsize=13, fontweight='bold')
    ax2.set_title('Emergent Causal Gain', fontsize=14, fontweight='bold')
    ax2.legend(loc='best', fontsize=11, framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(cycle_lengths)
    ax2.set_ylim([0.15, 0.30])
    
    # Add trend
    z = np.polyfit(cycle_lengths, delta_cps, 1)
    p = np.poly1d(z)
    ax2.plot(cycle_lengths, p(cycle_lengths), '--', 
             color='red', alpha=0.5, linewidth=2, label='Linear trend')
    ax2.legend(loc='best', fontsize=11, framealpha=0.9)
    
    # Panel 3: Emergent scales (KEY PLOT)
    ax3 = fig.add_subplot(gs[1, 0])
    colors = ['#C73E1D', '#C73E1D', '#C73E1D']  # red
    ax3.bar(cycle_lengths, emergent_scales, width=0.6, color=colors, 
            edgecolor='black', linewidth=2, alpha=0.8)
    ax3.set_xlabel('Cycle Length', fontsize=13, fontweight='bold')
    ax3.set_ylabel('Number of Emergent Scales', fontsize=13, fontweight='bold')
    ax3.set_title('Emergent Hierarchy Complexity', fontsize=14, fontweight='bold')
    ax3.set_xticks(cycle_lengths)
    ax3.set_ylim([0, 4])
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add hierarchy type labels
    hierarchy_types = ['Complex', 'Balloon', 'Balloon']
    for i, (length, scales, htype) in enumerate(zip(cycle_lengths, emergent_scales, hierarchy_types)):
        ax3.text(length, scales + 0.2, f'{scales}\n({htype})', 
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Highlight critical transition
    ax3.axvline(x=3.5, color='red', linestyle='--', linewidth=2, alpha=0.6)
    ax3.text(3.5, 3.5, 'Critical\nTransition', ha='center', 
            fontsize=10, color='red', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Panel 4: Summary table
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    summary_text = f"""
    CYCLE LENGTH EFFECT SUMMARY
    {'='*50}
    
    System Comparison (p_self = 0.20):
    
    6-state (length-3):
      • CP(micro) = {cp_micros[0]:.4f}
      • CP(macro) = {cp_macros[0]:.4f}
      • ΔCP       = {delta_cps[0]:.4f}
      • Emergent  = {emergent_scales[0]} scales
      • Type      = COMPLEX HIERARCHY
    
    8-state (length-4):
      • CP(micro) = {cp_micros[1]:.4f}
      • CP(macro) = {cp_macros[1]:.4f}
      • ΔCP       = {delta_cps[1]:.4f}
      • Emergent  = {emergent_scales[1]} scale
      • Type      = BALLOON HIERARCHY
    
    10-state (length-5):
      • CP(micro) = {cp_micros[2]:.4f}
      • CP(macro) = {cp_macros[2]:.4f}
      • ΔCP       = {delta_cps[2]:.4f}
      • Emergent  = {emergent_scales[2]} scale
      • Type      = BALLOON HIERARCHY
    
    {'='*50}
    
    KEY FINDING:
    Critical cycle length = 3
    
    • Length ≤ 3: Complex hierarchy
    • Length ≥ 4: Balloon hierarchy
    
    Longer cycles → Higher CP(micro)
                  → Less emergence "space"
                  → Direct micro→macro jump
    """
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    # Save
    output_file = Path('figures/final_cycle_length_effect.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_file}")
    
    plt.close()

def main():
    print("\n" + "="*70)
    print("FINAL VISUALIZATION: Cycle Length Effect")
    print("="*70)
    
    create_final_visualization()
    
    print("\n" + "="*70)
    print("COMPLETED")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
