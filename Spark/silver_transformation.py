
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_date,
    to_timestamp,
    trim,
)

ROOT = Path(__file__).resolve().parent.parent

BRONZE = ROOT / "data" / "bronze"
SILVER = ROOT / "data" / "silver"

# Primary keys for each dataset
PRIMARY_KEYS = {
    "customers": "customer_id",
    "accounts": "account_id",
    "merchants": "merchant_id",
    "transactions": "transaction_id",
    "payments": "payment_id",
}

# Columns to convert into dates
DATE_COLUMNS = {
    "customers": ["date_of_birth", "customer_since"],
    "accounts": ["account_open_date"],
    "merchants": [],
    "transactions": [],
    "payments": [],
}

spark = (
    SparkSession.builder
    .appName("NovaBank-Silver-Transformation")
    .master("local[2]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

try:
    for table, primary_key in PRIMARY_KEYS.items():

        print(f"\nProcessing {table}...")

        df = spark.read.parquet(str(BRONZE / table))

        # Remove surrounding spaces from text fields
        for field in df.schema.fields:
            if field.dataType.simpleString() == "string":
                df = df.withColumn(
                    field.name,
                    trim(col(field.name))
                )

        # Convert date columns
        for date_column in DATE_COLUMNS[table]:
            df = df.withColumn(
                date_column,
                to_date(col(date_column))
            )

        # Convert transaction types
        if table == "transactions":
            df = (
                df.withColumn(
                    "transaction_date",
                    to_timestamp(col("transaction_date"))
                )
                .withColumn(
                    "amount",
                    col("amount").cast("decimal(18,2)")
                )
            )

        # Validate primary keys
        before_count = df.count()

        invalid_keys = df.filter(
            col(primary_key).isNull()
            | (col(primary_key) == "")
        ).count()

        duplicate_keys = (
            df.groupBy(primary_key)
            .count()
            .filter(col("count") > 1)
            .count()
        )

        if invalid_keys > 0 or duplicate_keys > 0:
            raise ValueError(
                f"{table}: {invalid_keys} invalid keys, "
                f"{duplicate_keys} duplicated keys"
            )

        # Validate transaction amounts
        if table == "transactions":
            invalid_amounts = df.filter(
                col("amount").isNull()
                | (col("amount") <= 0)
            ).count()

            if invalid_amounts > 0:
                raise ValueError(
                    f"{invalid_amounts} invalid transaction amounts"
                )

        # Save validated Silver data
        output_path = SILVER / table

        df.write.mode("overwrite").parquet(
            str(output_path)
        )

        print(f"Rows: {before_count:,}")
        print(f"Invalid keys: {invalid_keys}")
        print(f"Duplicate key groups: {duplicate_keys}")
        print(f"Saved to: {output_path}")

    print("\nNovaBank Silver transformation completed!")

finally:
    spark.stop()
