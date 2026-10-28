# FINAL PUBLIC REPRODUCTION — FULL PASS
- Repo: https://github.com/bougtoir/physical-chained-provenance-currency (public, created this audit; prior sync workflow broken by billing)
- Pinned commit: da403ea7f8557b4fe8f4dfce6f78c18965d8d12a
- Procedure: clean `git clone` into empty dir -> `python3 -m venv .venv` -> `pip install -r requirements.txt` -> `pytest tests` -> `make data sims figures tables` -> `export_canonical.py` -> `build_docx.py`.
- Results: 13/13 tests pass; data fetched from IEDA DOIs via scripts/fetch_data.py (23 datasets, sha256 ledger); all sims/figures/tables rebuilt; docx regenerated (10 figures, 5 tables, 141 OMML).
- Canonical comparison: 47/49 keys bit-identical; sep_min and retro_fine_k20_log10 differ only in the 16th significant digit (identical displays 0.54 / 0.15) — FP noise, PASS.
- Exclusions (by policy, listed in sync EXCLUDE_MAP): data/raw, data/processed/sample_concentrations.csv (third-party AstroMat records, re-downloaded by fetch_data.py), prior zips.
