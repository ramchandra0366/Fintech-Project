
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit

# Find the main NovaBank project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input and output locations
RAW_PATH = PROJECT_ROOT / "data" / "raw"
BRONZE_PATH = PROJECT_ROOT / "data" / "bronze"

# NovaBank datasets
TABLES = [
    "customers",
    "accounts",
    "merchants",
    "transactions",
    "payments",
]

# Start Apache Spark locally
spark = (
    SparkSession.builder
    .appName("NovaBank-Bronze-Ingestion")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

try:
    for table in TABLES:
        input_path = RAW_PATH / f"{table}.csv"
        output_path = BRONZE_PATH / table

        print(f"\nProcessing {table}...")

        # Check that the CSV exists
        if not input_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {input_path}"
            )

        # Read raw CSV data
        df = (
            spark.read
            .option("header", True)
            .option("inferSchema", False)
            .csv(str(input_path))
        )

        # Add Bronze metadata columns
        bronze_df = (
            df.withColumn(
                "_source_file",
                lit(f"{table}.csv")
            )
            .withColumn(
                "_ingestion_timestamp",
                current_timestamp()
            )
        )

        # Save data in Parquet format
        bronze_df.write.mode("overwrite").parquet(
            str(output_path)
        )

        # Display record count
        row_count = bronze_df.count()

        print(f"Rows: {row_count:,}")
        print(f"Saved to: {output_path}")

    print("\nNovaBank Bronze ingestion completed!")

finally:
    spark.stop()
