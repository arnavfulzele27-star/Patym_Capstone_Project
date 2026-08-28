# Dashboard Interpretations

## Headline layer
Total GMV is INR 382,603 across 547 ledger transactions. The captured-transaction success rate is 85.6%, while the exact ledger-to-gateway match rate is 90.5%; the latter excludes amount/status mismatches and any transaction absent from either file. The count-based platform chargeback ratio is 5.1%.

## Trends layer
Daily GMV varies substantially across the 30-day period because the synthetic ledger contains a mix of low- and high-value transactions. Chargebacks are sparse relative to total transaction volume, so the daily chargeback series is best interpreted as an operational exception signal rather than a volume trend. The dual-axis design keeps the INR GMV scale separate from the small chargeback counts.

## Breakdown layer
UPI is expected to dominate transaction economics because it has the highest synthetic payment-method share, while Card receives an additional contribution from the seeded fraud scenarios. Category GMV highlights which merchant verticals account for the largest transaction value. These views help operations teams separate payment-method mix from merchant-category concentration.

## Details layer
The table ranks merchants by transaction count and separately calculates each merchant's count-based chargeback ratio. A merchant is flagged `HIGH RISK` only when its chargeback ratio is strictly greater than 1%, matching the task definition. The flag is scoped to the merchant's own transactions and does not use chargeback amount.
