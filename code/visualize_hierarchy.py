"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""

"""
Visualize emergent hierarchy for 6-state system
Similar to Hoel's Figure 4
"""

import sys
sys.path.insert(0, './stage1_hoel_verification/code')

import pickle
import matplotlib.pyplot as plt
import numpy as np

def plot_hierarchy_profile(results, output_path):
    """
    Plot ΔCP distribution across dimensionalities
    Similar to bottom panels in Figure 4
    """
    # Group by dimensionality
    dim_to_delta = {}
    for partition, delta in results['delta_cp_dict'].items():
        dim = len(partition)
        if dim not in dim_to_delta:
            dim_to_delta[dim] = []
        dim_to_delta[dim].append(delta)
    
    # Calculate mean ΔCP per dimension
    dims = sorted(dim_to_delta.keys())
    mean_delta = [np.mean([d for d in dim_to_delta[dim] if d > 0]) 
                  if any(d > 0 for d in dim_to_delta[dim]) else 0 
                  for dim in dims]
    
    # Create symmetric plot (как в Figure 4)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot as filled area (symmetric)
    ax.fill_betweenx(dims, -np.array(mean_delta), np.array(mean_delta), 
                      alpha=0.3, color='blue')
    ax.plot(mean_delta, dims, 'o-', color='blue', linewidth=2, markersize=8)
    ax.plot(-np.array(mean_delta), dims, 'o-', color='blue', linewidth=2, markersize=8)
    
    ax.set_ylabel('Dimensionality (number of blocks)', fontsize=12)
    ax.set_xlabel('Mean ΔCP (positive only)', fontsize=12)
    ax.set_title('6-state Two-Cycle: Emergent Hierarchy Profile', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axvline(0, color='black', linestyle='--', linewidth=1)
    
    # Add annotations
    max_idx = np.argmax(mean_delta)
    max_dim = dims[max_idx]
    max_delta = mean_delta[max_idx]
    ax.annotate(f'Peak: dim={max_dim}\nΔCP={max_delta:.3f}',
                xy=(max_delta, max_dim),
                xytext=(max_delta + 0.05, max_dim + 0.5),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, color='red')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved hierarchy profile: {output_path}")
    plt.close()

def plot_cp_distribution(results, output_path):
    """
    Plot CP values for all partitions grouped by dimensionality
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Group by dimensionality
    dim_to_cp = {}
    for partition, cp in results['cp_dict'].items():
        dim = len(partition)
        if dim not in dim_to_cp:
            dim_to_cp[dim] = []
        dim_to_cp[dim].append(cp)
    
    # Box plot
    dims = sorted(dim_to_cp.keys())
    data = [dim_to_cp[d] for d in dims]
    
    bp = ax.boxplot(data, positions=dims, widths=0.6, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    
    ax.set_xlabel('Dimensionality', fontsize=12)
    ax.set_ylabel('CP value', fontsize=12)
    ax.set_title('CP Distribution Across Scales', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(1.0, color='red', linestyle='--', label='CP = 1.0 (perfect)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved CP distribution: {output_path}")
    plt.close()

def plot_top_partitions(results, output_path):
    """
    Plot top 10 partitions by ΔCP
    """
    # Get top 10
    sorted_delta = sorted(results['delta_cp_dict'].items(), 
                         key=lambda x: x[1], reverse=True)[:10]
    
    partitions = [str(p)[:30] + '...' if len(str(p)) > 30 else str(p) 
                  for p, _ in sorted_delta]
    deltas = [d for _, d in sorted_delta]
    cps = [results['cp_dict'][p] for p, _ in sorted_delta]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ΔCP
    colors = ['red' if i == 1 else 'blue' for i in range(len(deltas))]
    ax1.barh(range(len(deltas)), deltas, color=colors, alpha=0.7)
    ax1.set_yticks(range(len(partitions)))
    ax1.set_yticklabels([f"{i+1}" for i in range(len(partitions))])
    ax1.set_xlabel('ΔCP', fontsize=12)
    ax1.set_ylabel('Rank', fontsize=12)
    ax1.set_title('Top 10 by ΔCP', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    ax1.invert_yaxis()
    
    # CP
    ax2.barh(range(len(cps)), cps, color=colors, alpha=0.7)
    ax2.set_yticks(range(len(partitions)))
    ax2.set_yticklabels([f"{i+1}" for i in range(len(partitions))])
    ax2.set_xlabel('CP', fontsize=12)
    ax2.set_title('Corresponding CP values', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.axvline(1.0, color='red', linestyle='--', linewidth=1)
    ax2.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved top partitions: {output_path}")
    plt.close()

def main():
    # Load results
    with open('stage1_hoel_verification/results/six_state_hierarchy.pkl', 'rb') as f:
        data = pickle.load(f)
    
    results = data['results']
    
    print("Creating visualizations...")
    
    # Generate plots
    plot_hierarchy_profile(results, 
        'stage1_hoel_verification/figures/hierarchy_profile.png')
    
    plot_cp_distribution(results,
        'stage1_hoel_verification/figures/cp_distribution.png')
    
    plot_top_partitions(results,
        'stage1_hoel_verification/figures/top_partitions.png')
    
    print("\nAll visualizations complete!")

if __name__ == '__main__':
    main()
