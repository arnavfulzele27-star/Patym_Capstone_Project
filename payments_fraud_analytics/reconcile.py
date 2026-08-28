import pandas as pd

def reconcile_payments(ledger_df, gateway_df):
    """
    Compare ledger_df and gateway_df using transaction_id set operations
    and pd.merge for pairwise comparisons.

    Returns:
        missing_in_gateway,
        missing_in_ledger,
        amount_mismatches,
        status_mismatches
    """
    ledger_ids = set(ledger_df["transaction_id"])
    gateway_ids = set(gateway_df["transaction_id"])

    missing_in_gateway_ids = ledger_ids - gateway_ids
    missing_in_ledger_ids = gateway_ids - ledger_ids

    missing_in_gateway = ledger_df[
        ledger_df["transaction_id"].isin(missing_in_gateway_ids)
    ].copy()

    missing_in_ledger = gateway_df[
        gateway_df["transaction_id"].isin(missing_in_ledger_ids)
    ].copy()

    common = pd.merge(
        ledger_df,
        gateway_df,
        on="transaction_id",
        how="inner",
        suffixes=("_ledger", "_gateway")
    )

    amount_mismatches = common[
        common["amount_inr_ledger"] != common["amount_inr_gateway"]
    ].copy()
    amount_mismatches["amount_difference_inr"] = (
        amount_mismatches["amount_inr_gateway"] -
        amount_mismatches["amount_inr_ledger"]
    )

    status_mismatches = common[
        common["status_ledger"] != common["status_gateway"]
    ].copy()
    status_mismatches["status_difference"] = (
        status_mismatches["status_ledger"] + " -> " +
        status_mismatches["status_gateway"]
    )

    return (
        missing_in_gateway,
        missing_in_ledger,
        amount_mismatches,
        status_mismatches,
    )


if __name__ == "__main__":
    ledger = pd.read_csv("ledger.csv", parse_dates=["transaction_time"])
    gateway = pd.read_csv("gateway_export.csv", parse_dates=["transaction_time"])

    results = reconcile_payments(ledger, gateway)
    labels = [
        "missing_in_gateway",
        "missing_in_ledger_extra_in_gateway",
        "amount_mismatches",
        "status_mismatches",
    ]

    lines = ["# Reconciliation Results", ""]
    for label, df in zip(labels, results):
        lines.append(f"- **{label}: {len(df)} rows**")
    lines.append("")
    lines.append("These are pairwise discrepancy categories; the injected mutations can overlap.")
    with open("reconciliation_output.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
