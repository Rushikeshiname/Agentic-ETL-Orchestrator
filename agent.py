
import os
import traceback

from openai import OpenAI

from tools import (
    profile_csv,
    run_data_quality_checks
)

from transforms import (
    execute_pyspark_transform
)

from prompts import (
    SYSTEM_PROMPT
)

from audit import (
    generate_audit_report
)

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------------------------------
# GENERATE TRANSFORM
# ---------------------------------------------------

def generate_transform(profile):

    prompt = f"""
You are an expert PySpark ETL engineer.

Dataset Profile:
{profile}

Generate ONLY valid executable PySpark code.

Rules:
1. Return ONLY Python code
2. Function name must be:
   def transform(df):
3. Always return df
4. Handle:
   - null values
   - invalid emails
   - invalid numeric values
   - date standardization
   - uppercase/lowercase cleaning
5. Use pyspark.sql.functions as F
6. Do not include markdown
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    generated_code = (
        response
        .choices[0]
        .message
        .content
    )

    return generated_code

# ---------------------------------------------------
# SELF HEAL CODE
# ---------------------------------------------------

def self_heal_code(
    broken_code,
    error_message
):

    prompt = f"""
The following PySpark code failed.

ERROR:
{error_message}

BROKEN CODE:
{broken_code}

Fix the code.

Rules:
1. Return ONLY valid Python
2. Keep function:
   def transform(df):
3. Return executable PySpark code
4. No markdown
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    fixed_code = (
        response
        .choices[0]
        .message
        .content
    )

    return fixed_code

# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

def run_etl_pipeline(
    source_path
):

    print("\nSTEP 1: Profiling dataset")

    profile = profile_csv(
        source_path
    )

    print(profile)

    print("\nSTEP 2: Generating transform")

    generated_code = generate_transform(
        profile
    )

    print(generated_code)

    retries = 2

    transformed_df = None

    # ---------------------------------------------------
    # EXECUTION LOOP
    # ---------------------------------------------------

    for attempt in range(retries):

        try:

            print(
                f"\nSTEP 3: Running transform attempt {attempt + 1}"
            )

            transformed_df = (
                execute_pyspark_transform(
                    source_path,
                    generated_code
                )
            )

            break

        except Exception as e:

            print("\nTRANSFORM FAILED")

            print(str(e))

            if attempt < retries - 1:

                generated_code = (
                    self_heal_code(
                        generated_code,
                        str(e)
                    )
                )

            else:

                traceback.print_exc()

                return {
                    "status": "failed",
                    "error": "Pipeline failed after retries"
                }

    # ---------------------------------------------------
    # DATA QUALITY CHECKS
    # ---------------------------------------------------

    print("\nSTEP 4: Running DQ checks")

    dq_issues = run_data_quality_checks(
        transformed_df
    )

    if len(dq_issues) > 0:

        print("\nDQ ISSUES FOUND")

        print(dq_issues)

    else:

        print("\nDQ PASSED")

    # ---------------------------------------------------
    # WRITE OUTPUT
    # ---------------------------------------------------

    print("\nSTEP 5: Writing output")

    output_path = (
        "outputs/final_dataset"
    )

    transformed_df.write.mode(
        "overwrite"
    ).parquet(
        output_path
    )

    print(
        f"\nSUCCESS: Written to {output_path}"
    )

    # ---------------------------------------------------
    # GENERATE AUDIT REPORT
    # ---------------------------------------------------

    audit_report = generate_audit_report(
        source_path,
        transformed_df
    )

    print("\nAUDIT REPORT")

    print(audit_report)

    # ---------------------------------------------------
    # RETURN RESPONSE
    # ---------------------------------------------------

    return {

        "status": "success",

        "output_path": output_path,

        "dq_issues": dq_issues,

        "transform_code": generated_code,

        "audit_report": audit_report
    }
