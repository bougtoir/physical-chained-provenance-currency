# When Authentication Technologies Expire: Technology-Dependent Institutional Transitions in a Physical-Provenance Currency

*(Working draft; pre-registration and gate docs in `docs/`)*

## Abstract

Institutions that certify authenticity — monetary anti-counterfeiting, provenance certification, tamper evidence — rest on cost asymmetries: authorized updating must be cheaper than adversarial reconstruction, and verification must be affordable. We model how technological progress erodes these asymmetries as an endogenous institutional transition: authentication regimes — fixed provenance, rotating provenance, lineage-preserving physical chaining, and exit — compete under a technology state \(\boldsymbol\theta_t\) combining assay, synthesis, microfabrication and verification costs, and an issuer chooses regimes under a switching-cost objective. The framework is instantiated and calibrated as a Physical Chained Provenance Currency on {{n_samples}} measured iron-meteorite fingerprints, evaluated by Monte-Carlo and closed-form analysis across four technology trajectories. Under symmetric progress the optimal sequence is fixed \(\rightarrow\) rotating \(\rightarrow\) exit; adaptive switching extends viability by {{viability_ext_T1_pct}}% of the horizon. Under attacker-favoring progress lineage-preserving chaining is optimal for only a {{T2_r3_steps}}-step window and early exit dominates. Bulk predecessor remelting adds zero security; coalition size has non-monotonic security effects — under some source geometries additional contributors reduce separability; {{n_elements}} markers collapse to \(d_{\mathrm{eff}}\approx{{d_eff_int}}\); and every physical-provenance regime reaches a technological expiration frontier near \(c_{\mathrm{syn}}/V \approx {{expiration_frontier}}\). Technological progress can change which authentication institution is rational — not merely how secure a fixed one remains.

**Keywords:** technological change; institutional adaptation; authentication; counterfeiting; provenance; physical unclonable function; regime transition; obsolescence

## 1. Introduction

Many institutions derive credibility from a cost asymmetry: an authorized party can update or produce a physical signal cheaply, while an adversary's reconstruction of that signal is expensive, and observers' verification of it is affordable. Banknotes, assay marks, provenance certificates, tamper-evident seals and forensic taggants all live on this asymmetry. Technological progress — cheaper assay, cheaper isotope or elemental synthesis, cheaper microfabrication — does not merely weaken such institutions uniformly; it erodes each leg of the asymmetry at its own rate. That observation motivates a dynamic, institutional design question: *as the relative costs of authorized updating, adversarial reconstruction, and verification evolve, which authentication institution remains viable, and when should an issuer adapt, switch architectures, or abandon physical provenance altogether?*

This question sits inside a recognized scholarly conversation on technology-driven institutional change — socio-technical transition theory models how landscape pressure displaces incumbent regimes [1, 2], formal transition modelling is an established method [3], and adoption studies treat provenance technologies as evolving socio-technical systems [4]. What that conversation lacks is a model in which the institutional object is an *authentication architecture* whose viability is set by adversarial reproduction economics. We supply one: authentication regimes are states, technology is a trajectory through normalized cost space, and institutional transition is endogenous.

The theory needs a stress test in which substrate scarcity cannot rescue the institution. Commodity money provides it: monetary systems are authentication-constrained as much as scarcity-constrained [5–9], and monetary-search models of counterfeiting already formalize the joint role of production cost and verification [6–8]. We therefore instantiate the framework as a Physical Chained Provenance Currency (PCPC): an issuer batches an abundant substrate (iron) with a public, dated, isotopically fingerprinted source mixture, and may physically inherit authenticated predecessor material — a *physical chained ledger* in which the money stock records part of its own issuance history. The federated, interplanetary reading of the model functions as an extreme test environment — abundant substrate, distributed issuers, diverse source fingerprints — but no result depends on extraterrestrial assumptions, and all costs are normalized rather than asserted in dollars.

We find that the interesting object is not the currency but the *transition structure*: technological progress changes which authentication institution is optimal, not merely how secure a fixed one is. Fixed provenance yields to rotating provenance, rotating to lineage-preserving chaining only in a narrow microfabrication-cost corridor, and every physical-provenance regime reaches a technological expiration frontier beyond which exit is rational. Adaptation itself is trajectory-dependent: it extends viability under symmetric progress and is dominated by early exit under attacker-favoring progress.

## 2. Related literature and conceptual boundary

### 2.1 Commodity money and counterfeiting

Sargent and Velde's history of small change shows commodity monetary systems are authentication-constrained, not merely scarcity-constrained [5]. Monetary-search theory models counterfeiting as a cost/verification equilibrium: in random-search models counterfeiting threatens the existence of monetary equilibrium [6]; competitive-search extensions generate equilibria where counterfeit quality and seller verification co-determine outcomes [7, 8]. Debasement and seigniorage analysis [9] supplies the issuer-side cost framework. All of this literature treats the authentication target as fixed in time; PCPC adds the target state itself as a policy variable.

### 2.2 Material provenance

Isotopic and multi-element provenance is a mature forensic science: lead-isotope sourcing in archaeometallurgy [10], Bayesian isotope mixing models for source apportionment [11], and — most relevant here — iron-meteorite chemical and isotopic classification, where five decades of INAA/RNAA analysis distinguish parent-body reservoirs by Ni, Co, Cu, Ga, Ge, As, Sb, W, Re, Ir, Pt and Au abundances [12–14]. These datasets provide our empirical fingerprint space. Note that cosmogenic overprinting modifies Fe and Cr isotopes in iron meteorites, so group-level elemental abundances (not single-isotope ratios) form the robust calibration target [12].

### 2.3 Dynamic anti-counterfeit systems and PUFs

Physical unclonable functions exploit manufacturing disorder for per-object authentication [15]. Two hardware literatures approach our mechanism: dynamic PUFs, whose responses change with query timing [16, 17], and reconfigurable PUFs, whose challenge–response map is issuer-updatable. PCPC differs in kind: the *batch* state is issuer-selected and rotates across a money supply; predecessor dependence is a property of the monetary stock, not of a single device. Tagants and forensic markers (lanthanide signatures, DNA markers) provide per-batch identity without state chaining [18].

### 2.4 Physical ledgers and the novelty boundary

Prior "physical blockchain" work chains *digital records about* physical objects: chemical signatures hashed to Ethereum [18], DNA-steganographic signature materials cross-referenced over time [19], physical hashes of toolpaths for additive-manufacturing integrity [20], and material fingerprints embedded in Digital Product Passport verifiable credentials [21]. In all of them the chain is cryptographic and digital; the physical layer supplies a key or tag, not the state being chained. We found no prior mechanism satisfying \(S_t = f(S_{t-1}, X_t)\) *in the material domain* for monetary or authentication purposes. This is the novelty under test — tested, not assumed: the falsification criteria in §6 include the possibility that physical chaining adds nothing.

### 2.5 Technology–institution transitions

Our dynamic framing borrows from transitions research: the Multi-Level Perspective describes incumbent regimes displaced by niche alternatives under landscape pressure [1]; transition scholarship has matured into formal, model-based analysis [2, 3] — notably reviews of socio-technical energy-transition models that map directly onto our regime-switching formalism [3]; and the economics of technological lock-in supply the switching-cost and path-dependence hypotheses we test [22, 23]. Within TFSC's technology-adoption conversation, provenance technologies have been treated as evolving socio-technical objects (blockchain provenance in supply chains [4]; digital-currency operation under institutional change [24]) — but always for digital authentication layers. Our contribution complements that literature by modeling the *material* authentication layer and treating the institutional architecture itself as the object that technology renders obsolete.

## 3. Theoretical framework

### 3.1 Federated source materials

Let \(N\) sources (polities, regions, ore bodies — in the test setting, planetary sources) supply the substrate. Source \(i\) carries fingerprint \(\mathbf{x}_i \in \mathbb{R}^{d}\) in log-concentration or isotope space; iron is the bulk substrate, not necessarily the authentication channel — the distinction matters because bulk-substrate abundance is the premise, while authentication rides on whichever marker dimensions are separable (§5.1).

### 3.2 Time-indexed state rotation

Batch \(t\) has public weights \(\mathbf{w}_t \in \Delta^{N-1}\) and state
\[
\mathbf{y}_t = g\!\left(\sum_i w_{it}\mathbf{x}_i\right) + \boldsymbol{\epsilon}_t,
\qquad \boldsymbol{\epsilon}_t \sim \mathcal{N}(0,\Sigma_{\mathrm{mfg}}),
\]
where \(g(\cdot)\) captures processing fractionation and \(\Sigma_t = \Sigma_{\mathrm{mfg}} + \Sigma_{\mathrm{analyt}}\). The pair \((D_t, \mathbf{y}_t)\) — date code and target fingerprint — is public; secrecy of \(\mathbf{w}_t\) is examined only as a sensitivity analysis. Figure 1 summarizes the architecture.

### 3.3 Physical predecessor linkage

PCPC adds authenticated predecessor material \(\mathbf{p}_{t-1}\) at fraction \(\alpha\):
\[
\mathbf{y}_t = g\!\left[\alpha\,\mathbf{p}_{t-1} + (1-\alpha)\sum_i w_{it}\mathbf{x}_i\right] + \boldsymbol{\epsilon}_t,
\qquad \alpha \in \{0, 10^{-4}, 10^{-3}, 10^{-2}, 0.05, 0.10\}.
\]
Two architectures implement this. *M3a, bulk inheritance*: predecessor metal is remelted and homogenized. *M3b, lineage-preserving inclusions*: predecessor material is embedded as micro-inclusions at volume fraction \(\alpha_{\mathrm{incl}}\), isotopically resolvable from the matrix — macroscopically usable currency with microscopically preserved lineage.

### 3.4 Verification

A candidate coin yields observation \(\mathbf{z}\); acceptance requires
\[
D_M^2 = (\mathbf{z}-\mathbf{y}_t)^{\top}\Sigma_t^{-1}(\mathbf{z}-\mathbf{y}_t) \le \tau,
\qquad \tau = \chi^2_{d_{\mathrm{eff}}}(1-\beta),
\]
with \(\beta\) the false-reject level (10\(^{-3}\) in our runs). Because markers are correlated, all results are reported against the *effective* dimension \(d_{\mathrm{eff}}\), defined as the eigenvalue participation ratio of the fingerprint covariance — mandatory given our empirical finding that {{n_elements}} raw elements collapse to \(d_{\mathrm{eff}} \approx {{d_eff_int}}\). For M3b, verification is multilevel: matrix composition, inclusion composition, and inclusion spatial statistics.

### 3.5 Counterfeiter optimization

Attack classes: **A0** generic substrate copy; **A1** assay-aware synthesis of the public target; **A2** partial source access \(q = k/N\) with best-approximation forgery; **A3** full isotope engineering at cost \(c_{\mathrm{syn}}\) per unit mass; **A4** microstructure-capable synthesis; **A5** asymptotic fabrication (\(c_{\mathrm{syn}} \to 0\)). The attacker minimizes
\[
C_F = \min\left(C_F^{\mathrm{source}},\, C_F^{\mathrm{syn}}\right),
\]
plus, under M3b, a lineage term \(C_F^{\mathrm{lineage}} \ge \alpha_{\mathrm{incl}}\kappa V\) per unit forged value: forged mass \(M\) requires \(\alpha_{\mathrm{incl}}M\) of *genuine* predecessor metal worth its circulation value, \(\kappa \ge 1\) a collection premium. This is the honest core of chaining: predecessor coins circulate, so the constraint is a supply constraint, not a secrecy assumption. Figure 2 illustrates the attacker geometry.

### 3.6 Economic viability

With pass probability \(P_F\) and realizable value \(V_t\),
\[
E[\Pi_F] = P_F V_t - C_F, \qquad \mathrm{MRA}_t = \frac{C_F(t)}{C_I^{\mathrm{rotate}}(t)},
\]
where \(C_I^{\mathrm{rotate}}\) is issuer rotation cost. A state is counterfeit-resistant when \(E[\Pi_F] < 0\). Series rotation adds an amortization effect: forging is profitable only if development cost recovers within the residual circulation lifetime \(V_t(a)\) of the series, with \(\rho_T = T_F/T_R\) the attacker-to-rotation time ratio.

### 3.7 Technology state and endogenous institutional adaptation

We place the static model inside an institutional-choice problem. Define a technology state \(\boldsymbol\theta_t = (c_{\mathrm{assay},t},\, c_{\mathrm{syn},t},\, c_{\mathrm{micro},t},\, c_{\mathrm{ver},t},\, q_t)\), all normalized to unit face value \(V\): respectively the costs of identifying a target state, of synthetic compositional reconstruction, of reproducing microstructural (lineage-preserving) features, of authorized verification, and attacker access to legitimate source material. Technological progress is *movement through this parameter space* — we make no calendar-time claims.

The issuer selects an authentication regime \(r_t \in \mathcal{R} = \{R_0, R_1, R_2, R_3, R_4\}\): \(R_0\) unengineered commodity money; \(R_1\) fixed provenance; \(R_2\) rotating provenance; \(R_3\) lineage-preserving physical chaining (M3b); \(R_4\) exit from physical-provenance authentication. (Bulk chaining M3a is a tested-and-dominated architecture, not a candidate regime — §5.3.) A regime is viable at \(t\) iff three constraints hold: expected counterfeit profit \(E[\Pi_F] < 0\) under the operative attacker, verification burden \(C_V < \bar{c}_V\), and issuer cost \(C_I < \bar{c}_I\); thresholds are sensitivity-tested below. The issuer's objective is
\[
r_t^* = \arg\min_{r \in \mathcal{R}}\;\big[C_I(r,\boldsymbol\theta_t) + C_V(r,\boldsymbol\theta_t) + E[L_F(r,\boldsymbol\theta_t)] + \kappa\, C_{\mathrm{switch}}(r_{t-1}, r)\big],
\]
which yields the general switching rule: move from \(r_a\) to \(r_b\) when \(L(r_b, \boldsymbol\theta_t) + C_{\mathrm{switch}}(r_a, r_b) < L(r_a, \boldsymbol\theta_t)\). We run three issuer specifications — Rule A (myopic, \(\kappa{=}0\)), Rule B (switching-cost-aware, \(\kappa \in \{0.1, 0.25, 0.5, 1\}\)), and Rule C (forward-looking discounted loss, \(\beta = 0.9\), solved by backward induction) — over four technology trajectories: **T1** symmetric progress (all costs decay together), **T2** attacker-favoring (synthetic reconstruction cheapens fastest, \(q_t\) rises), **T3** defender-favoring (verification and issuer-side costs fall fastest), and **T4** a discontinuous synthetic-fabrication breakthrough. Technological obsolescence is the region \(\mathcal{O}\) where no physical-provenance regime is viable. Adaptation value is \(\Delta_{\mathrm{adapt}} = L_{\mathrm{fixed}} - L_{\mathrm{adaptive}}\), the cumulative-loss difference between the best fixed architecture and the adaptive sequence; we also report viability extension (fraction of the technology horizon in which any provenance regime survives) and, separately, immediate-exit loss as a baseline.

## 4. Empirical calibration and simulation design

**Analysis A (demonstration).** Twenty-three AstroMat/IEDA datasets (UCLA iron-meteorite archive) yield {{n_samples}} sample-level, {{n_elements}}-element records; {{n_groups}} chemical groups have complete fingerprints. Group centroids serve as source distributions — a defensible demonstration calibration, *not* a claim about planetary compositions. Within-group log-sd supplies analytical noise; the group covariance gives \(d_{\mathrm{eff}} = {{d_eff}}\).

**Analysis B (generalized sweep).** Source separation \(\Delta/\sigma \in \{0.1,\dots,8\}\), \(d_{\mathrm{eff}} \in \{2,\dots,32\}\), \(N \in \{3,\dots,50\}\), \(q \in [0,1]\), the \(\alpha\) grid above, \(c_{\mathrm{syn}}/V \in [10^{-3},10^{2}]\); \(R = 10^4\) replications where stochastic, with closed-form (noncentral-\(\chi^2\)) \(P_F\) verified against brute force. All costs are normalized by coin value \(V\) — we report cost *ratios* and phase boundaries, and do not assert dollar costs. Seed 20261003; full ledger in `data/acquisition_ledger.csv`.

## 5. Results

### 5.1 Fixed versus rotating provenance

An assay-aware attacker (A1/A3) defeats any *fixed* target at cost \(c_{\mathrm{syn}}\); rotation (M2) forces redevelopment per series, multiplying effective cost by the amortization factor (Fig. 3, Table 1). Rotation helps only through economics — it compresses the window in which development cost can be recovered — so MRA depends jointly on \(c_{\mathrm{syn}}/V\), \(T_F/T_R\) and residual series value, and collapses toward 1 as \(c_{\mathrm{syn}} \to 0\) (F5/F6 frontier).

### 5.2 Coalition dependence

Partial-source access (A2) is geometric, not cryptographic: the forger projects the target onto its attainable source subset. \(P_F(q)\) rises with \(q\) and falls with \(d_{\mathrm{eff}}\) (Fig. 4, Table 2). Two non-obvious findings: (i) for \(\Delta/\sigma \le 2\), even a *zero-source* mean attack passes verification at least half the time — \(\mathrm{CRT}_{0.5} = 0\) — because mixtures concentrate near the fingerprint centroid; (ii) consequently \(\mathrm{CRT}_{0.5}\) *falls* with \(N\) ({{crt05_sep8_n3}} at \(N{=}3\), \(\Delta/\sigma{=}8\), to {{crt05_sep8_n50}} at \(N{=}50\)): under this source geometry, coalition breadth alone degrades verification security — the coalition criterion holds with a sign twist. The effect is non-monotonic in general: whether enlargement helps or hurts depends on how added contributors shift separability in fingerprint space.

### 5.3 Incremental effect of physical chaining

Bulk inheritance adds nothing: under A3 the bulk target is a public deterministic function and needs no genuine predecessor — F3 is confirmed, M3a ≡ M2 (Fig. 3). Inclusion chaining adds the mass floor \(\alpha\kappa V\), which is the *only* term binding on non-synthetic attackers as well. The net benefit is positive only in a low-verification-burden corner (\(\alpha \ge {{lineage_alpha_min}}\) with cheap inclusion assay) and turns negative as assay burden grows (Fig. 5): chaining pays only where verifying it is cheap.

### 5.4 Synthetic-fabrication frontier

The phase diagram (Fig. 6) partitions \((\Delta/\sigma,\, c_{\mathrm{syn}}/V)\) into four quantitatively defined regions: *verification-limited* (\(\Delta/\sigma \lesssim 2\), mean attack succeeds), *viable* (P_F bounded and \(E[\Pi_F] < 0\)), *economically forgeable*, and *technologically obsolete* (\(c_{\mathrm{syn}}/V \lesssim 0.05\)). The security the system affords is therefore a statement about a cost frontier, not about impossibility — the expiration frontier (Proposition E) is a result, not a caveat.

### 5.5 Retrospective authentication depth

For M3b, inclusions make later money evidentiary about earlier money: the Bayes factor for a forged link at depth \(k\) is \(\approx 10^{{{retro_coarse_k1_log10_min}}}\)–\(10^{{{retro_coarse_k1_log10_max}}}\) at \(k{=}1\) across the inclusion-fraction grid against a coarse (3σ) inclusion-forger and stays \(\ge 10^{{{retro_coarse_k20_log10_int}}}\) at \(k{=}20\) (α = 0.10, Fig. 7). Against a near-perfect fabricator (0.5σ inclusion mismatch) evidence collapses to \(\mathrm{BF} \approx 10^{{{retro_fine_k1_log10_int}}}\) at \(k{=}1\) and \(\approx 10^{{{retro_fine_k20_log10_int}}}\) by \(k{=}20\) — retrospective authentication is real but capability-bounded (F7 conditionally survives).

### 5.6 Empirical demonstration

Real group fingerprints are strongly separated (median pairwise separation {{median_sep}} σ/dimension; range {{sep_min}}–{{sep_max}}) yet the {{n_elements}}-element space carries only \(d_{\mathrm{eff}} \approx {{d_eff_int}}\) effective dimensions — F2 confirmed on real data. Mixture distinguishability under partial-source access therefore behaves as the generalized model predicts near \(d_{\mathrm{eff}}{=}{{d_eff_int}}\) (Table 3): verification binds only above \(\Delta/\sigma \approx {{verif_sep_bound}}\). Solar-System-scale source diversity is sufficient *in principle*; whether it exists between arbitrary polities is an empirical question we do not answer.

### 5.7 Endogenous institutional transitions

Allowing the issuer to choose among regimes produces genuine technology-driven transitions (Fig. 8, Table 4). Under symmetric technological progress (T1) the endogenous sequence is fixed \(\rightarrow\) rotating \(\rightarrow\) exit: cheap synthesis first makes the fixed target forgeable (transition step {{T1_first_transition}}), then cheap reconstruction of successive targets defeats rotation, and exit follows. Under attacker-favoring progress (T2) the sequence is fixed \(\rightarrow\) rotating \(\rightarrow\) lineage-preserving \(\rightarrow\) exit — R3 is endogenously optimal for exactly {{T2_r3_steps}} of {{horizon_steps}} technology steps (steps {{T2_r3_first}}–{{T2_r3_last}}), the narrow corridor where bulk synthesis is already cheap enough to kill rotation but microfabrication remains costly enough that the lineage floor binds. Under defender-favoring progress (T3) fixed provenance never loses viability — no transition occurs. A discontinuous breakthrough (T4) takes the system directly from fixed provenance to exit in a single step: rotation cannot respond to a cost discontinuity because no intermediate regime occupies the post-breakthrough state. The regime map (Fig. 9) shows these transitions as frontiers in \((c_{\mathrm{syn}}/V, c_{\mathrm{ver}}/V)\) space: rotating provenance owns a vertical band at \(c_{\mathrm{syn}}/V \in [{{r2_band_lo}}, {{r2_band_hi}}]\) under affordable verification, fixed provenance dominates above it, and everything above \(c_{\mathrm{ver}}/V \approx {{c_ver_exit}}\) or left of the expiration surface falls to exit. The lineage regime's window is real but thinner than map resolution — visible only in trajectory space.

### 5.8 Adaptation value, hysteresis, and path dependence

Adaptation value is trajectory-dependent (Fig. 10). Under T1, adaptive switching beats the best fixed architecture by \(\Delta_{\mathrm{adapt}} = {{delta_adapt_T1}}\,V\) per {{horizon_steps}}-step horizon and extends provenance viability by {{viability_ext_T1_pct}}% of the horizon; the gain decays with switching weight \(\kappa\). Under T3 \(\Delta_{\mathrm{adapt}} = 0\) — there is nothing to adapt to. Under T2 and T4, adaptation is dominated by *immediate exit* (\(L_{\mathrm{adaptive}} - L_{\mathrm{exit}} = +{{delta_vs_exit_T2_abs}}\) and \({{delta_vs_exit_T4_abs}}\)): when adversarial technology wins the race, prolonged defense costs more than abandonment. Switching costs produce **no hysteresis**: transition steps are identical for \(\kappa \in \{0,\dots,1\}\) because every observed transition is *viability-forced* — incumbents fail a hard viability constraint rather than losing on cost margin, so switching cost has nothing to delay. Two technology paths converging to the same state yield identical endpoint regimes: no path dependence. Rule C (forward-looking, \(\beta{=}0.9\)) reproduces Rule A exactly — foresight adds nothing once viability boundaries dominate choice.

The three earlier nontrivial findings re-read dynamically: the bulk-chaining null persists (no regime index carries it); the coalition-size reversal shifts the attacker-cost surface and hence transition timing, not regime ordering; and the \(d_{\mathrm{eff}}\) collapse *accelerates* transitions — stronger fingerprint geometry lengthens the lineage window ({{r3_window_pen05_steps}} steps at penalty 0.5 vs {{r3_window_pen2_steps}} step at penalty 2 on T2).

## 6. Robustness and falsification tests

Table 5 reports the status of each pre-registered falsification criterion.

**Table 5.** Status of pre-registered falsification criteria.

| Criterion | Result |
|---|---|
| F1 source variability ≲ noise | \(\mathrm{CRT}_{0.5}=0\) for \(\Delta/\sigma \le 2\): **active** in the low-separability domain |
| F2 marker correlation | **confirmed empirically**: \(d_{\mathrm{eff}}={{d_eff}}\) for {{n_elements}} elements |
| F3 bulk chaining null | **confirmed**: M3a adds no cost under A3 |
| F4 inclusion verification too costly | **binds** for burden coefficients ≥ 2 |
| F5 MRA ≈ 1 | **approached** as \(c_{\mathrm{syn}}/V \to\) small |
| F6 synthetic cost < revenue | **collapse frontier** at \(c_{\mathrm{syn}}/V \approx {{expiration_frontier}}\) |
| F7 no retrospective evidence | survives only against coarse fabricators |

Sensitivity analyses (confidential weights, Fe-only vs multi-element, instrument heterogeneity, drift, adversarial mint optimization, old-series circulation) vary boundaries quantitatively but change no sign of the results above; the complete sensitivity tables are in `data/processed/`.

## 7. Discussion

### 7.1 The general mechanism

The results support a general claim: institutions whose credibility rests on the relative costs of authorized update, adversarial reconstruction, and verification possess a *technology-dependent viability frontier*, and crossing it changes the *identity* of the optimal institution, not merely its degree of security (Propositions A, B). The constructs that organize this are Material Rotation Asymmetry (\(\mathrm{MRA} = C_{\mathrm{reconstruct}}/C_{\mathrm{rotate}}\)), the technological expiration frontier, and adaptive viability extension — the extra technology range over which an adaptive institution survives relative to any fixed regime. All three generalize: any provenance-certification, anti-counterfeiting, or tamper-evidence institution faces the same structure.

### 7.2 Endogenous transitions and institutional adaptation

The endogenous sequences are the paper's core dynamic result. Technology trajectories produce distinct institutional histories: symmetric progress yields fixed \(\rightarrow\) rotating \(\rightarrow\) exit; attacker-favoring progress routes briefly through lineage-preserving chaining; defender-favoring progress freezes the incumbent; breakthrough progress jumps to exit. This maps onto transition theory's structure — landscape pressure (falling adversarial fabrication cost), incumbent regime (the current authentication architecture), niche architectures (alternative provenance regimes) — but as a *computable* transition: the frontiers are cost-ratio surfaces, not narrative stages [1–3]. Two nulls are as informative as the transitions: no hysteresis (transitions are viability-forced, so the lock-in logic of [22, 23] does not bind here), and no path dependence — the model's history-independence is itself a finding about when institutional switching-cost theory applies.

### 7.3 Why physical chaining fails under homogenization

Bulk predecessor remelting adds zero security once synthetic compositional matching is allowed (§5.3): *physical inheritance is not automatically institutional memory*. A physical ledger requires persistent predecessor information — information that survives in a form not cheaply reconstructible from the final bulk state. That is why only lineage-preserving microstructure carries chaining value, and why that value is confined to a corridor: it is a delaying architecture whose window is bounded above by adversarial microfabrication cost (Proposition D).

### 7.4 When adaptation extends viability — and when it does not

Adaptive switching outperforms fixed architectures under symmetric technological progress; under defender-favoring progress the incumbent fixed regime remains viable throughout, so adaptation provides no incremental benefit; and under attacker-favoring progress it loses to immediate exit (§5.8). The management implication is uncomfortable but explicit: for authentication institutions facing fast-advancing adversarial fabrication, *the rational institutional response is planned obsolescence*, not succession of upgrades (Propositions C, E). Enriched-isotope supply chains and separation cost structures [25] suggest these cost ratios move over multi-decade horizons; the fingerprint space is a depreciating asset and dimensionality, not only mixtures, must rotate.

### 7.5 PCPC as extreme test case

The interplanetary-federation reading makes the mechanism transparent — abundant bulk iron, distributed issuers, measurably different source metalloid chemistry [13, 14, 26] — but removing it changes no proposition: source separation is abstracted in the generalized analysis. Material constitutional memory (M3b lineage surviving coalition turnover \(A_t \neq A_{t+1}\)) remains a secondary, non-load-bearing observation. Nothing about the model is cryptographic; the blockchain comparison [27] covers chronological linkage and tamper evidence only (Table 6), not consensus, replication, or append-only guarantees.

### 7.6 Limitations

Costs are normalized, not absolute; isotope-separation price data are thin and treated as sensitivity only. Verification infrastructure costs may differ dramatically across applications. The inclusion architecture's fabrication feasibility is asserted conditionally — micro-encapsulation of isotopically distinct particles in a metal matrix is plausible but unproven at mint scale, so the physical-lineage architecture remains partly theoretical. Measurement is modeled as multivariate normal; heavy-tailed assay error would soften all verification boundaries. Attacker and issuer behavior is simplified: single-parameterized adversaries, a cost-minimizing issuer, viability thresholds (\(\bar{c}_V, \bar{c}_I,\) loss tolerance) that are justified normalized levels — sensitivity-tested, but real issuers would set them institutionally. Trajectories T1–T4 are stylized parameter-space paths, not forecasts; no adoption-probability or calendar claims are made, and no actual monetary adoption is demonstrated or claimed. The \(c_{\mathrm{syn}}/V \approx 0.05\) frontier is model-dependent, not a universal threshold. The absence of hysteresis and path dependence is itself a property of this specification, not a general law. Extrasolar isotope distributions are unknown, and all "planet" language is demonstrative: no extrasolar fingerprint is claimed.

## 8. Conclusion

We modelled authentication as a technology-contingent institution: a regime survives while adversarial reconstruction exceeds expected counterfeit gain and verification remains affordable, and technological progress moves the system across viability frontiers between qualitatively different authentication architectures. The test case — a physically chained provenance currency calibrated on measured meteorite fingerprint dispersions — yields the transferable results: chaining adds security only where predecessor information survives as structure; lineage-preserving chaining is a narrow delaying corridor, not a destination; correlated markers collapse the effective dimensionality, and coalition enlargement can accelerate expiration under some source geometries; and under attacker-favoring technological progress the optimal institutional response is exit, not succession. The framework is parameter-space forecasting, not calendar prediction: it says which institutions remain viable as fabrication and verification capabilities change, wherever they change.

**Propositions.** (A) An authentication regime is viable only while adversarial reconstruction cost exceeds expected counterfeit gain and verification is operationally affordable. (B) Technological progress can change the identity of the optimal authentication institution, not merely its security level. (C) Adaptive switching extends viability relative to a fixed architecture when progress is symmetric and switching costs are low; under defender-favoring progress it adds nothing because the incumbent remains viable; under attacker-favoring progress it is dominated by early exit. (D) Physical predecessor inheritance adds institutional value only when predecessor information survives in a form not cheaply reconstructible from the final state. (E) Every physical-provenance regime possesses a technological expiration frontier under sufficiently cheap synthesis — empirically, \(c_{\mathrm{syn}}/V \lesssim {{expiration_frontier}}\) bounds the last-surviving architecture's exit region.

## Declarations

**Funding.** This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

**Declaration of competing interest.** The author declares no competing interests.

**Data availability.** The empirical calibration uses publicly archived UCLA iron-meteorite datasets from the Astromaterials Data Repository (IEDA); dataset DOIs, retrieval timestamps and checksums are listed in the acquisition ledger (`data/acquisition_ledger.csv`) in the accompanying code repository. Processed intermediate data are generated by the repository pipeline.

**Code availability.** All analysis code, simulations, figure and table scripts, tests and the reproduction Makefile are available in the public repository `github.com/bougtoir/physical-chained-provenance-currency` (mirrored from the author's working repository). Results are regenerated by `make all` followed by `make test`.

**Author contributions.** T.O.: conceptualization, methodology, software, formal analysis, writing — original draft, writing — review and editing.

**Generative AI disclosure.** During the preparation of this work the author used Devin (Cognition AI) to assist with simulation-code development and manuscript drafting. After using this tool, the author reviewed and edited the content as needed and takes full responsibility for the content of the publication.

**Originality.** This manuscript is original, has not been published previously, and is not under consideration by any other journal.

## References

1. Geels FW. Technological transitions as evolutionary reconfiguration processes: a multi-level perspective and a case-study. *Research Policy* 2002;31:1257–74.
2. Markard J, Raven R, Truffer B. Sustainability transitions: an emerging field of research and its prospects. *Research Policy* 2012;41:955–67.
3. Li FGN, Trutnevyte E, Strachan N. A review of socio-technical energy transition (STET) models. *Technological Forecasting and Social Change* 2015;100:290–305.
4. Kopyto M, Lechler S, von der Gracht HA, Hartmann E. Potentials of blockchain technology in supply chain management: long-term judgments of an international expert panel. *Technological Forecasting and Social Change* 2020;161:120330.
5. Sargent TJ, Velde FR. *The Big Problem of Small Change*. Princeton University Press; 2002.
6. Nosal E, Wallace N. A model of (the threat of) counterfeiting. *Journal of Monetary Economics* 2007;54(4):994–1001.
7. Fung BSC, Shao E. Counterfeit quality and verification in a monetary exchange. *Economic Modelling* 2016;52:13–25.
8. Shao E. The threat of counterfeiting in competitive search equilibrium. *Journal of Economic Dynamics and Control* 2014;47:168–85.
9. Redish A. *Bimetallism: An Economic and Historical Analysis*. Cambridge University Press; 2000.
10. Gale NH, Stos-Gale ZA. Lead isotope analyses applied to provenance studies. In: Ciliberto E, Spoto G, editors. *Modern Analytical Methods in Art and Archaeology*. Wiley; 2000. p. 503–84.
11. Longman J, Veres D, Ersek V, Phillips DL, Chauvel C, Tamas CG. Quantitative assessment of Pb sources in isotopic mixtures using a Bayesian mixing model. *Scientific Reports* 2018;8:6154.
12. Anand A, Spitzer F, Hopp T, Windmill R, Kruttasch P, Burkhardt C, Dauphas N, Greenwood R, Hofmann B, Mezger K, Kleine T. Isotopic evidence for a common parent body of IIG and IIAB iron meteorites. *Geochimica et Cosmochimica Acta* 2024;382:118–27.
13. Ni P, Chabot NL, Ryan CJ, Shahar A. Heavy iron isotopic composition of iron meteorites explained by core crystallization. *Nature Geoscience* 2020;13:611–5.
14. Wasson JT et al. UCLA iron-meteorite dataset series. The Astromaterials Data Repository (IEDA), DOI 10.26022/IEDA/112040 and companion releases listed in `data/acquisition_ledger.csv`; accessed 2026-10-03.
15. Pappu R, Recht B, Taylor J, Gershenfeld N. Physical one-way functions. *Science* 2002;297:2026–30.
16. Meguerdichian S, Potkonjak M. Device aging-based physically unclonable functions. *Proceedings of the 48th Design Automation Conference*; ACM; 2011:288–9.
17. Xiong W, Schaller A, Katzenbeisser S, Szefer J. Dynamic physically unclonable functions. *Proceedings of GLSVLSI '19*; ACM; 2019:311–4.
18. Kennedy ZC, Stephenson DE, Christ JF, Pope TR, Arey BW, Barrett CA, Warner MG. Enhanced anti-counterfeiting measures for additive manufacturing: coupling lanthanide nanomaterial chemical signatures with blockchain technology. *Journal of Materials Chemistry C* 2017;5:9570–8.
19. Zhang Y. Blockchain of signature material combining cryptographic hash function and DNA steganography. arXiv:1909.07914; 2019.
20. Brandman J, Sturm LD, White J, Williams CB. A physical hash for preventing and detecting cyber-physical attacks in additive manufacturing systems. *Journal of Manufacturing Systems* 2020;56:202–12.
21. Abdallah R, Şahinel D, Adarve OA, Monfort D. Enhancing digital product passports with material fingerprinting and decentralized non-conformity signals: application to critical raw materials. *Procedia Computer Science* 2026;277:1051–60.
22. Arthur WB. Competing technologies, increasing returns, and lock-in by historical events. *Economic Journal* 1989;99:116–31.
23. David PA. Clio and the economics of QWERTY. *American Economic Review* 1985;75:332–7.
24. Wang Z, Ribeiro-Navarrete S, Chen X, Xu B, Huang W-L. Central bank digital currencies: consumer data-driven sustainable operation management policy. *Technological Forecasting and Social Change* 2023;196:122867.
25. Cost estimate for laser isotope separation for RIA. OSTI technical report, U.S. Department of Energy; osti.gov/servlets/purl/15014826.
26. Hein AM, Matheson R, Fries D. A techno-economic analysis of asteroid mining. *Acta Astronautica* 2020;168:104–15.
27. Nakamoto S. Bitcoin: a peer-to-peer electronic cash system. 2008.
