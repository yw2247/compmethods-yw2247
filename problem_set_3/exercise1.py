#!/usr/bin/env python3
import time, json, requests, xml.etree.ElementTree as ET

YEAR  = "2024"
RETMAX = 1000
BATCH  = 200
SLEEP  = 1.0

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ESEARCH = f"{EUTILS}/esearch.fcgi"
EFETCH  = f"{EUTILS}/efetch.fcgi"

def text_content(elem):
    """extract plain text"""
    if elem is None:
        return ""
    return ET.tostring(elem, method="text", encoding="unicode").strip()

# 1a) ESearch - retrieve PMIDs
def esearch_pmids(term_tiab, year=YEAR, retmax=RETMAX):
    params = {
        "db": "pubmed",
        "term": term_tiab,
        "retmode": "xml",
        "retmax": str(retmax),
        "datetype": "pdat",
        "mindate": year,
        "maxdate": year
    }

    r = requests.get(ESEARCH, params=params, timeout=60)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    return [e.text for e in root.findall(".//IdList/Id")]

# 1b/d) EFetch metadata in batches (handle structured abstracts)
def efetch_metadata(pmids, query_label):
    """
    Returns {pmid: {"ArticleTitle": ..., "AbstractText": ..., "query": ...}}
    """
    out = {}
    for i in range(0, len(pmids), BATCH):
        ids = ",".join(pmids[i:i+BATCH])
        data = {
            "db": "pubmed",
            "id": ids,
            "retmode": "xml",
            "rettype": "abstract"
        }
        resp = requests.post(EFETCH, data=data, timeout=120)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)

        for art in root.findall(".//PubmedArticle"):
            pmid = (art.findtext(".//MedlineCitation/PMID") or "").strip()
            if not pmid:
                continue

            title = text_content(art.find(".//Article/ArticleTitle"))

            # structured abstracts: join all sections
            parts = []
            for p in art.findall(".//Article/Abstract/AbstractText"):
                label = p.attrib.get("Label")
                txt = text_content(p)
                if txt:
                    parts.append(f"{label}: {txt}" if label else txt)
            abstract = " ".join(parts)

            out[pmid] = {
                "ArticleTitle": title,
                "AbstractText": abstract,
                "query": query_label
            }
        time.sleep(SLEEP)  # rate limit
    return out

# 1c) Overlap
def compute_overlap(pmids_a, pmids_b):
    return sorted(set(pmids_a) & set(pmids_b), key=int)

# Main execution
def main():
    # 1(a) ESearch
    alz_pmids = esearch_pmids("Alzheimers+AND+2024[pdat]")
    time.sleep(SLEEP)
    can_pmids = esearch_pmids("cancer+AND+2024[pdat]")
    time.sleep(SLEEP)

    # 1(b)+ 1(d) EFetch metadata (batched; handle structured abstracts)
    alz_meta = efetch_metadata(alz_pmids, "Alzheimer")
    can_meta = efetch_metadata(can_pmids, "cancer")

    # Save JSON outputs
    with open("alzheimers_2024_metadata.json", "w", encoding="utf-8") as f:
        json.dump(alz_meta, f, ensure_ascii=False, indent=2)
    with open("cancer_2024_metadata.json", "w", encoding="utf-8") as f:
        json.dump(can_meta, f, ensure_ascii=False, indent=2)

    # 1(c) Overlap
    overlap = compute_overlap(alz_pmids, can_pmids)
    with open("overlap_pmids.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(overlap))
    
    # Summary
    print(f"Alzheimer PMIDs: {len(alz_pmids)}; Cancer PMIDs: {len(can_pmids)}")
    print(f"Metadata: {len(alz_meta)} Alz; {len(can_meta)} Cancer")
    print(f"Overlap PMIDs: {len(overlap)}")

if __name__ == "__main__":
    main()
