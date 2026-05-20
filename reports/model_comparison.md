# MediBench: AI Model Evaluation & Comparison Report

## Executive Summary
This report evaluates AI model capabilities across 60 rigorous healthcare analytics benchmark questions grounded in 101,766 hospital encounters.

| Run ID | Model Name | Evaluated Questions | Passed | Overall Score (%) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `RUN-20261124091750` | **Test-Bench-Model** | 10 | 10 | **100.0%** | `completed` |
| `RUN-001` | **MediBench-Clinical-LLM** | 60 | 56 | **92.5%** | `completed` |
| `RUN-002` | **General-Baseline-LLM** | 60 | 45 | **74.17%** | `completed` |

---

## Performance by Category Breakdown

### Model: Test-Bench-Model (`RUN-20261124091750`)
- **Average Question Latency**: 35.6 ms
- **Total Tokens Utilized**: 685
- **Passed**: 10 / 10 (100.0%)
- **Failed / Deviations**: 0

### Model: MediBench-Clinical-LLM (`RUN-001`)
- **Average Question Latency**: 34.9 ms
- **Total Tokens Utilized**: 4,287
- **Passed**: 56 / 60 (92.5%)
- **Failed / Deviations**: 4

### Model: General-Baseline-LLM (`RUN-002`)
- **Average Question Latency**: 35.1 ms
- **Total Tokens Utilized**: 4,270
- **Passed**: 45 / 60 (74.17%)
- **Failed / Deviations**: 15

---
*Report generated deterministically by MediBench Evaluation Suite.*