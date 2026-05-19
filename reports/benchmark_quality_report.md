# MediBench: Benchmark Quality & Verification Report

## Executive Summary
- **Total Benchmark Questions**: 60
- **Verified Ground-Truth Answers**: 60 (100% verification rate)
- **Retired Questions in Registry**: 3
- **Evaluation Mode**: Deterministic & Multi-Metric (Tolerant Numeric, Exact Categorical, Structured Rubric)

---

## 1. Questions Breakdown by Category
| Category | Target | Actual Created | Verification Status |
| :--- | :--- | :--- | :--- |
| `sql_analytics` | 15 | 15 | ✅ Complete |
| `statistical_reasoning` | 10 | 10 | ✅ Complete |
| `data_interpretation` | 10 | 10 | ✅ Complete |
| `data_quality` | 10 | 10 | ✅ Complete |
| `business_decision_making` | 10 | 10 | ✅ Complete |
| `contradictory_evidence` | 5 | 5 | ✅ Complete |

---

## 2. Difficulty Distribution
| Difficulty Level | Question Count | Share (%) |
| :--- | :--- | :--- |
| **Medium** | 19 | 31.7% |
| **Easy** | 5 | 8.3% |
| **Hard** | 36 | 60.0% |

---

## 3. Advanced Features Verification

### Feature 1: Retired Question Registry
| Question ID | Original Question | Reason for Retirement | Status | Replacement |
| :--- | :--- | :--- | :--- | :--- |
| `MED-RET-001` | What is the average patient weight in kg across all encounters? | Excessive sparsity (>95% missing); fails institutional data quality thresholds. | `hypothetical_expert_review` | `MED-036` |
| `MED-RET-002` | Which hospital facility had the lowest 30-day readmission rate? | De-identified institutional IDs; uninterpretable hospital site comparisons. | `hypothetical_expert_review` | `MED-001` |
| `MED-RET-003` | Did changing medication cause readmissions to increase? | Invalid causal framing on observational dataset. | `hypothetical_expert_review` | `MED-056` |

### Feature 2: Freshness-Aware Categories
| Freshness Category | Count | Description |
| :--- | :--- | :--- |
| `static` | 59 | Historical static calculations |
| `live_dependent` | 1 | Contextual snapshot or live-dependent reasoning |

### Feature 3: Contradictory Evidence & Operational Trade-offs
- Includes 5 matched analytical scenarios (`MED-056` to `MED-060`) testing model discernment regarding confounding by indication, testing omission, cost-per-prevented readmission efficiency, and length-of-stay vs readmission penalty trade-offs.

---
*Report generated automatically by MediBench Benchmark Suite.*