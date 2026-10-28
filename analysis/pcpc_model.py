"""Core model for Physical Chained Provenance Currency (PCPC) simulations.

All quantities in fingerprint space are log10-concentration vectors.
Verification uses the Mahalanobis statistic D_M^2 vs a chi-square threshold.
Where a closed form exists (P_F via noncentral chi-square), we use it and
validate with Monte Carlo on a subset of conditions.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import nnls
from scipy.stats import chi2, ncx2


def effective_rank(cov: np.ndarray) -> float:
    """Eigenvalue participation ratio (PR) of a covariance matrix."""
    w = np.linalg.eigvalsh(np.asarray(cov, float))
    w = np.clip(w, 0, None)
    if w.sum() <= 0:
        return 0.0
    p = w / w.sum()
    return float(1.0 / np.sum(p ** 2))


def whiten(cov: np.ndarray):
    """Return A such that A x whitens vectors with covariance `cov`."""
    w, V = np.linalg.eig(np.asarray(cov, float))
    w = np.clip(w, 1e-12, None)
    return np.diag(1.0 / np.sqrt(w)) @ V.T


def tau_threshold(d_eff: float, false_reject: float = 1e-3) -> float:
    return chi2.ppf(1.0 - false_reject, df=max(d_eff, 1e-9))


def pf_from_deficit(deficit: float, d_eff: float, tau: float) -> float:
    """P_F given the attacker's best achievable whitened distance `deficit`.

    z ~ N(y + delta, Sigma): D_M^2 ~ chi^2_{d_eff}(noncentrality = |delta|^2
    measured in whitened units)."""
    lam = deficit ** 2
    return float(ncx2.cdf(tau, max(d_eff, 1e-9), lam))


def attainable_deficit(target: np.ndarray, X_avail: np.ndarray,
                       A: np.ndarray) -> float:
    """Min whitened distance from `target` to the simplex over columns of X_avail.

    min_v ||A (X v - target)||^2 s.t. v >= 0, sum v = 1.
    NNLS on whitened (X, target) then renormalize; also includes the zero-mixture
    projection as candidate. Returns the residual distance.
    """
    AX = X_avail @ A.T if X_avail.ndim == 2 else None
    AX = (A @ X_avail.T).T  # (k, d) -> whiten columns: rows are sources
    # build NNLS system: minimize ||sum v_i AX_i - A target||
    B = AX.T  # (d, k)
    b = A @ target
    # enforce sum v = 1 by augmenting with a large-weight row
    lam = 10.0 * np.sqrt(np.trace(B.T @ B) / max(B.shape[1], 1))
    B_aug = np.vstack([B, np.full((1, B.shape[1]), lam)])
    b_aug = np.concatenate([b, [lam]])
    v, _ = nnls(B_aug, b_aug)
    if v.sum() <= 0:
        return float(np.linalg.norm(b))
    v = v / v.sum()
    resid = AX.T @ v - b if False else B @ v - b
    return float(np.linalg.norm(resid))


def dirichlet_weights(rng: np.random.Generator, n: int,
                      w_min: float = 0.0) -> np.ndarray:
    w = rng.dirichlet(np.ones(n))
    if w_min > 0:
        w = w_min + (1 - n * w_min) * w
    return w


def make_sources(rng: np.random.Generator, n: int, d: int,
                 sep: float) -> np.ndarray:
    """N source fingerprints in R^d with characteristic separation `sep`
    (in units of within-batch sigma). Sources on a random simplex-ish cloud."""
    base = rng.normal(0, 1, (n, d))
    base *= sep / np.std(base, axis=0)
    return base


def mixing_target(w: np.ndarray, X: np.ndarray, alpha: float = 0.0,
                  p_prev: np.ndarray | None = None) -> np.ndarray:
    y = w @ X
    if alpha > 0 and p_prev is not None:
        y = alpha * p_prev + (1 - alpha) * y
    return y


def retrospective_bf(alpha: float, depth: int, n_incl: int,
                     sigma_incl: float, sigma_sig: float) -> float:
    """Bayes factor for link at `depth` given nested inclusions in batch t.

    Model: batch t inclusions carry the recorded fingerprint of generation
    t-1 ... t-L. A forged link at depth k replaces genuine inclusions of
    generation t-k (present at fraction f_k = alpha * (1-alpha)^(k-1) under
    nested sequestration) by synthetic material deviating by sigma_sig in
    standardized inclusion-signal units; n_incl inclusions assayed.
    BF = likelihood ratio of observed inclusion signal under genuine vs forged.
    Approximate per-inclusion normal model.
    """
    f = alpha * (1.0 - alpha) ** (depth - 1)
    if f <= 0:
        return 1.0
    # signal-to-noise of mean inclusion tracer: separation / se of mean
    se = sigma_incl / np.sqrt(max(n_incl * f, 1e-9))
    z = sigma_sig / se
    # BF approximated as exp(z^2 / 2): how strongly the genuine signal rejects
    # the forged hypothesis when the mismatch is sigma_sig
    return float(np.exp(0.5 * z * z))
