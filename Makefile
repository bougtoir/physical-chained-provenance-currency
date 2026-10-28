PY := python3

all: data sims figures tables

data:
	$(PY) scripts/fetch_data.py
	$(PY) scripts/build_fingerprints.py

sims:
	$(PY) analysis/run_simulations.py
	$(PY) analysis/run_transition_sims.py

figures:
	$(PY) analysis/make_figures.py

tables:
	$(PY) analysis/make_tables.py

canonical:
	$(PY) analysis/export_canonical.py

docx: canonical
	$(PY) analysis/build_docx.py
	$(PY) analysis/build_front_matter.py

package: docx
	$(PY) analysis/make_submission_zip.py

test:
	$(PY) -m pytest tests/ -q

.PHONY: all data sims figures tables test
