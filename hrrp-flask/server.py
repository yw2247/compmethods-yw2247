from flask import Flask, render_template, request, jsonify
import pandas as pd
import math

app = Flask(__name__)
hrrp = pd.read_csv("hrrp_clean.csv")
hrrp.columns = [c.strip() for c in hrrp.columns]  

MEASURE_NAMES = {
    "READM-30-AMI-HRRP": "Heart Attack (AMI)",
    "READM-30-HF-HRRP": "Heart Failure (HF)",
    "READM-30-PN-HRRP": "Pneumonia (PN)",
    "READM-30-COPD-HRRP": "Chronic Obstructive Pulmonary Disease (COPD)",
    "READM-30-CABG-HRRP": "Coronary Artery Bypass Graft (CABG)",
    "READM-30-HIP-KNEE-HRRP": "Hip/Knee Replacement",
}

@app.route("/")
def index():
    hospitals = sorted(hrrp["Facility Name"].dropna().unique())
    return render_template("index.html", measures=MEASURE_NAMES, hospitals=hospitals)


@app.route("/lookup", methods=["POST"])
def lookup():
    """Handle form submission, look up hospital + measure, and show result page."""
    hospital = request.form.get("hospital", "").strip()
    measure = request.form.get("measure", "").strip()

    # Basic error handling: empty input
    if not hospital or not measure:
        error_message = "Please enter both a hospital name and a measure name."
        return render_template("result.html", error=error_message)

    # Case-insensitive matching on Facility Name and Measure Name
    df = hrrp.copy()
    df["Facility_lower"] = df["Facility Name"].str.strip().str.lower()
    df["Measure_lower"] = df["Measure Name"].str.strip().str.lower()

    mask = (
        (df["Facility_lower"] == hospital.lower())
        & (df["Measure_lower"] == measure.lower())
    )
    subset = df[mask]

    # Error handling: no matching rows
    if subset.empty:
        error_message = (
            f"No data found for hospital '{hospital}' "
            f"with measure '{measure}'."
        )
        return render_template("result.html", error=error_message)

    # If multiple rows match, just take the first one
    row = subset.iloc[0]

    # Pull out numeric fields (handle N/A)
    err = row.get("Excess Readmission Ratio", float("nan"))
    predicted = row.get("Predicted Readmission Rate", float("nan"))
    expected = row.get("Expected Readmission Rate", float("nan"))


    # Interpretation of ERR
    interpretation = "No Excess Readmission Ratio available."
    err_display = "N/A"
    if not (isinstance(err, str)) and not math.isnan(err):
        err_display = f"{err:.3f}"
        if err < 0.98:
            interpretation = "better than the national average."
        elif err > 1.02:
            interpretation = "worse than the national average."
        else:
            interpretation = "about the same as the national average."

    summary_text = (
        f"For {measure}, {hospital} has an Excess Readmission Ratio of "
        f"{err_display}, which is {interpretation}"
    )

    # Prepare extra fields for multiple analyses
    predicted_display = (
        f"{predicted:.4f}" if isinstance(predicted, (int, float)) and not math.isnan(predicted)
        else "N/A"
    )
    expected_display = (
        f"{expected:.4f}" if isinstance(expected, (int, float)) and not math.isnan(expected)
        else "N/A"
    )

    return render_template(
        "result.html",
        error=None,
        hospital=hospital,
        measure=measure,
        err=err_display,
        summary=summary_text,
        predicted=predicted_display,
        expected=expected_display,
    )


@app.route("/api/hrrp")
def api_hrrp():
    """
    Simple API: /api/hrrp?hospital=...&measure=...
    Returns ERR, predicted, expected as JSON.
    """
    hospital = request.args.get("hospital", "").strip()
    measure = request.args.get("measure", "").strip()

    if not hospital or not measure:
        return jsonify(
            {"error": "Please provide both 'hospital' and 'measure' query parameters."}
        ), 400

    df = hrrp.copy()
    df["Facility_lower"] = df["Facility Name"].str.strip().str.lower()
    df["Measure_lower"] = df["Measure Name"].str.strip().str.lower()

    mask = (
        (df["Facility_lower"] == hospital.lower())
        & (df["Measure_lower"] == measure.lower())
    )
    subset = df[mask]

    if subset.empty:
        return jsonify(
            {"error": f"No data for hospital '{hospital}' and measure '{measure}'."}
        ), 404

    row = subset.iloc[0]
    err = row.get("Excess Readmission Ratio", None)
    predicted = row.get("Predicted Readmission Rate", None)
    expected = row.get("Expected Readmission Rate", None)


    return jsonify(
        {
            "hospital": hospital,
            "measure": measure,
            "excess_readmission_ratio": None if pd.isna(err) else float(err),
            "predicted_readmission": None if pd.isna(predicted) else float(predicted),
            "expected_readmission_rate": None if pd.isna(expected) else float(expected),
        }
    )


@app.route("/api/summary")
def api_summary():
    """
    Example:
        /api/summary
        /api/summary?measure=READM-30-HF-HRRP

    Returns summary statistics for Excess Readmission Ratio,
    Predicted Readmission Rate, and Expected Readmission Rate.
    """
    measure = request.args.get("measure", "").strip()

    df = hrrp.copy()
    # Keep only rows with numeric ERR values
    df = df[pd.notna(df["Excess Readmission Ratio"])]

    if measure:
        df = df[df["Measure Name"].str.strip().str.lower() == measure.lower()]

    if df.empty:
        return jsonify(
            {"error": "No data found for the given filter."}
        ), 404

    def summarize(col):
        s = df[col].describe()
        # describe() gives count, mean, std, min, 25%, 50%, 75%, max
        return {
            "count": int(s["count"]),
            "mean": float(s["mean"]),
            "std": float(s["std"]) if not math.isnan(s["std"]) else None,
            "min": float(s["min"]),
            "q1": float(s["25%"]),
            "median": float(s["50%"]),
            "q3": float(s["75%"]),
            "max": float(s["max"]),
        }

    result = {
        "measure": measure if measure else "ALL",
        "n_rows": len(df),
        "err_summary": summarize("Excess Readmission Ratio"),
    }

    # Only add predicted/expected if present and not all NaN
    if "Predicted Readmission Rate" in df.columns and df["Predicted Readmission Rate"].notna().any():
        result["predicted_summary"] = summarize("Predicted Readmission Rate")

    if "Expected Readmission Rate" in df.columns and df["Expected Readmission Rate"].notna().any():
        result["expected_summary"] = summarize("Expected Readmission Rate")

    return jsonify(result)


@app.route("/api/by_state")
def api_by_state():
    """
    Example:
        /api/by_state?measure=READM-30-HF-HRRP

    Returns mean Excess Readmission Ratio by state for a given measure.
    """
    measure = request.args.get("measure", "").strip()

    df = hrrp.copy()
    df = df[pd.notna(df["Excess Readmission Ratio"])]

    if measure:
        df = df[df["Measure Name"].str.strip().str.lower() == measure.lower()]

    if df.empty:
        return jsonify(
            {"error": "No data found for the given filter."}
        ), 404

    grouped = (
        df.groupby("State", as_index=False)
          .agg(
              mean_err=("Excess Readmission Ratio", "mean"),
              n_rows=("Excess Readmission Ratio", "size"),
              n_hospitals=("Facility ID", "nunique")
          )
    )

    # Convert to list of dicts for JSON
    states = []
    for _, row in grouped.iterrows():
        states.append(
            {
                "state": row["State"],
                "mean_err": float(row["mean_err"]),
                "n_rows": int(row["n_rows"]),
                "n_hospitals": int(row["n_hospitals"]),
            }
        )

    return jsonify(
        {
            "measure": measure if measure else "ALL",
            "n_states": len(states),
            "by_state": states,
        }
    )

@app.route("/api/top_hospitals")
def api_top_hospitals():
    """
    Example:
        /api/top_hospitals?measure=READM-30-HF-HRRP&n=10&direction=high

    Parameters:
        measure   (optional): filter by measure name
        n         (optional): number of hospitals (default 10)
        direction (optional): 'high' for worst (high ERR),
                              'low' for best (low ERR)
    """
    measure = request.args.get("measure", "").strip()
    n_str = request.args.get("n", "10").strip()
    direction = request.args.get("direction", "high").strip().lower()

    try:
        n = int(n_str)
        if n <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "'n' must be a positive integer."}), 400

    if direction not in ("high", "low"):
        return jsonify(
            {"error": "direction must be 'high' or 'low'."}
        ), 400

    df = hrrp.copy()
    df = df[pd.notna(df["Excess Readmission Ratio"])]

    if measure:
        df = df[df["Measure Name"].str.strip().str.lower() == measure.lower()]

    if df.empty:
        return jsonify(
            {"error": "No data found for the given filter."}
        ), 404

    ascending = True if direction == "low" else False
    df_sorted = df.sort_values("Excess Readmission Ratio", ascending=ascending)

    top_df = df_sorted.head(n)

    hospitals = []
    for _, row in top_df.iterrows():
        hospitals.append(
            {
                "facility_name": row["Facility Name"],
                "facility_id": str(row["Facility ID"]),
                "state": row["State"],
                "measure": row["Measure Name"],
                "excess_readmission_ratio": float(row["Excess Readmission Ratio"]),
                "predicted_readmission_rate": (
                    None
                    if pd.isna(row.get("Predicted Readmission Rate", None))
                    else float(row["Predicted Readmission Rate"])
                ),
                "expected_readmission_rate": (
                    None
                    if pd.isna(row.get("Expected Readmission Rate", None))
                    else float(row["Expected Readmission Rate"])
                ),
                "number_of_discharges": (
                    None
                    if pd.isna(row.get("Number of Discharges", None))
                    else int(row["Number of Discharges"])
                ),
                "number_of_readmissions": (
                    None
                    if pd.isna(row.get("Number of Readmissions", None))
                    else int(row["Number of Readmissions"])
                ),
            }
        )

    return jsonify(
        {
            "measure": measure if measure else "ALL",
            "direction": direction,
            "n_returned": len(hospitals),
            "hospitals": hospitals,
        }
    )
    
@app.route("/api/volume_vs_err")
def api_volume_vs_err():
    """
    Returns points for plotting hospital volume (number of discharges)
    vs Excess Readmission Ratio (ERR).

    Example:
        /api/volume_vs_err
        /api/volume_vs_err?measure=READM-30-HF-HRRP
    """
    measure = request.args.get("measure", "").strip().lower()

    df = hrrp.copy()

    # Keep rows with valid ERR and discharge counts
    df = df[
        df["Excess Readmission Ratio"].notna() &
        df["Number of Discharges"].notna() &
        (df["Number of Discharges"] > 0) &
        df["Measure Name"].notna()
    ]

    # Filter if measure provided
    if measure:
        df = df[df["Measure Name"].str.strip().str.lower() == measure]

    if df.empty:
        return jsonify({
            "points": [],
            "message": "No data available for the given filter."
        })

    points = []
    for _, row in df.iterrows():
        measure_code = row["Measure Name"]
        measure_label = MEASURE_NAMES.get(measure_code, measure_code)

        points.append({
            "x": float(row["Number of Discharges"]),
            "y": float(row["Excess Readmission Ratio"]),
            "measure": measure_code,
            "measure_label": measure_label,
            "hospital": row["Facility Name"],
            "state": row["State"]
        })

    return jsonify({"points": points})



if __name__ == "__main__":
    app.run(debug=True)
