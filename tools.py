import pandas as pd
import json


# ---------------------------------------------------
# CSV PROFILING (Pandas)
# ---------------------------------------------------

def profile_csv(path):

    df = pd.read_csv(path)

    profile = {
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "nulls": df.isnull().sum().to_dict(),
        "sample_rows": df.head(5).to_dict(
            orient="records"
        )
    }

    return profile


# ---------------------------------------------------
# JSON PROFILING
# ---------------------------------------------------

def profile_json(path):

    with open(path, "r") as f:
        data = json.load(f)

    sample = data[:5] if isinstance(data, list) else [data]

    return {
        "sample": sample,
        "keys": list(sample[0].keys()) if sample else []
    }


# ---------------------------------------------------
# AUTO PROFILE DETECTION
# ---------------------------------------------------

def profile_dataset(path):

    if path.endswith(".csv"):
        return profile_csv(path)

    elif path.endswith(".json"):
        return profile_json(path)

    else:
        raise Exception(
            "Unsupported dataset format"
        )


# ---------------------------------------------------
# DATA QUALITY CHECKS (SPARK SAFE VERSION)
# ---------------------------------------------------

def run_data_quality_checks(df):

    issues = []

    # ---------------------------
    # 1. Null / empty check (Spark-safe)
    # ---------------------------
    try:
        if df is None:
            return ["DataFrame is None"]

        if df.count() == 0:
            return ["Dataset is empty"]

    except Exception as e:
        return [f"Failed to compute row count: {str(e)}"]

    # ---------------------------
    # 2. Missing value checks
    # ---------------------------
    try:
        for col in df.columns:
            null_count = df.filter(df[col].isNull()).count()

            if null_count > 0:
                issues.append(
                    f"{col}: {null_count} missing values"
                )

    except Exception as e:
        issues.append(
            f"Null check failed: {str(e)}"
        )

    # ---------------------------
    # 3. Duplicate rows check (Spark-safe)
    # ---------------------------
    try:
        total_rows = df.count()
        distinct_rows = df.dropDuplicates().count()

        duplicates = total_rows - distinct_rows

        if duplicates > 0:
            issues.append(
                f"{duplicates} duplicate rows found"
            )

    except Exception as e:
        issues.append(
            f"Duplicate check failed: {str(e)}"
        )

    # ---------------------------
    # 4. Schema check
    # ---------------------------
    if len(df.columns) == 0:
        issues.append("No columns found in dataset")

    # ---------------------------
    # Final output
    # ---------------------------
    return issues