# FINAL_FIGURE_TABLE_CITATION_AUDIT

Method: regex extraction of `Fig.|Figure N` and `Table N` mentions in
manuscript.md; first-citation position ordering; captions verified in the
built DOCX (FIG_CAPTIONS / TABLE_FILES in analysis/build_docx.py + inline
Table 5 caption).

| Object | Exists | First cited | Order | Caption | PASS |
|--------|--------|-------------|-------|---------|------|
| Figure 1 | figures/fig1_architecture.png | §3.2 | 1st | yes | PASS |
| Figure 2 | figures/fig2_geometry.png | §3.5 | 2nd | yes | PASS |
| Figure 3 | figures/fig3_regimes.png | §5.1 | 3rd | yes | PASS |
| Figure 4 | figures/fig4_pf_vs_q.png | §5.2 | 4th | yes | PASS |
| Figure 5 | figures/fig5_chain.png | §5.3 | 5th | yes | PASS |
| Figure 6 | figures/fig6_phase.png | §5.4 | 6th | yes | PASS |
| Figure 7 | figures/fig7_retro.png | §5.5 | 7th | yes | PASS |
| Figure 8 | figures/fig8_trajectories.png | §5.7 | 8th | yes | PASS |
| Figure 9 | figures/fig9_regime_map.png | §5.7 | 9th | yes | PASS |
| Figure 10 | figures/fig10_adaptation.png | §5.8 | 10th | yes | PASS |
| Table 1 | tables/table_regimes.csv | §5.1 | 1st | yes | PASS |
| Table 2 | tables/table_crt05.csv | §5.2 | 2nd | yes | PASS |
| Table 3 | tables/table_empirical_meta.csv | §5.6 | 3rd | yes | PASS |
| Table 4 | tables/table_transitions.csv | §5.7 | 4th | yes | PASS |
| Table 5 | in-text (§6) | §6 | 5th | yes | PASS |
| Table 6 | tables/table_blockchain_comparison.csv | §7.5 | 6th | yes | PASS |

Orphans: 0. Duplicated labels: 0. Numbering skips: 0.
First-citation order strictly increasing for both series: PASS.
No Supplement/Main confusion (no supplement in this package).
