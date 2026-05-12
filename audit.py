
import pandas as pd


def generate_audit_report(
    raw_path,
    transformed_df
):

    raw_df = pd.read_csv(
        raw_path
    )

    transformed_pd = (
        transformed_df.toPandas()
    )

    report = {}

    # ---------------------------------------------------
    # ROW COUNTS
    # ---------------------------------------------------

    report["raw_row_count"] = len(
        raw_df
    )

    report["transformed_row_count"] = len(
        transformed_pd
    )

    # ---------------------------------------------------
    # NULL CHANGES
    # ---------------------------------------------------

    raw_nulls = (
        raw_df.isnull().sum().to_dict()
    )

    transformed_nulls = (
        transformed_pd
        .isnull()
        .sum()
        .to_dict()
    )

    report["null_changes"] = {}

    for col in raw_nulls:

        report["null_changes"][col] = {
            "before": int(
                raw_nulls[col]
            ),
            "after": int(
                transformed_nulls.get(
                    col,
                    0
                )
            )
        }

    # ---------------------------------------------------
    # DTYPE CHANGES
    # ---------------------------------------------------

    report["dtype_changes"] = {}

    for col in raw_df.columns:

        report["dtype_changes"][col] = {
            "before": str(
                raw_df[col].dtype
            ),
            "after": str(
                transformed_pd[col].dtype
            )
        }

    # ---------------------------------------------------
    # SAMPLE OUTPUT
    # ---------------------------------------------------

    report["transformed_sample"] = (
        transformed_pd
        .head(5)
        .to_dict(
            orient="records"
        )
    )

    return report
