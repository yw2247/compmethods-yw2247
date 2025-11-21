from flask import Flask, render_template, request, jsonify
import pandas as pd
import math

app = Flask(__name__)
hrrp = pd.read_csv("hrrp_data.csv")
hrrp.columns = [c.strip() for c in hrrp.columns]

@app.route("/")
def index():
    """Show the input form."""
    return render_template("index.html")


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
    predicted = row.get("Predicted Readmission", float("nan"))
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


# Extra credit: simple JSON API endpoint
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
    predicted = row.get("Predicted Readmission", None)
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


if __name__ == "__main__":
    app.run(debug=True)
