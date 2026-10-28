#!/usr/bin/env python3
"""Download UCLA iron-meteorite datasets from the Astromaterials Data Repository (AstroMat/IEDA).

Each DOI resolves to a landing page at ada.astromat.org; the page embeds a
pre-signed S3 'bundle' link that packages the dataset files as a zip.
Raw downloads are kept byte-identical under data/raw/ (per repo data policy)
and logged to data/acquisition_ledger.csv.
"""
import csv
import hashlib
import html
import json
import re
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
LEDGER = ROOT / "data" / "acquisition_ledger.csv"
ADA = "https://ada.astromat.org/doi/"

DATASETS = {
    # doi -> short label used in filenames
    "10.26022/IEDA/112040": "wasson1980_iab_iiicd",
    "10.26022/IEDA/112041": "choi1995_iab_iiicd",
    "10.26022/IEDA/112042": "wasson2002_iab_complex",
    "10.26022/IEDA/112124": "wasson2007_iiab",
    "10.26022/IEDA/112128": "wasson2009_iig",
    "10.26022/IEDA/112129": "wasson2017_iie",
    "10.26022/IEDA/112123": "scott1976_viii",
    "10.26022/IEDA/112130": "wasson1974_vii",
    "10.26022/IEDA/112131": "wasson1998_xii",
    "10.26022/IEDA/112133": "wasson1970_v_iiic_iiid",
    "10.26022/IEDA/112138": "rasmussen_ivb",
    "10.26022/IEDA/112139": "wasson1967_i",
    "10.26022/IEDA/112117": "wasson1988_xi_antarctic",
    "10.26022/IEDA/112122": "wasson1972_iii_hexahedrites",
    "10.26022/IEDA/112045": "wasson1972_iv_highge",
    "10.26022/IEDA/112043": "wasson1990_canyondiablo",
    "10.26022/IEDA/112144": "wasson2011_comp_vs_size",
    "10.26022/IEDA/112116": "wasson1999_antarctic_ungrouped",
    "10.26022/IEDA/112121": "scott1977_four_new_irons",
    "10.26022/IEDA/112126": "wasson1986_iie_nonmagmatic",
    "10.26022/IEDA/112127": "kracher1980_ix_iif",
    "10.1594/IEDA/100622": "ru_isotopes_chondrites_irons",
    "10.1594/IEDA/111416": "pd_pt_isotopes_irons",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bundle_url(doi):
    url = ADA + doi
    with urllib.request.urlopen(url, timeout=60) as r:
        page = r.read().decode("utf-8", "replace")
    m = re.findall(r'href="([^"]*bundle[^"]*zip[^"]*)"', page)
    return html.unescape(m[0]) if m else None


def datacite_meta(doi):
    url = "https://api.datacite.org/dois/" + doi.lower()
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            a = json.load(r)["data"]["attributes"]
        return {
            "title": a["titles"][0]["title"],
            "publisher": a.get("publisher", ""),
            "license": (a.get("rightsList") or [{}])[0].get("rights", ""),
            "landing": a.get("url", ""),
        }
    except Exception as e:  # noqa: BLE001
        return {"title": "", "publisher": "IEDA/Astromat", "license": "", "landing": "", "error": str(e)}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for doi, label in DATASETS.items():
        dest = RAW / f"{label}.zip"
        meta = datacite_meta(doi)
        try:
            burl = bundle_url(doi)
            if not burl:
                rows.append({**meta, "doi": doi, "label": label, "status": "no_bundle_link"})
                continue
            if not dest.exists():
                req = urllib.request.Request(burl, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                    f.write(r.read())
            members = []
            try:
                with zipfile.ZipFile(dest) as z:
                    members = z.namelist()
                    z.extractall(RAW / label)
            except zipfile.BadZipFile:
                rows.append({**meta, "doi": doi, "label": label, "status": "bad_zip"})
                continue
            rows.append({**meta, "doi": doi, "label": label, "status": "ok",
                         "bytes": dest.stat().st_size, "sha256": sha256(dest),
                         "files": "; ".join(members)})
            print("ok", label, dest.stat().st_size)
            time.sleep(0.5)
        except Exception as e:  # noqa: BLE001
            rows.append({**meta, "doi": doi, "label": label, "status": f"error:{e}"})
            print("ERR", label, e)
    fieldnames = ["doi", "label", "title", "publisher", "license", "landing",
                  "status", "bytes", "sha256", "files"]
    with open(LEDGER, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    # UTC acquisition stamp
    with open(ROOT / "data" / "acquisition_utc.txt", "w") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + "\n")


if __name__ == "__main__":
    main()
