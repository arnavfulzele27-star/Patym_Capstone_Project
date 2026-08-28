import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "dashboard"
OUT.mkdir(exist_ok=True)

merchants = pd.read_csv(BASE / "merchants.csv")
ledger = pd.read_csv(BASE / "ledger.csv", parse_dates=["transaction_time"])
gateway = pd.read_csv(BASE / "gateway_export.csv", parse_dates=["transaction_time"])
df = ledger.merge(merchants, on="merchant_id", how="left")

total_gmv = int(ledger["amount_inr"].sum())
success_rate = float((ledger["status"] == "captured").mean())
common = ledger.merge(gateway, on="transaction_id", how="inner", suffixes=("_ledger", "_gateway"))
matched = int(((common["amount_inr_ledger"] == common["amount_inr_gateway"]) &
               (common["status_ledger"] == common["status_gateway"])).sum())
match_rate = matched / len(ledger)
chargeback_ratio = float((ledger["status"] == "chargeback").mean())

# Headline
fig, ax = plt.subplots(figsize=(12, 4.5)); ax.axis("off")
metrics = [("Total GMV", f"INR {total_gmv:,.0f}"),
           ("Success Rate", f"{success_rate:.1%}"),
           ("Reconciliation Match Rate", f"{match_rate:.1%}"),
           ("Chargeback Ratio", f"{chargeback_ratio:.1%}")]
for i, (label, value) in enumerate(metrics):
    x = 0.125 + i*0.25
    ax.text(x, .58, value, ha="center", va="center", fontsize=22, fontweight="bold")
    ax.text(x, .28, label, ha="center", va="center", fontsize=11)
ax.set_title("Paytm Payments — Headline Scorecards", fontsize=16, fontweight="bold", pad=18)
fig.tight_layout(); fig.savefig(OUT/"01_headline_scorecards.png", dpi=180, bbox_inches="tight"); plt.close(fig)

# Trends
df["transaction_date"] = df["transaction_time"].dt.date
daily = df.groupby("transaction_date").agg(
    daily_gmv=("amount_inr", "sum"),
    chargeback_count=("status", lambda s: (s == "chargeback").sum())
).reset_index()
fig, ax1 = plt.subplots(figsize=(12,5))
ax1.plot(daily["transaction_date"], daily["daily_gmv"], marker="o", linewidth=1.8)
ax1.set_ylabel("Daily GMV (INR)"); ax1.set_xlabel("Date"); ax1.tick_params(axis="x", rotation=45)
ax2 = ax1.twinx()
ax2.plot(daily["transaction_date"], daily["chargeback_count"], marker="s", linewidth=1.5)
ax2.set_ylabel("Daily Chargeback Count")
ax1.set_title("30-Day Payments Trend: GMV and Chargebacks")
fig.tight_layout(); fig.savefig(OUT/"02_trends_daily_gmv_chargebacks.png", dpi=180, bbox_inches="tight"); plt.close(fig)

# Breakdown
method_gmv = df.groupby("payment_method")["amount_inr"].sum().sort_values(ascending=False)
category_gmv = df.groupby("category")["amount_inr"].sum().sort_values(ascending=False)
fig, axes = plt.subplots(1,2,figsize=(13,5))
method_gmv.plot(kind="bar", ax=axes[0]); axes[0].set_title("GMV by Payment Method"); axes[0].set_ylabel("GMV (INR)"); axes[0].tick_params(axis="x", rotation=35)
category_gmv.plot(kind="bar", ax=axes[1]); axes[1].set_title("GMV by Merchant Category"); axes[1].set_ylabel("GMV (INR)"); axes[1].tick_params(axis="x", rotation=35)
fig.suptitle("Breakdown Layer", fontsize=16, fontweight="bold")
fig.tight_layout(); fig.savefig(OUT/"03_breakdown_gmv_method_category.png", dpi=180, bbox_inches="tight"); plt.close(fig)

# Details
detail = df.groupby(["merchant_id","merchant_name"], as_index=False).agg(
    transaction_count=("transaction_id","count"),
    gmv_inr=("amount_inr","sum"),
    chargeback_count=("status", lambda s: (s == "chargeback").sum())
)
detail["chargeback_ratio"] = detail["chargeback_count"] / detail["transaction_count"]
detail["flag"] = np.where(detail["chargeback_ratio"] > 0.01, "HIGH RISK", "")
top10 = detail.sort_values(["transaction_count","merchant_id"], ascending=[False,True]).head(10).copy()
display_df = top10.copy()
display_df["gmv_inr"] = display_df["gmv_inr"].map(lambda x: f"INR {x:,.0f}")
display_df["chargeback_ratio"] = display_df["chargeback_ratio"].map(lambda x: f"{x:.1%}")
fig, ax = plt.subplots(figsize=(12,5.8)); ax.axis("off")
cols = ["merchant_id","merchant_name","transaction_count","gmv_inr","chargeback_count","chargeback_ratio","flag"]
tbl = ax.table(cellText=display_df[cols].values.tolist(),
               colLabels=["ID","Merchant","Txn Count","GMV","Chargebacks","CB Ratio","Flag"],
               loc="center", cellLoc="center")
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1,1.65)
for r, flag in enumerate(display_df["flag"], start=1):
    if flag == "HIGH RISK":
        for c in range(len(cols)):
            tbl[(r,c)].set_facecolor("#ffd6d6")
ax.set_title("Details Layer — Top 10 Merchants by Transaction Count", fontsize=15, fontweight="bold", pad=15)
fig.tight_layout(); fig.savefig(OUT/"04_details_top10_merchants.png", dpi=180, bbox_inches="tight"); plt.close(fig)

print(f"total_gmv={total_gmv}")
print(f"success_rate={success_rate:.6f}")
print(f"match_rate={match_rate:.6f}")
print(f"chargeback_ratio={chargeback_ratio:.6f}")
