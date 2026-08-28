# SQL Query Outputs

## Q1_basic_select_where_order_limit_distinct
```text
payment_method     status
    Netbanking   captured
        Wallet chargeback
          Card chargeback
        Wallet   captured
          Card     failed
          Card   captured
           UPI   captured
    Netbanking     failed
        Wallet     failed
           UPI chargeback
```

## Q2_chargeback_impact
```text
 chargeback_transactions  unique_users_affected  total_chargeback_amount_inr
                      28                     27                        54472
```

## Q3_burner_accounts
```text
transaction_id  user_id    transaction_time         signup_date  signup_age_days  amount_inr     status
     TXN200001      352 2026-01-11 12:00:00 2025-12-31 12:00:00               11        4999 chargeback
     TXN200009      360 2026-01-13 13:00:00 2025-12-22 13:00:00               22        1999 chargeback
     TXN200004      355 2026-01-16 12:00:00 2026-01-05 12:00:00               11        4999 chargeback
     TXN200014      365 2026-01-18 21:00:00 2025-12-27 21:00:00               22        1999 chargeback
     TXN200010      361 2026-01-20 07:00:00 2026-01-11 07:00:00                9        4999 chargeback
     TXN200002      353 2026-01-21 14:00:00 2026-01-10 14:00:00               11        1999 chargeback
     TXN200003      354 2026-01-21 19:00:00 2025-12-29 19:00:00               23        4999 chargeback
     TXN200013      364 2026-01-22 22:00:00 2026-01-04 22:00:00               18         999 chargeback
     TXN200011      362 2026-01-23 02:00:00 2026-01-08 02:00:00               15        4999 chargeback
     TXN200006      357 2026-01-23 11:00:00 2026-01-19 11:00:00                4        1999 chargeback
     TXN200012      363 2026-01-23 17:00:00 2026-01-06 17:00:00               17         999 chargeback
     TXN200008      359 2026-01-25 22:00:00 2026-01-18 22:00:00                7        2999 chargeback
     TXN200007      358 2026-01-28 05:00:00 2026-01-06 05:00:00               22         999 chargeback
     TXN200005      356 2026-01-29 07:00:00 2026-01-18 07:00:00               11        2999 chargeback
     TXN200000      351 2026-01-30 06:00:00 2026-01-15 06:00:00               15        1999 chargeback
```

## Q4_velocity_attacks_10min_buckets
```text
 user_id   ten_minute_bucket cluster_earliest_transaction_time  transaction_count
     200 2026-01-01 22:00:00               2026-01-01 22:00:00                  4
     314 2026-01-02 18:00:00               2026-01-02 18:00:00                  4
     154 2026-01-02 22:00:00               2026-01-02 22:00:00                  4
      59 2026-01-09 21:00:00               2026-01-09 21:00:00                  4
      73 2026-01-12 09:00:00               2026-01-12 09:00:00                  4
     229 2026-01-12 12:00:00               2026-01-12 12:00:00                  4
     287 2026-01-14 14:00:00               2026-01-14 14:00:00                  4
     345 2026-01-23 09:00:00               2026-01-23 09:00:00                  4
```

## Q5_high_risk_merchants
```text
 merchant_id  transaction_count  total_gmv_inr  avg_risk_score
          25                 17          15533       70.000000
          17                 13          13037       69.538462
          20                  9           4241       66.777778
          38                 10           3940       62.600000
          27                 16          13584       62.500000
          14                 12           6488       62.333333
           7                 16          15934       61.375000
          18                 11           7089       60.000000
```

## Q6_inner_join_category_gmv
```text
     category  transaction_count  gmv_inr
    ecommerce                104    79896
       travel                100    75250
      grocery                114    71936
food_delivery                 95    57205
entertainment                 63    56887
 bill_payment                 46    26304
     recharge                 25    15125
```

## Q7_left_join_all_merchants
```text
 merchant_id merchant_name  transaction_count
          16  Merchant_016                 20
          29  Merchant_029                 19
          37  Merchant_037                 19
           9  Merchant_009                 18
           3  Merchant_003                 17
          25  Merchant_025                 17
          30  Merchant_030                 17
           7  Merchant_007                 16
           8  Merchant_008                 16
          22  Merchant_022                 16
```

## Q8_chargebacks_by_region
```text
region  chargeback_count  chargeback_amount_inr
 North                14                  26286
 South                 6                  12944
  East                 5                   8195
  West                 3                   7047
```
