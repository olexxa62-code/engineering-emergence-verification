"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

#!/usr/bin/env python3
"""
CORRECTED Comparative Analysis: 6-state vs 8-state
З правильним виключенням microscale
"""
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_results(filepath):
    """Завантажує pickle результати"""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def create_comparison_plots():
    """Створює порівняльні графіки"""
    # Завантажуємо дані
    results_6 = load_results('results/sensitivity_analysis_6state_corrected.pkl')
    results_8 = load_results('results/sensitivity_analysis_8state.pkl')
    
    # Екстракція даних
    p_self_6 = [r['p_self'] for r in results_6]
    p_self_8 = [r['p_self'] for r in results_8]
    
    cp_micro_6 = [r['cp_micro'] for r in results_6]
    cp_micro_8 = [r['cp_micro'] for r in results_8]
    
    cp_macro_6 = [r['cp_macro'] for r in results_6]
    cp_macro_8 = [r['cp_macro'] for r in results_8]
    
    delta_cp_6 = [r['delta_cp'] for r in results_6]
    delta_cp_8 = [r['delta_cp'] for r in results_8]
    
    emergent_6 = [r['n_emergent_corrected'] for r in results_6]
    emergent_8 = [r['n_emergent_corrected'] for r in results_8]
    
    # Створюємо фігуру
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('CORRECTED Comparative Analysis: 6-state vs 8-state Systems', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Panel 1: CP(microscale)
    ax = axes[0, 0]
    ax.plot(p_self_6, cp_micro_6, 'bo-', label='6-state (3-cycles)', 
            linewidth=2, markersize=8)
    ax.plot(p_self_8, cp_micro_8, 'rs-', label='8-state (4-cycles)', 
            linewidth=2, markersize=8)
    ax.set_xlabel('p_self (noise)', fontsize=11)
    ax.set_ylabel('CP(microscale)', fontsize=11)
    ax.set_title('Microscale Causal Power', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Panel 2: Emergent scales (CORRECTED)
    ax = axes[0, 1]
    ax.plot(p_self_6, emergent_6, 'bo-', label='6-state (3-cycles)', 
            linewidth=2, markersize=8)
    ax.plot(p_self_8, emergent_8, 'rs-', label='8-state (4-cycles)', 
            linewidth=2, markersize=8)
    ax.set_xlabel('p_self (noise)', fontsize=11)
    ax.set_ylabel('Emergent scales (corrected)', fontsize=11)
    ax.set_title('Emergent Hierarchy Complexity', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 4])
    
    # Додаємо текстові мітки
    ax.text(0.25, 3.2, 'Complex hierarchy\n(3 scales)', 
            fontsize=9, color='blue', ha='center')
    ax.text(0.25, 1.3, 'Balloon hierarchy\n(1 scale)', 
            fontsize=9, color='red', ha='center')
    
    # Panel 3: ΔCP
    ax = axes[1, 0]
    ax.plot(p_self_6, delta_cp_6, 'bo-', label='6-state (3-cycles)', 
            linewidth=2, markersize=8)
    ax.plot(p_self_8, delta_cp_8, 'rs-', label='8-state (4-cycles)', 
            linewidth=2, markersize=8)
    ax.set_xlabel('p_self (noise)', fontsize=11)
    ax.set_ylabel('ΔCP', fontsize=11)
    ax.set_title('Emergent Causal Gain', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Panel 4: Summary comparison
    ax = axes[1, 1]
    ax.axis('off')
    
    summary_text = f"""
    CORRECTED COMPARISON SUMMARY
    {'='*40}
    
    Baseline (p_self = 0.20):
    
    6-state (Two 3-cycles):
      CP(micro) = {results_6[4]['cp_micro']:.4f}
      CP(macro) = {results_6[4]['cp_macro']:.4f}
      ΔCP = {results_6[4]['delta_cp']:.4f}
      Emergent scales = {results_6[4]['n_emergent_corrected']}
    
    8-state (Two 4-cycles):
      CP(micro) = {results_8[4]['cp_micro']:.4f}
      CP(macro) = {results_8[4]['cp_macro']:.4f}
      ΔCP = {results_8[4]['delta_cp']:.4f}
      Emergent scales = {results_8[4]['n_emergent_corrected']}
    
    KEY INSIGHT:
    Shorter cycles → Complex hierarchy
    Longer cycles → Balloon hierarchy
    
    Cycle length affects emergent
    hierarchy structure!
    """
    
    ax.text(0.1, 0.95, summary_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    
    # Зберігаємо
    output_file = Path('figures/comparative_analysis_corrected.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Збережено: {output_file}")
    
    plt.close()

def print_summary_table():
    """Друкує зведену таблицю"""
    results_6 = load_results('results/sensitivity_analysis_6state_corrected.pkl')
    results_8 = load_results('results/sensitivity_analysis_8state.pkl')
    
    print("\n" + "="*80)
    print("CORRECTED COMPARISON TABLE")
    print("="*80)
    print(f"{'Metric':<25} {'6-state':<15} {'8-state':<15} {'Difference':<15}")
    print("-"*80)
    
    # Baseline p_self = 0.20
    r6 = results_6[4]
    r8 = results_8[4]
    
    metrics = [
        ('CP(microscale)', r6['cp_micro'], r8['cp_micro']),
        ('CP(macroscale)', r6['cp_macro'], r8['cp_macro']),
        ('ΔCP', r6['delta_cp'], r8['delta_cp']),
        ('Emergent scales', r6['n_emergent_corrected'], r8['n_emergent_corrected'])
    ]
    
    for name, val6, val8 in metrics:
        if isinstance(val6, int):
            diff = val8 - val6
            print(f"{name:<25} {val6:<15} {val8:<15} {diff:+d}")
        else:
            diff = ((val8 - val6) / val6) * 100
            print(f"{name:<25} {val6:<15.4f} {val8:<15.4f} {diff:+.2f}%")
    
    print("="*80)
    print("\nKEY FINDINGS:")
    print("  • 6-state (3-cycles): COMPLEX hierarchy with 3 emergent scales")
    print("  • 8-state (4-cycles): BALLOON hierarchy with 1 emergent scale")
    print("  • Longer cycles → Simpler emergence structure")
    print("  • Both reach CP(macro) = 1.0 (perfect determinism)")
    print("="*80 + "\n")

def main():
    print("\nСтворюю порівняльні візуалізації...")
    create_comparison_plots()
    print_summary_table()

if __name__ == "__main__":
    main()
