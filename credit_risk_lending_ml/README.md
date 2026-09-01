# Part 2 — Credit Risk & Lending ML

## Scope

This folder implements the Paytm Postpaid / lending analytics requirement using the exact seeded synthetic data generator from the assignment.

## Files

- `generate_data.py` — exact seed-data generator.
- `credit_applicants.csv` — 400 applicant rows.
- `txn_behaviour.csv` — 265 transaction-behaviour rows, including 15 seeded anomalies.
- `credit_risk_model.py` — complete EDA, preprocessing, classification, pricing and anomaly-detection pipeline.
- `model_comparison.csv` — side-by-side classifier metrics.
- `risk_pricing_table.csv` — four-tier risk-pricing output.
- `isolation_forest_results.csv` — anomaly-detection result.
- `charts/` — saved chart images.

## Installation

From the `credit_risk_lending_ml` folder:

```bash
pip install -r requirements.txt
```

## Run

```bash
python generate_data.py
python credit_risk_model.py
```

The generator must be run from this folder because it writes the two CSV files using relative paths.

## EDA and thin-file handling

The generated dataset contains **400 applicants**. The measured default rate is **20.25%**. Exactly **80 applicants (20.00%)** have no bureau score.

`is_thin_file` is engineered directly from the raw missingness indicator before any imputation. No applicant is dropped.

The split is **75% train / 25% test**, stratified on `default`, with `random_state=42`. Stratification preserves the default-class proportion across train and test and makes model comparison more stable.

The median bureau score is fitted only on the training data and then used to impute both train and test. This avoids test-set leakage while retaining thin-file applicants. Employment type is one-hot encoded, and numeric features are standardized using training-fitted preprocessing.

## Model comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 76.00% | 38.89% | 35.00% | 36.84% | 71.50% |
| Decision Tree | 63.00% | 18.52% | 25.00% | 21.28% | 48.75% |

Confusion matrices are stored numerically in `model_comparison.csv`.

Logistic Regression is the preferred baseline because it has stronger overall discrimination and is easier to explain and audit than the single Decision Tree in this synthetic experiment.

## Risk-based pricing

Risk tiers are based on quartiles of Logistic Regression predicted default probability on the held-out test set.

| Risk tier | Applicants | Mean predicted PD | Observed default rate | Illustrative interest rate |
|---|---:|---:|---:|---:|
| Low | 25 | 2.02% | 8.00% | 12%–14% |\n| Moderate | 25 | 7.34% | 12.00% | 14%–16% |\n| High | 25 | 23.62% | 24.00% | 16%–19% |\n| Very High | 25 | 59.21% | 36.00% | 19%–24% |\n
The observed default rate increases from **8.00%** in the Low tier to **36.00%** in the Very High tier. This supports the intended monotonic relationship between predicted risk and indicative pricing.

The interest-rate bands are illustrative analytical tiers, not claims about Paytm's actual lending rates.

## Isolation Forest anomaly detection

The Isolation Forest uses the required standardized behavioural features:

- `txn_hour`
- `is_new_device`
- `txn_amount_inr`

The contamination parameter is **15 / 265 = 5.66%**, matching the seeded anomaly proportion.

- Total transactions: **265**
- Seeded anomalies: **15**
- Transactions flagged: **15**
- Seeded anomalies detected: **11**
- Isolation Forest recall: **73.33%**

Recall is calculated as detected seeded anomalies divided by all 15 seeded anomalies.

## Bias-awareness note

Even though the synthetic dataset does not explicitly contain gender or location, `employment_type`, `monthly_income_inr`, and `credit_bureau_score` could act as correlated proxies for protected or vulnerable characteristics in a real deployment. For example, employment type can correlate with socioeconomic status and occupational access, while income and bureau history can reflect structural differences in access to formal employment and credit. A model may therefore appear neutral while still producing systematically different outcomes for groups affected by those underlying correlations.

The appropriate governance control is a maker-checker human-in-the-loop review for high-impact lending decisions, particularly declined thin-file applicants. The review should check the model's reason codes, verify that the decision is supported by legitimate credit-risk variables, and allow escalation when alternative data is sparse or contradictory. Segment-level monitoring should also track approval rates, false-negative rates and other performance indicators over time. Any production deployment should include periodic model validation, drift monitoring and documented adverse-action reasoning.

## Final recommendation

| Component | Result |
|---|---|
| Logistic Regression ROC-AUC | 71.50% |
| Decision Tree ROC-AUC | 48.75% |
| Logistic Regression F1 | 36.84% |
| Decision Tree F1 | 21.28% |
| Isolation Forest recall | 73.33% |

For Paytm Postpaid, I would deploy **Logistic Regression as the initial credit-risk classifier** because it provides better discrimination than the Decision Tree in this experiment and is easier to explain and audit. Its ROC-AUC is **71.50%**, compared with **48.75%** for the tree. The Isolation Forest should remain a separate transaction-risk signal rather than replacing the credit model. Borderline and high-impact decisions, especially thin-file declines, should retain human review before production deployment.
