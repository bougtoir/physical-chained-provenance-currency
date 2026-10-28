#!/usr/bin/env python3
"""Machine-readable + manuscript tables."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data" / "processed"
T = ROOT / "tables"
T.mkdir(exist_ok=True)

# T1: CRT_0.5 grid (sep x N), d_eff=8
ps = pd.read_csv(D / "sim_partial_source.csv")
sub = ps[ps.d_eff == 8]
rows = []
for (s, n), g in sub.groupby(["sep", "N"]):
    g = g.sort_values("q")
    hit = g[g.P_F >= 0.5]
    rows.append(dict(sep_over_sigma=s, N=n,
                     CRT_05=hit.q.min() if len(hit) else np.nan))
pd.DataFrame(rows).pivot(index="sep_over_sigma", columns="N",
                         values="CRT_05").to_csv(T / "table_crt05.csv")

# T2: regime summary at c_syn/V = 0.05
rg = pd.read_csv(D / "sim_regimes.csv")
rg[np.isclose(rg.c_syn_over_V, 0.0464, atol=0.01)].to_csv(
    T / "table_regimes.csv", index=False)

# T3: empirical fingerprint summary
fp = pd.read_csv(D / "group_fingerprints.csv", index_col=0)
meta = pd.read_json(D / "empirical_meta.json", typ="series")
pd.DataFrame(meta).to_csv(T / "table_empirical_meta.csv")
fp[fp["n"] >= 15][["n"]].to_csv(T / "table_groups_n.csv")

# T4: blockchain vs PCPC comparison (static content per brief §34)
comp = pd.DataFrame([
    ["Previous-state link", "cryptographic hash", "physical material inheritance"],
    ["Append-only history", "protocol-enforced", "production-sequence-dependent"],
    ["Distributed consensus", "typically yes", "not necessarily"],
    ["Replicated ledger", "yes", "not inherent (issuer records)"],
    ["Tamper evidence", "cryptographic", "material / forensic"],
    ["Authentication cost", "computational", "metrological (assay)"],
    ["State copying", "digital, free", "physical, costly"],
    ["Failure mode", "key/protocol/consensus compromise",
     "fabrication & assay economics"],
], columns=["Property", "Cryptographic blockchain", "PCPC"])
comp.to_csv(T / "table_blockchain_comparison.csv", index=False)

# T5: endogenous transition summary across trajectories
tr = pd.read_csv(D / "sim_trajectories.csv")
tr = tr[(tr.rule == "A") & (tr.kappa == 0.0)]
ad = pd.read_csv(D / "sim_adaptation.csv")
hy = pd.read_csv(D / "sim_hysteresis.csv")
rows = []
for tn in ["T1", "T2", "T3", "T4"]:
    s = tr[tr.traj == tn]
    seq = ">".join(dict.fromkeys(s.regime))
    switches = s[s.regime != s.regime.shift()].iloc[1:]
    a0 = ad[(ad.traj == tn) & (ad.kappa == 0.0)].iloc[0]
    rows.append(dict(
        trajectory=tn,
        endogenous_sequence=seq,
        first_transition_step=(int(switches.step.min())
                               if len(switches) else np.nan),
        n_transitions=int(len(switches)),
        r3_window_steps=int((s.regime == "R3").sum()),
        delta_adapt_V=round(float(a0.delta_adapt), 3),
        viability_extension_frac=round(float(a0.viability_extension), 3)))
pd.DataFrame(rows).to_csv(T / "table_transitions.csv", index=False)
print("tables written")
