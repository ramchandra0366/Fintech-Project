# NovaBank — Azure FinTech Data Engineering Project

## Project Overview

NovaBank is a fictional banking data engineering project demonstrating an end-to-end data pipeline using Python, SQL Server 2025, Azure Data Lake Storage Gen2, and Apache PySpark.

The project processes **132,700 synthetic banking records** across five datasets:

| Dataset | Records |
|---|---:|
| Customers | 1,000 |
| Accounts | 1,500 |
| Merchants | 200 |
| Transactions | 100,000 |
| Payments | 30,000 |
| **Total** | **132,700** |

## Data Pipeline Architecture

```text
Synthetic Banking Data (Python)
              |
              v
        CSV Raw Data
              |
              +----> SQL Server 2025
              |      Data quality, fraud analysis,
              |      and financial reconciliation
              |
              +----> Azure Data Lake Storage Gen2
              |      Bronze container (raw CSV)
              |
              v
       Local Apache PySpark
              |
              v
       Bronze Layer (Parquet)
              |
              v
       Silver Layer (Cleaned Data)
              |
              v
       Gold Layer (Business KPIs)
              |
              v
       Data Quality Validation
```

*The Azure raw-data upload and local PySpark processing are separate parts of this project. The local Spark pipeline currently reads files from the project directory.*

## Key Features

- Synthetic banking data generation using Python
- SQL Server data ingestion and SQL-based analysis
- Azure Data Lake Storage Gen2 integration
- Bronze, Silver, and Gold data transformations using PySpark
- Transaction and payment reporting
- High-value transaction review indicators
- Automated pipeline execution using `Spark/run_pipeline.py`
- Data quality and reconciliation checks

## Pipeline Execution

Run the complete local pipeline from the project root:

```bash
./.venv-spark/bin/python Spark/run_pipeline.py
```

The pipeline runs Bronze ingestion, Silver transformations, Gold reporting, and data quality checks.

**Validation result:** All checks passed in the completed local pipeline run.

## Project Status

**Completed:** Local Bronze–Silver–Gold pipeline, SQL analysis, Azure raw-data storage integration, automated execution, and validation.

**Future enhancements:** Cloud orchestration, monitoring, and Power BI dashboards.




Enterprise Banking Data Engineering Platform — NovaBank

End-to-End Azure FinTech Data Engineering Portfolio Project
A banking data engineering portfolio project demonstrating how synthetic financial data can be generated, validated, stored, transformed, orchestrated, and analysed using Python, SQL Server, Microsoft Azure, Databricks, PySpark, Delta Lake, Azure Data Factory, and Power BI.

Project Status: In Development — local Python and SQL Server implementation is underway, with Azure cloud integration planned.

1. Project Overview
NovaBank is a fictional digital bank designed to simulate an enterprise banking data environment.

The project focuses on building an end-to-end data engineering platform capable of processing banking datasets, including:

Customer information
Bank accounts
Financial transactions
Merchant information
Payment records
The platform aims to provide reliable data pipelines, high-quality financial data, automated processing, and business-ready datasets for reporting and analytics.

All datasets are synthetically generated. No real customer or financial information is used.

2. Business Problem
Financial institutions process large volumes of data from multiple banking systems. This creates challenges involving data quality, integration, reconciliation, reporting, and operational reliability.

The NovaBank platform is designed to address these challenges by:

Integrating data from multiple banking datasets.
Identifying missing, duplicate, and invalid records.
Maintaining relationships between customers, accounts, and transactions.
Reconciling payment and transaction information.
Supporting financial reporting and customer activity analysis.
Identifying potentially unusual transaction patterns.
Automating and monitoring data processing pipelines.
3. Technology Stack
Technology	Purpose
Python	Synthetic data generation, ETL and data validation
CSV	Raw banking data storage
SQL Server 2025	Relational database for banking datasets
SQL Server Management Studio (SSMS)	Database management and SQL querying
pyodbc	Connecting Python to SQL Server
Azure Data Lake Storage Gen2	Scalable cloud data storage
Azure Databricks	Distributed data processing and transformation
PySpark	Large-scale data processing
Delta Lake	Reliable data storage with ACID transactions
Azure Data Factory	Data pipeline orchestration and scheduling
Power BI	Financial reporting and interactive dashboards
Git & GitHub	Version control and project documentation
4. Data Architecture
Current Local Architecture
Synthetic Banking Data
          |
          v
  Python Data Generator
          |
          v
      CSV Files
          |
          v
 Python ETL & Validation
          |
          v
    SQL Server 2025
          |
          v
       NovaBankDB
          |
          v
 Customers | Accounts | Merchants
 Transactions | Payments
          |
          v
   SQL Analysis & Reporting
Planned Azure Architecture
       Synthetic Data Sources
                |
                v
        Azure Data Factory
                |
                v
    Azure Data Lake Storage Gen2
                |
                v
        BRONZE — Raw Data
                |
                v
       Azure Databricks
            PySpark
                |
                v
       SILVER — Clean Data
                |
                v
    Data Quality & Validation
                |
                v
      GOLD — Business Data
                |
                v
    Financial Analytics Models
                |
                v
             Power BI
The Azure implementation will follow the Medallion Architecture, consisting of three layers:

Bronze Layer: Stores raw source data for traceability and reprocessing.

Silver Layer: Contains cleaned, validated, standardised, and deduplicated data.

Gold Layer: Provides business-ready datasets for financial analytics, reconciliation, and reporting.

5. Synthetic Banking Datasets
The project uses five related synthetic datasets.

Dataset	Target Records	Description
Customers	1,000	Fictional customer profiles
Accounts	1,500	Customer-linked bank accounts
Merchants	200	Fictional merchant records
Transactions	100,000	Credit and debit transactions
Payments	30,000	Payment records linked to transactions
Total	132,700	Synthetic records
The record counts represent the configured data generation targets and are verified during the loading process.

Database Relationships
One customer can own multiple accounts.
One account can contain multiple transactions.
One merchant can be associated with multiple transactions.
A transaction may have an associated payment record.
SQL Server primary keys and foreign keys are used to maintain relational integrity.

6. Project Folder Structure
FinTechProject/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── accounts.csv
│   │   ├── merchants.csv
│   │   ├── transactions.csv
│   │   └── payments.csv
│   ├── processed/
│   └── test_data/
│
├── python/
│   ├── data_generator.py
│   ├── test_sql_connection.py
│   └── database_loader_sqlserver.py
│
├── sql/
│   ├── schema/
│   │   └── create_tables_sqlserver.sql
│   └── queries/
│
├── databricks/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── data_factory/
├── powerbi/
├── tests/
├── docs/
│
├── README.md
└── .gitignore
This represents the intended repository structure. Additional files will be added as the project progresses.

7. Local Environment Setup
Prerequisites
Python 3.x
Visual Studio Code
SQL Server 2025
SQL Server Management Studio
Microsoft ODBC Driver 17 or 18 for SQL Server
Git
Step 1 — Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
Replace the placeholders with your repository details once published.

Step 2 — Install Python dependencies
python -m pip install pyodbc
Step 3 — Generate synthetic banking datasets
python python/data_generator.py
The generator produces CSV files in the data/raw/ directory.

Step 4 — Create the SQL Server database
Open SSMS and connect to the local SQL Server instance.

Execute the database schema script:

sql/schema/create_tables_sqlserver.sql
The script creates the NovaBankDB database and five relational tables.

Step 5 — Test the database connection
python python/test_sql_connection.py
The local connection uses Windows authentication.

Step 6 — Load the banking datasets
python python/database_loader_sqlserver.py
The loader imports synthetic banking records into SQL Server.

Before rerunning the loader, verify existing records to avoid duplicate primary-key errors.

8. Data Quality Framework
The platform will implement data quality rules to identify:

Missing customer or account identifiers.
Duplicate transaction IDs.
Invalid transaction types.
Negative or zero transaction amounts.
Invalid date formats.
Broken foreign-key relationships.
Invalid transaction statuses.
Payment and transaction inconsistencies.
Data quality checks will be applied during ingestion and transformation, with exceptions recorded for investigation.

9. Financial Reconciliation
Financial reconciliation is an important component of banking data engineering.

The planned reconciliation framework will include:

Transaction-to-payment matching.
Missing payment identification.
Payment status comparison.
Transaction count reconciliation.
Financial amount reconciliation.
Source-to-target record count validation.
Detection of unexpected financial differences.
Financial reporting will distinguish completed transactions from declined and pending activity.

10. Fraud-Indicator Analysis
The project will implement rule-based indicators for potentially unusual banking activity.

Examples include:

High-value transactions.
Repeated transactions within short time intervals.
Unusually high transaction frequency.
Sudden changes in transaction amounts.
Unexpected account activity patterns.
These rules provide analytical indicators only and do not establish that fraud has occurred.

11. Power BI Reporting
The planned Power BI dashboards will provide insights into:

Total settled transaction value.
Credit and debit activity.
Monthly transaction trends.
Transaction status distribution.
Customer and account activity.
Merchant transaction performance.
Data quality metrics.
Reconciliation exceptions.
Fraud-indicator trends.
The reporting layer will use curated Gold datasets from the data platform.

12. Testing and Validation
The project will include testing for:

Synthetic data generation.
CSV structure and required fields.
Duplicate record detection.
SQL primary-key and foreign-key integrity.
Transaction amount calculations.
Source-to-target record counts.
Data transformation logic.
Financial reconciliation accuracy.
Pipeline rerun behaviour.
13. Security and Cost Management
The project follows several security and cost-management principles:

Use synthetic banking data exclusively.
Do not store passwords or access keys in source code.
Exclude secrets and local environment files from GitHub.
Apply least-privilege access to cloud resources.
Review Azure pricing before provisioning resources.
Configure Azure budgets and cost alerts before using chargeable services.
Stop unused cloud compute resources.
Monitor pipeline activity and operational failures.
14. Project Development Roadmap
Python fundamentals and CSV processing.
Generate synthetic banking datasets.
Create SQL Server database and relational tables.
Complete automated loading of all five banking datasets.
Develop advanced SQL financial analysis.
Learn Azure fundamentals and cost controls.
Configure Azure Data Lake Storage Gen2.
Implement Bronze ingestion using Databricks.
Develop Silver transformations with PySpark.
Build Gold datasets using Delta Lake.
Implement automated data quality checks.
Develop financial reconciliation pipelines.
Implement fraud-indicator rules.
Orchestrate data pipelines using Azure Data Factory.
Configure security and monitoring.
Build Power BI dashboards.
Add automated testing and documentation.
Publish final architecture and project demonstration.
15. Data Engineering Skills Demonstrated
Python and ETL: Data generation, CSV processing, validation, automation, and error handling.

SQL and Database Design: Relational modelling, primary keys, foreign keys, joins, aggregations, and financial reporting.

Azure Data Engineering: Data Lake Storage, Databricks, PySpark, Delta Lake, and Azure Data Factory.

Data Reliability: Data quality, reconciliation, testing, and pipeline monitoring.

Business Intelligence: Financial analytics, reporting models, and Power BI dashboards.

Engineering Practices: Git, GitHub, documentation, security, and cloud cost management.

16. Future Enhancements
Potential future improvements include:

Incremental data ingestion.
Change Data Capture (CDC).
Slowly Changing Dimensions (SCD).
Automated monitoring and alerts.
CI/CD pipelines.
Advanced anomaly detection.
Additional synthetic banking products and data sources.
17. Disclaimer
NovaBank is a fictional banking organisation created solely for educational and portfolio purposes.

All customer, account, merchant, transaction, and payment data is synthetic.

The project is not affiliated with a real financial institution and is not intended for production banking operations.

Project Name: Enterprise Banking Data Engineering Platform
Fictional Organisation: NovaBank
Domain: Financial Services / FinTech
Focus: Azure Data Engineering, Python, SQL Server, PySpark, Delta Lake, Data Quality and Financial Analytics