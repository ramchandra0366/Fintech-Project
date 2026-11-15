
# NovaBank — Data Engineering Architecture

## Architecture Diagram

```mermaid
flowchart TD
    A["Python Data Generator"]
    B["132,700 Synthetic Banking Records"]
    C["SQL Server 2025"]
    D["Azure ADLS Gen2 - Raw CSV Storage"]
    E["Local PySpark Bronze Layer"]
    F["Local PySpark Silver Layer"]
    G["Local PySpark Gold Layer"]
    H["Data Quality Validation"]
    I["Financial Reporting Datasets"]

    A --> B
    B --> C
    B --> D
    B --> E
    E --> F
    F --> G
    G --> H
    G --> I
```

## Technologies

- Python
- SQL Server 2025
- Azure Data Lake Storage Gen2
- Apache PySpark
- Parquet
- Git and GitHub

## Implementation Notes

The Azure storage workflow and local PySpark pipeline
are separate in the current implementation.

The local pipeline reads CSV files from data/raw/
and produces Bronze, Silver, and Gold Parquet datasets.
