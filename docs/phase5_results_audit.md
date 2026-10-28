# Phase 5 — Results audit (pre-manuscript)

All answers trace to `data/processed/*.csv` produced by
`analysis/run_simulations.py` (seed 20261003).

## The 10 mandated questions

1. **Does rotation outperform a fixed fingerprint?**
   Yes under the normalized cost model, conditionally. For fixed targets (M1)
   the attacker amortizes development cost across the entire series life;
   rotation forces re-development per series (`sim_regimes.csv`). The gain is
   an *amortization* gain, not an authentication gain: an attacker who can
   synthesize a state cheaply beats both.

2. **Does physical chaining outperform rotation alone?**
   Bulk chaining (M3a): **No.** Under Attack 3 the bulk target y_t is a public
   deterministic function; synthesis matches it without predecessor material.
   F3 confirmed.
   Inclusion chaining (M3b): **Yes, narrowly.** It adds a mass-conservation
   floor \(C_F^{lineage} \ge \alpha\kappa V\) per unit forged value, binding on
   all attacker classes that lack genuine predecessor mass.

3. **Is bulk chaining actually useful?**
   No incremental security under assay-aware synthesis (F3). Its only role is
   as an issuer-attestation signal (cosmetic chaining).

4. **Is lineage-preserving chaining useful?**
   Only when inclusion verification is cheap: net benefit positive at
   α ≥ 0.05 under burden coefficient 0.5, negative under burden coefficient
   ≥ 2 (`sim_chain.csv`). F4 is a live risk.

5. **How large is MRA?**
   In normalized units, \(C_F/C_I^{rotate}\) ranges ~1.5–150 across the
   c_syn/V grid at c_rotate = 0.02V (`sim_regimes.csv`, MRA column). MRA ≫ 1
   holds only where synthetic fabrication remains costly.

6. **What determines CRT?**
   CRT_0.5 = 0 whenever Δ/σ ≤ 2: a zero-source "mean" attack already passes
   verification ≥ 50 % of the time. Only for Δ/σ ≥ 4 do positive thresholds
   appear; at Δ/σ = 8, CRT_0.5 ≈ 0.7–0.9 for small N and falls toward 0 as
   N → 50 (`table_crt05.csv`). Counter-intuitively, **larger N reduces CRT**
   because mixtures concentrate near the centroid — coalition size alone does
   not buy security (Proposition 3 supported, with a sign twist).

7. **At what fabrication cost does the system collapse?**
   Phase diagram (`sim_phase.csv`, Fig. 5): economically forgeable once
   \(c_{syn}/V \lesssim 0.05\); technologically obsolete below that across all
   Δ/σ. Verification-limited whenever Δ/σ ≲ 2.

8. **Does future money provide measurable evidence about past states?**
   Yes but decaying (`sim_retro.csv`, Fig. 7): against a 3σ-mismatch
   inclusion-forger, log10 BF ≈ 21–39 at depth 1 and ≈ 5 at depth 20
   (α=0.10). Against a 0.5σ-mismatch near-perfect fabricator, BF ≈ 1.4–3.8
   at depth 1 and ≈ 1.1 at depth 20 — i.e., retrospective evidence evaporates.
   F7: conditional pass.

9. **Are effects practically meaningful?**
   The binding constraint is *verification capability*, not fingerprint
   entropy. With realistic analytical noise and correlated markers,
   Δ/σ must exceed ~4 per effective dimension for source-access attacks to
   bind — satisfied by real meteorite-group separations (median 3.9 σ/dim
   across 16 complete 13-element group fingerprints).

10. **Which original intuitions failed?**
    - Bulk physical inheritance adds zero security (F3) — the strongest prior
      intuition fails.
    - Chaining's real contribution is a *supply-side* constraint (needing
      genuine predecessor mass), not a new cryptographic property.
    - More coalition sources can *hurt* verification security via centroid
      concentration.
    - Empirical d_eff ≈ 3 for a 13-element fingerprint — marker correlation
      eats most apparent dimensionality (F2 confirmed).

## Empirical calibration highlights

- 2,612 sample-level records, 23 AstroMat/IEDA datasets, acquisition ledger
  with SHA-256 in `data/acquisition_ledger.csv`.
- 16 iron-meteorite chemical groups with complete 13-element fingerprints;
  pairwise separations 0.54–10.6 σ per dimension, median 3.9.
- d_eff = 2.97 (eigenvalue participation ratio of group covariance).
- MC convergence at R = 200 geometry reps: MC se < 0.004; closed-form P_F
  verified against brute-force MC (test_model.py).

## Honest negative results carried into the manuscript

- F2 (correlated markers) — confirmed empirically.
- F3 (bulk chaining null) — confirmed analytically + in regimes table.
- F4 (verification burden) — binds for realistic inclusion-assay cost.
- F6 (synthetic collapse) — collapse frontier at c_syn/V ≈ 0.05.
- F7 (retrospective decay) — confirmed for capable fabricators.
