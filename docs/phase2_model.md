# Phase 2 — Formal model specification (locked before simulation)

## 1. Notation

- Sources $i = 1,\dots,N$; source fingerprint $\mathbf{x}_i \in \mathbb{R}^{d}$ in log-concentration (or log-ratio) space.
- Issued batch $t$: mixture weights $\mathbf{w}_t \in \Delta^{N-1}$, $w_{it} \ge w_{\min}$.
- Batch state $\mathbf{y}_t = g\!\left(\alpha\,\mathbf{p}_{t-1} + \sum_i w_{it}\mathbf{x}_i\right) + \boldsymbol{\epsilon}_t$, $\boldsymbol{\epsilon}_t \sim \mathcal{N}(0, \Sigma_{\mathrm{mfg}})$.
- $\mathbf{p}_{t-1}$: authenticated material of batch $t{-}1$; $\alpha \in \{0, 10^{-4}, 10^{-3}, 10^{-2}, 0.05, 0.10\}$.
- Batch code $D_t$ (public); target fingerprint $\mathbf{y}_t$ **public** (main analysis). Confidential-$\mathbf{w}$ is a sensitivity analysis only.
- Observation of a candidate coin: $\mathbf{z}$; verification $\;D_M^2 = (\mathbf{z}-\mathbf{y}_t)^{\top}\Sigma_t^{-1}(\mathbf{z}-\mathbf{y}_t) \le \tau$, $\tau = \chi^2_{d_{\mathrm{eff}}}(1-\beta)$ with false-reject level $\beta$.
- $\Sigma_t = \Sigma_{\mathrm{analyt}} + \Sigma_{\mathrm{mfg}}$; markers correlated; $d_{\mathrm{eff}}$ = effective rank (eigenvalue participation ratio).

## 2. Regimes

- **M0** ordinary commodity coin: no engineered fingerprint (verification = none; $P_F = 1$).
- **M1** fixed provenance: one authenticated composition, static.
- **M2** rotating provenance: $\alpha = 0$, $\mathbf{y}_t$ rotates each interval $T_R$.
- **M3** PCPC: rotation + predecessor inheritance ($\alpha > 0$), two architectures:
  - **M3a bulk inheritance**: predecessor remelted and homogenized; only bulk composition observable.
  - **M3b lineage-preserving inclusions**: predecessor material embedded as detectable micro-inclusions at volume fraction $\alpha_{\mathrm{incl}}$, isotopically resolvable from matrix.

## 3. Attacker classes (locked)

- A0 generic copy (no assay): $z \sim$ global population mixture.
- A1 assay-aware: measures public $\mathbf{y}_t$; synthesizes with residual tolerance $\Sigma_{\mathrm{syn}}$.
- A2 partial source access: holds $k$ of $N$ authentic sources, $q = k/N$; best approximation = Euclidean projection of target mixture onto attainable set.
- A3 isotope engineering: A2 + synthesis; cost $C_{\mathrm{syn}}$ per unit mass, residual error $\Sigma_{\mathrm{syn}}$.
- A4 microstructure-capable: can synthesize inclusions at extra cost $C_{\mathrm{incl}}$, residual microstructural error.
- A5 asymptotic: $C_{\mathrm{syn}} \to 0$ (defines failure frontier).

## 4. Costs (normalized; no fabricated dollars)

All costs normalized by coin/batch face value $V$ (reported as ratios; absolute
calibration via isotope-separation literature as sensitivity only).

- Issuer rotation cost $C_I^{\mathrm{rotate}} = c_{\mathrm{mix}} + c_{\mathrm{assay,issue}}$ (bounded by remelt+assay; normalized grid).
- Attacker $C_F = \min(C_F^{\mathrm{source}}, C_F^{\mathrm{syn}})$; for M3b add $C_F^{\mathrm{lineage}}$.
- **Mass-conservation constraint (M3b only):** forging mass $M$ of batch $t$ requires $\ge \alpha_{\mathrm{incl}} M$ of *genuine* batch $t{-}1$ metal. Genuine predecessor mass has circulation value $\approx V$ per unit mass, hence a floor cost $C_F^{\mathrm{lineage}} \ge \alpha_{\mathrm{incl}} M \cdot V/M = \alpha_{\mathrm{incl}} V$ per unit forged mass — plus collection premium $\kappa \ge 1$. This is the core additional cost the chaining hypothesis must exploit; it is honest only because old coins circulate at face value. It is *not* a secrecy assumption.
- $C_F^{\mathrm{syn}} = c_{\mathrm{syn}} \cdot (\text{mass}) + c_{\mathrm{dev}}$ (one-time development cost amortized over forgeable mass within residual lifetime of series).

## 5. Metrics (locked)

- $P_F$: probability a forged coin passes authentication.
- $E[\Pi_F]/V = P_F \cdot 1 - C_F/V$: primary outcome.
- $\mathrm{MRA}_t = C_F(t) / C_I^{\mathrm{rotate}}(t)$.
- $\mathrm{CRT}_p = \min\{q : P_F(q) \ge p\}$, $p \in \{0.1, 0.5, 0.9\}$.
- $\rho_T = T_F / T_R$; residual circulation value $V_t(a) = V_0 \rho(a)$ with exponential decay to recall.
- Retrospective evidence: Bayes factor $\mathrm{BF}_k = p(\mathbf{z}_{\mathrm{incl}}^{(t)} \mid \mathrm{chain\ genuine}) / p(\mathbf{z}_{\mathrm{incl}}^{(t)} \mid \mathrm{link\ } k \mathrm{\ forged})$ for depth $k = 1, 2, 5, 10, 20$.

## 6. Falsification criteria (F1–F7, as briefed)

F1 source variability ≲ noise; F2 marker correlation collapses $d_{\mathrm{eff}}$;
F3 bulk chaining adds nothing under A3; F4 inclusion verification too costly;
F5 $\mathrm{MRA} \approx 1$; F6 $C_{\mathrm{syn}} <$ counterfeit revenue;
F7 no retrospective evidence at depth ≥ 2.

## 7. Key structural results derived analytically (to be confirmed by simulation)

- **M3a null (expected F3):** under full homogenization, $\mathbf{y}_t$ is a
  deterministic function of observables; an A3 attacker matching bulk
  composition needs no genuine predecessor → bulk $\alpha$ adds zero
  reconstruction cost. Bulk chaining is security only through the *issuer's
  attestation channel* (claimed lineage), i.e., cosmetic chaining.
- **M3b mass floor:** forgeable value per unit genuine predecessor mass
  acquired $\le 1/(\alpha_{\mathrm{incl}}\kappa)$; chaining converts
  counterfeiting into a *supply-constrained* attack.
- **Retrospective depth:** inclusion lineage signal decays $\propto \alpha^k$
  unless inclusions are *nested-sequestered* (inclusions of generation $t{-}1$
  preserved intact, each carrying its own older inclusions). With nested
  preservation the signal decays only through measurement dilution, giving
  bounded but non-trivial depth — quantified in Phase 4.

## 8. Simulation design (locked)

- Analysis A: empirical fingerprints from UCLA/AstroMat groups
  ($\sim$50 parent-body groups, 13 elements, log-space); pairwise
  separability + $d_{\mathrm{eff}}$ via effective rank; mixture
  distinguishability demo for $N \in \{3,5,10,20,50\}$ sampled groups.
- Analysis B: generalized sweep, source separation $\Delta/\sigma \in \{0.1,0.25,0.5,1,2,4,8\}$, $d_{\mathrm{eff}} \in \{2,4,8,16,32\}$, $N \in \{3,5,10,20,50\}$, $q \in [0,1]$ step 0.1, $\alpha$ grid, $c_{\mathrm{syn}}/V \in [10^{-3}, 10^{2}]$ log-grid, $R = 10^4$ replicates per condition; common random seeds; convergence check at $R/10$.
- Mint optimization: $\mathbf{w}^*_t = \arg\max [C_F(\mathbf{w}) - \lambda C_I(\mathbf{w}) - \gamma C_V(\mathbf{w})]$ with minimum inter-state distance $D_{\min}$; solved by projected gradient / random restarts on the simplex.
