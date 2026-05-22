import pandas as pd
import plotly.express as px
import streamlit as st

from medibench.analytics.demographics import DemographicsAnalytics
from medibench.analytics.readmission import ReadmissionAnalytics
from medibench.database import SessionLocal

st.set_page_config(page_title="Healthcare Overview | MediBench", page_icon="📊", layout="wide")

st.title("📊 Healthcare Dataset & Cohort Overview")
st.caption("Historical Encounter Analysis (Diabetes 130-US Hospitals, 1999–2008)")

db = SessionLocal()
try:
    readm = ReadmissionAnalytics(db)
    demo = DemographicsAnalytics(db)

    metrics = readm.get_overall_metrics()
    age_dist = demo.get_age_distribution()["data"]
    gender_dist = demo.get_gender_distribution()["data"]
    race_dist = demo.get_race_distribution()["data"]

    # Top KPI Metrics Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Encounters", f"{metrics['total_encounters']:,}")
    col2.metric("Unique Patients", f"{metrics['unique_patients']:,}")
    col3.metric("30-Day Readmission Rate", f"{metrics['readmission_30d_rate_pct']}%", delta="11,357 encounters")
    col4.metric("Any Readmission Rate", f"{metrics['readmission_any_rate_pct']}%")
    col5.metric("Avg Length of Stay", f"{metrics['avg_time_in_hospital']} Days")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Encounter Distribution by Age Group")
        df_age = pd.DataFrame(age_dist)
        fig_age = px.bar(
            df_age,
            x="age",
            y="encounter_count",
            color="readmission_rate_pct",
            color_continuous_scale="Reds",
            labels={"encounter_count": "Hospital Encounters", "age": "Age Cohort", "readmission_rate_pct": "30d Readmit Rate (%)"},
            title="Encounters & Readmission Rate by Age",
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col_right:
        st.subheader("Gender & Demographic Representation")
        df_gender = pd.DataFrame(gender_dist)
        fig_gender = px.pie(
            df_gender,
            names="gender",
            values="encounter_count",
            hole=0.4,
            title="Gender Distribution (Excl. Invalid)",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    st.subheader("Racial & Ethnic Distribution")
    df_race = pd.DataFrame(race_dist)
    fig_race = px.bar(
        df_race,
        x="race",
        y="encounter_count",
        color="readmission_rate_pct",
        color_continuous_scale="Viridis",
        title="Encounters by Racial Category with 30-Day Readmission Rate",
        labels={"encounter_count": "Encounters", "race": "Race Category", "readmission_rate_pct": "30d Readmit %"},
    )
    st.plotly_chart(fig_race, use_container_width=True)

finally:
    db.close()
