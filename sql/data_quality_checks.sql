USE NovaBankDB;
GO

SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM dbo.customers
UNION ALL
SELECT 'accounts', COUNT(*) FROM dbo.accounts
UNION ALL
SELECT 'merchants', COUNT(*) FROM dbo.merchants
UNION ALL
SELECT 'transactions', COUNT(*) FROM dbo.transactions
UNION ALL
SELECT 'payments', COUNT(*) FROM dbo.payments;


SELECT transaction_id, COUNT(*) AS duplicate_count
FROM dbo.transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;


SELECT COUNT(*) AS missing_accounts
FROM dbo.transactions AS t
LEFT JOIN dbo.accounts AS a
    ON t.account_id = a.account_id
WHERE a.account_id IS NULL;


SELECT COUNT(*) AS invalid_amounts
FROM dbo.transactions
WHERE amount IS NULL OR amount <= 0;




SELECT
    transaction_status,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount_gbp
FROM dbo.transactions
GROUP BY transaction_status
ORDER BY total_transactions DESC;