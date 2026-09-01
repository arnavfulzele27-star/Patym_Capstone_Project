# Part 2 — Credit Risk & Lending ML

## Model Performance

- Dataset: 400 credit applicants
- Thin-file applicants: 80
- Default rate: 20.25%
- Model: Logistic Regression
- Training rows: 320
- Testing rows: 80
- Accuracy: 77.50%
- ROC-AUC: 71.68%

## Transaction Anomaly Detection

- Total transactions: 265
- Normal transactions: 250
- Anomalous transactions detected: 15
- Detection rule: unusual hour (1–4 AM) + new device + high transaction amount

## Confusion Matrix

[[56, 8],
 [10, 6]]

 ## Risk Pricing Table

The risk-pricing framework converts predicted credit risk into a practical lending recommendation. The objective is to compensate for higher expected default risk through higher pricing while avoiding excessive pricing for low-risk applicants.

| Risk Band | Predicted Risk | Pricing Recommendation | Lending Action |
|---|---:|---:|---|
| Low Risk | < 10% | 12.0% | Approve |
| Medium Risk | 10%–20% | 15.0% | Approve with monitoring |
| High Risk | 20%–30% | 18.0% | Conditional approval |
| Very High Risk | > 30% | 22.0% | Decline / manual review |

The pricing table is a risk-management decision rule rather than a claim about Paytm's actual lending rates. Higher-risk applicants receive higher indicative pricing because their expected credit loss is greater.

## Isolation Forest — Transaction Anomaly Detection

Isolation Forest was used as an unsupervised anomaly-detection method because fraudulent or unusual transactions may not always have reliable labelled examples.

The transaction dataset contains:

- Total transactions: 265
- Normal transactions: 250
- Seeded anomalous transactions: 15
- Detection rule used in the baseline analysis: unusual transaction hour, new device and high transaction amount.

**Recall:** The final Isolation Forest recall must be calculated directly from the committed `txn_behaviour.csv` rather than manually entered. Recall is calculated as:

`Recall = True Positives / (True Positives + False Negatives)`

This metric is particularly important for fraud detection because failing to identify an anomalous transaction can be more costly than reviewing a legitimate transaction.

## Bias Awareness

The credit-risk model is trained on synthetic data and therefore its performance should not be interpreted as evidence of real-world lending fairness.

A model can reproduce historical or structural biases when variables associated with protected or vulnerable groups act as proxies for those characteristics. Even when sensitive attributes are removed, correlated variables such as income, employment history, location or transaction behaviour can still produce unequal outcomes.

Therefore, model accuracy and ROC-AUC should be evaluated alongside segment-level performance, approval rates, false-positive rates and false-negative rates. Any production deployment should include fairness monitoring, human review for borderline decisions, explainability and periodic model validation.

The synthetic dataset used in this project is suitable for demonstrating the analytical pipeline but is not sufficient for making real lending decisions.

## Final Recommendation

The recommended approach is to use the Logistic Regression model as a transparent baseline credit-risk model and combine its probability output with a rule-based risk-pricing framework.

Applicants in the low-risk band can receive standard pricing and streamlined approval. Medium-risk applicants should receive additional monitoring, while high-risk applicants should receive conditional approval or manual review. Very-high-risk applicants should generally be declined unless additional evidence materially changes the assessment.

The transaction anomaly model should operate as a complementary fraud-risk signal rather than replacing the credit-risk model. An anomalous transaction should trigger additional verification rather than automatically resulting in a credit rejection.

The final system should therefore use:

1. Logistic Regression for interpretable credit-risk estimation.
2. Risk bands for consistent lending and pricing decisions.
3. Isolation Forest as an additional transaction-anomaly signal.
4. Human review for borderline or high-impact decisions.
5. Bias and performance monitoring before any real-world deployment.

Because the project uses synthetic data, these recommendations are analytical demonstrations and should not be interpreted as actual Paytm lending-policy recommendations.
