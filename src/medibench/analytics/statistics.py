import math
from typing import Any

import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sqlalchemy.orm import Session


class StatisticalAnalytics:
    def __init__(self, db: Session):
        self.db = db

    def calculate_confidence_interval(
        self, successes: int, total: int, confidence: float = 0.95
    ) -> dict[str, float]:
        """
        Calculates Wilson score interval for binomial proportion.
        """
        if total == 0:
            return {"point_estimate": 0.0, "lower_bound": 0.0, "upper_bound": 0.0}

        p = successes / total
        z = stats.norm.ppf(1 - (1 - confidence) / 2)
        denominator = 1 + z**2 / total
        centre_adjusted_probability = p + z**2 / (2 * total)
        adjusted_standard_deviation = math.sqrt((p * (1 - p) + z**2 / (4 * total)) / total)

        lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
        upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) / denominator

        return {
            "point_estimate": round(p * 100, 2),
            "lower_bound": round(max(0.0, lower_bound) * 100, 2),
            "upper_bound": round(min(1.0, upper_bound) * 100, 2),
            "confidence_level": confidence,
        }

    def chi_square_test(self, feature1: str, feature2: str) -> dict[str, Any]:
        """
        Runs Chi-Square test of independence between two categorical features.
        """
        sql = f"SELECT {feature1}, {feature2} FROM patient_encounters WHERE {feature1} IS NOT NULL AND {feature2} IS NOT NULL;"
        df = pd.read_sql(sql, self.db.bind)

        contingency_table = pd.crosstab(df[feature1], df[feature2])
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)

        return {
            "feature1": feature1,
            "feature2": feature2,
            "chi2_statistic": round(float(chi2), 3),
            "p_value": float(p_val),
            "degrees_of_freedom": int(dof),
            "statistically_significant": bool(p_val < 0.05),
            "contingency_shape": list(contingency_table.shape),
        }

    def group_comparison_stay(self) -> dict[str, Any]:
        """
        Compares length of stay between 30-day readmitted vs non-readmitted patients
        using Student's t-test and Mann-Whitney U test.
        """
        sql = "SELECT time_in_hospital, readmitted_30d FROM patient_encounters;"
        df = pd.read_sql(sql, self.db.bind)

        group_readmit = df[df["readmitted_30d"] == 1]["time_in_hospital"]
        group_non_readmit = df[df["readmitted_30d"] == 0]["time_in_hospital"]

        t_stat, t_pval = stats.ttest_ind(group_readmit, group_non_readmit, equal_var=False)
        u_stat, u_pval = stats.mannwhitneyu(group_readmit, group_non_readmit, alternative="two-sided")

        return {
            "readmitted_mean_stay": round(float(group_readmit.mean()), 2),
            "readmitted_median_stay": float(group_readmit.median()),
            "non_readmitted_mean_stay": round(float(group_non_readmit.mean()), 2),
            "non_readmitted_median_stay": float(group_non_readmit.median()),
            "t_statistic": round(float(t_stat), 3),
            "t_p_value": float(t_pval),
            "mann_whitney_u": float(u_stat),
            "mann_whitney_p_value": float(u_pval),
            "difference_significant": bool(t_pval < 0.05),
        }

    def correlation_matrix(self) -> dict[str, Any]:
        """
        Calculates Pearson and Spearman correlations among clinical continuous metrics.
        """
        cols = ["time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications", "number_diagnoses"]
        sql = f"SELECT {', '.join(cols)} FROM patient_encounters;"
        df = pd.read_sql(sql, self.db.bind)

        pearson_corr = df.corr(method="pearson").round(3).to_dict()
        spearman_corr = df.corr(method="spearman").round(3).to_dict()

        return {
            "columns": cols,
            "pearson": pearson_corr,
            "spearman": spearman_corr,
        }

    def logistic_regression_readmission(self) -> dict[str, Any]:
        """
        Fits multivariable logistic regression model to estimate Odds Ratios for 30-day readmission.
        """
        sql = """
        SELECT
            readmitted_30d,
            time_in_hospital,
            num_medications,
            num_lab_procedures,
            number_emergency,
            number_inpatient,
            number_diagnoses,
            CASE WHEN diabetes_med = 'Yes' THEN 1 ELSE 0 END AS diabetes_med_flag,
            CASE WHEN change = 'Ch' THEN 1 ELSE 0 END AS med_change_flag
        FROM patient_encounters;
        """
        df = pd.read_sql(sql, self.db.bind)

        y = df["readmitted_30d"].astype(int)
        X = df.drop(columns=["readmitted_30d"])
        X = sm.add_constant(X)

        model = sm.Logit(y, X).fit(disp=False)
        params = model.params
        conf = model.conf_int()
        pvalues = model.pvalues

        results = {}
        for feature in X.columns:
            coef = float(params[feature])
            odds_ratio = math.exp(coef)
            ci_lower = math.exp(conf.loc[feature, 0])
            ci_upper = math.exp(conf.loc[feature, 1])
            results[feature] = {
                "coefficient": round(coef, 4),
                "odds_ratio": round(odds_ratio, 4),
                "ci_95": [round(ci_lower, 4), round(ci_upper, 4)],
                "p_value": float(pvalues[feature]),
            }

        return {
            "pseudo_r_squared": round(float(model.prsquared), 4),
            "aic": round(float(model.aic), 2),
            "features": results,
        }
