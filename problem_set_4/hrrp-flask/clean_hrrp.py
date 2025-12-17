import pandas as pd
df = pd.read_csv("hrrp_data.csv")

# Strip whitespace from column names
df.columns = [c.strip() for c in df.columns]

# Convert date columns 
for col in ["Start Date", "End Date"]:
    df[col] = pd.to_datetime(df[col], format="%m/%d/%Y", errors="coerce")

# Clean numeric columns
# These are stored as strings like "N/A" or "Too Few to Report"
numeric_cols = [
    "Number of Discharges",
    "Excess Readmission Ratio",
    "Predicted Readmission Rate",
    "Expected Readmission Rate",
    "Number of Readmissions",
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop rows where all key readmission metrics are missing
df = df.dropna(
    subset=["Excess Readmission Ratio", "Predicted Readmission Rate", "Expected Readmission Rate"],
    how="all"
)

df.to_csv("hrrp_clean.csv", index=False)
