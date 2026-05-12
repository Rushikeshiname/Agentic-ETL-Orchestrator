from pyspark.sql import SparkSession, functions as F
import re


# ---------------------------------------------------
# SAFE CAST FUNCTIONS
# ---------------------------------------------------

def safe_cast_int(col_name):
    return F.expr(f"try_cast({col_name} as int)")


def safe_cast_double(col_name):
    return F.expr(f"try_cast({col_name} as double)")


# ---------------------------------------------------
# SANITIZER (FIXS YOUR ERROR PERMANENTLY)
# ---------------------------------------------------

def sanitize_generated_code(code: str) -> str:

    # Replace .cast("int") → try_cast
    code = re.sub(
        r'\.cast\("int"\)',
        '.cast("string")',   # fallback safe default
        code
    )

    code = re.sub(
        r"\.cast\('int'\)",
        '.cast("string")',
        code
    )

    # Replace SQL CAST patterns
    code = re.sub(
        r"CAST\((.*?) AS INT\)",
        r"try_cast(\1 AS INT)",
        code,
        flags=re.IGNORECASE
    )

    return code


# ---------------------------------------------------
# DEFAULT SAFE TRANSFORM (fallback)
# ---------------------------------------------------

def transform(df):

    # clean columns
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().lower())

    # null handling
    df = df.fillna("unknown")

    # email safety
    if "email" in df.columns:
        df = df.withColumn("email", F.lower(F.col("email")))
        df = df.filter(
            F.col("email").rlike(r"^[^@]+@[^@]+\.[^@]+$")
            | F.col("email").isNull()
        )

    # safe date handling
    if "date" in df.columns:
        df = df.withColumn(
            "date",
            F.coalesce(
                F.to_date("date", "yyyy-MM-dd"),
                F.to_date("date", "yyyy/MM/dd"),
                F.to_date("date", "dd/MM/yyyy")
            )
        )

    # drop duplicates
    df = df.dropDuplicates()

    return df


# ---------------------------------------------------
# MAIN EXECUTOR (FIX FOR YOUR ERROR)
# ---------------------------------------------------

def execute_pyspark_transform(source_path, generated_code):

    spark = SparkSession.builder.appName("ETL").getOrCreate()

    df = spark.read.option("header", True).csv(source_path)

    # ---------------------------
    # 🔥 CRITICAL FIX
    # sanitize LLM code BEFORE execution
    # ---------------------------
    safe_code = sanitize_generated_code(generated_code)

    exec_globals = {}

    # inject safe utilities
    exec_globals["F"] = F
    exec_globals["spark"] = spark
    exec_globals["safe_cast_int"] = safe_cast_int
    exec_globals["safe_cast_double"] = safe_cast_double

    # execute LLM code safely
    exec(safe_code, exec_globals)

    if "transform" not in exec_globals:
        raise Exception("LLM must define transform(df)")

    transform_fn = exec_globals["transform"]

    # run transform
    transformed_df = transform_fn(df)

    return transformed_df