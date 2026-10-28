#!/usr/bin/env python3
"""Parse AstroMat/IEDA UCLA iron-meteorite xls workbooks into a tidy
sample-level concentration table (data/processed/sample_concentrations.csv)
and a per-group fingerprint summary (data/processed/group_fingerprints.csv).

Workbook layout (verified on IIAB_Wasson2007.xls):
  sheet '3 Samples'       : col0 name, col4 lithology string ("Iron meteorite, IIAB")
  sheet '4 Analytical Data': row1 element names (cols>=10), row3 units,
                            data from row6; col0 sample name; col8 = 'A' means
                            the row is a (mean) average we may use.
Concentrations are normalized to ug/g (mg/g * 1000).
"""
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

GROUP_RE = re.compile(r"iron meteorite[, ]+(.+)", re.I)


def parse_workbook(path: Path, dataset: str):
    try:
        xl = pd.ExcelFile(path)
    except Exception:  # noqa: BLE001
        return []
    if "4 Analytical Data" not in xl.sheet_names:
        return []
    # group lookup from samples sheet
    groups = {}
    if "3 Samples" in xl.sheet_names:
        s = xl.parse("3 Samples", header=None)
        for _, r in s.iterrows():
            name = str(r.iloc[0]).strip()
            lith = str(r.iloc[4]) if len(r) > 4 else ""
            m = GROUP_RE.search(lith)
            if m:
                groups[name.lower()] = m.group(1).strip()
    a = xl.parse("4 Analytical Data", header=None)
    params = a.iloc[1].tolist()
    units = a.iloc[3].tolist()
    rows = []
    for i in range(6, len(a)):
        row = a.iloc[i]
        name = str(row.iloc[0]).strip()
        if not name or name.lower() == "nan":
            continue
        rec = {"sample": name, "dataset": dataset,
               "group": groups.get(name.lower(), "")}
        for j in range(10, len(row)):
            el = params[j]
            if not isinstance(el, str) or not el.strip():
                continue
            el = el.strip()
            v = row.iloc[j]
            try:
                v = float(str(v).replace("<", "").replace(">", ""))
            except (TypeError, ValueError):
                continue
            if str(row.iloc[j]).strip().startswith("<"):
                continue  # drop detection-limit values
            unit = str(units[j]).strip()
            if "mg/g" in unit:
                v *= 1000.0  # -> ug/g
            rec[el] = v
        rows.append(rec)
    return rows


def main():
    all_rows = []
    for xls in sorted(RAW.glob("**/*.xls*")):
        dataset = xls.parent.name
        all_rows += parse_workbook(xls, dataset)
    df = pd.DataFrame(all_rows)
    df.to_csv(OUT / "sample_concentrations.csv", index=False)

    elems = [c for c in df.columns if c not in ("sample", "dataset", "group")]
    # keep elements with broad coverage
    coverage = df[elems].notna().mean()
    elems = [e for e in elems if coverage[e] > 0.3]
    df["group"] = df["group"].str.upper().str.replace(" ", "")
    known = df[df["group"].str.len() > 0]
    # group fingerprint = mean & sd of log10(ug/g) per element
    logs = known.groupby("group")[elems].agg(lambda s: np.log10(s.dropna()).mean())
    sds = known.groupby("group")[elems].agg(lambda s: np.log10(s.dropna()).std())
    n = known.groupby("group").size()
    fp = logs.join(sds, lsuffix="_mean", rsuffix="_sd")
    fp["n"] = n
    fp.to_csv(OUT / "group_fingerprints.csv")
    print("samples:", len(df), "groups:", fp.shape[0])
    print(fp[["n"]].sort_values("n", ascending=False).head(15).T)
    print("elements kept:", elems)


if __name__ == "__main__":
    main()
