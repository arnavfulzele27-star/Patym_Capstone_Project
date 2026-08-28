# Reconciliation Results

- **missing_in_gateway: 27 rows**
- **missing_in_ledger_extra_in_gateway: 10 rows**
- **amount_mismatches: 16 rows**
- **status_mismatches: 9 rows**

The discrepancy categories are pairwise comparisons. Because the generator mutates a gateway copy in sequence, amount/status mutations can overlap; therefore these counts are not expected to sum to a simple percentage of 547.
