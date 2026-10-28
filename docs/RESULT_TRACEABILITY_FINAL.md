# Result traceability audit (final, pre-submission)

Every quantitative claim in the abstract, results, discussion, conclusion,
cover letter and highlights traces to a pipeline output. Machine-readable
index: `results/final_key_results.csv`. Regenerate all sources with
`make all` (or `make sims figures tables`).

## Abstract

| Statement | Value | Source |
|---|---|---|
| 13 raw elements collapse to ~3 effective dimensions | d_eff = 2.9735 | data/processed/empirical_meta.json |
| fixed → rotating → exit under symmetric progress | R1>R2>R4, first switch step 24 | sim_trajectories.csv (rule A, all κ) |
| adaptation extends viability ~28% under symmetric progress | viability_extension = 0.275 (adaptive 0.875 vs fixed 0.600 of horizon) | sim_adaptation.csv (T1, all κ) |
| lineage-preserving optimal only in narrow window | R3 optimal steps 26–27 of 40 (T2) | sim_r3_window.csv |
| bulk chaining adds nothing | M3a ≡ M2 (net 0) | pcpc_model.py / sim_chain.csv |
| technological expiration near c_syn/V ≈ 0.05 | frontier cell boundary | sim_phase.csv, table_regimes.csv |
| no hysteresis, no path dependence | identical switch steps κ∈{0–1}; end_A=end_B=R2 | sim_hysteresis.csv, sim_pathdep.csv |

## Results (§5)

- §5.2 Fig. 4/Table 2: CRT_0.5, P_F values → sim_partial_source.csv, table_crt05.csv.
- §5.3 chain null + floor: net_benefit +0.013 (α=0.05) / +0.038 (α=0.10) at
  burden 0.5, negative at burden 2–8 → sim_chain.csv.
- §5.4 phase regions: verification-limited Δ/σ≲2, obsolete c_syn/V≲0.05 →
  sim_phase.csv classification.
- §5.5 retrospective BF: log10 BF ≈ 21–39 (k=1, σ_sig=3) → 5.28 at k=20;
  ≲4 at k=1 for σ_sig=0.5 → sim_retro.csv.
- §5.6 empirical: median separation 3.9σ (range 0.54–10.6), d_eff=2.97 →
  empirical_separability.csv / empirical_meta.json.
- §5.7 transitions: sequences and steps as abstract; regime-map bands
  R2 at c_syn/V∈[0.33,1] → sim_regime_map.csv.
- §5.8 adaptation: Δ_adapt = +1.2392V (T1, κ=0), −0.5247V (T2), 0 (T3,T4);
  Δ vs exit −0.6483V (T2), −0.0533V (T4) → sim_adaptation.csv.
  R3 window sensitivity 3 steps (penalty 0.5), 1 step (penalty 2) →
  sim_r3_window.csv.

## Discussion / Conclusion

- §7.2 (MLP mapping, hysteresis/path-dependence nulls): qualitative only;
  quantitative claims reuse §5.7–5.8 outputs.
- §7.3 bulk null, §7.4 adaptation-vs-exit, §7.6 frontier: as above.
- Propositions A–E: derived/demonstrated statements, no new numbers.
- Conclusion "empirically c_syn/V ≲ 0.05 bounds the last-surviving
  architecture's exit region" — table_regimes.csv (R4 boundary) +
  sim_phase.csv.

Numbering note: Table 5 = in-text falsification table (§6); Table 6 =
blockchain comparison (§7.5) — renumbered to first-citation order in the
minor final pass.

## Cover letter / Highlights

- "~28% viability extension" = 0.275 (T1) — sim_adaptation.csv.
- "two-step lineage window" = steps 26–27 — sim_r3_window.csv.
- "bulk chaining null", "attacker-favoring failure" (Δ vs exit = −0.65V),
  "expiration frontier" — sim_chain/sim_adaptation/sim_phase as above.

No headline number is unsupported. All costs are normalized (V=1); no
dollar magnitudes appear anywhere.
