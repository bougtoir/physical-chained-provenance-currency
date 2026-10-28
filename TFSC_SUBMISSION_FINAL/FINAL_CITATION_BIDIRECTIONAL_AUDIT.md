# FINAL_CITATION_BIDIRECTIONAL_AUDIT

Method: regex extraction of all bracketed citations in manuscript.md body
(excluding the References section), with `[0,1]` math intervals excluded;
ranges `[a–b]` expanded; first-appearance order computed.

Results:

- Total references in list: **27**
- Total cited references: **27**
- Orphan references (listed, never cited): **0**
- Unresolved citations (cited, not in list): **0**
- Duplicate list entries: **0**
- Citation events: 51 (multi-cite groups expanded)

Citation numbering order (first appearance): 1,2,3,…,27 — strictly
sequential, no backward first-appearance ordering. PASS.

Ref style: Vancouver numbered, matches TFSC numbered-reference convention.
