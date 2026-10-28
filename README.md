# Physical Chained Provenance Currency (PCPC)

Theoretical + computational study: can commodity money derive counterfeit
resistance from the cost asymmetry of *rotating* vs *reconstructing*
time-indexed material states, and can successive monetary states be physically
chained into a material chronological ledger?

## Layout

- `docs/phase1_novelty_audit.md` — literature audit + GO verdict (Gate 1)
- `docs/phase2_model.md` — locked formal model, propositions, falsification criteria
- `docs/phase5_results_audit.md` — results audit (10 mandated questions)
- `docs/TFSC_JOURNAL_SELECTION_GATE.md` — journal gate + re-score after upgrade
- `docs/TFSC_UPGRADE_RESULTS_AUDIT.md` — dynamic-model results audit
- `scripts/fetch_data.py` — downloads 23 AstroMat/IEDA raw datasets -> `data/raw/`
- `scripts/build_fingerprints.py` — parses workbooks -> `data/processed/`
- `analysis/pcpc_model.py` — model library (verification, attackers, metrics)
- `analysis/run_simulations.py` — factorial sims -> `data/processed/sim_*.csv`
- `analysis/run_transition_sims.py` — endogenous regime-transition analysis
  (technology trajectories T1-T4, regimes R0-R4, issuer rules A/B/C,
  switching costs, hysteresis, path dependence, adaptation value)
- `analysis/make_figures.py`, `analysis/make_tables.py` -> `figures/`, `tables/`
- `data/acquisition_ledger.csv` — DOI, sha256, license, file inventory
- `manuscript/manuscript.md` — journal-neutral draft (pre-journal-gate)
- `tests/` — unit tests incl. closed-form vs Monte-Carlo validation

## Reproduce

    make data sims figures tables   # or: make all
    make test

Seed: 20261003 (in `analysis/run_simulations.py`).

## Integrity notes

- Raw data are never edited; derived files live under `data/processed/`.
- All costs in the model are normalized (cost/V); no fabricated dollar values.
- Negative results are reported (see docs/phase5_results_audit.md).
- Figures/tables are generated only by scripts; no manual data edits.
