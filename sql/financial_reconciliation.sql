USE NovaBankDB;
GO

SELECT
    COUNT(*) AS matched_payments
FROM dbo.payments AS p
INNER JOIN dbo.transactions AS t
    ON p.transaction_id = t.transaction_id;


SELECT
    p.payment_id,
    p.transaction_id,
    p.payment_status
FROM dbo.payments AS p
LEFT JOIN dbo.transactions AS t
    ON p.transaction_id = t.transaction_id
WHERE t.transaction_id IS NULL;


SELECT
    p.payment_id,
    p.transaction_id,
    p.payment_status,
    t.transaction_status
FROM dbo.payments AS p
JOIN dbo.transactions AS t
    ON p.transaction_id = t.transaction_id
WHERE p.payment_status <> t.transaction_status;





SELECT
    COUNT(*) AS total_payments,

    SUM(
        CASE
            WHEN t.transaction_id IS NOT NULL
            THEN 1 ELSE 0
        END
    ) AS matched_payments,

    SUM(
        CASE
            WHEN t.transaction_id IS NULL
            THEN 1 ELSE 0
        END
    ) AS missing_transactions,

    SUM(
        CASE
            WHEN t.transaction_id IS NOT NULL
             AND p.payment_status <> t.transaction_status
            THEN 1 ELSE 0
        END
    ) AS status_mismatches

FROM dbo.payments AS p
LEFT JOIN dbo.transactions AS t
    ON p.transaction_id = t.transaction_id;


SELECT
    CAST(transaction_date AS DATE) AS transaction_day,
    COUNT(*) AS settled_count,
    SUM(amount) AS settled_amount_gbp
FROM dbo.transactions
WHERE transaction_status = 'SETTLED'
GROUP BY CAST(transaction_date AS DATE)
ORDER BY transaction_day;