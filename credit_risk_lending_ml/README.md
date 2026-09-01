# Credit Risk & Lending ML

Part 2 of the Paytm FinTech Analytics & AI Platform capstone.

## Files

- generate_data.py
- credit_risk_model.py
- credit_applicants.csv
- txn_behaviour.csv
- model_comparison.csv
- risk_pricing_table.csv
- charts/
- README.md

## Objective

Build a credit-risk scoring and lending analytics workflow for Paytm-style lending products. The project includes:

1. Synthetic applicant data generation
2. Credit-risk prediction using machine learning
3. Model comparison and evaluation
4. Transaction anomaly detection
5. Risk-based pricing recommendations
6. Bias-awareness review

## Dataset

### credit_applicants.csv

Contains applicant-level features such as:

- income
- age
- employment_years
- credit_score
- existing_debt
- loan_amount
- thin_file_flag
- defaulted

### txn_behaviour.csv

Contains transaction behaviour information used for anomaly detection.

## Model

Primary model:

- Logistic Regression

Evaluation metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

## Isolation Forest

Isolation Forest is used for anomaly detection on transaction behaviour data.

Required output:

- Recall on seeded anomalies
- Total anomalies detected

## Risk Pricing

Applicants are segmented into risk bands:

| Risk Band | Suggested Interest Premium |
|------------|---------------------------|
| Low Risk | +0% |
| Medium Risk | +2% |
| High Risk | +5% |

Detailed results are stored in:

- risk_pricing_table.csv

## Bias Awareness

Protected characteristics should not be used directly for lending decisions.

The model should be monitored for:

- disparate impact
- approval-rate imbalance
- proxy-variable bias

Human review is recommended for borderline cases.

## Recommendation

Deploy the credit-risk model as a decision-support tool rather than a fully automated lending decision engine.

Combine model outputs with policy rules, affordability checks, fraud screening, and manual review for high-risk applicants.

## Run

Generate data:

```bash
python generate_data.py
```

Run model:

```bash
python credit_risk_model.py
```

Outputs:

- model_comparison.csv
- risk_pricing_table.csv
- charts/
