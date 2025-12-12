# Methodology

**Verification of Engineering Emergence (Jansma & Hoel, 2025)**  
**Author:** Oleksii Onasenko  
**Developer:** SubstanceNet

---

## 1. Theoretical Background

### 1.1 Causal Emergence Framework

The framework analyzes how causation is distributed across scales by computing **Causal Primitives (CP)** for each partition of a system's state space.

**CP = Determinism + Specificity - 1**

Where:
- **Determinism** = 1 - H(E|C)/log₂(n) — certainty of effects given causes
- **Specificity** = 1 - Degeneracy — uniqueness of effects (inverse degeneracy)
- **Degeneracy** = 1 - H(E)/log₂(n) — overlap in effects

Range: CP ∈ [0, 1]

### 1.2 Non-Redundant Gain (ΔCP)

For each partition P, the non-redundant causal contribution is:

**ΔCP(P) = CP(P) - max{CP(Q) : Q ∈ Ancestors(P)}**

This captures the unique causal contribution beyond all finer-grained partitions.

### 1.3 Emergent Hierarchy

**Emergent = {P ∈ Partitions | ΔCP(P) > ε}**

The subset of scales with positive non-redundant causal contributions.

**Critical Note:** The microscale is excluded as it serves as the baseline reference, not an emergent scale itself (see Section 4).

---

## 2. Implementation Architecture

### 2.1 Core Components
```python
# System Definition
class MarkovChain:
    - TPM (Transition Probability Matrix)
    - n_states
    - state_labels

# Partition Operations
def generate_partitions(n) -> List[Partition]
def coarse_grain(TPM, partition) -> TPM_macro
def is_refinement(P1, P2) -> bool

# Causal Analysis
def compute_determinism(TPM) -> float
def compute_degeneracy(TPM) -> float
def compute_CP(TPM) -> float
def compute_delta_CP(CP_dict, refinement_graph) -> Dict
```

### 2.2 Two-Cycle System Construction

All systems follow the pattern: Two disjoint cycles with diffusion dynamics.
```python
def create_two_cycle_system(cycle_length: int, p_self: float = 0.2):
    """
    Creates system with two symmetric cycles.
    
    Parameters:
    - cycle_length: Length of each cycle (3, 4, 5, ...)
    - p_self: Probability of self-loop
    - p_next: Probability of advancing = 1 - p_self
    
    States: 0 to (2*cycle_length - 1)
    Cycle 1: states 0 to (cycle_length-1)
    Cycle 2: states cycle_length to (2*cycle_length-1)
    """
    n = 2 * cycle_length
    TPM = np.zeros((n, n))
    
    for i in range(n):
        # Self-loop probability
        TPM[i, i] = p_self
        
        # Advance probability
        if i < cycle_length:
            next_state = (i + 1) % cycle_length
        else:
            next_state = cycle_length + ((i - cycle_length + 1) % cycle_length)
        TPM[i, next_state] = 1 - p_self
    
    return TPM
```

**Example:** 6-state system (two 3-cycles)
- Cycle 1: 0→1→2→0
- Cycle 2: 3→4→5→3
- p_self = 0.2, p_next = 0.8

---

## 3. Algorithm 1: Brute Force (n ≤ 9)

### 3.1 Complete Enumeration
```python
def run_algorithm1(TPM):
    """
    Exhaustive search over all partitions.
    Feasible for n ≤ 9 states.
    """
    n = len(TPM)
    
    # Step 1: Generate all partitions
    all_partitions = generate_all_partitions(n)
    # Count: Bell number B(n)
    # B(6) = 203, B(8) = 4140, B(9) = 21147
    
    # Step 2: Compute CP for each partition
    CP_dict = {}
    for P in all_partitions:
        TPM_macro = coarse_grain(TPM, P)
        CP_dict[P] = compute_CP(TPM_macro)
    
    # Step 3: Build refinement lattice
    refinement_graph = build_refinement_graph(all_partitions)
    
    # Step 4: Compute ΔCP
    delta_CP_dict = {}
    for P in all_partitions:
        ancestors = get_ancestors(P, refinement_graph)
        if len(ancestors) == 0:
            baseline = 0  # Microscale case
        else:
            baseline = max(CP_dict[Q] for Q in ancestors)
        delta_CP_dict[P] = CP_dict[P] - baseline
    
    # Step 5: Extract emergent hierarchy
    epsilon = 1e-10
    emergent = [P for P in all_partitions if delta_CP_dict[P] > epsilon]
    
    # Step 6: Exclude microscale
    microscale = tuple((i,) for i in range(n))
    emergent_filtered = [P for P in emergent if P != microscale]
    
    return {
        'CP': CP_dict,
        'delta_CP': delta_CP_dict,
        'emergent': emergent_filtered,
        'n_emergent': len(emergent_filtered)
    }
```

### 3.2 Complexity Analysis

- **Partitions:** B(n) — Bell number (superexponential)
- **CP Computation:** O(n²) per partition
- **Refinement Check:** O(B(n)²) worst case
- **Total:** O(B(n) · n² + B(n)²)

**Practical Limit:** n ≤ 9 states

---

## 4. Algorithm 2: Branching Greedy (n > 9)

### 4.1 Sampling Strategy

For larger systems, exhaustive enumeration is infeasible:
- B(10) = 115,975
- B(15) ≈ 1.38 × 10⁹

Branching greedy algorithm samples high-CP paths through partition lattice.
```python
def branching_greedy(TPM, n_paths=3):
    """
    Samples multiple greedy paths from microscale upward.
    """
    n = len(TPM)
    microscale = tuple((i,) for i in range(n))
    
    CP_dict = {microscale: compute_CP(TPM)}
    sampled_partitions = {microscale}
    
    current_level = [microscale]
    
    while len(current_level) > 0:
        next_level = []
        
        for P in current_level:
            # Generate all one-step coarsenings
            candidates = []
            blocks = list(P)
            k = len(blocks)
            
            for i in range(k):
                for j in range(i+1, k):
                    # Merge blocks i and j
                    Q = merge_blocks(P, i, j)
                    
                    if Q not in CP_dict:
                        TPM_Q = coarse_grain(TPM, Q)
                        CP_dict[Q] = compute_CP(TPM_Q)
                        sampled_partitions.add(Q)
                    
                    candidates.append((CP_dict[Q], Q))
            
            # Select top n_paths candidates
            candidates.sort(reverse=True)
            top_candidates = candidates[:n_paths]
            next_level.extend([Q for (cp, Q) in top_candidates])
        
        current_level = next_level
    
    # Build refinement graph over sampled partitions
    refinement_graph = build_refinement_graph(sampled_partitions)
    
    # Compute ΔCP
    delta_CP_dict = compute_delta_CP(CP_dict, refinement_graph)
    
    # Extract emergent hierarchy (excluding microscale)
    emergent = [P for P in sampled_partitions 
                if delta_CP_dict[P] > 1e-10 and P != microscale]
    
    return {
        'CP': CP_dict,
        'delta_CP': delta_CP_dict,
        'emergent': emergent,
        'n_emergent': len(emergent),
        'n_sampled': len(sampled_partitions)
    }
```

### 4.2 Coverage Analysis

**10-state system (two 5-cycles):**
- Total partitions: 115,975
- Sampled: ~500-1000 (with n_paths=3)
- Coverage: ~0.5-1%
- **Key insight:** High-CP partitions are sparse, greedy search effective

---

## 5. Microscale Exclusion

### 5.1 Conceptual Issue

**Algorithm 1 (Step 4)** mathematically includes microscale:
- Microscale has no ancestors → baseline = 0
- ΔCP(microscale) = CP(microscale) - 0 = CP(microscale) > 0
- Formally satisfies ΔCP > ε criterion

**However**, conceptually the microscale should be excluded:
- Jansma & Hoel: "scales **beyond** the microscale"
- Microscale is the **baseline reference**, not an emergent scale
- Emergence requires transcending a more fundamental level

### 5.2 Solution

**Post-processing filter (Step 6):**
```python
microscale = tuple((i,) for i in range(n))
emergent_filtered = [P for P in emergent if P != microscale]
```

This aligns implementation with conceptual definition.

### 5.3 Impact on Results

**6-state system:**
- Before filtering: 4 emergent scales (including microscale)
- After filtering: 3 emergent scales (correct)

**8-state and 10-state systems:**
- Before filtering: 2 emergent scales
- After filtering: 1 emergent scale (balloon hierarchy)

---

## 6. Validation Methods

### 6.1 Direct Verification

**CP values** verified against paper's Figure 2:
- Our CP(micro) for 6-state: 0.7207
- Paper's approximate value: ~0.72 

**Optimal macroscale** always achieves CP = 1.0:
- Partitioning two cycles into two blocks
- Creates perfect deterministic dynamics (self-loops)

### 6.2 Sensitivity Analysis

Test robustness across p_self ∈ [0.0, 0.5]:
```python
for p_self in np.linspace(0.0, 0.5, 11):
    TPM = create_two_cycle_system(cycle_length, p_self)
    results = run_algorithm1(TPM)
    # Track: CP(micro), ΔCP, n_emergent
```

**Findings:**
- CP(micro) decreases as p_self increases (more noise)
- ΔCP increases (larger gap between micro and macro)
- n_emergent remains stable (hierarchy structure preserved)

### 6.3 Cross-System Comparison

Compare systems of different sizes:
- 6-state (two 3-cycles): 203 partitions → 3 emergent
- 8-state (two 4-cycles): 4,140 partitions → 1 emergent
- 10-state (two 5-cycles): 115,975 partitions → 1 emergent

**Reveals:** Cycle length effect (see CYCLE_LENGTH_DISCOVERY.md)

---

## 7. Computational Infrastructure

### 7.1 Hardware

**HP Omen 17 Workstation:**
- CPU: AMD Ryzen 9 8945HS (8 cores, 16 threads)
- RAM: 32 GB DDR5-5600
- GPU: RTX 4060 (not used for this project)
- OS: Pop!_OS 22.04 LTS

### 7.2 Software

**Python Environment:**
- Python 3.10.12
- NumPy 2.2.6 (numerical computations)
- Matplotlib 3.10.3 (visualizations)
- Standard library: itertools, pickle, csv

### 7.3 Runtime Performance

| System | States | Partitions | Algorithm | Time |
|--------|--------|------------|-----------|------|
| 6-state | 6 | 203 | Brute Force | ~2 sec |
| 8-state | 8 | 4,140 | Brute Force | ~45 sec |
| 10-state | 10 | 115,975 | Greedy | ~3 min |

---

## 8. Reproducibility

### 8.1 Deterministic Execution

All computations are deterministic:
- No random seeds required
- Fixed system parameters (p_self = 0.2)
- Exhaustive enumeration (where feasible)

### 8.2 Verification Checksum

**6-state system (two 3-cycles, p_self=0.2):**
- CP(microscale) = 0.720749
- CP(optimal) = 1.000000
- ΔCP = 0.279251
- n_emergent = 3

**8-state system (two 4-cycles, p_self=0.2):**
- CP(microscale) = 0.759398
- CP(optimal) = 1.000000
- ΔCP = 0.240602
- n_emergent = 1

**10-state system (two 5-cycles, p_self=0.2):**
- CP(microscale) = 0.782729
- CP(optimal) = 1.000000
- ΔCP = 0.217271
- n_emergent = 1

---

## 9. Limitations and Future Work

### 9.1 Current Limitations

1. **System Size:** Brute force limited to n ≤ 9
2. **System Type:** Only two-cycle diffusion systems tested
3. **Greedy Coverage:** Samples ~1% of partition space for n=10
4. **No Parallelization:** Single-threaded implementation

### 9.2 Potential Extensions

1. **Larger Systems:** GPU-accelerated partition enumeration
2. **Diverse Systems:** Source-cycle-sink, modular, hierarchical
3. **Smarter Sampling:** Information-theoretic guided search
4. **Parallel Implementation:** Multi-core CP computation
5. **Theoretical Analysis:** Formal proof of cycle length effect

---

**End of Methodology**
