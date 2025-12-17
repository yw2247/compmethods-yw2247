import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("hrrp_clean.csv")

df["Excess Readmission Ratio"] = pd.to_numeric(
    df["Excess Readmission Ratio"], errors="coerce"
)
err = df["Excess Readmission Ratio"].dropna()

#ERR Distribution Histogram
plt.figure(figsize=(8, 5))
plt.hist(err, bins=30, edgecolor="black")
plt.xlabel("Excess Readmission Ratio (ERR)")
plt.ylabel("Number of hospital–measure records")
plt.title("Distribution of Excess Readmission Ratio (ERR)")
plt.axvline(err.mean(), linestyle="--", linewidth=1.5, label=f"Mean = {err.mean():.3f}")
plt.legend()
plt.tight_layout()

plt.savefig("err_histogram.png", dpi=300)
plt.show()

# Boxplot of ERR by Disease Category
# Ensure numeric ERR
df["Excess Readmission Ratio"] = pd.to_numeric(
    df["Excess Readmission Ratio"], errors="coerce"
)
df = df.dropna(subset=["Excess Readmission Ratio"])

# Map measure codes to disease names (same mapping you used in server.py)
MEASURE_NAMES = {
    "READM-30-AMI-HRRP": "Heart Attack (AMI)",
    "READM-30-HF-HRRP": "Heart Failure (HF)",
    "READM-30-PN-HRRP": "Pneumonia (PN)",
    "READM-30-COPD-HRRP": "COPD",
    "READM-30-CABG-HRRP": "CABG Surgery",
    "READM-30-HIP-KNEE-HRRP": "Hip/Knee Replacement",
}

df["Disease"] = df["Measure Name"].map(MEASURE_NAMES)
df = df.dropna(subset=["Disease"])

disease_order = [
    "Heart Attack (AMI)",
    "Heart Failure (HF)",
    "Pneumonia (PN)",
    "COPD",
    "CABG Surgery",
    "Hip/Knee Replacement",
]
df["Disease"] = pd.Categorical(df["Disease"], categories=disease_order, ordered=True)

data_to_plot = [
    df.loc[df["Disease"] == d, "Excess Readmission Ratio"].values
    for d in disease_order
]

plt.figure(figsize=(9, 5))
plt.boxplot(data_to_plot, labels=disease_order, showfliers=True)
plt.xticks(rotation=20, ha="right")
plt.ylabel("Excess Readmission Ratio (ERR)")
plt.title("ERR by Disease Category")
plt.tight_layout()

plt.savefig("err_boxplot_by_disease.png", dpi=300)
plt.show()