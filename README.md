# MediBench: Healthcare Data Analytics & AI Benchmark Evaluation System

[![MediBench CI/CD Pipeline](https://github.com/medibench/medibench/actions/workflows/ci.yml/badge.svg)](https://github.com/medibench/medibench/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL%20%7C%20SQLite-336791.svg)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/Tests-25%20Passed-brightgreen.svg)](tests/)

MediBench is a production-grade healthcare analytics platform and AI benchmark evaluation system. Built upon **101,766 real hospital encounters** from 130 US hospitals (1999–2008), MediBench produces complex analytical queries, verifies reference ground truths deterministically using Python and SQL, and assesses how accurately AI models solve real-world clinical and operational reasoning challenges.

---

## Table of Contents
1. [Project Overview & Problem Statement](#project-overview--problem-statement)
2. [Dataset Details & Profiling](#dataset-details--profiling)
3. [System Architecture](#system-architecture)
4. [Technology Stack](#technology-stack)
5. [Core Analytics Engine](#core-analytics-engine)
6. [Benchmark Suite & The Three Advanced Habits](#benchmark-suite--the-three-advanced-habits)
7. [AI Evaluation & Scoring Engine](#ai-evaluation--scoring-engine)
8. [Installation & Quickstart](#installation--quickstart)
9. [FastAPI Endpoints](#fastapi-endpoints)
10. [Streamlit Interactive Dashboard](#streamlit-interactive-dashboard)
11. [Testing & Quality Assurance](#testing--quality-assurance)
12. [Results, Governance & Limitations](#results-governance--limitations)

---

## 1. Project Overview & Problem Statement

Large Language Models (LLMs) frequently hallucinate or fail subtle multi-condition constraints when presented with complex clinical analytics tasks. While AI models can write generic SQL, healthcare data involves:
- **Confounding by indication** (e.g., changing medications associates with higher readmission because sicker patients receive adjustments).
- **Severe data sparsity** (e.g., patient weight missing in >95% of encounters).
- **Unit of analysis confusion** (encounter-level vs. patient-level metrics).
- **Operational trade-offs** (cost per prevented readmission vs. length-of-stay reduction).

**MediBench** solves this by establishing **60 verified benchmark questions** across six categories with deterministic ground-truth answers computed directly from the underlying database, paired with a multi-metric scoring engine.

---

## 2. Dataset Details & Profiling

- **Source**: UCI Machine Learning Repository — *Diabetes 130-US Hospitals (1999–2008)*
- **Records**: 101,766 hospital encounters
- **Patients**: 71,518 unique individuals
- **Features**: 47 original attributes (demographics, admission details, diagnoses, 23 medications, readmission outcomes)
- **Primary Target**: 30-Day Hospital Readmission (`readmitted == '<30'`)
- **Raw Checksum (SHA-256)**: `0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97`

Detailed data validation results are documented in [`reports/dataset_quality_report.md`](reports/dataset_quality_report.md).

---

## 3. System Architecture

```text
                  MEDIBENCH
                      |
              Healthcare Dataset (101,766 encounters)
                      |
                Data Ingestion (Clean & Standardize)
                      |
              Data Validation (Checks & Profiling)
                      |
                Database Layer (PostgreSQL / SQLite via SQLAlchemy)
                      |
             Analytics Engine
                /         \
           SQL Queries   Python Analytics (SciPy, Statsmodels, Scikit-learn)
                \         /
              Ground Truth Engine (Deterministic Answers & Hashes)
                      |
             Benchmark Builder (60 Questions across 6 Categories)
                      |
              Benchmark Store (DB Tables: benchmark_questions / answers)
                      |
                AI Evaluator (OpenAI-compatible client + Mock runner)
                      |
              Scoring Engine (Numeric tolerance, Categorical, Rubric)
                      |
              Results Database (evaluation_runs & evaluation_results)
                      |
              FastAPI Backend (REST API on port 8000)
                      |
             Streamlit Dashboard (Interactive multi-page UI on port 8501)
```

---

## 4. Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ | Primary backend execution |
| **Database** | PostgreSQL / SQLite | Encounter storage and relational queries |
| **ORM & Migrations** | SQLAlchemy 2.0, Alembic | Data schema management and migrations |
| **Data Processing** | Pandas, NumPy, PyArrow | Ingestion, ETL, and vector transformations |
| **Statistical Modeling** | SciPy, Statsmodels | Chi-square tests, Wilson CIs, multivariable Logit |
| **Machine Learning** | Scikit-learn | Predictive baselines and metrics |
| **API Backend** | FastAPI, Uvicorn | Production REST API with background task queue |
| **AI Evaluation** | OpenAI-compatible API | LLM querying, latency, and token tracking |
| **Dashboard** | Streamlit, Plotly | Multi-page interactive exploratory dashboard |
| **Testing** | Pytest, Pytest-Asyncio | Automated unit, integration, and benchmark tests |
| **Containerization** | Docker, Docker Compose | Multi-container deployment |
| **CI/CD** | GitHub Actions | Automated linting, test execution, and validation |

---

## 5. Core Analytics Engine

The analytics engine is divided into five modular components:
1. **Module A (Demographics)**: Age, gender, and racial encounter distributions and length-of-stay metrics.
2. **Module B (Readmission)**: Overall 30-day baseline (11.16%), readmission by admission type, stay duration, and ICD-9 primary diagnosis categories.
3. **Module C (Treatment)**: 23 diabetes medications tracked (insulin prescribed in >50% of encounters, followed by metformin at 19.6%), medication changes, and lab procedures.
4. **Module D (Statistical Analysis)**:
   - 95% Wilson Confidence Interval for 30-day readmissions: `[10.97%, 11.36%]`.
   - Chi-square test of independence: Medication change vs. readmission ($\chi^2 = 72.82$, $p = 1.42 \times 10^{-17}$).
   - Two-sample group comparisons on stay duration: Readmitted ($4.77$ days) vs. non-readmitted ($4.35$ days), $t = 12.06$, $p < 10^{-32}$.
   - Multivariable Logistic Regression: Quantifies Odds Ratios for prior inpatient stays ($OR = 1.35$), stay length ($OR = 1.03$), and medication changes.
5. **Module E (Advanced SQL)**: 20 verified SQL queries located in `sql/` utilizing CTEs, window functions (`ROW_NUMBER()`, `NTILE()`, `DENSE_RANK()`), and conditional aggregation.

Comprehensive analytical findings are compiled in [`reports/analytics_report.md`](reports/analytics_report.md).

---

## 6. Benchmark Suite & The Three Advanced Habits

MediBench includes **60 verified benchmark questions** categorized as:
- **SQL Analytics** (15 Questions: `MED-001` – `MED-015`)
- **Statistical Reasoning** (10 Questions: `MED-016` – `MED-025`)
- **Data Interpretation** (10 Questions: `MED-026` – `MED-035`)
- **Data Quality & Governance** (10 Questions: `MED-036` – `MED-045`)
- **Business Decision-Making** (10 Questions: `MED-046` – `MED-055`)
- **Contradictory Evidence & Trade-offs** (5 Questions: `MED-056` – `MED-060`)

### The Three Advanced Habits:
1. **Retired Question Registry**: Questions retired due to domain expert review or data limitations (e.g., patient weight dropped due to >95% sparsity, facility IDs omitted due to de-identification).
2. **Freshness-Aware Benchmarking**: Classifies questions into `static`, `slowly_changing`, and `live_dependent` to test AI temporal reasoning.
3. **Contradictory Dataset Evaluation**: Matched operational trade-offs testing whether models discern confounding by indication and evaluate intervention efficiency ($ per readmission prevented).

Full benchmark quality metrics are in [`reports/benchmark_quality_report.md`](reports/benchmark_quality_report.md).

---

## 7. AI Evaluation & Scoring Engine

The evaluator runs benchmark queries against target AI models using:
- **Numeric Tolerance**: Relative or absolute tolerance matching ($|pred - exp| \le \text{tol} \times \max(|exp|, 1.0)$).
- **Categorical Matching**: Exact entity verification.
- **Structured Rubric**: Evaluates multi-concept explanations and confounding flags.

### Benchmark Evaluation Summary:
- **Run `RUN-001` (MediBench-Clinical-LLM)**: **92.5% score**, 56/60 passed, avg latency 30 ms.
- **Run `RUN-002` (General-Baseline-LLM)**: **74.17% score**, 45/60 passed, avg latency 29 ms.

Artifacts: [`reports/evaluation_results.json`](reports/evaluation_results.json) and [`reports/model_comparison.md`](reports/model_comparison.md).

---

## 8. Installation & Quickstart

### Prerequisites
- Python 3.11+
- Virtual environment or Docker

### Local Setup
```bash
# 1. Clone repository
git clone https://github.com/medibench/medibench.git
cd medibench

# 2. Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Copy environment configuration
cp .env.example .env

# 5. Run Database Migrations
alembic upgrade head

# 6. Run Data Ingestion & Benchmark Generation
python -m medibench.ingestion.pipeline
python -m medibench.benchmarks.generator
```

### Docker Compose
To run PostgreSQL, FastAPI, and Streamlit in containers:
```bash
docker compose up -d --build
```

---

## 9. FastAPI Endpoints

Launch API server:
```bash
uvicorn medibench.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

Key Endpoints:
- `GET /health`: System & database health status
- `GET /api/analytics/overview`: Encounter summary KPIs
- `GET /api/analytics/readmissions`: Readmission analysis breakdown
- `GET /api/benchmarks`: List 60 benchmark questions (with filters)
- `GET /api/benchmarks/{id}`: Detailed benchmark question with verified answer
- `GET /api/benchmarks/retired`: View Retired Question Registry
- `POST /api/evaluations`: Start background AI model evaluation
- `GET /api/evaluations/{id}/results`: Model answers and evaluation scores
- `GET /api/reports/summary`: Executive performance summary

---

## 10. Streamlit Interactive Dashboard

Launch the interactive UI:
```bash
streamlit run dashboard/app.py
```
Open `http://localhost:8501` to explore:
1. **Healthcare Overview**: Demographics, age, gender, race distributions.
2. **Advanced Analytics**: Readmission trends, ICD-9 diagnoses, and statistical regression tables.
3. **Benchmark Explorer**: Interactive question inspector and retired registry.
4. **AI Evaluation**: Real-time evaluation runs, error classifications, and latency metrics.

---

## 11. Testing & Quality Assurance

Run the comprehensive test suite:
```bash
pytest tests/ -v
```
All **25 tests pass**:
- `test_database.py`: Connection and table schema integrity
- `test_ingestion.py`: CSV download and cleaning transformations
- `test_validation.py`: Data profiler and quality rules
- `test_analytics.py`: Demographics, readmissions, treatment, and statistical models
- `test_benchmarks.py`: 60 questions verification and registry validation
- `test_scoring.py`: Scoring algorithms and failure classifications
- `test_api.py`: FastAPI routes and responses

---

## 12. Results, Governance & Limitations

### Results Summary
- Ingested and accounted for all **101,766 hospital encounters**.
- Formulated **20 advanced SQL analytical queries** using window functions and CTEs.
- Created and validated **60 benchmark questions** with 100% deterministic ground truth.
- Validated end-to-end AI evaluation pipeline across multiple model baselines.

### Limitations & Governance Note
This platform analyzes historical encounter-level data (1999–2008). Findings represent statistical associations within this retrospective observational cohort and do not establish direct medical causality. Operational exercises are designed for healthcare informatics benchmarks, not individual patient medical guidance.
