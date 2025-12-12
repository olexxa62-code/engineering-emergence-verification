# Figure Descriptions

**Verification of Engineering Emergence (Jansma & Hoel, 2025)**  
**Author:** Oleksii Onasenko  
**Developer:** SubstanceNet

---

## Overview

This document provides detailed descriptions of all figures generated during the verification and discovery process. All figures are publication-ready and demonstrate key findings.

---

## Figure 1: Cycle Length Discovery

**Filename:** `figures/figure_cycle_length_discovery.png`

**Title:** Critical Cycle Length Effect in Emergent Hierarchies

### Description

This figure demonstrates the critical discovery that cycle length determines emergent hierarchy structure in two-cycle systems.

**Layout:**
- **Top Row:** Complete emergent hierarchy visualizations for three systems
- **Bottom Row:** ΔCP distribution profiles across dimensionality levels

**Systems Shown:**
1. **Left:** 6-state system (two 3-cycles) - Complex hierarchy
2. **Center:** 8-state system (two 4-cycles) - Balloon hierarchy
3. **Right:** 10-state system (two 5-cycles) - Balloon hierarchy

### Key Features

**Top Row Visualizations:**
- Node size proportional to ΔCP value
- Multiple nodes at same level indicate complex hierarchy
- Single node indicates balloon (pinpoint) emergence
- Vertical position shows dimensionality (coarse-graining level)

**Bottom Row Profiles:**
- Horizontal axis: Dimensionality (2 = macroscale, n = microscale)
- Vertical axis: Mean ΔCP at each level
- Width of shaded region indicates ΔCP magnitude
- Complex hierarchy: ΔCP distributed across multiple levels
- Balloon hierarchy: ΔCP concentrated at single level

### Interpretation

**Critical Transition:**
- Cycle length ≤ 3: Complex hierarchies with multiple contributing scales
- Cycle length ≥ 4: Balloon hierarchies with single emergent scale
- Sharp discontinuous transition between length 3 and 4

**Mechanistic Insight:**
- Length-3 allows beneficial intermediate partitions
- Length-4+ forces direct microscale-to-macroscale jump
- Reflects topological constraint on emergent structure

### Technical Details

**Generation:**
- Script: `code/create_final_figures.py`
- Data sources: 
  - `results/results_6state_two_3cycles.pkl`
  - `results/results_8state_two_4cycles.pkl`
  - 10-state computed on-the-fly (greedy algorithm)
- Format: PNG, 300 DPI
- Dimensions: ~3000×2000 pixels

---

## Figure 2: Comparative Analysis

**Filename:** `figures/figure_comparative_analysis.png`

**Title:** Quantitative Comparison Across Cycle Lengths

### Description

This figure provides quantitative comparison of key metrics across the three verified systems, revealing systematic trends with cycle length.

**Layout:**
- **Left Panel:** CP values (microscale vs optimal macroscale)
- **Middle Panel:** ΔCP (degree of emergence)
- **Right Panel:** Number of emergent scales

### Key Features

**Left Panel: Causal Primitives**
- Blue bars: CP(microscale) - baseline causal power
- Orange bars: CP(optimal) - maximum causal power
- All systems achieve CP(optimal) = 1.0 (perfect determinism)
- CP(micro) increases with cycle length: 0.72 → 0.76 → 0.78

**Middle Panel: Emergence Magnitude**
- Green bars: ΔCP = CP(optimal) - CP(microscale)
- Decreases with cycle length: 0.28 → 0.24 → 0.22
- Represents "room for improvement" above microscale
- Longer cycles leave less causal structure to emerge

**Right Panel: Hierarchy Structure**
- Red bars: Count of emergent scales (excluding microscale)
- Sharp transition: 3 → 1 → 1
- Visualizes the critical cycle length effect
- Confirms balloon pattern for length ≥ 4

### Interpretation

**Trends with Increasing Cycle Length:**
1. CP(microscale) increases (more baseline structure)
2. ΔCP decreases (less emergence possible)
3. Emergent scales collapse (complex → balloon)

**Critical Point:**
- Between cycle lengths 3 and 4
- Not gradual transition - sharp discontinuity
- Suggests fundamental topological constraint

### Technical Details

**Generation:**
- Script: `code/comparative_cycle_analysis.py`
- Data source: `results/comparative_analysis.csv`
- Format: PNG, 300 DPI
- Dimensions: ~2400×800 pixels

**Data Values:**
```
System          | CP(micro) | CP(optimal) | ΔCP    | n_emergent
----------------|-----------|-------------|--------|------------
Two 3-cycles    | 0.7207    | 1.0000      | 0.2793 | 3
Two 4-cycles    | 0.7594    | 1.0000      | 0.2406 | 1
Two 5-cycles    | 0.7827    | 1.0000      | 0.2173 | 1
```

---

## Supplementary Figures (Archive)

### Archived Diagnostic Figures

Located in: `archive/figures_diagnostic/`

These figures were generated during the development process for diagnostic purposes:

1. **sensitivity_analysis.png** - Parameter sweep results (p_self variations)
2. **cp_distribution.png** - CP value distributions across partition space
3. **hierarchy_profile.png** - Detailed hierarchy structure analysis
4. **top_partitions.png** - Highest-CP partitions visualization

**Note:** These are not included in main results but available for reference.

---

## Usage in Publications

### Recommended Figure References

**In text:**
- "As shown in Figure 1, cycle length determines hierarchy structure..."
- "Quantitative comparison (Figure 2) reveals systematic trends..."

**Caption templates:**

**Figure 1:**
```
Emergent hierarchy structures for two-cycle systems with different 
cycle lengths. (Top) Complete hierarchies showing all scales with 
positive ΔCP. (Bottom) ΔCP distribution profiles. Note sharp transition 
from complex (length-3) to balloon (length-4,5) hierarchies.
```

**Figure 2:**
```
Quantitative comparison across cycle lengths. (Left) Causal Primitives 
at microscale and optimal macroscale. (Middle) Degree of emergence (ΔCP). 
(Right) Number of emergent scales, revealing critical transition at 
cycle length > 3.
```

### Citation

When using these figures, please cite:
```bibtex
@misc{onasenko2025verification,
  author = {Onasenko, Oleksii},
  title = {Independent Verification of Engineering Emergence},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/olexxa62-code/engineering-emergence-verification}
}
```

---

## Reproducibility

All figures can be regenerated from source data:
```bash
# Generate Figure 1 (cycle length discovery)
python code/create_final_figures.py

# Generate Figure 2 (comparative analysis)
python code/comparative_cycle_analysis.py
```

**Requirements:**
- Python 3.10+
- NumPy 2.2+
- Matplotlib 3.10+

**Runtime:**
- Figure 1: ~3 minutes (includes 10-state computation)
- Figure 2: <1 second (uses pre-computed results)

---

**Document Version:** 1.0  
**Last Updated:** December 12, 2025  
**Status:** [COMPLETE]
