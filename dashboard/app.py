import streamlit as st

st.set_page_config(
    page_title="MediBench | Healthcare Analytics & AI Benchmark",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏥 MediBench: Healthcare Analytics & AI Benchmark System")
st.markdown("""
### Welcome to MediBench
MediBench is an enterprise healthcare data analytics platform and clinical AI benchmark evaluation suite built on **101,766 real hospital encounters** (Diabetes 130-US Hospitals Dataset, 1999–2008).

---

#### System Architecture & Core Capabilities
1. **Data Ingestion & Quality Engine**: 101,766 encounters accounted for with strict schema verification and missingness profiling.
2. **Healthcare Analytics Engine**: 5 production analytical modules (Demographics, Readmission, Treatment, Statistical Models, 20 Advanced SQL queries).
3. **Verified Benchmark Suite**: 60 multi-category evaluation questions with 100% deterministic ground truth.
4. **Three Advanced Benchmark Habits**:
   - **Retired Question Registry**: Documents deprecated questions with domain expert review rationale.
   - **Freshness-Aware Benchmarking**: Classifies questions into temporal categories and tests temporal snapshot reasoning.
   - **Contradictory Dataset Evaluation**: Matched operational trade-offs testing model discernment under competing constraints.
5. **AI Model Evaluator**: Multi-method evaluation (numeric tolerance, SQL result match, structured rubrics) with latency and token metrics.

---
👈 **Use the sidebar navigation to explore the 4 dashboard modules:**
- **1. Healthcare Overview**: High-level KPIs, demographics, and encounter distributions.
- **2. Advanced Analytics**: Deep clinical associations, ICD-9 diagnoses, and statistical tests.
- **3. Benchmark Explorer**: Detailed inspector for all 60 benchmark questions and retired registry.
- **4. AI Evaluations**: Model performance comparisons, error categorizations, and interactive evaluation runs.
""")

st.sidebar.success("MediBench System Active | 101,766 Encounters Loaded")
st.sidebar.markdown("""
---
**Technical Stack**
- Backend: Python 3.11+, FastAPI, SQLAlchemy
- Storage: PostgreSQL / SQLite
- Analytics: Pandas, NumPy, SciPy, Statsmodels
- Visualization: Streamlit, Plotly
""")
