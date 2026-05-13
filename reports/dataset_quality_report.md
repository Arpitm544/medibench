# MediBench: Healthcare Dataset Quality & Profiling Report

## Executive Summary
- **Dataset**: Diabetes 130-US Hospitals (1999–2008)
- **Source**: UCI Machine Learning Repository
- **Total Encounters Accounted For**: 101,766
- **Unique Patients**: 71,518
- **Encounters per Patient**: 1.42
- **Raw File Checksum (SHA-256)**: `0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97`
- **Ingestion Status**: Fully Validated & Ingested into Database

---

## 1. Data Integrity & Completeness Checks

| Check Name | Category | Status | Records Checked | Affected / Deviant | Pct Affected |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `total_record_count` | completeness | ✅ PASS | 101,766 | 0 | 100.0% |
| `encounter_id_uniqueness` | integrity | ✅ PASS | 101,766 | 0 | 0.0% |
| `weight_sparsity_check` | sparsity | ⚠️ WARNING | 101,766 | 98,569 | 96.86% |
| `medical_specialty_sparsity` | sparsity | ⚠️ WARNING | 101,766 | 49,949 | 49.08% |
| `gender_validity` | validity | ✅ PASS | 101,766 | 3 | 0.0029% |
| `time_in_hospital_range` | range | ✅ PASS | 101,766 | 0 | 0.0% |
| `readmitted_values_validity` | validity | ✅ PASS | 101,766 | 0 | 0.0% |

---

## 2. Demographic Distributions

### Gender Breakdown
- **Female**: 54,708 encounters (53.76%)
- **Male**: 47,055 encounters (46.24%)
- **Unknown/Invalid**: 3 encounters (0.0%)

### Age Group Breakdown
- **[70-80)**: 26,068 encounters (25.62%)
- **[60-70)**: 22,483 encounters (22.09%)
- **[50-60)**: 17,256 encounters (16.96%)
- **[80-90)**: 17,197 encounters (16.9%)
- **[40-50)**: 9,685 encounters (9.52%)
- **[30-40)**: 3,775 encounters (3.71%)
- **[90-100)**: 2,793 encounters (2.74%)
- **[20-30)**: 1,657 encounters (1.63%)
- **[10-20)**: 691 encounters (0.68%)
- **[0-10)**: 161 encounters (0.16%)

---

## 3. Readmission Distribution (Target Variable)
- **Readmitted `NO`**: 54,864 encounters (53.91%)
- **Readmitted `>30`**: 35,545 encounters (34.93%)
- **Readmitted `<30`**: 11,357 encounters (11.16%)

---

## 4. Sparsity & Missing Values (Original '?' markers)
High-sparsity features identified:
- **`race`**: 2,273 missing values (2.23%)
- **`weight`**: 98,569 missing values (96.86%)
- **`payer_code`**: 40,256 missing values (39.56%)
- **`medical_specialty`**: 49,949 missing values (49.08%)
- **`diag_1`**: 21 missing values (0.02%)
- **`diag_2`**: 358 missing values (0.35%)
- **`diag_3`**: 1,423 missing values (1.4%)
- **`max_glu_serum`**: 96,420 missing values (94.75%)
- **`A1Cresult`**: 84,748 missing values (83.28%)

---

## 5. Numerical Metrics Summary
- **time_in_hospital**: Min=1, Max=14, Mean=4.4
- **num_lab_procedures**: Min=1, Max=132, Mean=43.1
- **num_medications**: Min=1, Max=81, Mean=16.02
- **number_diagnoses**: Min=1, Max=16, Mean=7.42

---
*Generated automatically by MediBench Ingestion Pipeline.*
