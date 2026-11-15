USE NovaBankDB;
GO

-- 1. CUSTOMERS
IF OBJECT_ID('dbo.customers', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.customers (
        customer_id VARCHAR(20) PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        date_of_birth DATE,
        customer_since DATE,
        country VARCHAR(2),
        risk_segment VARCHAR(20)
    );
END;
GO

-- 2. ACCOUNTS
IF OBJECT_ID('dbo.accounts', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.accounts (
        account_id VARCHAR(20) PRIMARY KEY,
        customer_id VARCHAR(20) NOT NULL,
        account_type VARCHAR(30),
        currency VARCHAR(3),
        account_open_date DATE,
        account_status VARCHAR(20),

        CONSTRAINT fk_accounts_customers
            FOREIGN KEY (customer_id)
            REFERENCES dbo.customers(customer_id)
    );
END;
GO

-- 3. MERCHANTS
IF OBJECT_ID('dbo.merchants', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.merchants (
        merchant_id VARCHAR(20) PRIMARY KEY,
        merchant_name VARCHAR(100),
        merchant_category VARCHAR(50),
        country VARCHAR(2),
        merchant_status VARCHAR(20)
    );
END;
GO

-- 4. TRANSACTIONS
IF OBJECT_ID('dbo.transactions', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.transactions (
        transaction_id VARCHAR(20) PRIMARY KEY,
        account_id VARCHAR(20) NOT NULL,
        transaction_date DATE,
        transaction_type VARCHAR(20),
        amount DECIMAL(15,2),
        currency VARCHAR(3),
        merchant_id VARCHAR(20),
        country VARCHAR(2),
        channel VARCHAR(20),
        transaction_status VARCHAR(20),

        CONSTRAINT fk_transactions_accounts
            FOREIGN KEY (account_id)
            REFERENCES dbo.accounts(account_id),

        CONSTRAINT fk_transactions_merchants
            FOREIGN KEY (merchant_id)
            REFERENCES dbo.merchants(merchant_id)
    );
END;
GO

-- 5. PAYMENTS
IF OBJECT_ID('dbo.payments', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.payments (
        payment_id VARCHAR(20) PRIMARY KEY,
        transaction_id VARCHAR(20) NOT NULL,
        payment_method VARCHAR(30),
        payment_status VARCHAR(20),
        payment_reference VARCHAR(30),

        CONSTRAINT fk_payments_transactions
            FOREIGN KEY (transaction_id)
            REFERENCES dbo.transactions(transaction_id)
    );
END;
GO