#!/usr/bin/env python3
"""
Візуалізація результатів sensitivity analysis
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Завантаження результатів
results_file = Path("../results/sensitivity_analysis_8state.pkl")
with open(results_file, 'rb') as f:
    results = pickle.load(f)

# Екстракція даних
p_self = [r['p_self'] for r in results]
cp_micro = [r['cp_micro'] for r in results]
cp_macro = [r['cp_macro'] for r in results]
delta_cp = [r['delta_cp'] for r in results]
det_micro = [r['det_micro'] for r in results]
deg_micro = [r['deg_micro'] for r in results]

# Створення графіків
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Sensitivity Analysis: 8-state Two Length-4 Cycles\np_self ∈ [0.0, 0.5]', 
             fontsize=14, fontweight='bold')

# Plot 1: CP values
ax = axes[0, 0]
ax.plot(p_self, cp_micro, 'o-', linewidth=2, markersize=8, label='CP(microscale)', color='blue')
ax.plot(p_self, cp_macro, 's-', linewidth=2, markersize=8, label='CP(macroscale)', color='red')
ax.axvline(0.2, color='gray', linestyle='--', alpha=0.5, label='Baseline (p=0.2)')
ax.set_xlabel('p_self', fontsize=12)
ax.set_ylabel('Causal Power (CP)', fontsize=12)
ax.set_title('CP vs p_self', fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: ΔCP
ax = axes[0, 1]
ax.plot(p_self, delta_cp, 'o-', linewidth=2, markersize=8, color='green')
ax.axvline(0.2, color='gray', linestyle='--', alpha=0.5, label='Baseline')
ax.axhline(0.2406, color='green', linestyle=':', alpha=0.5, label='Baseline ΔCP')
ax.set_xlabel('p_self', fontsize=12)
ax.set_ylabel('ΔCP', fontsize=12)
ax.set_title('Causal Emergence (ΔCP) vs p_self', fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: Determinism & Degeneracy
ax = axes[1, 0]
ax.plot(p_self, det_micro, 'o-', linewidth=2, markersize=8, label='Determinism', color='purple')
ax.plot(p_self, deg_micro, 's-', linewidth=2, markersize=8, label='Degeneracy', color='orange')
ax.axvline(0.2, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('p_self', fontsize=12)
ax.set_ylabel('Value', fontsize=12)
ax.set_title('Causal Primitives vs p_self', fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 4: Summary statistics
ax = axes[1, 1]
ax.axis('off')
summary_text = f"""
SUMMARY STATISTICS

Total configurations: {len(results)}
Parameter range: p_self ∈ [{min(p_self):.2f}, {max(p_self):.2f}]

BASELINE (p_self = 0.20):
  CP(micro):    {results[4]['cp_micro']:.4f}
  CP(macro):    {results[4]['cp_macro']:.4f}
  ΔCP:          {results[4]['delta_cp']:.4f}
  Determinism:  {results[4]['det_micro']:.4f}
  Degeneracy:   {results[4]['deg_micro']:.4f}

TRENDS:
  CP(micro):    {cp_micro[1]:.4f} → {cp_micro[-1]:.4f} (↓)
  ΔCP:          {delta_cp[1]:.4f} → {delta_cp[-1]:.4f} (↑)
  CP(macro):    Constant = 1.0000

EMERGENT SCALES:
  All configs:  1 scale (balloon shape)
  Exception:    p=0.0 → 0 scales (trivial)
"""
ax.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
        verticalalignment='center')

plt.tight_layout()
output_file = Path("../figures/sensitivity_analysis_plots.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Збережено: {output_file}")
plt.close()

print("\nВізуалізація завершена!")
