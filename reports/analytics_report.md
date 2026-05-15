# MediBench: Healthcare Analytics Engine Comprehensive Report

## 1. Overall Readmission Baseline
- **Total Hospital Encounters**: 101,766
- **Unique Patients**: 71,518
- **Overall 30-Day Readmission Count**: 11,357
- **30-Day Readmission Rate**: 11.16% (95% Wilson CI: [10.97%, 11.35%])
- **Any Readmission Rate (<30d or >30d)**: 46.09%
- **Average Length of Stay**: 4.4 days

---

## 2. Demographic Analytics (Module A)

### Age Group Distribution & Readmission
| Age Cohort | Encounters | Share (%) | 30d Readmissions | Readmission Rate (%) | Avg Stay (Days) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [0-10) | 161 | 0.16% | 3 | 1.86% | 2.55 |
| [10-20) | 691 | 0.68% | 40 | 5.79% | 3.19 |
| [20-30) | 1,657 | 1.63% | 236 | 14.24% | 3.56 |
| [30-40) | 3,775 | 3.71% | 424 | 11.23% | 3.8 |
| [40-50) | 9,685 | 9.52% | 1,027 | 10.6% | 4.04 |
| [50-60) | 17,256 | 16.96% | 1,668 | 9.67% | 4.13 |
| [60-70) | 22,483 | 22.09% | 2,502 | 11.13% | 4.38 |
| [70-80) | 26,068 | 25.62% | 3,069 | 11.77% | 4.59 |
| [80-90) | 17,197 | 16.9% | 2,078 | 12.08% | 4.81 |
| [90-100) | 2,793 | 2.74% | 310 | 11.1% | 4.76 |

### Gender Distribution
| Gender | Encounters | Share (%) | 30d Readmission Rate (%) |
| :--- | :--- | :--- | :--- |
| Female | 54,708 | 53.76% | 11.25% |
| Male | 47,055 | 46.24% | 11.06% |

### Race Distribution
| Race Category | Encounters | Share (%) | 30d Readmission Rate (%) |
| :--- | :--- | :--- | :--- |
| Caucasian | 76,099 | 74.78% | 11.29% |
| AfricanAmerican | 19,210 | 18.88% | 11.22% |
| ? | 2,273 | 2.23% | 8.27% |
| Hispanic | 2,037 | 2.0% | 10.41% |
| Other | 1,506 | 1.48% | 9.63% |
| Asian | 641 | 0.63% | 10.14% |

---

## 3. Readmission Analysis (Module B)
- **Primary Insight**: Older cohorts ([70-80), [80-90)) experience higher readmission rates (~11.8%–11.9%) than pediatric/young adult cohorts.
- **Medication Change Effect**: Encounters with medication changes exhibited statistically significant differences in readmission rates compared to encounters without changes (Chi-square = 38.596, p = 5.212417406066971e-10).

---

## 4. Treatment & Medication Patterns (Module C)
| Medication | Prescriptions | Prescription Pct (%) |
| :--- | :--- | :--- |
|  | 54,383 | 53.44% |
|  | 19,988 | 19.64% |
|  | 12,686 | 12.47% |
|  | 10,650 | 10.47% |
|  | 7,328 | 7.2% |

---

## 5. Statistical Rigor (Module D)
- **Length of Stay Group Comparison**:
  - Readmitted (<30d) Mean Stay: **4.77 days**
  - Non-Readmitted Mean Stay: **4.35 days**
  - Two-sample t-statistic: **13.926** (p = 8.549546879359549e-44)
  - Mann-Whitney U: **560893881.0** (p = 2.689648414149974e-59)
  - Conclusion: Readmitted patients have a statistically significant longer initial hospital stay.

---
*Report generated deterministically by MediBench Analytics Engine.*
