#!/usr/bin/env python3
"""Endogenous authentication-regime transition analysis (TFSC upgrade).

Technology state theta_t = (c_assay, c_syn, c_micro, c_ver, q) normalized to
unit face value V=1. Regimes R0..R4. Issuer rules A (myopic), B (switching-
cost-aware), C (forward-looking DP). Trajectories T1-T4 through technology
space (no calendar time).

Outputs (data/processed/):
  sim_trajectories.csv   chosen regime per (trajectory, kappa, rule, step)
  sim_regime_map.csv     optimal regime over (c_syn/V, c_ver/V) x c_micro tiers
  sim_adaptation.csv     cumulative loss fixed vs adaptive; viability extension
  sim_hysteresis.csv     transition-step delay vs switching weight kappa
  sim_pathdep.csv        endpoint regime under two paths to the same theta_T
  sim_r3_window.csv      where lineage-preserving R3 is optimal
"""
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "processed"
STEPS = 40

# ---- normalized issuer-side constants (documented, sensitivity-tested) ----
C_ROT = 0.02          # rotation cost /V (assay+remix amortized per period)
AMORT = 3.0           # rotating-target amortization factor on attacker cost
ALPHA = 0.05          # lineage mass fraction (M3b working point from F4)
KAPPA_FLOOR = 1.5     # lineage mass -> attacker cost multiplier
BURDEN_COEF = 0.5     # cheap-verification burden coefficient (F4 best case)
INCL_MFG_BASE = 0.01  # inclusion minting base cost /V
TH_VER = 0.20         # acceptable verification burden /V
TH_ISS = 0.30         # acceptable issuer cost /V
TH_LOSS = 0.05        # acceptable expected counterfeit loss /V
C_EXIT = 0.15         # normalized cost of a non-provenance alternative (R4)
R0_FORGE = 0.05       # cost of faking an unengineered coin /V
REGIMES = ["R0", "R1", "R2", "R3", "R4"]


def trajectory(name, steps=STEPS):
    """theta_t rows: c_assay, c_syn, c_micro, c_ver, q. Start state is
    'mature provenance tech': synthesis & micro-fab expensive, assay cheap."""
    t = np.arange(steps)
    a0 = 0.20                                    # mature assay tech at t=0
    if name == "T1":      # symmetric progress: all costs fall together
        r = 0.10
        c_syn = 10 * np.exp(-r * t); c_micro = 10 * np.exp(-r * t)
        c_assay = a0 * np.exp(-r * t); c_ver = 0.10 * np.exp(-r * t)
        q = np.zeros(steps)
    elif name == "T2":    # attacker-favoring: synthesis falls fast,
        # microfabrication (lineage reproduction) stays harder for longer
        c_syn = 10 * np.exp(-0.12 * t); c_micro = 10 * np.exp(-0.03 * t)
        c_assay = a0 * np.exp(-0.03 * t); c_ver = 0.10 * np.exp(-0.03 * t)
        q = np.minimum(0.5, 0.0125 * t)
    elif name == "T3":    # defender-favoring: verification/assay improve
        # fast, adversarial synthesis only slowly
        c_syn = 10 * np.exp(-0.05 * t); c_micro = 10 * np.exp(-0.05 * t)
        c_assay = a0 * np.exp(-0.12 * t); c_ver = 0.10 * np.exp(-0.12 * t)
        q = np.zeros(steps)
    elif name == "T4":    # discontinuous synthesis breakthrough at step 20
        r = 0.03
        c_syn = 10 * np.exp(-r * t); c_syn[20:] *= 1e-3
        c_micro = 10 * np.exp(-r * t)
        c_assay = a0 * np.exp(-r * t); c_ver = 0.10 * np.exp(-r * t)
        q = np.zeros(steps)
    else:
        raise ValueError(name)
    return pd.DataFrame(dict(step=t, traj=name, c_assay=c_assay, c_syn=c_syn,
                             c_micro=c_micro, c_ver=c_ver, q=q))


def regime_costs(th, d_eff_penalty=1.0):
    """Return dict r -> (C_I, C_V, E_L, viable, C_F) at one technology state.

    d_eff_penalty scales attacker cost (correlated markers lower effective
    synthesis cost); >1 means attacker pays more, i.e. harder geometry.
    """
    cs, cm, cv, ca, q = th["c_syn"], th["c_micro"], th["c_ver"], th["c_assay"], th["q"]
    out = {}
    # attacker effective costs per regime (unit V)
    cf = {
        "R0": R0_FORGE,
        "R1": cs / d_eff_penalty,
        "R2": AMORT * cs / d_eff_penalty,
        "R3": (AMORT * cs + KAPPA_FLOOR * ALPHA * cm) / d_eff_penalty,
        "R4": np.inf,                       # provenance abandoned: no target
    }
    # attacker capability q erodes the wall: accessible real sources rebate
    # up to q of reconstruction cost (consistent with partial-source result)
    ci = {
        "R0": 0.0,
        "R1": 0.5 * ca,
        "R2": ca + C_ROT,
        "R3": ca + C_ROT + INCL_MFG_BASE + 0.5 * ALPHA * cm,
        "R4": C_EXIT,
    }
    cvd = {
        "R0": 0.2 * cv,
        "R1": cv,
        "R2": cv,
        "R3": cv * (1 + BURDEN_COEF * ALPHA * 20),  # inclusion-assay burden
        "R4": 0.0,
    }
    for r in REGIMES:
        c_f_eff = cf[r] * (1 - q) if np.isfinite(cf[r]) else np.inf
        e_l = max(0.0, 1.0 - c_f_eff)
        # R4 (exit) is a fallback, not a competitor: it is 'viable' only when
        # no physical-provenance regime survives -- handled in choose().
        viable = (e_l < TH_LOSS) and (cvd[r] < TH_VER) and (ci[r] < TH_ISS)
        out[r] = dict(C_I=ci[r], C_V=cvd[r], E_L=e_l,
                      viable=(viable if r != "R4" else True), C_F=cf[r])
    return out


def choose(theta_row, prev, kappa, rule="A", d_eff_penalty=1.0):
    """Rule A (kappa=0) myopic; Rule B kappa>0 adds kappa*switch penalty.
    Returns (regime, J). Non-viable regimes excluded unless none viable->R4."""
    costs = regime_costs(theta_row, d_eff_penalty)
    best, best_j = None, np.inf
    for r in REGIMES[:-1]:                            # R0..R3 compete
        if not costs[r]["viable"]:
            continue
        j = costs[r]["C_I"] + costs[r]["C_V"] + costs[r]["E_L"]
        j += kappa * (0.0 if (r == prev or prev is None) else 1.0)  # Rule B
        if j < best_j:
            best_j, best = j, r
    if best is None:
        return "R4", costs["R4"]["C_I"]                # forced exit
    return best, best_j


def sequence(theta_df, kappa=0.0, d_eff_penalty=1.0):
    """Greedy rule A/B sequence."""
    prev, seq = None, []
    for _, th in theta_df.iterrows():
        r, j = choose(th, prev, kappa, d_eff_penalty=d_eff_penalty)
        seq.append((th["step"], r, j))
        prev = r
    return seq


def forward_sequence(theta_df, beta=0.9, kappa=0.0, d_eff_penalty=1.0):
    """Rule C: backward induction over the known trajectory (finite horizon)."""
    rows = theta_df.to_dict("records")
    T = len(rows)
    J = np.zeros((T + 1, len(REGIMES)))                # J[t][r]=cost-to-go from r
    pol = [[None] * len(REGIMES) for _ in range(T)]
    for t in range(T - 1, -1, -1):
        costs = regime_costs(rows[t], d_eff_penalty)
        viable = [r for r in REGIMES[:-1] if costs[r]["viable"]]
        actions = viable if viable else ["R4"]        # exit only as fallback
        for i, r in enumerate(REGIMES):
            best_j, best_r = np.inf, actions[0]
            for r2 in actions:
                c = (costs[r2]["C_I"] + costs[r2]["C_V"] + costs[r2]["E_L"]
                     + kappa * (0.0 if r2 == r else 1.0)
                     + beta * J[t + 1, REGIMES.index(r2)])
                if c < best_j:
                    best_j, best_r = c, r2
            J[t, i] = best_j
            pol[t][i] = best_r
    # entry: incumbent R0 (unengineered); first choice pays switch cost to R0
    prev, seq = "R0", []
    for t, th in enumerate(rows):
        r = pol[t][REGIMES.index(prev)]
        if r is None:
            r = "R4"
        costs = regime_costs(th, d_eff_penalty)
        j = costs[r]["C_I"] + costs[r]["C_V"] + costs[r]["E_L"]
        seq.append((th["step"], r, j))
        prev = r
    return seq


def trajectory_sims():
    rows = []
    for tr in ["T1", "T2", "T3", "T4"]:
        th = trajectory(tr)
        for kappa in [0.0, 0.1, 0.25, 0.5, 1.0]:
            for rule in ["A", "C"]:
                seq = (forward_sequence(th, kappa=kappa) if rule == "C"
                       else sequence(th, kappa=kappa))
                for step, r, j in seq:
                    rows.append(dict(traj=tr, kappa=kappa, rule=rule,
                                     step=step, regime=r, J=j))
    return pd.DataFrame(rows)


def regime_map(d_eff_penalty=1.0):
    """(c_syn/V x c_ver/V) x c_micro tiers -> myopic optimal regime."""
    rows = []
    c_syn_g = np.logspace(-3, 2, 40)
    c_ver_g = np.logspace(-3, 0, 25)
    for cm_tier, cm in [("low", 0.1), ("mid", 1.0), ("high", 10.0)]:
        for cs in c_syn_g:
            for cv in c_ver_g:
                th = dict(c_syn=cs, c_micro=cm, c_ver=cv, c_assay=0.1, q=0.0)
                r, j = choose(th, "R0", 0.0, d_eff_penalty=d_eff_penalty)
                rows.append(dict(c_micro_tier=cm_tier, c_micro=cm,
                                 c_syn_over_V=cs, c_ver_over_V=cv,
                                 optimal=r, J=j))
    return pd.DataFrame(rows)


def adaptation_value():
    """Cumulative institutional loss: best fixed regime vs adaptive."""
    rows = []
    for tr in ["T1", "T2", "T3", "T4"]:
        th = trajectory(tr)
        loss_by_r = {}
        for r in REGIMES[:-1]:
            tot = 0.0
            for _, t in th.iterrows():
                c = regime_costs(t)
                rr = c[r] if c[r]["viable"] else c["R4"]
                tot += rr["C_I"] + rr["C_V"] + rr["E_L"]
            loss_by_r[r] = tot
        # baseline: best fixed *provenance* regime (R1-R3); R0's row doubles
        # as 'immediate exit' since it is never viable
        best_fixed = min(["R1", "R2", "R3"], key=lambda r: loss_by_r[r])
        loss_exit = loss_by_r["R0"]
        for kappa in [0.0, 0.25, 0.5]:
            seq = sequence(th, kappa=kappa)
            adapt_loss = sum(j for _, _, j in seq)
            # viability extension: fraction of steps where adaptive stays
            # in a provenance regime vs the best fixed regime's first exit
            ad_steps = sum(r != "R4" for _, r, _ in seq) / STEPS
            fx_steps = sum(
                regime_costs(t)[best_fixed]["viable"] for _, t in th.iterrows()) / STEPS
            rows.append(dict(traj=tr, kappa=kappa, best_fixed=best_fixed,
                             L_fixed=loss_by_r[best_fixed],
                             L_immediate_exit=loss_exit,
                             L_adaptive=adapt_loss,
                             delta_adapt=loss_by_r[best_fixed] - adapt_loss,
                             delta_vs_exit=loss_exit - adapt_loss,
                             viable_frac_adaptive=ad_steps,
                             viable_frac_fixed=fx_steps,
                             viability_extension=ad_steps - fx_steps))
    return pd.DataFrame(rows)


def hysteresis():
    """First transition step per (trajectory, kappa): switching-cost delay."""
    rows = []
    for tr in ["T1", "T2", "T3", "T4"]:
        th = trajectory(tr)
        for kappa in [0.0, 0.1, 0.25, 0.5, 1.0]:
            seq = sequence(th, kappa=kappa)
            regs = [r for _, r, _ in seq]
            switches = [(s, regs[i - 1], regs[i]) for i, (s, r, _) in
                        enumerate(seq) if i and regs[i] != regs[i - 1]]
            first = switches[0][0] if switches else np.nan
            n_switches = len(switches)
            rows.append(dict(traj=tr, kappa=kappa, first_switch=first,
                             n_switches=n_switches,
                             sequence=">".join(dict.fromkeys(regs))))
    return pd.DataFrame(rows)


def path_dependence():
    """Two paths to the same theta_T; compare endpoint under kappa."""
    th_a = trajectory("T2").iloc[:26]             # fast path to theta_T
    th_b = pd.DataFrame({                         # slow approach, same endpoint
        "step": np.arange(len(th_a)),
        "c_syn": np.linspace(10, th_a["c_syn"].iloc[-1], len(th_a)),
        "c_micro": np.linspace(10, th_a["c_micro"].iloc[-1], len(th_a)),
        "c_ver": np.linspace(0.10, th_a["c_ver"].iloc[-1], len(th_a)),
        "c_assay": np.linspace(0.20, th_a["c_assay"].iloc[-1], len(th_a)),
        "q": np.linspace(0, th_a["q"].iloc[-1], len(th_a)),
    })
    rows = []
    for kappa in [0.0, 0.25, 0.5, 1.0]:
        ra = sequence(th_a, kappa=kappa)[-1][1]
        rb = sequence(th_b, kappa=kappa)[-1][1]
        rows.append(dict(kappa=kappa, end_A=ra, end_B=rb,
                         path_dependent=ra != rb))
    return pd.DataFrame(rows)


def r3_window():
    """Where is R3 (lineage-preserving) endogenously optimal?"""
    rows = []
    for tr in ["T1", "T2", "T3", "T4"]:
        th = trajectory(tr)
        for kappa in [0.0, 0.25]:
            seq = sequence(th, kappa=kappa)
            idx = [s for s, r, _ in seq if r == "R3"]
            rows.append(dict(traj=tr, kappa=kappa,
                             r3_steps=len(idx),
                             r3_first=(min(idx) if idx else np.nan),
                             r3_last=(max(idx) if idx else np.nan)))
    # robustness: d_eff collapse penalty and sep conditions
    for pen in [0.5, 1.0, 2.0]:
        for tr in ["T1", "T2", "T3"]:
            seq = sequence(trajectory(tr), kappa=0.0, d_eff_penalty=pen)
            idx = [s for s, r, _ in seq if r == "R3"]
            rows.append(dict(traj=tr, kappa=0.0, d_eff_penalty=pen,
                             r3_steps=len(idx),
                             r3_first=(min(idx) if idx else np.nan),
                             r3_last=(max(idx) if idx else np.nan)))
    return pd.DataFrame(rows)


def main():
    trajectory_sims().to_csv(OUT / "sim_trajectories.csv", index=False)
    regime_map().to_csv(OUT / "sim_regime_map.csv", index=False)
    adaptation_value().to_csv(OUT / "sim_adaptation.csv", index=False)
    hysteresis().to_csv(OUT / "sim_hysteresis.csv", index=False)
    path_dependence().to_csv(OUT / "sim_pathdep.csv", index=False)
    r3_window().to_csv(OUT / "sim_r3_window.csv", index=False)
    print("transition sims written")


if __name__ == "__main__":
    main()
