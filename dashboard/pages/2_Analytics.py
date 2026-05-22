import pandas as pd
import plotly.express as px
import streamlit as st

from medibench.analytics.readmission import ReadmissionAnalytics
from medibench.analytics.statistics import StatisticalAnalytics
from medibench.analytics.treatment import TreatmentAnalytics
from medibench.database import SessionLocal

st.set_page_config(page_title="Advanced Analytics | MediBench", page_icon="🔬", layout="wide")

st.title("🔬 Advanced Healthcare Analytics & Statistical Rigor")
st.caption("Investigating Associations, Clinical Modalities, and Predictive Confounders")

db = SessionLocal()
try:
    readm = ReadmissionAnalytics(db)
    treat = TreatmentAnalytics(db)
    stats = StatisticalAnalytics(db)

    tab1, tab2, tab3 = st.tabs(["Readmission Drivers", "Treatment & Diagnostics", "Statistical Rigor"])

    with tab1:
        st.subheader("1. Readmission Rate by Hospital Stay Duration")
        stay_data = readm.get_readmission_by_stay()["data"]
        df_stay = pd.DataFrame(stay_data)

        fig_stay = px.line(
            df_stay,
            x="time_in_hospital",
            y="readmission_rate_pct",
            markers=True,
            title="30-Day Readmission Risk Across Days in Hospital (1 to 14 Days)",
            labels={"time_in_hospital": "Length of Stay (Days)", "readmission_rate_pct": "30-Day Readmission Rate (%)"},
        )
        st.plotly_chart(fig_stay, use_container_width=True)

        st.subheader("2. Readmission by Primary Diagnosis Category (ICD-9)")
        diag_data = readm.get_readmission_by_diagnosis_category()["data"]
        df_diag = pd.DataFrame(diag_data)

        fig_diag = px.bar(
            df_diag,
            x="primary_diagnosis_category",
            y="readmission_rate_pct",
            color="total_encounters",
            title="30-Day Readmission Rate Across Primary Disease Categories",
            labels={"primary_diagnosis_category": "Diagnosis Group", "readmission_rate_pct": "Readmission Rate (%)"},
        )
        st.plotly_chart(fig_diag, use_container_width=True)

    with tab2:
        st.subheader("Medication Change vs 30-Day Readmission")
        change_data = readm.get_readmission_by_medication_change()["data"]
        df_change = pd.DataFrame(change_data)
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.dataframe(df_change, use_container_width=True)
        with col_c2:
            fig_change = px.bar(
                df_change,
                x="change",
                y="readmission_rate_pct",
                color="change",
                title="Readmission Rate: Medication Changed (Ch) vs No Change (No)",
            )
            st.plotly_chart(fig_change, use_container_width=True)

        st.subheader("Top Diabetes Medications Prescribed")
        med_data = treat.get_medication_patterns()["data"]
        df_med = pd.DataFrame(med_data)
        fig_med = px.bar(
            df_med,
            x="drug",
            y="count",
            color="pct",
            title="Active Prescription Frequencies for Common Agents",
            labels={"drug": "Medication", "count": "Prescription Count", "pct": "Cohort Percentage (%)"},
        )
        st.plotly_chart(fig_med, use_container_width=True)

    with tab3:
        st.subheader("Statistical Tests of Independence & Group Comparisons")
        chi2 = stats.chi_square_test("change", "readmitted_30d")
        comp = stats.group_comparison_stay()

        c1, c2 = st.columns(2)
        with c1:
            st.info(f"""
            **Chi-Square Test of Independence**
            - Variables: `Medication Change` vs `30-Day Readmission`
            - Chi2 Statistic: **{chi2['chi2_statistic']}**
            - p-value: **{chi2['p_value']:.4e}**
            - Statistically Significant: **{chi2['statistically_significant']}** (p < 0.05)
            """)

        with c2:
            st.info(f"""
            **Length of Stay Two-Sample Comparison**
            - Readmitted Patients Mean Stay: **{comp['readmitted_mean_stay']} days**
            - Non-Readmitted Mean Stay: **{comp['non_readmitted_mean_stay']} days**
            - Welch's t-statistic: **{comp['t_statistic']}** (p = {comp['t_p_value']:.4e})
            - Mann-Whitney U: **{comp['mann_whitney_u']:,}** (p = {comp['mann_whitney_p_value']:.4e})
            - Significant: **{comp['difference_significant']}**
            """)

        st.subheader("Multivariable Logistic Regression (Odds Ratios for 30-Day Readmission)")
        logit_res = stats.logistic_regression_readmission()
        rows = []
        for feature, vals in logit_res["features"].items():
            rows.append({
                "Feature": feature,
                "Odds Ratio": vals["odds_ratio"],
                "95% CI Lower": vals["ci_95"][0],
                "95% CI Upper": vals["ci_95"][1],
                "Coefficient": vals["coefficient"],
                "p-value": vals["p_value"],
            })
        df_lr = pd.DataFrame(rows)
        st.dataframe(df_lr, use_container_width=True)
        st.caption(f"Model Pseudo R²: {logit_res['pseudo_r_squared']} | AIC: {logit_res['aic']:,}")

finally:
    db.close()
