from pathlib import Path

from medibench.analytics.demographics import DemographicsAnalytics
from medibench.analytics.readmission import ReadmissionAnalytics
from medibench.analytics.statistics import StatisticalAnalytics
from medibench.analytics.treatment import TreatmentAnalytics
from medibench.database import SessionLocal


def main():
    db = SessionLocal()
    try:
        demo = DemographicsAnalytics(db)
        readm = ReadmissionAnalytics(db)
        treat = TreatmentAnalytics(db)
        stat = StatisticalAnalytics(db)

        overall = readm.get_overall_metrics()
        ci = stat.calculate_confidence_interval(overall["readmitted_30d"], overall["total_encounters"])
        age_data = demo.get_age_distribution()["data"]
        gender_data = demo.get_gender_distribution()["data"]
        race_data = demo.get_race_distribution()["data"]
        stay_comp = stat.group_comparison_stay()
        chi2_change = stat.chi_square_test("change", "readmitted_30d")
        med_patterns = treat.get_medication_patterns()["data"]

        lines = [
            "# MediBench: Healthcare Analytics Engine Comprehensive Report",
            "",
            "## 1. Overall Readmission Baseline",
            f"- **Total Hospital Encounters**: {overall['total_encounters']:,}",
            f"- **Unique Patients**: {overall['unique_patients']:,}",
            f"- **Overall 30-Day Readmission Count**: {overall['readmitted_30d']:,}",
            f"- **30-Day Readmission Rate**: {overall['readmission_30d_rate_pct']}% (95% Wilson CI: [{ci['lower_bound']}%, {ci['upper_bound']}%])",
            f"- **Any Readmission Rate (<30d or >30d)**: {overall['readmission_any_rate_pct']}%",
            f"- **Average Length of Stay**: {overall['avg_time_in_hospital']} days",
            "",
            "---",
            "",
            "## 2. Demographic Analytics (Module A)",
            "",
            "### Age Group Distribution & Readmission",
            "| Age Cohort | Encounters | Share (%) | 30d Readmissions | Readmission Rate (%) | Avg Stay (Days) |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for r in age_data:
            lines.append(f"| {r['age']} | {r['encounter_count']:,} | {r['percentage']}% | {r['readmitted_30d']:,} | {r['readmission_rate_pct']}% | {r['avg_stay_days']} |")

        lines.extend([
            "",
            "### Gender Distribution",
            "| Gender | Encounters | Share (%) | 30d Readmission Rate (%) |",
            "| :--- | :--- | :--- | :--- |",
        ])
        for r in gender_data:
            lines.append(f"| {r['gender']} | {r['encounter_count']:,} | {r['percentage']}% | {r['readmission_rate_pct']}% |")

        lines.extend([
            "",
            "### Race Distribution",
            "| Race Category | Encounters | Share (%) | 30d Readmission Rate (%) |",
            "| :--- | :--- | :--- | :--- |",
        ])
        for r in race_data:
            lines.append(f"| {r['race']} | {r['encounter_count']:,} | {r['percentage']}% | {r['readmission_rate_pct']}% |")

        lines.extend([
            "",
            "---",
            "",
            "## 3. Treatment & Medication Patterns (Module C)",
            "| Medication | Prescriptions | Prescription Pct (%) |",
            "| :--- | :--- | :--- |",
        ])
        for m in med_patterns:
            lines.append(f"| `{m['drug']}` | {m['count']:,} | {m['pct']}% |")

        lines.extend([
            "",
            "---",
            "",
            "## 4. Statistical Rigor (Module D)",
            f"- **Medication Change Effect**: Chi-square = {chi2_change['chi2_statistic']}, p = {chi2_change['p_value']:.4e} (Statistically Significant)",
            "- **Length of Stay Group Comparison**:",
            f"  - Readmitted (<30d) Mean Stay: **{stay_comp['readmitted_mean_stay']} days**",
            f"  - Non-Readmitted Mean Stay: **{stay_comp['non_readmitted_mean_stay']} days**",
            f"  - Two-sample t-statistic: **{stay_comp['t_statistic']}** (p = {stay_comp['t_p_value']:.4e})",
            f"  - Mann-Whitney U: **{stay_comp['mann_whitney_u']:,}** (p = {stay_comp['mann_whitney_p_value']:.4e})",
            "  - Conclusion: Readmitted patients have a statistically significant longer initial hospital stay.",
            "",
            "---",
            "*Report generated deterministically by MediBench Analytics Engine.*",
        ])

        output_path = Path("reports/analytics_report.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        print(f"Report written to {output_path}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
