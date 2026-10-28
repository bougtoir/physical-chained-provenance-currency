#!/usr/bin/env python3
"""Generate all manuscript figures for the PCPC study."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pcpc_model import dirichlet_weights, make_sources  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data" / "processed"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False})


def fig1_architecture():
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.axis("off")
    boxes = [
        (0.03, "Sources\nA, B, C, D", "#dbe9f6"),
        (0.20, "Federated mint\nmixture w_t", "#dbe9f6"),
        (0.37, "Batch t\n+ predecessor\nfraction α", "#f6e3db"),
        (0.55, "Dated coin\nD_t + y_t", "#e2f0da"),
        (0.73, "Assay &\nlineage check", "#e2f0da"),
        (0.90, "Ledger: chain\nS_1..S_t", "#fff2cc"),
    ]
    for x, label, c in boxes:
        ax.add_patch(plt.Rectangle((x, 0.35), 0.13, 0.35, fc=c, ec="k", lw=0.8,
                                   transform=ax.transAxes))
        ax.text(x + 0.065, 0.525, label, ha="center", va="center", fontsize=8,
                transform=ax.transAxes)
    for a, b in zip(boxes[:-1], boxes[1:]):
        ax.annotate("", xy=(b[0], 0.525), xytext=(a[0] + 0.135, 0.525),
                    arrowprops=dict(arrowstyle="->", lw=1.0),
                    xycoords="axes fraction")
    ax.annotate("α·p_{t−1} recycled",
                xy=(0.44, 0.30), xytext=(0.55, 0.10), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.9, ls="--"),
                xycoords="axes fraction")
    ax.annotate("", xy=(0.30, 0.30), xytext=(0.44, 0.25),
                arrowprops=dict(arrowstyle="->", lw=0.9, ls="--", color="gray"),
                xycoords="axes fraction")
    fig.savefig(FIG / "fig1_architecture.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig2_geometry():
    rng = np.random.default_rng(7)
    X = make_sources(rng, 4, 2, 3.0)
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.scatter(X[:, 0], X[:, 1], s=90, c="k", marker="s", zorder=5)
    for i, p in enumerate(X):
        ax.annotate(f"$x_{i+1}$", p + 0.12, fontsize=10)
    for order in range(3):
        w = dirichlet_weights(rng, 4)
        y = w @ X
        ax.scatter(*y, s=60, label=f"batch $t_{order+1}$")
        ax.annotate("", xy=y + 0.05, xytext=X.mean(0),
                    arrowprops=dict(arrowstyle="->", color="gray", lw=0.7))
    from matplotlib.patches import Polygon
    hull = Polygon(X, closed=True, fill=False, ls="--", ec="k", lw=0.8)
    ax.add_patch(hull)
    ax.text(*X.mean(0) + [0.1, 0.6], "attacker hull\n(q = 3/4 subset)",
            fontsize=8, color="gray")
    ax.set_xlabel("fingerprint dim 1 (log)")
    ax.set_ylabel("fingerprint dim 2 (log)")
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIG / "fig2_geometry.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig3_pf_vs_q():
    df = pd.read_csv(D / "sim_partial_source.csv")
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    for d, g in df[df.sep == 2.0].groupby("d_eff"):
        gg = g.groupby("q")["P_F"].mean()
        ax.plot(gg.index, gg.values, marker="o", ms=3,
                label=f"$d_{{eff}}$={d}")
    ax.set_xlabel("coalition source access q = k/N")
    ax.set_ylabel(r"$P_F$  (counterfeit pass prob.)")
    ax.set_title(r"$\Delta/\sigma = 2$, mean over $N$", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    ax.set_ylim(-0.02, 1.02)
    fig.savefig(FIG / "fig4_pf_vs_q.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig4_regimes():
    df = pd.read_csv(D / "sim_regimes.csv")
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    for r, g in df.groupby("regime"):
        ax.plot(g.c_syn_over_V, g.E_Pi_over_V, marker="o", ms=3, label=r)
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xscale("log")
    ax.set_xlabel("synthetic fabrication cost / coin value  $c_{syn}/V$")
    ax.set_ylabel(r"$E[\Pi_F]/V$")
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIG / "fig3_regimes.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig5_phase():
    df = pd.read_csv(D / "sim_phase.csv")
    piv = df.pivot_table(index="sep", columns="c_syn_over_V",
                         values="cls", aggfunc="first")
    codes = {"verification-limited": 0, "economically-forgeable": 1,
             "viable": 2, "technologically-obsolete": 3}
    Z = piv.replace(codes).astype(float).values
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    cmap = matplotlib.colors.ListedColormap(
        ["#f4b6b6", "#f9e2ae", "#b7dfb7", "#c9c9f0"])
    ax.pcolormesh(np.log10(piv.columns.values), np.arange(len(piv.index) + 1),
                  np.vstack([Z, Z[-1:]]), cmap=cmap, shading="auto")
    ax.set_yticks(np.arange(len(piv.index)) + 0.5)
    ax.set_yticklabels(piv.index)
    xt = ax.get_xticks()
    ax.set_xticklabels([f"$10^{{{int(t)}}}$" for t in xt])
    ax.set_xlabel(r"$c_{syn}/V$  (log$_{10}$)")
    ax.set_ylabel(r"$\Delta/\sigma$")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=c, label=k) for k, c in
                       zip(codes, cmap.colors)],
              fontsize=7, frameon=True, loc="upper left")
    fig.savefig(FIG / "fig6_phase.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig6_chain():
    df = pd.read_csv(D / "sim_chain.csv")
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    for b, g in df.groupby("burden_coef"):
        gg = g.groupby("alpha")["net_benefit"].mean()
        ax.plot(gg.index, gg.values, marker="o", ms=3,
                label=f"burden coef. {b}")
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xscale("symlog", linthresh=1e-4)
    ax.set_xlabel(r"inheritance fraction $\alpha$")
    ax.set_ylabel(r"net security benefit of chaining (per $V$)")
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIG / "fig5_chain.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig7_retro():
    df = pd.read_csv(D / "sim_retro.csv")
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    for s, g in df.groupby("sigma_sig"):
        gg = g.groupby("depth")["log10_BF"].mean()
        ax.plot(gg.index, gg.values, marker="o", ms=3,
                label=rf"attacker mismatch $\sigma_{{sig}}$={s}$\sigma$")
    ax.axhline(0, color="k", lw=0.7)
    ax.axhline(2, color="gray", lw=0.7, ls="--")
    ax.text(12, 2.15, "decisive evidence (BF=100)", fontsize=7, color="gray")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 5, 10, 20])
    ax.set_xticklabels([1, 2, 5, 10, 20])
    ax.set_xlabel("chain depth k (generations)")
    ax.set_ylabel(r"log$_{10}$ Bayes factor")
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIG / "fig7_retro.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


REGIME_COLORS = {"R1": "#4e79a7", "R2": "#f28e2b", "R3": "#59a14f",
                 "R4": "#bab0ac", "R0": "#e15759"}
REGIME_LABELS = {"R0": "R0 unengineered", "R1": "R1 fixed provenance",
                 "R2": "R2 rotating provenance", "R3": "R3 lineage-preserving",
                 "R4": "R4 exit"}


def fig8_regime_map():
    """Endogenous optimal regime over technology space + T1-T4 trajectories."""
    m = pd.read_csv(D / "sim_regime_map.csv")
    trajs = pd.read_csv(D / "sim_trajectories.csv")
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6), sharex=True, sharey=True)
    reg_to_int = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4}
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap([REGIME_COLORS[r] for r in ["R0", "R1", "R2", "R3", "R4"]])
    norm = BoundaryNorm(np.arange(-0.5, 5.5, 1), cmap.N)
    traj_colors = {"T1": "k", "T2": "purple", "T3": "teal", "T4": "red"}
    import run_transition_sims as ts
    for ax, tier in zip(axes, ["low", "mid", "high"]):
        sub = m[m.c_micro_tier == tier]
        Z = sub.pivot(index="c_ver_over_V", columns="c_syn_over_V",
                      values="optimal").map(reg_to_int.get)
        ax.pcolormesh(Z.columns, Z.index, Z.values, cmap=cmap, norm=norm,
                      shading="auto")
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(f"c_micro/V = {dict(low=0.1, mid=1.0, high=10.0)[tier]}",
                     fontsize=9)
        ax.set_xlabel(r"$c_{syn}/V$")
    for tr_name in ["T1", "T2", "T3", "T4"]:
        th = ts.trajectory(tr_name)
        for ax in axes:
            ax.plot(th["c_syn"], th["c_ver"], lw=1.2,
                    color=traj_colors[tr_name], label=tr_name)
            ax.plot(th["c_syn"].iloc[0], th["c_ver"].iloc[0], "o", ms=3,
                    color=traj_colors[tr_name])
            ax.plot(th["c_syn"].iloc[-1], th["c_ver"].iloc[-1], "x", ms=4,
                    color=traj_colors[tr_name])
    axes[0].set_ylabel(r"$c_{verification}/V$")
    handles = [plt.Rectangle((0, 0), 1, 1, fc=REGIME_COLORS[r]) for r in
               ["R1", "R2", "R3", "R4"]]
    axes[1].legend(handles, [REGIME_LABELS[r] for r in ["R1", "R2", "R3", "R4"]],
                   fontsize=7, frameon=False, loc="upper right")
    axes[2].legend([plt.Line2D([0], [0], color=c, lw=1.2)
                    for c in traj_colors.values()],
                   list(traj_colors.keys()), fontsize=7, frameon=False,
                   loc="upper right")
    fig.savefig(FIG / "fig9_regime_map.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig9_trajectories():
    """Regime index over technology-progression step, T1-T4."""
    t = pd.read_csv(D / "sim_trajectories.csv")
    t = t[(t.rule == "A") & (t.kappa == 0.0)]
    reg_to_int = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4}
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.8), sharey=True)
    for ax, tr in zip(axes, ["T1", "T2", "T3", "T4"]):
        s = t[t.traj == tr]
        ax.step(s.step, s.regime.map(reg_to_int), where="post", lw=1.6)
        ax.set_title(tr, fontsize=9)
        ax.set_xlabel("technology progression step")
        for _, row in s.iterrows():
            ax.plot(row.step, reg_to_int[row.regime], ".", ms=2,
                    color=REGIME_COLORS[row.regime])
    axes[0].set_yticks(range(5))
    axes[0].set_yticklabels(["R0", "R1", "R2", "R3", "R4"])
    axes[0].set_ylabel("endogenous regime")
    fig.savefig(FIG / "fig8_trajectories.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig10_adaptation():
    """Delta_adapt and viability extension by trajectory and kappa."""
    a = pd.read_csv(D / "sim_adaptation.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.2))
    w = 0.22
    x = np.arange(len(a.traj.unique()))
    for i, k in enumerate(sorted(a.kappa.unique())):
        s = a[a.kappa == k].set_index("traj").loc[["T1", "T2", "T3", "T4"]]
        ax1.bar(x + (i - 1) * w, s.delta_adapt, w,
                label=rf"$\kappa$={k}")
        ax2.bar(x + (i - 1) * w, s.viability_extension * 100, w,
                label=rf"$\kappa$={k}")
    ax1.axhline(0, color="k", lw=0.7); ax2.axhline(0, color="k", lw=0.7)
    for ax, ttl in [(ax1, r"$\Delta_{adapt}$ = L_fixed - L_adaptive (V)"),
                    (ax2, "viability extension (% of steps)")]:
        ax.set_xticks(x); ax.set_xticklabels(["T1", "T2", "T3", "T4"])
        ax.set_ylabel(ttl); ax.legend(frameon=False, fontsize=7)
    fig.savefig(FIG / "fig10_adaptation.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    for f in (fig1_architecture, fig2_geometry, fig3_pf_vs_q, fig4_regimes,
              fig5_phase, fig6_chain, fig7_retro, fig8_regime_map,
              fig9_trajectories, fig10_adaptation):
        f()
        print("wrote", f.__name__)
