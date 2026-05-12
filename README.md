# ⚡ Agentic ETL Orchestrator

An autonomous AI-powered ETL platform that profiles raw datasets, generates PySpark transformations using OpenAI, executes transformations, validates data quality, self-heals failed pipelines, and produces audit summaries — all with minimal human intervention.

---

# 🚀 Features

* ✅ Autonomous schema profiling
* ✅ AI-generated PySpark transformations
* ✅ Self-healing retry mechanism
* ✅ Automated data quality checks
* ✅ Transformation audit reporting
* ✅ FastAPI backend orchestration
* ✅ Streamlit UI dashboard
* ✅ OpenAI-powered code generation
* ✅ Parquet output generation
* ✅ End-to-end ETL observability

---

# 🏗️ Architecture

```text
CSV / Raw Data
       ↓
Dataset Profiling
       ↓
OpenAI Generates PySpark Transform
       ↓
PySpark Execution
       ↓
Data Quality Validation
       ↓
Self-Healing Retries (if failure)
       ↓
Audit Report Generation
       ↓
Parquet Output + Streamlit Dashboard
```

---

# 📂 Project Structure

```text
ETL/
│
├── app.py                  # FastAPI backend
├── agent.py                # AI orchestration logic
├── transforms.py           # PySpark execution engine
├── tools.py                # Profiling + DQ checks
├── audit.py                # Audit report generation
├── prompts.py              # LLM system prompts
├── streamlit_app.py        # Streamlit UI
│
├── sample_data/
│   └── orders.csv
│
├── outputs/
│   └── final_dataset/
│
├── requirements.txt
└── README.md
```

---

# 🧠 How It Works

## 1. Dataset Profiling

The agent automatically analyzes:

* columns
* datatypes
* null counts
* sample rows

Example:

```python
{
  "columns": ["email", "country"],
  "nulls": {
      "email": 3,
      "country": 2
  }
}
```

---

## 2. AI Transform Generation

Using OpenAI GPT-4.1, the platform generates executable PySpark transformation logic dynamically.

Generated transformations include:

* null handling
* schema standardization
* date normalization
* invalid value cleanup
* email correction
* numeric casting

---

## 3. Self-Healing Retries

If generated PySpark code fails:

```text
name 'upper' is not defined
```

The system:

1. captures the error
2. sends the stacktrace back to the LLM
3. regenerates corrected code
4. retries execution automatically

---

## 4. Data Quality Validation

The platform automatically checks:

* null violations
* invalid records
* schema mismatches
* transformation consistency

---

## 5. Audit Reporting

The platform generates transformation audit summaries including:

* row counts
* null reductions
* datatype changes
* transformed sample rows

Example:

```json
{
  "null_changes": {
    "email": {
      "before": 3,
      "after": 0
    }
  }
}
```

---

# 🖥️ Streamlit Dashboard

The UI provides:

* Raw dataset preview
* Transformation audit summary
* Null fix tracking
* Schema change tracking
* Generated PySpark code
* Pipeline execution status

---

# ⚙️ Tech Stack

* Python
* PySpark
* FastAPI
* Streamlit
* OpenAI API
* Pandas
* OpenTelemetry

---

# 📦 Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/agentic-etl-orchestrator.git

cd agentic-etl-orchestrator
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ☕ Java + PySpark Setup

Install OpenJDK 17.

### Mac (Homebrew)

```bash
brew install openjdk@17
```

Set environment variables:

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17
export PATH=$JAVA_HOME/bin:$PATH
```

Verify:

```bash
java -version
```

---

# 🔑 OpenAI API Setup

Set your API key:

### Mac/Linux

```bash
export OPENAI_API_KEY="your_api_key"
```

### Windows

```bash
set OPENAI_API_KEY=your_api_key
```

---

# ▶️ Run FastAPI Backend

```bash
uvicorn app:app --reload --port 8001
```

API Docs:

```text
http://127.0.0.1:8001/docs
```

---

# ▶️ Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

# 🧪 Test Dataset

Upload:

```text
sample_data/orders.csv
```

The sample dataset intentionally contains:

* null values
* invalid emails
* malformed dates
* datatype inconsistencies
* bad numeric values

to demonstrate autonomous ETL remediation.

---

# 📊 Example Pipeline Output

```json
{
  "pipeline_status": "success",
  "dq_status": "PASSED",
  "output_path": "outputs/final_dataset"
}
```

---



---

# 📜 License

MIT License

---

# 👨‍💻 Author

Rushikesh Iname

Built with ❤️ using OpenAI + PySpark + FastAPI + Streamlit
