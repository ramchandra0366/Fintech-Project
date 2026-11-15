IF DB_ID('NovaBankDB') IS NULL
BEGIN
    CREATE DATABASE NovaBankDB;
END;
GO


USE NovaBankDB;
GO

SELECT DB_NAME() AS current_database;

SELECT name AS table_name
FROM sys.tables
ORDER BY name;