#!/usr/bin/env python3
"""Run the PCPC factorial simulation design and write machine-readable tables.

Outputs (data/processed/, all CSV):
  sim_partial_source.csv   P_F(q) across N, d_eff, Delta/sigma  -> Fig 3, CRT
  sim_regimes.csv          E[Pi]/V and MRA for M0-M3 vs c_syn/V -> Fig 4
  sim_phase.csv            phase classification over Delta/sigma x c_syn/V -> Fig 5
  sim_chain.csv            alpha sweep: cost floor, burden, net benefit -> Fig 6
  sim_retro.csv            retrospective Bayes factor by chain depth -> Fig 7
  empirical_separability.csv  Analysis A: real group separation table
  empirical_mixtures.csv      Analysis A: mixture distinguishability demo
  convergence.csv          MC convergence checks
"""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pcpc_model import (attainable_deficit, dirichlet_weights, effective_rank,
                        make_sources, mixing_target, pf_from_deficit,
                        retrospective_bf, tau_threshold, whiten)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
PROC = OUT
SEED = 20261003
FALSE_REJECT = 1e-3

SEP_GRID = [0.1, 0.25, 0.5, 1, 2, 4, 8]
D_GRID = [2, 4, 8, 16, 32]
N_GRID = [3, 5, 10, 20, 50]
Q_GRID = np.arange(0, 1.0001, 0.1)
ALPHA_GRID = [0.0, 1e-4, 1e-3, 1e-2, 0.05, 0.10]
CSYN_GRID = np.logspace(-3, 2, 21)  # c_syn / V
R = 10_000


def partial_source_sim(rng):
    """Attack 2: P_F(q) for each (sep, d, N). Closed-form via ncx2.

    Geometry resampled R_geo times; w resampled per rep.
    """
    rows = []
    for sep in SEP_GRID:
        for d in D_GRID:
            tau = tau_threshold(d, FALSE_REJECT)
            A = whiten(np.eye(d))  # isotropic unit noise
            for n in N_GRID:
                if n <= 1:
                    continue
                for q in Q_GRID:
                    k = int(round(q * n))
                    pf_acc = []
                    R_geo = 200  # geometry reps; P_F itself is closed form
                    for _ in range(R_geo):
                        X = make_sources(rng, n, d, sep)
                        w = dirichlet_weights(rng, n)
                        y = w @ X
                        if k == 0:
                            deficit = np.linalg.norm(A @ y - A @ X.mean(0))
                        elif k >= n:
                            deficit = 0.0
                        else:
                            avail = rng.choice(n, size=k, replace=False)
                            deficit = attainable_deficit(y, X[avail], A)
                        pf_acc.append(pf_from_deficit(deficit, d, tau))
                    pf = np.array(pf_acc)
                    rows.append(dict(sep=sep, d_eff=d, N=n, q=q,
                                     P_F=pf.mean(), P_F_lo=np.quantile(pf, 0.025),
                                     P_F_hi=np.quantile(pf, 0.975),
                                     n_rep=len(pf)))
    return pd.DataFrame(rows)


def regime_sim(rng):
    """M0-M3 economics: E[Pi_F]/V vs c_syn/V at fixed favourable geometry."""
    rows = []
    sep, d, n, q = 2.0, 8, 10, 0.0
    tau = tau_threshold(d, FALSE_REJECT)
    A = whiten(np.eye(d))
    # defender-side quantities (fixed geometry, expected over reps)
    X = make_sources(rng, n, d, sep)
    deficit_a0 = []
    for _ in range(500):
        w = dirichlet_weights(rng, n)
        y = w @ X
        deficit_a0.append(np.linalg.norm(A @ (y - X.mean(0))))
    d_a0 = np.median(deficit_a0)
    pf_a0 = pf_from_deficit(d_a0, d, tau)           # generic copy
    pf_a1_syn = 1.0                                  # synthesis hits target (A3/A4)
    c_rotate = 0.02                                  # issuer rotation cost /V (assay+remix)
    for cs in CSYN_GRID:
        for regime in ("M0", "M1", "M2", "M3a", "M3b"):
            if regime == "M0":
                pf, cf = 1.0, 0.0
            elif regime == "M1":
                pf, cf = pf_a1_syn, cs              # fixed target fully known
            elif regime == "M2":
                # rotating target: attacker must finish within residual series
                # lifetime; effective cost = dev cost / forgeable mass window
                pf, cf = pf_a1_syn, cs * 3.0        # amortization penalty x3 (calibrated grid label)
            elif regime == "M3a":
                pf, cf = pf_a1_syn, cs * 3.0        # bulk chain adds nothing under A3 (F3)
            else:  # M3b
                alpha, kappa = 0.05, 1.5
                pf = pf_a1_syn
                cf = cs * 3.0 + alpha * kappa       # + lineage mass floor
            profit = pf * 1.0 - cf
            mra = cf / c_rotate
            rows.append(dict(regime=regime, c_syn_over_V=cs, P_F=pf,
                             C_F_over_V=cf, E_Pi_over_V=profit, MRA=mra))
    return pd.DataFrame(rows)


def phase_sim(rng):
    """Phase diagram: (Delta/sigma) x (c_syn/V) -> regime class for M2/M3b."""
    rows = []
    d, n = 8, 10
    tau = tau_threshold(d, FALSE_REJECT)
    A = whiten(np.eye(d))
    for sep in SEP_GRID:
        X = make_sources(rng, n, d, sep)
        d_a0 = np.median([np.linalg.norm(A @ (dirichlet_weights(rng, n) @ X - X.mean(0)))
                          for _ in range(300)])
        pf0 = pf_from_deficit(d_a0, d, tau)
        for cs in CSYN_GRID:
            # security = max(P_F of best attack) is pf_synth (cs) economically gated
            cf = cs * 3.0
            profitable = (1.0 - cf) > 0
            detectable = pf0 < 0.5
            if not detectable:
                cls = "verification-limited"
            elif cs <= 0.05:
                cls = "technologically-obsolete"
            elif profitable:
                cls = "economically-forgeable"
            else:
                cls = "viable"
            rows.append(dict(sep=sep, c_syn_over_V=cs, P_F_copy=pf0, cls=cls))
    return pd.DataFrame(rows)


def chain_sim():
    """alpha sweep for M3b: lineage floor vs verification burden.

    burden_coef scales the inclusion-assay burden ~ burden_coef * alpha; we
    sweep it because the true coefficient is uncertain (honest parametric
    exploration, not a fitted value).
    """
    rows = []
    kappa = 1.5
    for alpha in ALPHA_GRID:
        floor = alpha * kappa                      # extra cost per unit forged value
        mfg = 0.01 + 0.5 * alpha                   # extra issuer cost
        for bcoef in [0.5, 2.0, 8.0]:
            burden = 0.002 + bcoef * alpha
            net = floor - burden - mfg
            rows.append(dict(alpha=alpha, burden_coef=bcoef,
                             lineage_floor=floor, verif_burden=burden,
                             issuer_cost=mfg, net_benefit=net))
    return pd.DataFrame(rows)


def retro_sim():
    """Retrospective BF by depth; sigma_sig = attacker inclusion mismatch (sigma).

    sigma_sig sweeps attacker capability: large = crude forged inclusions,
    small = near-perfect microstructure synthesis (Attack 4/5 frontier).
    """
    rows = []
    for alpha in [0.01, 0.05, 0.10]:
        for depth in [1, 2, 5, 10, 20]:
            for sigma_sig in [0.5, 1.0, 3.0]:
                bf = retrospective_bf(alpha, depth, n_incl=200,
                                      sigma_incl=1.0, sigma_sig=sigma_sig)
                rows.append(dict(alpha=alpha, depth=depth, sigma_sig=sigma_sig,
                                 log10_BF=np.log10(max(bf, 1.0))))
    return pd.DataFrame(rows)


def empirical_analysis(rng):
    """Analysis A on real UCLA group fingerprints."""
    fp = pd.read_csv(PROC / "group_fingerprints.csv", index_col=0)
    mean_cols = [c for c in fp.columns if c.endswith("_mean")]
    fp = fp[fp["n"] >= 15].dropna(subset=mean_cols).copy()
    X = fp[mean_cols].to_numpy()
    groups = fp.index.to_numpy()
    cov = np.cov(X.T)
    d_eff = effective_rank(cov)
    # within-group sd as sigma (mean across elements & groups)
    sd_cols = [c for c in fp.columns if c.endswith("_sd")]
    sigma_within = float(np.nanmedian(fp[sd_cols].to_numpy()))
    # pairwise whitened separation between group centroids (pooled within-cov)
    sep_rows = []
    # pairwise Mahalanobis-ish separation using pooled within-group log sd
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            dist = np.linalg.norm((X[i] - X[j]) / np.maximum(sigma_within, 1e-9))
            sep_rows.append(dict(g1=groups[i], g2=groups[j],
                                 delta_over_sigma=dist / np.sqrt(len(mean_cols))))
    seps = pd.DataFrame(sep_rows)
    # mixture distinguishability: N sampled groups, random w, attacker with q
    mix_rows = []
    mean_names = mean_cols
    sig = np.full(len(mean_names), sigma_within)
    for N in [3, 5, 10, 20, min(50, len(groups))]:
        N = min(N, len(groups))
        for rep in range(500):
            idx = rng.choice(len(groups), size=N, replace=False)
            Xn = X[idx]
            w = dirichlet_weights(rng, N)
            y = w @ Xn
            # best full-knowledge attacker with k sources (N-1 missing -> q)
            for q in [0.0, 0.5, 0.8]:
                k = int(round(q * N))
                if k == 0:
                    deficit = np.linalg.norm((y - Xn.mean(0)) / sig)
                elif k >= N:
                    deficit = 0.0
                else:
                    sub = rng.choice(N, size=k, replace=False)
                    deficit = attainable_deficit(y / sig, Xn[sub] / sig, np.eye(len(sig)))
                tau = tau_threshold(d_eff, FALSE_REJECT)
                mix_rows.append(dict(N=N, q=q, deficit=deficit,
                                     P_F=pf_from_deficit(deficit, d_eff, tau)))
    mixes = pd.DataFrame(mix_rows)
    meta = dict(d_eff_empirical=d_eff, sigma_within=sigma_within,
                n_groups=len(groups), n_elements=len(mean_cols))
    return seps, mixes, meta


def convergence_check(rng):
    rows = []
    sep, d, n, q = 2.0, 8, 10, 0.5
    k = int(q * n)
    tau = tau_threshold(d, FALSE_REJECT)
    A = whiten(np.eye(d))
    for reps in [200, 2000]:
        pf = []
        r2 = np.random.default_rng(SEED + reps)
        for _ in range(reps):
            X = make_sources(r2, n, d, sep)
            w = dirichlet_weights(r2, n)
            y = w @ X
            avail = r2.choice(n, size=k, replace=False)
            deficit = attainable_deficit(y, X[avail], A)
            pf.append(pf_from_deficit(deficit, d, tau))
        pf = np.array(pf)
        rows.append(dict(reps=reps, P_F=pf.mean(), se=pf.std() / np.sqrt(reps)))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    print("partial source ...", flush=True)
    partial_source_sim(rng).to_csv(OUT / "sim_partial_source.csv", index=False)
    print("  done", time.time() - t0, flush=True)
    regime_sim(rng).to_csv(OUT / "sim_regimes.csv", index=False)
    phase_sim(rng).to_csv(OUT / "sim_phase.csv", index=False)
    chain_sim().to_csv(OUT / "sim_chain.csv", index=False)
    retro_sim().to_csv(OUT / "sim_retro.csv", index=False)
    convergence_check(rng).to_csv(OUT / "convergence.csv", index=False)
    print("empirical ...", flush=True)
    seps, mixes, meta = empirical_analysis(rng)
    seps.to_csv(OUT / "empirical_separability.csv", index=False)
    mixes.to_csv(OUT / "empirical_mixtures.csv", index=False)
    json.dump(meta, open(OUT / "empirical_meta.json", "w"), indent=2)
    print("total", time.time() - t0)


if __name__ == "__main__":
    main()
