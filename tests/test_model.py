import sys
from pathlib import Path

import numpy as np
from scipy.stats import chi2, ncx2

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import pcpc_model as m  # noqa: E402


def test_effective_rank():
    assert m.effective_rank(np.eye(4)) == 4.0
    assert abs(m.effective_rank(np.diag([1.0, 0.0, 0.0])) - 1.0) < 1e-9


def test_whiten_identity():
    A = m.whiten(np.diag([4.0, 1.0]))
    x = np.array([2.0, 3.0])
    w = A @ x
    assert abs(np.linalg.norm(w) ** 2 - (x ** 2 / np.array([4.0, 1.0])).sum()) < 1e-9


def test_pf_closed_form_matches_monte_carlo():
    rng = np.random.default_rng(0)
    d, deficit = 8, 3.0
    tau = m.tau_threshold(d, 1e-3)
    pf = m.pf_from_deficit(deficit, d, tau)
    z = rng.normal(0, 1, (200_000, d)) + deficit / np.sqrt(d)
    mc = (z ** 2).sum(1) <= tau
    assert abs(mc.mean() - pf) < 4 * mc.std() / np.sqrt(len(mc)) + 0.005


def test_attainable_deficit_full_set_zero():
    rng = np.random.default_rng(1)
    X = m.make_sources(rng, 6, 8, 2.0)
    w = m.dirichlet_weights(rng, 6)
    y = w @ X
    A = m.whiten(np.eye(8))
    assert m.attainable_deficit(y, X, A) < 1e-3


def test_attainable_deficit_subset_nonnegative():
    rng = np.random.default_rng(2)
    X = m.make_sources(rng, 10, 4, 4.0)
    w = m.dirichlet_weights(rng, 10)
    y = w @ X
    A = m.whiten(np.eye(4))
    deficit = m.attainable_deficit(y, X[:3], A)
    assert deficit >= 0


def test_retro_bf_monotone_depth():
    b1 = m.retrospective_bf(0.05, 1, 200, 1.0, 3.0)
    b5 = m.retrospective_bf(0.05, 5, 200, 1.0, 3.0)
    assert b1 > b5 >= 1


def test_ledger_complete():
    import pandas as pd
    led = pd.read_csv(Path(__file__).resolve().parents[1]
                      / "data" / "acquisition_ledger.csv")
    assert (led["status"] == "ok").all()
    assert led["sha256"].str.len().eq(64).all()
