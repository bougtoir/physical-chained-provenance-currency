# TFSC JOURNAL SELECTION GATE

Evaluation of the frozen PCPC manuscript (post-results, post-novelty-audit)
against *Technological Forecasting and Social Change*, per the gate protocol.
Verdict is rendered as a gate, not an advocacy document.

## 1. Current TFSC facts (verified 2026-10-03)

- **Scope**: "a major forum for those wishing to deal directly with the
  methodology and practice of technological forecasting and future studies as
  planning tools as they interrelate social, environmental and technological
  factors"; publishes theory + practice contributions spanning technology
  forecasting, innovation adoption, and societal effects.
- **JCR**: Q1 — JCR categories BUSINESS (4/316) and REGIONAL & URBAN PLANNING
  (1/55), SSCI. JIF ~12.9–13.3 (Elsevier page shows 13.3; CiteScore 21.3).
  Quartile from JCR-derived secondary sources; not read directly from JCR —
  low uncertainty.
- **Publication model**: hybrid — subscription publication available without
  mandatory APC; OA APC USD 3,840.
- **Article types**: research articles, short articles, technical articles,
  special issues.
- **Relevant editorial emphasis**: socio-technical transitions modelling,
  technology adoption/diffusion, blockchain/CBDC adoption studies,
  anticipatory governance.

## 2. Manuscript in one paragraph

The paper formalizes and simulates whether commodity money can derive
counterfeit resistance from the cost asymmetry between *rotating* a
time-indexed material state (cheap for the issuer) and *reconstructing* it
(expensive for a counterfeiter), and whether physically preserved
predecessor material chains monetary states into a material ledger.
Calibrated on 2,612 measured iron-meteorite sample records (23 AstroMat/IEDA
datasets, 13 elements, 50 parent-body groups), it finds: nominal
fingerprint dimensionality collapses to d_eff ≈ 3; a viability frontier at
c_syn/V ≈ 0.05 separating viable and collapsed provenance regimes; bulk
compositional chaining adds zero security under a synthetic attacker;
microstructural (inclusion) chaining adds a supply-side forgery floor that
nets positive only above α ≈ 0.05 of lineage mass under cheap verification;
larger source coalitions increase attacker mixing freedom; and retrospective
lineage evidence decays with depth and attacker assay capability.

## 3. Citation ecology (current reference distribution, n=20)

| Field | Count | Refs |
|---|---|---|
| Monetary economics | 4 | Sargent & Velde; Nosal & Wallace; Fung & Shao; Shao |
| Economic history | 1 | Redish |
| Materials provenance | 5 | Gale & Stos-Gale; Longman; Anand; Ni; Wasson series |
| PUF / physical security | 4 | Pappu; Meguerdichian; Xiong; Kennedy |
| Blockchain / supply chain | 3 | Zhang; Brandman; MaDiTraCe; (Nakamoto) |
| Space economics | 1 | Hein et al. |
| Isotope separation / tech cost | 1 | OSTI |
| Cryptocurrency | 1 | Nakamoto |
| Technology forecasting / transitions / institutional adaptation | **0** | — |

TFSC-relevant literature is currently **peripheral (category B)**: no
transitions, forecasting, or institutional-adaptation citations. The
mechanism itself (cost-ratio-driven institutional viability) is genuinely
adjacent to the MLP/regime-transition conversation, so integration would not
be wholly artificial, but the present bibliography does not sit inside it.

## 4. Closest TFSC literature

| TFSC paper | Relevance | What our paper adds |
|---|---|---|
| Li, Trutnevyte & Strachan 2015, TFSC 100:290–305 (review of socio-technical energy transition models) | Establishes formal modelling of regime transitions as a TFSC method | Applies transition modelling to *authentication institutions* — a domain the review does not cover — with falsifiable cost-ratio frontier rather than narrative MLP stages |
| Kopyto et al. 2020, TFSC 161:120330 (blockchain in supply chains, expert-panel long-term judgments) | TFSC-level treatment of provenance/authentication technology adoption | Complements digital-ledger provenance with *material-domain* chaining; shows where digital provenance's physical anchor must sit |
| Wang et al. 2023, TFSC 196:122867 (CBDC consumer-data-driven operation) | Currency systems as socio-technical objects | Shifts currency analysis from adoption/acceptance to *viability under adversarial technological change* |
| Geels 2002 and MLP transition papers appearing in TFSC | Regime/niche transition theory the frontier maps onto | Converts "regime transition" into a computable cost-ratio boundary with attacker-issuer equilibrium |

## 5. Result-strength audit

- **Type A (threshold): YES** — collapse frontier at c_syn/V ≈ 0.05
  (empirical mixtures + generalized sim, Fig. 5).
- **Type B (transition): PARTIAL** — phase diagram yields four distinguishable
  regimes (viable / verification-limited / forgeable / obsolete) across
  cost-ratio space; transition is parameterized, not temporally modeled.
- **Type C (adaptation advantage): PARTIAL** — M3b vs M2 comparison quantifies
  when lineage architecture extends viability; not a co-evolution analysis.
- **Type D (expiration): YES** — finite technological region: provenance money
  ceases to be viable once synthetic-fabrication cost ratio crosses frontier;
  §7.3 frames fingerprint space as depreciating asset.
- **Type E (counterintuitive): YES, three** — (i) bulk chaining is exactly
  null under synthetic attack despite intuitive appeal; (ii) larger
  federations *hurt* security (mixtures concentrate near centroid); (iii)
  13 nominal marker dimensions collapse to ~3 effective dims (correlation).
  Results are not merely "cheaper counterfeiting helps counterfeiters".

## 6. Physical-chain incremental-value audit (M3 vs M2)

- M3a (bulk chain): **NULL** — adds zero deterrence under synthetic attacker
  (attacker reproduces bulk state directly; F3).
- M3b (inclusion/lineage chain): **CONDITIONAL POSITIVE** — adds forgery
  mass-floor ακV; net advantage only at α ≥ 0.05 and cheap-verification
  burden coefficient ≈ 0.5; negative under heavy verification burden.
- Retrospective authentication: real but decaying evidence channel
  (log-BF declines with depth and attacker assay capability).
- Net: chaining matters **only where lineage survives as structure** —
  itself a nontrivial finding about when chaining is meaningful.

## 7. Technology-transition audit

A genuine frontier exists: regimes are separated by the cost ratios
c_syn/V (fabrication), c_ver (verification burden), α (lineage mass).
Technological progress is interpretable as movement through parameter space
(rising fabrication capability → crossing c_syn/V ≈ 0.05), but the manuscript
does not yet present an explicit parameter-space trajectory analysis —
frontiers are drawn; the *passage* across them is inferred, not modeled.

## 8. Generalizability audit

Mechanism statement without space: *"institutions whose credibility depends
on the relative technological costs of authorized updating, verification,
and adversarial reconstruction face a technology-dependent viability
frontier."* The generalized simulations abstract source separation entirely
(d_eff, Δ/σ given), so the result survives removal of the interplanetary
narrative. **Space-specificity = 2** (mechanism independent; narrative uses
space as extreme test; no unknowable-civilization assumptions). Applies to
commodity authentication, anti-counterfeiting, provenance certification.

## 9. Desk-rejection risk table

| Risk | Rating | Basis |
|---|---|---|
| DR1 speculative-futures | Moderate | Space frame prominent; mitigated by measured-data calibration and parameter-space (not calendar) forecasting |
| DR2 engineering-only | Low | Paper is an economic/security model, not hardware |
| DR3 economics-only | Moderate | Counterfeit-verification model could be read as JME-adjacent; transition framing must lead to avoid this |
| DR4 novelty compression | Low–Moderate | Audited: no material-state S_t=f(S_{t-1},X_t) in five adjacent literatures; dynamic PUFs are device-level, not issuer monetary |
| DR5 trivial result | Low | Three counterintuitive findings; null chaining result is non-obvious |
| DR6 arbitrary calibration | Low | All costs normalized; empirical calibration on real assay data; no invented dollar values |
| DR7 weak societal relevance | Moderate | Generalizability arguable (§8) but manuscript currently underweights non-space implications |
| DR8 citation-ecology mismatch | **High** | Zero transitions/forecasting/institutional-adaptation refs; would currently read as economics+materials paper |

Unresolved HIGH risk: **DR8**.

## 10. Scoring table (0–4 each)

| Criterion | Score | Justification |
|---|---|---|
| A. Theoretical contribution | 3 | MRA (cost asymmetry), technological expiration frontier, and regime classification are identifiable general constructs; theory is mechanism-level, not a grand framework |
| B. Technology-dependent transition | 3 | Clear cost-ratio frontier with four regimes; transition parameterized but not yet dynamically modeled as passage |
| C. Institutional adaptation | 2 | Adaptation options (rotation, lineage architecture, dimensionality) compared quantitatively but not modeled as issuer strategy/co-evolution |
| D. Generalizability | 3 | Mechanism abstracts away space; results hold on abstracted fingerprint geometry; applications section needed |
| E. Empirical/computational rigor | 3 | Real-data calibration (2,612 samples, ledgered), factorial sims, closed-form-vs-MC validation, seed, tests; costs normalized (defensible) |
| F. Novelty | 3 | Material-state chaining demonstrably unoccupied; integrates monetary theory + PUF + provenance into one model |
| G. TFSC citation ecology | 2 | Adjacent (transitions modelling, provenance-tech adoption) but not currently embedded — fixable with genuine literature integration, not decoration |
| H. Societal relevance | 2 | Plausible implications for authentication institutions generally; currently framed too speculatively |

**Total: 21 / 32.**

## 11. Final verdict

**CONDITIONAL TFSC**

## 12. Rationale

The manuscript satisfies the non-triviality tests: it contains a genuine
technology-dependent viability frontier (c_syn/V ≈ 0.05), a non-obvious null
(bulk chaining), a counterintuitive coalition-size effect, and an effective
dimensionality collapse — none of which are tautological "cheap faking wins"
results. The core mechanism (relative costs of authorized rotation,
verification, and adversarial reconstruction determine which authentication
institution is viable) is exactly the technology-driven institutional
transition object TFSC readers study. Empirical calibration on measured
meteorite dispersions and honest negative results give it methodological
weight above a conceptual essay.

It does not yet meet the bar. The blocking deficit is DR8: the paper's
bibliography contains no forecasting/transitions/institutional-adaptation
literature, so it currently reads as economics-plus-materials. Second, the
technology→institution *transition* is parameterized rather than analyzed as
movement through parameter space (§5 dynamic requirement partially met).
Third, institutional adaptation is comparative statics (C=2), not modeled
issuer strategy.

## 13. If SUBMIT — n/a

## 14. If CONDITIONAL — minimum scientific changes required

1. **Explicit parameter-space transition analysis** (required, §5 of gate):
   add a frontier-crossing analysis presenting technological progress as a
   trajectory in (c_syn/V, c_ver, α) space — e.g. a fixed-arrow diagram and
   optimal-regime map fixed→rotating→chained→obsolete; no calendar claims.
2. **Institutional adaptation as modeled response** (required, §6): formalize
   at least one adaptive rule (e.g. issuer increases marker dimensionality or
   lineage mass α as attacker capability falls below threshold) and quantify
   its effect on the frontier position — a small addition to the existing sim.
3. **Genuine TFSC literature integration** (required, §8–9): engage MLP /
   transition-modelling and provenance-technology-adoption conversations
   (Li et al. 2015; Kopyto et al. 2020; Wang et al. 2023; Geels lineage) in
   intro + discussion — real engagement with the transition framework, not
   citation sprinkling.
4. **Reframe around the general mechanism** (required, §14): lead with
   "technology changes which authentication institutions are viable"; demote
   space currency to explicit extreme test case; add a generalizability
   subsection (commodity auth, reserve assets, provenance certification).
   No results change.
5. **Retitle around the transition mechanism** (advisory): e.g. "When does
   provenance expire? Technology-dependent viability of chained material
   authentication institutions".

Estimated scope: one additional sim component (adaptive rule + trajectory
figure), intro/discussion rewrite, ~6–10 added references. No new
experiments, no changed results.

## 15. If DO NOT SUBMIT — n/a (fallback list retained in docs/journal_gate.md)

---

# RE-RUN AFTER UPGRADE REVISION (same rubric, unchanged thresholds)

The upgrade added: a technology-state model θ_t; four trajectories T1–T4;
regime set R0–R4 with issuer objective and switching cost; three issuer rules
(myopic / switching-aware / forward-looking DP); endogenous transition
sequences; a (c_syn/V, c_ver/V) × c_micro regime map; adaptation value and
viability-extension metrics; hysteresis and path-dependence tests; seven new
transition-literature references (Geels 2002; Markard et al. 2012; Li et al.
2015; Arthur 1989; David 1985; Kopyto et al. 2020; Wang et al. 2023); and a
general-mechanism-first title/abstract/intro/discussion reframe. All frozen
results preserved.

## Scoring delta

| Criterion | Old | New | Justification |
|---|---|---|---|
| A theoretical contribution | 3 | 4 | General three-cost framework, switching rule, Propositions A–E, constructs (MRA, expiration frontier, adaptive viability extension) that organize all results |
| B transition result | 3 | 4 | Endogenous sequences across four trajectories, regime map, robust under κ and d_eff_penalty sweeps |
| C institutional adaptation | 2 | 3 | Issuer adaptation now modeled (three rules) and quantified (Δ_adapt, viability extension); not full co-evolution — technology stays exogenous |
| D generalizability | 3 | 3 | Framework general; still one instantiation domain |
| E rigor | 3 | 3 | Same calibration + added deterministic transition model with sensitivity on κ and geometry |
| F novelty | 3 | 3 | Dynamic institutional-transition view of authentication remains clear conceptual integration |
| G citation ecology | 2 | 3 | Transitions/forecasting literature now genuinely load-bearing in intro, §2.5, §7.2 across the four mandated argument parts |
| H societal relevance | 2 | 3 | Explicit implication: under attacker-favoring progress, planned obsolescence beats succession — actionable for authentication institutions generally |

**New total: 26 / 32** (old 21).

## Desk-rejection risk delta

| Risk | Old | New |
|---|---|---|
| DR1 speculative-futures | Moderate | Low — space demoted to test case; parameter-space framing only |
| DR4 novelty compression | Low–Mod | Low — dynamic institutional-transition framing adds space |
| DR6 arbitrary calibration | Low | Low |
| DR8 citation ecology | **High** | Low–Moderate — now embedded in four argument parts |

No unresolved HIGH among DR1/DR4/DR6/DR8.

## New findings relevant to the rubric

- Endogenous sequences: T1 fixed→rotating→exit (step 24); T2
  fixed→rotating→lineage→exit with a 2-step R3 window; T3 no transition;
  T4 abrupt fixed→exit on breakthrough.
- Lineage-preserving chaining optimal only in a narrow microfabrication-cost
  corridor — quantified, and invisible at regime-map resolution.
- Adaptation value positive under symmetric progress (+28% viability
  extension), zero under defender-favoring, **negative vs immediate exit**
  under attacker-favoring progress.
- No hysteresis and no path dependence — all transitions viability-forced;
  honest nulls for switching-cost theory's domain of application.
- The static c_syn/V ≈ 0.05 frontier survives as the deep-obsolescence
  (R4) boundary, superseded by a stack of per-regime expiration surfaces.

## Final verdict (re-run)

**SUBMIT TO TFSC** — score 26/32 ≥ 25; all mandatory dims met
(A4, B4, D3, E3, F3, G3); no unresolved high DR1/DR4/DR6/DR8.

## If SUBMIT — per gate protocol

- **Recommended TFSC title**: "When Authentication Technologies Expire:
  Technology-Dependent Institutional Transitions in a Physical-Provenance
  Currency" (manuscript already retitled; alternatives recorded:
  "From Fixed Security to Institutional Exit: Authentication Regime
  Transitions under Falling Reconstruction Costs"; "Technological Progress
  and the Expiration of Physical Authentication Institutions";
  "Cost Asymmetries, Regime Switching, and the Viability Frontier of
  Provenance-Based Money"; "Adaptive Authentication Institutions under
  Adversarial Technological Change: a Chained-Material Test Case").
- **Central claim (one sentence)**: Technological progress determines not
  merely the security level but the identity of the optimal authentication
  institution — fixed, rotating, lineage-chained, or none — through a
  quantifiable, cost-ratio-driven viability frontier.
- **Remaining framing changes**: none structural; adapt length/format to
  TFSC author instructions at packaging time.
- **Sections needing adaptation**: Introduction (already general-mechanism
  first), §2.5 (transitions literature — could host 1–2 more current TFSC
  items if the editor expects), Discussion order (already per protocol).

