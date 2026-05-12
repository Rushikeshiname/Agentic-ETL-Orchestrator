
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent import run_etl_pipeline

# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------

app = FastAPI(
    title="Agentic ETL Orchestrator",
    version="1.0.0"
)

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Agentic ETL Running"
    }

# ---------------------------------------------------
# HEALTH
# ---------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# ---------------------------------------------------
# RUN PIPELINE
# ---------------------------------------------------

@app.post("/run")
def run_pipeline(payload: dict):

    try:

        source_path = payload[
            "source_path"
        ]

        result = run_etl_pipeline(
            source_path
        )

        return {

            "pipeline_status": result[
                "status"
            ],

            "output_path": result[
                "output_path"
            ],

            "dq_status": (
                "PASSED"
                if len(
                    result["dq_issues"]
                ) == 0
                else "FAILED"
            ),

            "dq_issue_count": len(
                result["dq_issues"]
            ),

            "generated_transform_preview":
            result[
                "transform_code"
            ][:500],

            # IMPORTANT
            "audit_report": result[
                "audit_report"
            ]
        }

    except Exception as e:

        return {
            "pipeline_status": "failed",
            "error": str(e)
        }
