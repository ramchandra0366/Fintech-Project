SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;


SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM dbo.customers

UNION ALL

SELECT 'accounts', COUNT(*)
FROM dbo.accounts

UNION ALL

SELECT 'merchants', COUNT(*)
FROM dbo.merchants

UNION ALL

SELECT 'transactions', COUNT(*)
FROM dbo.transactions

UNION ALL

SELECT 'payments', COUNT(*)
FROM dbo.payments;
