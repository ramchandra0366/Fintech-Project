USE NovaBankDB;
GO

SELECT
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;



SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME IN (
      'customers',
      'accounts',
      'merchants',
      'transactions',
      'payments'
  )
  AND COLUMN_NAME LIKE '%_id'
ORDER BY TABLE_NAME, COLUMN_NAME;


SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM dbo.customers
UNION ALL
SELECT 'accounts', COUNT(*) FROM dbo.accounts
UNION ALL
SELECT 'merchants', COUNT(*) FROM dbo.merchants
UNION ALL
SELECT 'transactions', COUNT(*) FROM dbo.transactions
UNION ALL
SELECT 'payments', COUNT(*) FROM dbo.payments;