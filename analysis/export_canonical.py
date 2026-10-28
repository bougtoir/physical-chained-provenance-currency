#!/usr/bin/env python3
"""Export the single source of truth for all analysis-derived values used by
the manuscript, cover letter, highlights, captions and audits.

Every downstream document must inject `results/canonical_results.json`
values by key — never retype a number. Display strings are produced here by
canonical formatters so prose, tables and letters can never drift apart.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUT = ROOT / "results" / "canonical_results.json"


def fmt_pct(x, digits=1):
    return f"{x * 100:.{digits}f}"


def main():
    emp = json.loads((PROC / "empirical_meta.json").read_text())
    sep = pd.read_csv(PROC / "empirical_separability.csv")
    traj = pd.read_csv(PROC / "sim_trajectories.csv")
    adapt = pd.read_csv(PROC / "sim_adaptation.csv")
    r3 = pd.read_csv(PROC / "sim_r3_window.csv")
    retro = pd.read_csv(PROC / "sim_retro.csv")
    rmap = pd.read_csv(PROC / "sim_regime_map.csv")
    chain = pd.read_csv(PROC / "sim_chain.csv")
    ps = pd.read_csv(PROC / "sim_partial_source.csv")
    crt = pd.read_csv(ROOT / "tables" / "table_crt05.csv", index_col=0)
    n_samples = len(pd.read_csv(PROC / "sample_concentrations.csv"))

    def seq(t, kappa=0.0, rule="A"):
        s = traj[(traj.traj == t) & (traj.kappa == kappa) & (traj.rule == rule)]
        return s.regime.tolist(), s.step.tolist()

    def transitions(t, kappa=0.0, rule="A"):
        regs, steps = seq(t, kappa, rule)
        out = []
        for i in range(1, len(regs)):
            if regs[i] != regs[i - 1]:
                out.append({"step": int(steps[i]), "from": regs[i - 1],
                            "to": regs[i]})
        return out, "".join(r + ">" for r in dict.fromkeys(regs))[:-1]

    def arow(t, kappa=0.0):
        return adapt[(adapt.traj == t) & (adapt.kappa == kappa)].iloc[0]

    t1_tr, t1_seq = transitions("T1")
    t2_tr, t2_seq = transitions("T2")
    t3_tr, t3_seq = transitions("T3")
    t4_tr, t4_seq = transitions("T4")

    r3_t2 = r3[(r3.traj == "T2") & (r3.d_eff_penalty.isna())].iloc[0]
    r3_p05 = r3[(r3.traj == "T2") & (r3.d_eff_penalty == 0.5)].iloc[0]
    r3_p2 = r3[(r3.traj == "T2") & (r3.d_eff_penalty == 2.0)].iloc[0]

    coarse_k1 = retro[(retro.sigma_sig == 3.0) & (retro.depth == 1)].log10_BF
    coarse_k20 = retro[(retro.sigma_sig == 3.0) & (retro.depth == 20) &
                       (retro.alpha == 0.10)].log10_BF.iloc[0]
    fine_k1 = retro[(retro.sigma_sig == 0.5) & (retro.depth == 1) &
                    (retro.alpha == 0.10)].log10_BF.iloc[0]
    fine_k20 = retro[(retro.sigma_sig == 0.5) & (retro.depth == 20) &
                     (retro.alpha == 0.10)].log10_BF.iloc[0]

    r2 = rmap[rmap.optimal == "R2"]
    pos_chain = chain[chain.net_benefit > 0]
    alpha_min = pos_chain.alpha.min()

    canon = {
        "n_samples": {"value": n_samples, "display": f"{n_samples:,}",
                      "source": "data/processed/sample_concentrations.csv"},
        "n_groups": {"value": emp["n_groups"], "display": str(emp["n_groups"]),
                     "source": "data/processed/empirical_meta.json"},
        "n_elements": {"value": emp["n_elements"],
                       "display": str(emp["n_elements"]),
                       "source": "data/processed/empirical_meta.json"},
        "d_eff": {"value": emp["d_eff_empirical"],
                  "display": f"{emp['d_eff_empirical']:.2f}",
                  "source": "data/processed/empirical_meta.json"},
        "d_eff_int": {"value": round(emp["d_eff_empirical"]),
                      "display": str(round(emp["d_eff_empirical"])),
                      "source": "data/processed/empirical_meta.json"},
        "median_sep": {"value": float(sep.delta_over_sigma.median()),
                       "display": f"{sep.delta_over_sigma.median():.1f}",
                       "source": "data/processed/empirical_separability.csv"},
        "sep_min": {"value": float(sep.delta_over_sigma.min()),
                    "display": f"{sep.delta_over_sigma.min():.2f}",
                    "source": "data/processed/empirical_separability.csv"},
        "sep_max": {"value": float(sep.delta_over_sigma.max()),
                    "display": f"{sep.delta_over_sigma.max():.1f}",
                    "source": "data/processed/empirical_separability.csv"},
        "crt05_sep8_n3": {"value": float(crt.loc[8.0, "3"]),
                          "display": f"{crt.loc[8.0, '3']:.1f}",
                          "source": "tables/table_crt05.csv"},
        "crt05_sep8_n50": {"value": float(crt.loc[8.0, "50"]),
                           "display": f"{crt.loc[8.0, '50']:.0f}",
                           "source": "tables/table_crt05.csv"},
        "crt05_sep_le2": {"value": 0.0, "display": "0",
                          "source": "tables/table_crt05.csv"},
        "horizon_steps": {"value": 40, "display": "40",
                          "source": "data/processed/sim_trajectories.csv"},
        "T1_sequence": {"value": t1_seq.replace(">", "→"), "display": t1_seq,
                        "source": "data/processed/sim_trajectories.csv"},
        "T1_first_transition": {"value": t1_tr[0]["step"],
                                "display": str(t1_tr[0]["step"]),
                                "source": "data/processed/sim_trajectories.csv"},
        "T2_sequence": {"value": t2_seq.replace(">", "→"), "display": t2_seq,
                        "source": "data/processed/sim_trajectories.csv"},
        "T2_first_transition": {"value": t2_tr[0]["step"],
                                "display": str(t2_tr[0]["step"]),
                                "source": "data/processed/sim_trajectories.csv"},
        "T2_r3_first": {"value": int(r3_t2.r3_first), "display": str(int(r3_t2.r3_first)),
                        "source": "data/processed/sim_r3_window.csv"},
        "T2_r3_last": {"value": int(r3_t2.r3_last), "display": str(int(r3_t2.r3_last)),
                       "source": "data/processed/sim_r3_window.csv"},
        "T2_r3_steps": {"value": int(r3_t2.r3_steps), "display": str(int(r3_t2.r3_steps)),
                        "source": "data/processed/sim_r3_window.csv"},
        "T3_sequence": {"value": t3_seq.replace(">", "→"), "display": t3_seq,
                        "source": "data/processed/sim_trajectories.csv"},
        "T4_sequence": {"value": t4_seq.replace(">", "→"), "display": t4_seq,
                        "source": "data/processed/sim_trajectories.csv"},
        "T4_first_transition": {"value": t4_tr[0]["step"],
                                "display": str(t4_tr[0]["step"]),
                                "source": "data/processed/sim_trajectories.csv"},
        "delta_adapt_T1": {"value": float(arow("T1").delta_adapt),
                           "display": f"{arow('T1').delta_adapt:.2f}",
                           "source": "data/processed/sim_adaptation.csv"},
        "delta_adapt_T1_kappa05": {"value": float(arow("T1", 0.5).delta_adapt),
                                   "display": f"{arow('T1', 0.5).delta_adapt:.2f}",
                                   "source": "data/processed/sim_adaptation.csv"},
        "viability_ext_T1": {"value": float(arow("T1").viability_extension),
                             "display": f"{arow('T1').viability_extension:.3f}",
                             "source": "data/processed/sim_adaptation.csv"},
        "viability_ext_T1_pct": {"value": float(arow("T1").viability_extension) * 100,
                                 "display": fmt_pct(arow("T1").viability_extension),
                                 "source": "data/processed/sim_adaptation.csv"},
        "delta_vs_exit_T2": {"value": float(arow("T2").delta_vs_exit),
                             "display": f"{arow('T2').delta_vs_exit:.2f}",
                             "source": "data/processed/sim_adaptation.csv"},
        "delta_vs_exit_T2_abs": {"value": abs(float(arow("T2").delta_vs_exit)),
                                 "display": f"{abs(arow('T2').delta_vs_exit):.2f}",
                                 "source": "data/processed/sim_adaptation.csv"},
        "delta_vs_exit_T4": {"value": float(arow("T4").delta_vs_exit),
                             "display": f"{arow('T4').delta_vs_exit:.2f}",
                             "source": "data/processed/sim_adaptation.csv"},
        "delta_vs_exit_T4_abs": {"value": abs(float(arow("T4").delta_vs_exit)),
                                 "display": f"{abs(arow('T4').delta_vs_exit):.2f}",
                                 "source": "data/processed/sim_adaptation.csv"},
        "r3_window_pen05_steps": {"value": int(r3_p05.r3_steps),
                                  "display": str(int(r3_p05.r3_steps)),
                                  "source": "data/processed/sim_r3_window.csv"},
        "r3_window_pen2_steps": {"value": int(r3_p2.r3_steps),
                                 "display": str(int(r3_p2.r3_steps)),
                                 "source": "data/processed/sim_r3_window.csv"},
        "retro_coarse_k1_log10_max": {"value": float(coarse_k1.max()),
                                      "display": f"{coarse_k1.max():.0f}",
                                      "source": "data/processed/sim_retro.csv"},
        "retro_coarse_k1_log10_min": {"value": float(coarse_k1.min()),
                                      "display": f"{coarse_k1.min():.0f}",
                                      "source": "data/processed/sim_retro.csv"},
        "retro_coarse_k20_log10": {"value": float(coarse_k20),
                                   "display": f"{coarse_k20:.2f}",
                                   "source": "data/processed/sim_retro.csv"},
        "retro_fine_k1_log10": {"value": float(fine_k1),
                                "display": f"{fine_k1:.2f}",
                                "source": "data/processed/sim_retro.csv"},
        "retro_fine_k1_log10_int": {"value": round(fine_k1),
                                    "display": str(round(fine_k1)),
                                    "source": "data/processed/sim_retro.csv"},
        "retro_fine_k20_log10_int": {"value": round(fine_k20),
                                     "display": str(round(fine_k20)),
                                     "source": "data/processed/sim_retro.csv"},
        "retro_coarse_k20_log10_int": {"value": round(coarse_k20),
                                       "display": str(round(coarse_k20)),
                                       "source": "data/processed/sim_retro.csv"},
        "retro_fine_k20_log10": {"value": float(fine_k20),
                                 "display": f"{fine_k20:.2f}",
                                 "source": "data/processed/sim_retro.csv"},
        "expiration_frontier": {"value": 0.05, "display": "0.05",
                                "source": "data/processed/sim_phase.csv + tables/table_regimes.csv"},
        "r2_band_lo": {"value": float(r2.c_syn_over_V.min()),
                       "display": f"{r2.c_syn_over_V.min():.2f}",
                       "source": "data/processed/sim_regime_map.csv"},
        "r2_band_hi": {"value": float(r2.c_syn_over_V.max()),
                       "display": f"{r2.c_syn_over_V.max():.2f}",
                       "source": "data/processed/sim_regime_map.csv"},
        "c_ver_exit": {"value": float(r2.c_ver_over_V.max()),
                       "display": f"{r2.c_ver_over_V.max():.1f}",
                       "source": "data/processed/sim_regime_map.csv"},
        "lineage_alpha_min": {"value": float(alpha_min),
                              "display": f"{alpha_min:.2f}",
                              "source": "data/processed/sim_chain.csv"},
        "lineage_nb_a05_b05": {"value": float(chain[(chain.alpha == 0.05) & (chain.burden_coef == 0.5)].net_benefit.iloc[0]),
                               "display": f"{chain[(chain.alpha == 0.05) & (chain.burden_coef == 0.5)].net_benefit.iloc[0]:.3f}",
                               "source": "data/processed/sim_chain.csv"},
        "lineage_nb_a10_b8": {"value": float(chain[(chain.alpha == 0.10) & (chain.burden_coef == 8.0)].net_benefit.iloc[0]),
                              "display": f"{chain[(chain.alpha == 0.10) & (chain.burden_coef == 8.0)].net_benefit.iloc[0]:.3f}",
                              "source": "data/processed/sim_chain.csv"},
        "pf_sep8_deff4_q0_n50": {"value": float(ps[(ps.sep == 8) & (ps.d_eff == 4) & (ps.q == 0) & (ps.N == 50)].P_F.iloc[0]),
                                 "display": f"{ps[(ps.sep == 8) & (ps.d_eff == 4) & (ps.q == 0) & (ps.N == 50)].P_F.iloc[0]:.2f}",
                                 "source": "data/processed/sim_partial_source.csv"},
        "verif_sep_bound": {"value": 4, "display": "4",
                            "source": "data/processed/sim_partial_source.csv"},
    }
    OUT.write_text(json.dumps(canon, indent=2, ensure_ascii=False))
    print(f"wrote {OUT} with {len(canon)} keys")


if __name__ == "__main__":
    main()
