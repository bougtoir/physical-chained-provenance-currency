# Phase 1 — Novelty and feasibility audit

Project: Physical Chained Provenance Currency (PCPC)
Date: 2026-10-03 (UTC)
Status: Integration Gate 1 — **CONDITIONAL GO**

## 1. Search protocol

Broad keyword searches across the five mandated domains (§4.1–4.5 of the
brief), executed 2026-10-03 via web search plus targeted repository searches
(figshare API, DataCite API, AstroMat/IEDA, NASA NTRS, arXiv). This document
records the nearest prior art found; it is not a systematic review.

## 2. Domain findings and nearest prior art

### 2.1 Commodity money and counterfeit economics

Established literature separates *intrinsic commodity value* from *verification
and recognizability*:

- Sargent & Velde, *The Big Problem of Small Change* (2002): small-change
  commodity money is constrained by authentication and production cost, not
  only by metal scarcity.
- Monetary-search counterfeiting literature: Nosal & Wallace (2007, JME),
  Hu, Kennan & Wallace (2009), Li & Rocheteau (2011), and — closest to our
  verification framing — "Counterfeit quality and verification in a monetary
  exchange" (Economic Modelling 52, 2016) and "The threat of counterfeiting
  in competitive search equilibrium" (JET, 2014). These model a cost/quality
  trade-off for counterfeiters and endogenous verification, but all treat the
  authentication problem as static in time.
- Debasement / seigniorage: Redish, *Bimetallism* (2000); Velde's debasement
  chronicles; Gandal & Sussman on inflationary incentives.

Gap relative to PCPC: counterfeit-economics models assume a *fixed*
authentication target. Rotating the physical target as a policy variable, and
physically coupling successive targets, is not present in this literature.

### 2.2 Banknote security, taggants, PUFs

- Banknotes already rotate security feature *sets* across series (threads,
  holograms, microprinting, machine-readable features). Novelty cannot rest
  on "features change over time" — confirmed and adopted as an explicit
  boundary (§32 of the brief).
- Tagants / forensic markers: molecular taggants, lanthanide signatures,
  DNA marking — per-object or per-batch markers, not chained states.
- PUFs: static PUFs exploit manufacturing disorder; **dynamic PUFs exist**
  (DRAM decay-based DPUFs; device-aging DPUFs, DAC'11) where the response
  depends on query timing. Reconfigurable PUFs change challenge-response
  behaviour under issuer control. This is the closest hardware analog of
  issuer-controlled state rotation and must be cited; however DPUF
  "time-dependence" is *aging/decay of the same object*, not issuer-selected
  batch state rotation with predecessor inheritance across a money supply.

Gap: no PUF work found links a physical object of generation *t* to the
authenticated physical output of generation *t−1* as a security mechanism.

### 2.3 Isotope / elemental provenance

- Archaeometallurgical provenance: Pb and Sr isotope sourcing (Gale &
  Stos-Gale lineage), multi-element + isotope fingerprinting; Bayesian
  isotope mixing models for source apportionment (e.g., Scientific Reports
  2018 Pb Bayesian mixing model) — directly supplies our verification model.
- Meteoritics: iron meteorite chemical groups (Wasson UCLA INAA/RNAA
  programme, 50+ years, AstroMat/IEDA-archived); nucleosynthetic isotope
  anomalies (ε54Cr, ε62Ni, μ54Fe, ε100Ru, ε196Pt) distinguishing NC vs CC
  reservoirs and individual parent bodies (e.g., Anand et al. 2024 GCA;
  Spitzer et al. 2020; Cook et al. 2020; Nanne et al. 2019).
- Cosmogenic overprint on Fe/Cr isotopes in irons (Qin et al. 2010; Hopp et
  al. 2022) — a real measurement caveat for empirical calibration.

Gap: provenance literature attributes a *natural* composition to a source;
it does not study an issuer *choosing* mixtures of sources per batch as a
security policy, nor deliberate predecessor-material carryover.

### 2.4 Space-resource economics

- Techno-economic asteroid mining (Acta Astronautica techno-economic
  analyses; PGM reassessments drawing on the UCLA meteorite statistics;
  Sowers & Dreyfus; Elvis). Relevant only as the extreme test environment:
  commodity abundance, dispersed sources, long logistics. No monetary/
  authentication mechanism found in this literature.

### 2.5 Physical ledgers / material hash chains — the critical novelty boundary

Nearest collisions found:

1. **DNA-steganography "blockchain of signature material"** (arXiv:1909.07914):
   time-stamped records whose DNA-encrypted blocks are validated via hash
   against published values and cross-referenced over time. This couples a
   physical tag to a *digital* hash chain — the chaining is cryptographic,
   in the digital layer.
2. **Chemical-signature + blockchain anti-counterfeiting** (Kennedy et al.,
   J. Mater. Chem. C 2017): lanthanide chemical signatures in 3-D printed
   parts linked to Ethereum entries. Physical fingerprint → digital ledger.
3. **"Physical hash" for additive manufacturing** (Computers in Industry):
   side-channel toolpath/process measurements hashed to detect tampering.
   A physical *measurement* hash, not a material-state chain.
4. **MaDiTraCe / Digital Product Passports**: isotopic/chemical material
   fingerprints as verifiable credentials, optional blockchain anchoring.
   Again, fingerprint → digital credential.
5. **Physical unclonable functions** generally: per-object uniqueness; no
   intergenerational state chain.

**No prior work found in which the monetary/material state itself satisfies
S_t = f(S_{t−1}, X_t)** — i.e., where authenticated predecessor *material*
is physically inherited into the next issuance and contributes security
beyond the issuer's own attestation. All "physical blockchain" work found
chains *digital records about* physical objects.

## 3. Novelty matrix

| Component | Exists in literature? | Nearest form |
|---|---|---|
| Commodity money under authentication cost | yes | monetary-search counterfeiting |
| Rotating authentication features | yes | banknote redesign; reconfigurable PUF |
| Issuer-controlled physical state rotation | partial | dynamic/reconfigurable PUF (non-monetary) |
| Isotope/multi-element provenance verification | yes | archaeometallurgy, meteoritics |
| Mixture-design authentication of a money | no | — |
| Physical predecessor-material inheritance as security (α>0) | not found | DNA-steg. chain is digital-layer only |
| Retrospective authentication: later state evidences earlier state | not found | — |
| Extreme-environment (interplanetary) framing | partial | space-resource economics (non-monetary) |

## 4. Overlap risks to manage in the manuscript

- Must explicitly delimit vs. banknote feature rotation (done in §32).
- Must cite dynamic/reconfigurable PUF literature and state precisely what
  PCPC adds (batch-state + inheritance + monetary equilibrium).
- Must call the DNA-steganography paper a *digital* hash chain aided by a
  physical tag, not a physical state chain.
- Must not claim blockchain equivalence (§34 comparison table).

## 5. Candidate empirical datasets (acquired in Phase 3)

| Dataset | Content | Access |
|---|---|---|
| AstroMat/IEDA UCLA iron-meteorite releases (20+ DOIs) | sample-level Ni, Co, Cu, Ga, Ge, As, W, Re, Ir, Pt, Au for IAB, IIAB, IIG, IIE, IIIAB, IVB, IC, ungrouped … | downloaded raw zip + xls; see data/acquisition_ledger.csv |
| Anand et al. 2024 GCA | Fe, Ni, O, Cr isotopes, IIG/IIAB/IC/IIIAB | full PDF downloaded |
| Ni et al. 2020 Nat. Geosci. | Fe-isotope run products + SI compilation | figshare CC-BY xlsx + SI PDF downloaded |
| Ru isotope dataset (IEDA 100622) | ε100Ru chondrites + irons | downloaded |
| Pd/Pt isotope dataset (IEDA 111416) | ε196Pt irons | downloaded |
| OSTI isotope-separation cost reports | AVLIS vs EM cost structure; enriched-isotope prices | web sources, cited in ledger notes |

Licensing: UCLA/AstroMat datasets are published synthesis datasets (IEDA
repository, CC-type terms; recorded per-file in the ledger). Third-party
individual-record redistributions to public mirrors are handled per repo
policy (aggregate/derived only in public; raw acquisition script regenerates).

## 6. Feasibility verdict: CONDITIONAL GO

- GO on novelty: the S_t = f(S_{t−1}, X_t) *material-state* mechanism with
  counterfeit-economics evaluation appears unoccupied; collisions are
  digital-layer chains, citable as adjacent.
- CONDITION on empirics: meteorite-group fingerprints are real but only a
  *demonstration* calibration (source bodies, not "planets"). The main
  results must ride on the generalized Δ/σ sweep (Analysis B).
- CONDITION on integrity: bulk chaining (α>0, architecture A) may provide
  zero incremental security under Attack 3 synthesis — this is a designed
  falsification test (F3), not a bug to hide.
