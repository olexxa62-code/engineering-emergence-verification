#!/usr/bin/env python3
"""
Порівняльний аналіз: 6-state vs 8-state Two-Cycle Systems
Детальне дослідження під мікроскопом
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

def load_data():
    """Завантаження даних обох систем"""
    # 6-state
    with open('results/sensitivity_analysis.pkl', 'rb') as f:
        data_6 = pickle.load(f)
    
    # 8-state
    with open('results/sensitivity_analysis_8state.pkl', 'rb') as f:
        data_8 = pickle.load(f)
    
    return data_6, data_8

def create_comparison_table(data_6, data_8):
    """Створює порівняльну таблицю"""
    
    # Baseline values (p_self = 0.2)
    baseline_6 = [d for d in data_6 if abs(d['p_self'] - 0.2) < 0.01][0]
    baseline_8 = [d for d in data_8 if abs(d['p_self'] - 0.2) < 0.01][0]
    
    comparison = {
        'Metric': [
            'n_states',
            'Cycle structure',
            'CP(micro) @ p=0.2',
            'CP(macro) @ p=0.2',
            'ΔCP @ p=0.2',
            'Determinism @ p=0.2',
            'Degeneracy @ p=0.2',
            'Emergent scales',
            'Hierarchy shape'
        ],
        '6-state': [
            '6',
            'Two 3-cycles',
            f"{baseline_6['cp_micro']:.4f}",
            f"{baseline_6['cp_optimal']:.4f}",
            f"{baseline_6['delta_cp_optimal']:.4f}",
            'N/A',
            'N/A',
            f"{baseline_6['n_emergent']}",
            'balloon'
        ],
        '8-state': [
            '8',
            'Two 4-cycles',
            f"{baseline_8['cp_micro']:.4f}",
            f"{baseline_8['cp_macro']:.4f}",
            f"{baseline_8['delta_cp']:.4f}",
            f"{baseline_8['det_micro']:.4f}",
            f"{baseline_8['deg_micro']:.4f}",
            f"{baseline_8['n_emergent_corrected']}",
            'balloon'
        ]
    }
    
    df = pd.DataFrame(comparison)
    print("\n" + "="*70)
    print("ПОРІВНЯЛЬНА ТАБЛИЦЯ: 6-state vs 8-state (p_self = 0.2)")
    print("="*70)
    print(df.to_string(index=False))
    print("="*70 + "\n")
    
    return df

def create_comparative_plots(data_6, data_8):
    """Створює порівняльні графіки"""
    
    # Екстракція даних
    p_self_6 = [d['p_self'] for d in data_6]
    cp_micro_6 = [d['cp_micro'] for d in data_6]
    cp_macro_6 = [d['cp_optimal'] for d in data_6]
    delta_cp_6 = [d['delta_cp_optimal'] for d in data_6]
    
    p_self_8 = [d['p_self'] for d in data_8]
    cp_micro_8 = [d['cp_micro'] for d in data_8]
    cp_macro_8 = [d['cp_macro'] for d in data_8]
    delta_cp_8 = [d['delta_cp'] for d in data_8]
    
    # Створення графіків
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Comparative Analysis: 6-state vs 8-state Two-Cycle Systems\n' + 
                 'Детальний порівняльний аналіз під мікроскопом',
                 fontsize=15, fontweight='bold')
    
    # Plot 1: CP(microscale) comparison
    ax = axes[0, 0]
    ax.plot(p_self_6, cp_micro_6, 'o-', linewidth=2.5, markersize=9, 
            label='6-state (two 3-cycles)', color='#1f77b4', alpha=0.8)
    ax.plot(p_self_8, cp_micro_8, 's-', linewidth=2.5, markersize=9,
            label='8-state (two 4-cycles)', color='#ff7f0e', alpha=0.8)
    ax.axvline(0.2, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.set_xlabel('p_self', fontsize=13, fontweight='bold')
    ax.set_ylabel('CP(microscale)', fontsize=13, fontweight='bold')
    ax.set_title('Microscale Causal Power', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: CP(macroscale) comparison
    ax = axes[0, 1]
    ax.plot(p_self_6, cp_macro_6, 'o-', linewidth=2.5, markersize=9,
            label='6-state', color='#1f77b4', alpha=0.8)
    ax.plot(p_self_8, cp_macro_8, 's-', linewidth=2.5, markersize=9,
            label='8-state', color='#ff7f0e', alpha=0.8)
    ax.axvline(0.2, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.axhline(1.0, color='red', linestyle=':', alpha=0.5, linewidth=1.5, label='Perfect CP')
    ax.set_xlabel('p_self', fontsize=13, fontweight='bold')
    ax.set_ylabel('CP(macroscale)', fontsize=13, fontweight='bold')
    ax.set_title('Macroscale Causal Power', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: ΔCP comparison
    ax = axes[1, 0]
    ax.plot(p_self_6, delta_cp_6, 'o-', linewidth=2.5, markersize=9,
            label='6-state', color='#2ca02c', alpha=0.8)
    ax.plot(p_self_8, delta_cp_8, 's-', linewidth=2.5, markersize=9,
            label='8-state', color='#d62728', alpha=0.8)
    ax.axvline(0.2, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.set_xlabel('p_self', fontsize=13, fontweight='bold')
    ax.set_ylabel('ΔCP (Causal Emergence)', fontsize=13, fontweight='bold')
    ax.set_title('Emergent Causal Power', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Differential Analysis
    ax = axes[1, 1]
    
    # Difference plots
    diff_cp_micro = np.array(cp_micro_8) - np.array(cp_micro_6)
    diff_delta_cp = np.array(delta_cp_8) - np.array(delta_cp_6)
    
    ax.plot(p_self_6, diff_cp_micro, 'o-', linewidth=2.5, markersize=9,
            label='Δ[CP(micro)]: 8-state - 6-state', color='#9467bd', alpha=0.8)
    ax.plot(p_self_6, diff_delta_cp, 's-', linewidth=2.5, markersize=9,
            label='Δ[ΔCP]: 8-state - 6-state', color='#8c564b', alpha=0.8)
    ax.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax.axvline(0.2, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.set_xlabel('p_self', fontsize=13, fontweight='bold')
    ax.set_ylabel('Difference (8-state minus 6-state)', fontsize=13, fontweight='bold')
    ax.set_title('Differential Analysis', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_file = Path("figures/comparative_analysis_6v8.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Збережено: {output_file}")
    plt.close()

def analyze_trends(data_6, data_8):
    """Аналіз трендів і patterns"""
    
    print("\n" + "="*70)
    print("АНАЛІЗ ТРЕНДІВ ТА PATTERNS")
    print("="*70)
    
    # 6-state trends
    cp_micro_6 = [d['cp_micro'] for d in data_6[1:]]  # Skip p=0
    delta_cp_6 = [d['delta_cp_optimal'] for d in data_6[1:]]
    
    # 8-state trends
    cp_micro_8 = [d['cp_micro'] for d in data_8[1:]]
    delta_cp_8 = [d['delta_cp'] for d in data_8[1:]]
    
    print("\n1. MICROSCALE CP DEGRADATION:")
    print(f"   6-state: {cp_micro_6[0]:.4f} → {cp_micro_6[-1]:.4f} "
          f"(Δ = {cp_micro_6[-1]-cp_micro_6[0]:.4f})")
    print(f"   8-state: {cp_micro_8[0]:.4f} → {cp_micro_8[-1]:.4f} "
          f"(Δ = {cp_micro_8[-1]-cp_micro_8[0]:.4f})")
    
    print("\n2. EMERGENT ΔCP GROWTH:")
    print(f"   6-state: {delta_cp_6[0]:.4f} → {delta_cp_6[-1]:.4f} "
          f"(Δ = {delta_cp_6[-1]-delta_cp_6[0]:.4f})")
    print(f"   8-state: {delta_cp_8[0]:.4f} → {delta_cp_8[-1]:.4f} "
          f"(Δ = {delta_cp_8[-1]-delta_cp_8[0]:.4f})")
    
    print("\n3. SYSTEM COMPARISON @ p_self=0.2:")
    baseline_6 = [d for d in data_6 if abs(d['p_self']-0.2)<0.01][0]
    baseline_8 = [d for d in data_8 if abs(d['p_self']-0.2)<0.01][0]
    
    print(f"   CP(micro): 8-state HIGHER by "
          f"{baseline_8['cp_micro']-baseline_6['cp_micro']:.4f} "
          f"({(baseline_8['cp_micro']/baseline_6['cp_micro']-1)*100:.2f}%)")
    
    print(f"   ΔCP: 6-state HIGHER by "
          f"{baseline_6['delta_cp_optimal']-baseline_8['delta_cp']:.4f} "
          f"({(baseline_6['delta_cp_optimal']/baseline_8['delta_cp']-1)*100:.2f}%)")
    
    print("\n4. ARCHITECTURAL IMPLICATIONS:")
    print("   - Довші цикли (4 vs 3) → вищий CP(micro)")
    print("   - Коротші цикли (3 vs 4) → вищий ΔCP (більше емердженції)")
    print("   - Обидві системи: balloon topology (1 emergent scale)")
    print("   - Макромасштаб: CP=1.0 для обох (perfect determinism)")
    
    print("="*70 + "\n")

def main():
    print("\n" + "="*70)
    print("COMPARATIVE ANALYSIS: 6-state vs 8-state")
    print("Детальний порівняльний аналіз під мікроскопом 🔬")
    print("="*70)
    
    # Завантаження даних
    print("\nЗавантаження даних...")
    data_6, data_8 = load_data()
    print(f"  6-state: {len(data_6)} configurations")
    print(f"  8-state: {len(data_8)} configurations")
    
    # Порівняльна таблиця
    df = create_comparison_table(data_6, data_8)
    
    # Графіки
    print("\nСтворення порівняльних графіків...")
    create_comparative_plots(data_6, data_8)
    
    # Аналіз трендів
    analyze_trends(data_6, data_8)
    
    # Збереження таблиці
    output_csv = Path("results/comparative_table_6v8.csv")
    df.to_csv(output_csv, index=False)
    print(f"Таблицю збережено: {output_csv}")
    
    print("\n✅ ПОРІВНЯЛЬНИЙ АНАЛІЗ ЗАВЕРШЕНО!\n")

if __name__ == "__main__":
    main()
