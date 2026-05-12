
def run_dq_checks(df):
    issues = []

    total_rows = df.count()

    if total_rows == 0:
        issues.append("Dataset is empty")

    for col in df.columns:
        null_count = df.filter(df[col].isNull()).count()

        if null_count > total_rows * 0.5:
            issues.append(f"Column {col} has >50% nulls")

    return issues