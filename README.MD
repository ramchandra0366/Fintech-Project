NovaBank — Azure FinTech Data Engineering Project
A hands-on banking data engineering project built with Python, SQL Server, Azure Data Factory, Azure Data Lake Storage, and Azure Databricks.
Project Overview
I built NovaBank to practice the steps involved in a banking data engineering project: generating data, loading it into SQL Server, moving files into Azure, transforming transactions with PySpark, and building a dashboard from the results.

The project uses 132,700 generated records across five related banking datasets. All data is synthetic.
Dataset	Records
Customers	1,000
Accounts	1,500
Merchants	200
Transactions	100,000
Payments	30,000
Total	132,700


Architecture
I worked on two parts of the project: a local Python, SQL Server, and PySpark pipeline, and a cloud workflow in Azure. They are separate implementations rather than one fully automated pipeline.
                   Python Synthetic Data Generator
                                |
                     Five Banking CSV Datasets
                                |
                +---------------+----------------+
                |                                |
                v                                v
       SQL Server 2025 (Docker)         Azure Data Lake Storage Gen2
       NovaBankDB                       bronze/raw/*.csv
       - Relational tables                      |
       - SQL analysis                  Azure Data Factory
       - Fraud indicators              (validated copy pipeline)
       - Reconciliation                         |
                |                     bronze/adf-output/transactions.csv
                |                                |
                |                   Azure Databricks (separate processing)
                |                   Bronze -> Silver -> Gold Delta tables
                |                                |
                |                       Databricks AI/BI Dashboard
                |                       - Transaction KPIs
                |                       - Daily trends
                |                       - Status breakdown
                |
                +-- Local PySpark workflow (from local project files)
                    Bronze -> Silver -> Gold -> Data quality checks
I tested the Azure Data Factory copy pipeline and the Databricks transformations separately. Connecting them into one scheduled workflow would be a future improvement.

See [`docs/architecture.md`](docs/architecture.md) for additional architecture notes.
Technology Stack
Technology	Implementation
Python	Synthetic banking data generation and loading scripts
SQL Server 2025 + Docker	Local NovaBankDB, SQL analysis and reconciliation
Apache PySpark	Local Medallion pipeline and Azure Databricks transformations
Azure Data Lake Storage Gen2	Cloud raw data and ADF copy output
Azure Data Factory	Validated cloud data-copy pipeline
Azure Databricks	Bronze, Silver and Gold data processing
Delta Lake + Unity Catalog	Managed analytics tables and data governance
Databricks AI/BI Dashboards	Published banking analytics dashboard
GitHub Actions	Automated Python test workflow
VS Code + GitHub	Development, version control and documentation


I used Databricks AI/BI Dashboards for reporting, so the project does not depend on Power BI.
Completed Work
1. Synthetic banking data and SQL Server
- Generated five related CSV datasets with 132,700 records.
- Loaded the datasets into SQL Server 2025 running in Docker (NovaBankDB).
- Implemented SQL-based data quality checks, banking analysis, fraud-indicator queries, and financial reconciliation.
- Used rule-based queries to flag potentially unusual activity for review.
2. Azure Data Lake Storage Gen2
- Provisioned the storage account stnovabankdev01 in Germany West Central.
- Created bronze, silver, and gold containers.
- Uploaded the five raw CSV files to the bronze/raw/ path.
3. Azure Data Factory ingestion
- Created the Azure Data Factory instance adf-novabank-dev02.
- Built and successfully debugged the pipeline PL_NovaBank_Bronze_Ingestion.
- Verified a copy of bronze/raw/transactions.csv to bronze/adf-output/transactions.csv.
- Configured managed-identity-based access for the storage account.
This ADF pipeline copies the transactions file. The other datasets were uploaded to ADLS separately, and Databricks processing was run independently.
4. Local PySpark Medallion pipeline
- Implemented local Bronze, Silver, and Gold processing.
- Added data cleaning, reporting outputs, and data quality checks.
- Created Spark/run_pipeline.py to run the local stages in sequence.
- Successfully executed and validated the local pipeline.
Run from the project root after setting up the project's local Python/Java environment:
./.venv-spark/bin/python Spark/run_pipeline.py
The local pipeline reads files from the project directory rather than directly from Azure Data Lake.
5. Azure Databricks Medallion Architecture
- Provisioned the Azure Databricks workspace dbw-novabank-dev01.
- Connected Databricks to ADLS Gen2 using an Azure Databricks Access Connector and a dedicated Unity Catalog storage credential.
- Processed 100,000 transactions through Bronze, Silver and Gold stages.
- Validated data and prepared Gold reporting tables, including:
  - dbw_novabank_dev01.novabank_gold.daily_transaction_summary
  - dbw_novabank_dev01.novabank_gold.transaction_status_summary
- Verified the status totals reconcile to the 100,000 source transactions.
6. Databricks AI/BI Dashboard
I built and published a Databricks AI/BI dashboard using the Gold tables. It brings together the transaction metrics and charts in one place.
Dashboard visual	Result
Total Transactions KPI	100,000
Total Transaction Amount KPI	249.98M (displayed total; currencies not converted)
Daily Transaction Volume	Line chart with daily transaction counts
Transaction Status Breakdown	Bar chart by transaction status


Transaction status breakdown:
Status	Transactions
SETTLED	95,998
DECLINED	2,991
PENDING	1,011
Total	100,000



The dashboard stays private in Databricks. I included a screenshot here so the results can be viewed without workspace access.
7. Testing and engineering practices
- Ran SQL data checks and reconciliation queries.
- Verified the local PySpark pipeline and its data quality checks.
- Validated the Azure Data Factory copy activity and its output file.
- Verified Databricks Gold reporting results.
- Configured a GitHub Actions Python test workflow.
- Used Azure managed identities and role assignments for cloud storage access.
- Configured an Azure budget alert to help monitor cloud spending.
What I Learned
- How to move from raw CSV files to cleaned, analysis-ready Delta tables.
- How to check record counts, missing IDs, duplicates, amounts, and dates before reporting.
- How Azure Data Factory, ADLS Gen2, and Databricks fit into a data engineering workflow.
- How to build useful charts and KPIs from Gold-layer tables.
- How to use GitHub Actions, documentation, and Azure cost alerts alongside the technical work.
Project Status
Completed: Data generation, SQL Server analysis, local PySpark pipeline, ADLS Gen2 uploads, a tested ADF copy pipeline, Databricks Bronze/Silver/Gold tables, validation checks, and a published Databricks dashboard.

Still to explore: Connecting ADF and Databricks into a scheduled pipeline, adding monitoring, and extending the dashboard.
Future Enhancements
- Orchestrate Databricks notebooks from Azure Data Factory and schedule incremental ingestion.
- Add stronger operational monitoring, alerts, and pipeline retry logic.
- Implement Change Data Capture (CDC), incremental processing, and Slowly Changing Dimensions (SCD).
- Add deployment automation for Azure infrastructure and Databricks assets.
- Add currency-aware financial reporting and additional customer, merchant, and payment dashboards.
- Explore Power BI if an appropriate organizational account becomes available.
Security and Cost
- All banking records are synthetic.
- Do not commit secrets, passwords, access keys, or local environment files.
- Use managed identities and least-privilege access where possible.
- Databricks SQL/serverless compute and other Azure resources may incur charges; budget alerts notify but do not automatically stop spending.
- The published dashboard is not publicly accessible by default; the repository screenshot provides a portfolio preview.