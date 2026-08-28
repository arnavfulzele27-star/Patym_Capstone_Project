-- Part B: SQL fraud-pattern detection
-- All queries execute against paytm_payments.db.

-- Q1_basic_select_where_order_limit_distinct
SELECT DISTINCT payment_method, status
FROM transactions
WHERE amount_inr >= 2999
ORDER BY amount_inr DESC
LIMIT 10;

-- Q2_chargeback_impact
SELECT
    COUNT(*) AS chargeback_transactions,
    COUNT(DISTINCT user_id) AS unique_users_affected,
    SUM(amount_inr) AS total_chargeback_amount_inr
FROM transactions
WHERE status = 'chargeback';

-- Q3_burner_accounts
SELECT
    t.transaction_id,
    t.user_id,
    t.transaction_time,
    u.signup_date,
    CAST((julianday(t.transaction_time) - julianday(u.signup_date)) AS INTEGER) AS signup_age_days,
    t.amount_inr,
    t.status
FROM transactions AS t
INNER JOIN users AS u ON t.user_id = u.user_id
WHERE t.status = 'chargeback'
  AND julianday(t.transaction_time) >= julianday(u.signup_date)
  AND julianday(t.transaction_time) - julianday(u.signup_date) < 30
ORDER BY t.transaction_time, t.transaction_id;

-- Q4_velocity_attacks_10min_buckets
WITH bucketed AS (
    SELECT
        user_id,
        transaction_time,
        datetime(
            strftime('%Y-%m-%d %H:', transaction_time) ||
            printf('%02d:00', (CAST(strftime('%M', transaction_time) AS INTEGER) / 10) * 10)
        ) AS ten_minute_bucket
    FROM transactions
)
SELECT
    user_id,
    ten_minute_bucket,
    MIN(transaction_time) AS cluster_earliest_transaction_time,
    COUNT(*) AS transaction_count
FROM bucketed
GROUP BY user_id, ten_minute_bucket
HAVING COUNT(*) >= 3
ORDER BY cluster_earliest_transaction_time;

-- Q5_high_risk_merchants
SELECT
    merchant_id,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_gmv_inr,
    AVG(risk_score) AS avg_risk_score
FROM transactions
GROUP BY merchant_id
HAVING AVG(risk_score) >= 60
ORDER BY avg_risk_score DESC
LIMIT 10;

-- Q6_inner_join_category_gmv
SELECT
    m.category,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS gmv_inr
FROM transactions AS t
INNER JOIN merchants AS m ON t.merchant_id = m.merchant_id
GROUP BY m.category
HAVING SUM(t.amount_inr) > 0
ORDER BY gmv_inr DESC;

-- Q7_left_join_all_merchants
SELECT
    m.merchant_id,
    m.merchant_name,
    COUNT(t.transaction_id) AS transaction_count
FROM merchants AS m
LEFT JOIN transactions AS t ON m.merchant_id = t.merchant_id
GROUP BY m.merchant_id, m.merchant_name
ORDER BY transaction_count DESC, m.merchant_id
LIMIT 10;

-- Q8_chargebacks_by_region
SELECT
    m.region,
    COUNT(t.transaction_id) AS chargeback_count,
    SUM(t.amount_inr) AS chargeback_amount_inr
FROM merchants AS m
INNER JOIN transactions AS t ON m.merchant_id = t.merchant_id
WHERE t.status = 'chargeback'
GROUP BY m.region
HAVING COUNT(t.transaction_id) > 0
ORDER BY chargeback_count DESC;

