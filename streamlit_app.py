
import streamlit as st
import pandas as pd
import requests
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Agentic ETL Orchestrator",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("⚡ Agentic ETL Orchestrator")

st.markdown("""
Autonomous AI-powered ETL pipeline using:
- OpenAI GPT-4.1
- PySpark
- FastAPI
- Self-Healing Retry Logic
- Data Quality Validation
- Transformation Audit Reports
""")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header(
    "Pipeline Features"
)

st.sidebar.markdown("""
✅ Schema Profiling  
✅ AI Transform Generation  
✅ PySpark Execution  
✅ DQ Validation  
✅ Self-Healing Retries  
✅ Transformation Auditing  
✅ Parquet Output  
""")

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

# ---------------------------------------------------
# PROCESS FILE
# ---------------------------------------------------

if uploaded_file:

    os.makedirs(
        "sample_data",
        exist_ok=True
    )

    save_path = os.path.join(
        "sample_data",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    # ---------------------------------------------------
    # RAW DATA PREVIEW
    # ---------------------------------------------------

    df = pd.read_csv(save_path)

    st.subheader(
        "Raw Dataset Preview"
    )

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.subheader(
        "Dataset Shape"
    )

    st.write(df.shape)

    st.subheader(
        "Columns"
    )

    st.write(
        list(df.columns)
    )

    # ---------------------------------------------------
    # RUN PIPELINE
    # ---------------------------------------------------

    if st.button(
        "Run Agentic ETL"
    ):

        with st.spinner(
            "Running AI ETL Agent..."
        ):

            try:

                response = requests.post(
                    "http://127.0.0.1:8001/run",
                    json={
                        "source_path": save_path
                    }
                )

                result = response.json()

                # ---------------------------------------------------
                # SUCCESS
                # ---------------------------------------------------

                if (
                    response.status_code == 200
                    and result.get(
                        "pipeline_status"
                    ) == "success"
                ):

                    st.success(
                        "ETL Pipeline Completed"
                    )

                    # ---------------------------------------------------
                    # TOP METRICS
                    # ---------------------------------------------------

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Pipeline Status",
                            result.get(
                                "pipeline_status",
                                "unknown"
                            )
                        )

                    with col2:

                        st.metric(
                            "DQ Status",
                            result.get(
                                "dq_status",
                                "unknown"
                            )
                        )

                    with col3:

                        st.metric(
                            "DQ Issue Count",
                            result.get(
                                "dq_issue_count",
                                0
                            )
                        )

                    # ---------------------------------------------------
                    # OUTPUT PATH
                    # ---------------------------------------------------

                    st.subheader(
                        "Output Path"
                    )

                    st.code(
                        result.get(
                            "output_path",
                            "N/A"
                        )
                    )

                    # ---------------------------------------------------
                    # AUDIT REPORT
                    # ---------------------------------------------------

                    audit = result.get(
                        "audit_report",
                        None
                    )

                    if audit:

                        st.subheader(
                            "Transformation Audit Summary"
                        )

                        # ---------------------------------------------------
                        # ROW COUNTS
                        # ---------------------------------------------------

                        c1, c2 = st.columns(2)

                        with c1:

                            st.metric(
                                "Raw Rows",
                                audit.get(
                                    "raw_row_count",
                                    0
                                )
                            )

                        with c2:

                            st.metric(
                                "Transformed Rows",
                                audit.get(
                                    "transformed_row_count",
                                    0
                                )
                            )

                        # ---------------------------------------------------
                        # NULL FIXES
                        # ---------------------------------------------------

                        st.subheader(
                            "Null Value Fixes"
                        )

                        null_rows = []

                        for col, values in (
                            audit.get(
                                "null_changes",
                                {}
                            ).items()
                        ):

                            before = values.get(
                                "before",
                                0
                            )

                            after = values.get(
                                "after",
                                0
                            )

                            fixed = (
                                before - after
                            )

                            null_rows.append({
                                "column": col,
                                "nulls_before": before,
                                "nulls_after": after,
                                "fixed": fixed
                            })

                        null_df = pd.DataFrame(
                            null_rows
                        )

                        st.dataframe(
                            null_df,
                            use_container_width=True
                        )

                        # ---------------------------------------------------
                        # SCHEMA CHANGES
                        # ---------------------------------------------------

                        st.subheader(
                            "Schema Changes"
                        )

                        dtype_rows = []

                        for col, values in (
                            audit.get(
                                "dtype_changes",
                                {}
                            ).items()
                        ):

                            dtype_rows.append({
                                "column": col,
                                "before": values.get(
                                    "before",
                                    ""
                                ),
                                "after": values.get(
                                    "after",
                                    ""
                                )
                            })

                        dtype_df = pd.DataFrame(
                            dtype_rows
                        )

                        st.dataframe(
                            dtype_df,
                            use_container_width=True
                        )

                        # ---------------------------------------------------
                        # TRANSFORMED DATASET
                        # ---------------------------------------------------

                        st.subheader(
                            "Transformed Dataset Preview"
                        )

                        sample_df = pd.DataFrame(
                            audit.get(
                                "transformed_sample",
                                []
                            )
                        )

                        st.dataframe(
                            sample_df,
                            use_container_width=True
                        )

                    else:

                        st.warning(
                            "No audit report generated."
                        )

                    # ---------------------------------------------------
                    # GENERATED CODE
                    # ---------------------------------------------------

                    with st.expander(
                        "Generated PySpark Code"
                    ):

                        st.code(
                            result.get(
                                "generated_transform_preview",
                                ""
                            ),
                            language="python"
                        )

                    # ---------------------------------------------------
                    # FULL RESPONSE
                    # ---------------------------------------------------

                    with st.expander(
                        "Full API Response"
                    ):

                        st.json(result)

                # ---------------------------------------------------
                # FAILURE
                # ---------------------------------------------------

                else:

                    st.error(
                        "Pipeline Failed"
                    )

                    st.code(
                        result.get(
                            "error",
                            "Unknown Error"
                        )
                    )

                    with st.expander(
                        "Full Failure Response"
                    ):

                        st.json(result)

            except Exception as e:

                st.error(
                    "Application Error"
                )

                st.code(str(e))

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Built with OpenAI + PySpark + FastAPI + Streamlit"
)
