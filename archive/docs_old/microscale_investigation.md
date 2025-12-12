# Microscale Exclusion in "Engineering Emergence": Algorithm vs. Intent

The microscale **should NOT be counted as an "emergent scale"** in Jansma and Hoel's emergent hierarchy, despite Algorithm 1's formalism appearing to include it. This apparent inconsistency between the mathematical specification and conceptual intent represents an important definitional ambiguity in the paper that warrants clarification.

## The algorithm mathematically includes the microscale

Algorithm 1 in Supplementary Section S2 (page 23) defines how ΔCP is computed for every partition in the lattice:

```
foreach P ∈ Nodes(H) do
    A ← Ancestors(H, P)
    if A is empty then
        b ← 0
    else
        b ← max{CPdict[Q] : Q ∈ A}
    ΔCPdict[P] ← CPdict[P] - b
```

For the microscale partition (the finest-grained partition with all individual states separate), there are **no ancestors**—nothing lies below it in the refinement lattice. When `A is empty`, the baseline `b` is set to **0**. This means:

**ΔCP(microscale) = CP(microscale) − 0 = CP(microscale)**

The "Emergent" set is then defined as `{P ∈ P | ΔCP[P] > ε}`. Since the paper shows microscale CP values like **0.63** (Figure 2) for typical systems, and ε is presumably a small threshold near zero, the microscale would mathematically satisfy the inclusion criterion. Nothing in Algorithm 1 explicitly excludes it.

## The conceptual definition explicitly excludes the microscale

Erik Hoel's blog post "I Figured Out How to Engineer Emergence" (October 2025) provides decisive clarification that contradicts the algorithm's literal interpretation:

- "In panel A (on the left) we see the full lattice, and, within it, the meager **4 scales (beyond the microscale)** that irreducibly causally contribute"
- "This is an emergent hierarchy: it is emergent because **all members are scales above the microscale** that have positive causal contributions when checked against every scale below it"

The phrase "beyond the microscale" when counting emergent scales, and "scales above the microscale" when defining the emergent hierarchy, unambiguously indicate that the microscale itself is **not** counted as an emergent scale. It serves as the **baseline reference** from which emergence is measured.

## Figure 3 corroborates the exclusion

Figure 3 shows a 5-state system with its emergent hierarchy. The caption states: "Panel B shows the sublattice that contains only these **five scales** (the emergent hierarchy)." The partitions explicitly listed are macroscale coarse-grainings like (0)(12)(34), (012)(34), etc.—none corresponding to the microscale partition where all 5 states remain separate. Additionally, "the microscale TPM is shown at the bottom of the panels" is phrased as contextual information displayed **separately** from the emergent hierarchy itself.

## Figure 4 shows ΔCP only for macroscales

The Figure 4 caption describes visualization "across the eight levels of coarse-graining" for 8-state systems. The shaded regions showing "average ΔCP at that level" represent the emergent hierarchy sublattice—the subset of scales with positive ΔCP relative to their ancestors. Since the microscale has no ancestors against which ΔCP can measure a meaningful "gain," it is conceptually excluded from this visualization. The emergent hierarchy captures scales that **contribute beyond** what lies below them; the microscale has nothing below to surpass.

## The philosophical rationale for exclusion

The paper defines the emergent hierarchy as "the subset of scales that contribute **non-zero and non-redundant gains in CP**." The key word is "gains"—implying comparison against something more fundamental. For macroscales, ΔCP measures their unique causal contribution above and beyond all scales beneath them along any micro→macro path. 

The microscale poses a conceptual problem: it has full CP but cannot claim any "gain" since nothing exists below it for comparison. Its causal contribution is not "emergent" in the sense that emergence requires transcending a more fundamental level. The microscale **is** the fundamental level—the ground truth baseline from which emergence is measured.

## The "balloon" example illuminates the distinction

Figure 4 (system ii) and Figure 6 show "balloon" emergent hierarchies where **only a single macroscale** contributes to the system's causal workings. If the microscale were counted as emergent, these would be "two-scale" hierarchies, but they're described as isolated single emergent macroscales "hanging up there by its lonesome." This confirms the microscale serves as the foundation of the lattice, not as a member of the emergent set.

## Summary of key findings

| Source | Treatment of Microscale |
|--------|------------------------|
| **Algorithm 1** | Would include if CP(micro) > ε, since baseline b = 0 when ancestors empty |
| **Emergent definition text** | "Scales that contribute non-redundant gains"—microscale has no scale to be non-redundant against |
| **Figure 3 caption** | Lists 5 emergent scales; microscale partition not among them |
| **Blog clarification** | "4 scales **(beyond the microscale)**" and "**scales above the microscale**" |
| **Conceptual interpretation** | Microscale is ground truth baseline, not an emergent contributor |

## Conclusion

The microscale should be **excluded** from the count of emergent scales. The algorithm's handling of empty ancestors (setting b = 0) appears to be a practical edge case rather than a statement that the microscale "emerges from nothing." The emergent hierarchy conceptually represents the causally-contributing macroscales that form **above** the microscale foundation. When the paper or authors discuss "n emergent scales," this count refers to scales beyond/above the microscale baseline, not including it. This interpretation aligns with the philosophy that emergence requires transcending a more fundamental description—a condition the microscale cannot satisfy by definition.