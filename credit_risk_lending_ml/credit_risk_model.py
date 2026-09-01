import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score, roc_curve, roc_auc_score
)
from sklearn.ensemble import IsolationForest

BASE = Path(__file__).resolve().parent
CHARTS = BASE / "charts"
CHARTS.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "credit_applicants.csv")
df["is_thin_file"] = df["credit_bureau_score"].isna().astype(int)

print("=== EDA ===")
print(f"Rows: {len(df)}")
print(f"Default rate: {df['default'].mean():.2%}")
print(
    f"Missing credit_bureau_score: "
    f"{df['credit_bureau_score'].isna().sum()} "
    f"({df['credit_bureau_score'].isna().mean():.2%})"
)

train, test = train_test_split(
    df, test_size=0.25, stratify=df["default"], random_state=42
)

numeric_features = [
    "age", "monthly_income_inr", "existing_loans_count",
    "credit_utilization_ratio", "upi_monthly_inflow_inr",
    "bounced_payments_count", "credit_bureau_score"
]
categorical_features = ["employment_type"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42)
}

comparison_rows = []
roc_curves = {}
fitted_models = {}

for name, estimator in models.items():
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("model", estimator)
    ])
    model.fit(train.drop(columns="default"), train["default"])

    pred = model.predict(test.drop(columns="default"))
    prob = model.predict_proba(test.drop(columns="default"))[:, 1]
    cm = confusion_matrix(test["default"], pred)
    auc = roc_auc_score(test["default"], prob)

    comparison_rows.append({
        "model": name,
        "accuracy": accuracy_score(test["default"], pred),
        "precision": precision_score(test["default"], pred, zero_division=0),
        "recall": recall_score(test["default"], pred, zero_division=0),
        "f1": f1_score(test["default"], pred, zero_division=0),
        "roc_auc": auc,
        "tn": cm[0, 0], "fp": cm[0, 1],
        "fn": cm[1, 0], "tp": cm[1, 1]
    })

    roc_curves[name] = roc_curve(test["default"], prob)
    fitted_models[name] = model

comparison = pd.DataFrame(comparison_rows)
comparison.to_csv(BASE / "model_comparison.csv", index=False)
print("\n=== MODEL COMPARISON ===")
print(comparison.to_string(index=False))

# Risk pricing
logit = fitted_models["Logistic Regression"]
pricing = test[["applicant_id", "default"]].copy()
pricing["predicted_default_probability"] = logit.predict_proba(
    test.drop(columns="default")
)[:, 1]
pricing["risk_tier"] = pd.qcut(
    pricing["predicted_default_probability"],
    4,
    labels=["Low", "Moderate", "High", "Very High"],
    duplicates="drop"
)

rate_ranges = {
    "Low": "12%–14%",
    "Moderate": "14%–16%",
    "High": "16%–19%",
    "Very High": "19%–24%"
}

risk_pricing = pricing.groupby("risk_tier", observed=False).agg(
    applicants=("default", "size"),
    mean_predicted_pd=("predicted_default_probability", "mean"),
    observed_default_rate=("default", "mean")
).reset_index()
risk_pricing["illustrative_interest_rate"] = (
    risk_pricing["risk_tier"].astype(str).map(rate_ranges)
)
risk_pricing.to_csv(BASE / "risk_pricing_table.csv", index=False)

print("\n=== RISK PRICING ===")
print(risk_pricing.to_string(index=False))

# Isolation Forest
txns = pd.read_csv(BASE / "txn_behaviour.csv")
features = ["txn_hour", "is_new_device", "txn_amount_inr"]

scaled = StandardScaler().fit_transform(txns[features])
iso = IsolationForest(
    random_state=42,
    contamination=15 / 265
)
txns["is_anomaly_flag"] = (iso.fit_predict(scaled) == -1).astype(int)
txns["seeded_anomaly"] = txns["txn_id"].str.startswith("BTXNA")

detected = int(
    ((txns["seeded_anomaly"]) & (txns["is_anomaly_flag"] == 1)).sum()
)
recall = detected / 15

pd.DataFrame([{
    "total_transactions": len(txns),
    "seeded_anomalies": 15,
    "flagged_anomalies": int(txns["is_anomaly_flag"].sum()),
    "seeded_anomalies_detected": detected,
    "isolation_forest_recall": recall
}]).to_csv(BASE / "isolation_forest_results.csv", index=False)

print("\n=== ISOLATION FOREST ===")
print(f"Flagged transactions: {int(txns['is_anomaly_flag'].sum())}")
print(f"Seeded anomalies detected: {detected}/15")
print(f"Recall: {recall:.2%}")

# Saved charts
df["default"].value_counts().sort_index().plot(kind="bar")
plt.title("Default Class Distribution")
plt.xlabel("Default")
plt.ylabel("Applicants")
plt.tight_layout()
plt.savefig(CHARTS / "default_distribution.png", dpi=180)
plt.close()

plt.figure(figsize=(7, 5))
for name, (fpr, tpr, thresholds) in roc_curves.items():
    auc = comparison.loc[comparison["model"] == name, "roc_auc"].iloc[0]
    plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.4f})")
plt.plot([0, 1], [0, 1], linestyle="--", label="Random")
plt.title("ROC Curve — Credit Risk Models")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS / "roc_comparison.png", dpi=180)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(
    risk_pricing["risk_tier"].astype(str),
    risk_pricing["observed_default_rate"] * 100
)
plt.title("Observed Default Rate by Risk Tier")
plt.xlabel("Risk Tier")
plt.ylabel("Observed Default Rate (%)")
plt.tight_layout()
plt.savefig(CHARTS / "risk_tier_default_rate.png", dpi=180)
plt.close()

normal = txns[~txns["seeded_anomaly"]]
seeded = txns[txns["seeded_anomaly"]]
plt.figure(figsize=(8, 5))
plt.scatter(
    normal["txn_hour"], normal["txn_amount_inr"],
    alpha=0.55, label="Normal"
)
plt.scatter(
    seeded["txn_hour"], seeded["txn_amount_inr"],
    marker="x", s=60, label="Seeded anomaly"
)
plt.title("Transaction Behaviour — Seeded Anomalies")
plt.xlabel("Transaction Hour")
plt.ylabel("Transaction Amount (INR)")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS / "transaction_anomalies.png", dpi=180)
plt.close()

print("\nSaved all required outputs to this folder.")
