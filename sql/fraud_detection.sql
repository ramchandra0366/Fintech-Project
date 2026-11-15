USE NovaBankDB;
GO

SELECT TOP 20
    transaction_id,
    account_id,
    transaction_date,
    amount,
    transaction_type,
    transaction_status
FROM dbo.transactions
WHERE amount >= 4000
ORDER BY amount DESC;



SELECT TOP 20
    t.transaction_id,
    t.transaction_date,
    t.amount,
    c.customer_id,
    c.risk_segment
FROM dbo.transactions AS t
INNER JOIN dbo.accounts AS a
    ON t.account_id = a.account_id
INNER JOIN dbo.customers AS c
    ON a.customer_id = c.customer_id
WHERE c.risk_segment = 'HIGH'
ORDER BY t.amount DESC;




SELECT TOP 20
    account_id,
    CAST(transaction_date AS DATE) AS transaction_day,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount_gbp
FROM dbo.transactions
GROUP BY
    account_id,
    CAST(transaction_date AS DATE)
HAVING COUNT(*) >= 10
ORDER BY transaction_count DESC;







SELECT TOP 50
    t.transaction_id,
    t.account_id,
    t.transaction_date,
    t.amount,
    c.customer_id,
    c.risk_segment,

    CASE
        WHEN t.amount >= 4000
             AND c.risk_segment = 'HIGH'
            THEN 'HIGH_PRIORITY'

        WHEN t.amount >= 4000
            THEN 'LARGE_AMOUNT'

        WHEN c.risk_segment = 'HIGH'
            THEN 'HIGH_RISK_SEGMENT'

        ELSE 'NO_FLAG'
    END AS fraud_indicator

FROM dbo.transactions AS t
INNER JOIN dbo.accounts AS a
    ON t.account_id = a.account_id
INNER JOIN dbo.customers AS c
    ON a.customer_id = c.customer_id

WHERE
    t.amount >= 4000
    OR c.risk_segment = 'HIGH'

ORDER BY
    t.amount DESC;



WITH fraud_flags AS (
    SELECT
        t.transaction_id,

        CASE
            WHEN t.amount >= 4000
                 AND c.risk_segment = 'HIGH'
                THEN 'HIGH_PRIORITY'

            WHEN t.amount >= 4000
                THEN 'LARGE_AMOUNT'

            WHEN c.risk_segment = 'HIGH'
                THEN 'HIGH_RISK_SEGMENT'

            ELSE 'NO_FLAG'
        END AS fraud_indicator

    FROM dbo.transactions AS t
    JOIN dbo.accounts AS a
        ON t.account_id = a.account_id
    JOIN dbo.customers AS c
        ON a.customer_id = c.customer_id
)

SELECT
    fraud_indicator,
    COUNT(*) AS transaction_count
FROM fraud_flags
GROUP BY fraud_indicator
ORDER BY transaction_count DESC;