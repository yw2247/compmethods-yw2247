#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np
import pandas as pd
import tqdm
import matplotlib.pyplot as plt

import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.decomposition import PCA

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
model = AutoModel.from_pretrained('allenai/specter')

# load papers from Exercise 1 outputs
ALZ_JSON = Path("alzheimers_2024_metadata.json")
CAN_JSON = Path("cancer_2024_metadata.json")

with ALZ_JSON.open("r", encoding="utf-8") as f:
    alz_meta = json.load(f)
with CAN_JSON.open("r", encoding="utf-8") as f:
    can_meta = json.load(f)

# merge into one dict; keep order stable by sorting PMIDs numerically
def sort_by_pmid(d):
    def _k(x):
        try:
            return int(x)
        except:
            return x
    return dict(sorted(d.items(), key=lambda kv: _k(kv[0])))

alz_meta = sort_by_pmid(alz_meta)
can_meta = sort_by_pmid(can_meta)

papers = {}
papers.update(alz_meta)
papers.update(can_meta)

print(f"Total papers loaded: {len(papers)}  (Alz: {len(alz_meta)}, Cancer: {len(can_meta)})")

# get_abstract 
def get_abstract(paper: dict) -> str:
    txt = paper.get("AbstractText", "")
    if txt is None:
        return ""
    if isinstance(txt, list):
        return " ".join([t for t in txt if t])
    return str(txt)

# compute embeddings
pmids_in_order = list(papers.keys())
embeddings = []

for pmid in tqdm.tqdm(pmids_in_order, desc="Embedding papers"):
    paper = papers[pmid]
    text = (paper.get("ArticleTitle", "") or "") + tokenizer.sep_token + get_abstract(paper)

    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
        vec = outputs.last_hidden_state[:, 0, :].cpu().numpy()[0]  
        embeddings.append(vec)

embeddings = np.vstack(embeddings)  

# PCA to 3 components 
pca = PCA(n_components=3, random_state=0)
emb3 = pca.fit_transform(embeddings)

# build a dataframe with labels for plotting
labels = [papers[pmid].get("query", "") for pmid in pmids_in_order]
df = pd.DataFrame(emb3, columns=["PC0", "PC1", "PC2"])
df["query"] = labels

print("Explained variance ratios:", pca.explained_variance_ratio_)

# 2D scatter plots
pairs = [("PC0", "PC1"), ("PC0", "PC2"), ("PC1", "PC2")]
for x, y in pairs:
    plt.figure()
    for label in sorted(set(labels)):
        subset = df[df["query"] == label]
        plt.scatter(subset[x], subset[y], label=label, alpha=0.7)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    plt.title(f"{x} vs {y} (SPECTER embeddings, PCA)")
    plt.tight_layout()
    plt.show()

