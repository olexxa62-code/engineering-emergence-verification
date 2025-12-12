# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-12-12

### Added

**Verification Complete:**
- Independent implementation of Algorithm 1 (CE 2.0) from Jansma & Hoel (2025)
- Brute force analysis for systems up to 9 states
- Branching greedy algorithm for systems with 100,000+ partitions
- Three verified systems: 6-state, 8-state, 10-state (two-cycle configurations)

**Original Discovery:**
- Critical cycle length effect in emergent hierarchies
- Systems with cycle length 3 show complex hierarchies (3 emergent scales)
- Systems with cycle length 4+ show balloon hierarchies (1 emergent scale)
- Sharp transition between cycle lengths 3 and 4

**Documentation:**
- README.md with project overview and quick start
- METHODOLOGY.md with complete implementation details
- VERIFICATION_REPORT.md with system-by-system results
- CYCLE_LENGTH_DISCOVERY.md documenting original findings

**Code:**
- `analyze_6state_two_3cycles.py` - Six-state system analysis
- `analyze_8state_two_4cycles.py` - Eight-state system analysis
- `analyze_10state_two_5cycles.py` - Ten-state system analysis (greedy)
- `comparative_cycle_analysis.py` - Cross-system comparison
- `create_final_figures.py` - Publication-ready visualizations

**Results:**
- Validated CP calculations (within 1% of theoretical predictions)
- Confirmed emergent hierarchy structures match expected patterns
- Demonstrated algorithm scales to 115,975 partitions

**Metadata:**
- Apache 2.0 License
- CITATION.cff for academic citations
- requirements.txt for reproducibility

### Validated

- Causal Primitives (CP) formulas: Determinism and Specificity
- ΔCP computation: Non-redundant causal contributions
- Emergent hierarchy extraction: Correctly identifies contributing scales
- Microscale exclusion: Clarified as baseline reference, not emergent scale

### Discovered

- **Cycle length ≤ 3:** Complex emergent hierarchies
- **Cycle length ≥ 4:** Balloon emergent hierarchies
- **Critical transition:** Between cycle lengths 3 and 4
- **Topological constraint:** Hierarchy structure determined by cycle length, independent of dynamics parameters

### Fixed

- Microscale exclusion: Added post-processing filter to align mathematical algorithm with conceptual definition
- `is_refinement` bug in greedy algorithm: Was comparing partition with itself, causing ΔCP=0

## [0.2.0] - 2025-12-10

### Added
- Ten-state system analysis using branching greedy algorithm
- Sensitivity analysis across diffusion parameter range (p_self ∈ [0.0, 0.5])
- Comparative analysis framework

### Fixed
- Corrected 6-state emergent scale count (4 → 3) after microscale exclusion

## [0.1.0] - 2025-12-08

### Added
- Initial implementation of Algorithm 1 (CE 2.0)
- Six-state system verification (two 3-cycles)
- Eight-state system verification (two 4-cycles)
- Basic visualization tools

---

## Future Roadmap

### [1.1.0] - Planned

**Extended Verification:**
- [ ] Test cycle lengths 2, 6, 7, 8
- [ ] Asymmetric two-cycle systems (different cycle lengths)
- [ ] Three-cycle systems

**Theoretical Analysis:**
- [ ] Formal proof of cycle length effect
- [ ] Divisibility theorem for emergent scales
- [ ] Connection to graph automorphisms

**Performance:**
- [ ] GPU-accelerated partition enumeration
- [ ] Parallel computation of CP values
- [ ] Memory-efficient storage for large systems

**Applications:**
- [ ] Real-world network analysis
- [ ] Biological system modeling
- [ ] Neural network design principles

---

**Project:** Independent Verification of Engineering Emergence  
**Author:** Oleksii Onasenko  
**Repository:** https://github.com/olexxa62-code/engineering-emergence-verification
