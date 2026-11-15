
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum,
    coalesce, lit
)

ROOT = Path(__file__).resolve().parent.parent

BRONZE = ROOT / "data" / "bronze"
SILVER = ROOT / "data" / "silver"
GOLD = ROOT / "data" / "gold"

TABLES = {
    "customers": "customer_id",
    "accounts": "account_id",
    "merchants": "merchant_id",
    "transactions": "transaction_id",
    "payments": "payment_id"
}

spark = (
    SparkSession.builder
    .appName("NovaBank-Data-Quality")
    .master("local[2]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

failures = []

def check(condition, description):
    if condition:
        print(f"PASS: {description}")
    else:
        print(f"FAIL: {description}")
        failures.append(description)

try:
    print("\n1. BRONZE VS SILVER ROW COUNTS")

    for table, primary_key in TABLES.items():
        bronze = spark.read.parquet(
            str(BRONZE / table)
        )
        silver = spark.read.parquet(
            str(SILVER / table)
        )

        bronze_count = bronze.count()
        silver_count = silver.count()

        check(
            bronze_count == silver_count,
            f"{table}: Bronze={bronze_count:,}, "
            f"Silver={silver_count:,}"
        )

        null_keys = silver.filter(
            col(primary_key).isNull()
            | (col(primary_key) == "")
        ).count()

        duplicate_keys = (
            silver.groupBy(primary_key)
            .count()
            .filter(col("count") > 1)
            .count()
        )

        check(
            null_keys == 0 and duplicate_keys == 0,
            f"{table}: valid unique primary keys"
        )

    print("\n2. TRANSACTION AMOUNT VALIDATION")

    transactions = spark.read.parquet(
        str(SILVER / "transactions")
    )

    invalid_amounts = transactions.filter(
        col("amount").isNull()
        | (col("amount") <= 0)
    ).count()

    check(
        invalid_amounts == 0,
        f"Invalid transaction amounts: {invalid_amounts}"
    )

    print("\n3. PAYMENT REFERENTIAL INTEGRITY")

    payments = spark.read.parquet(
        str(SILVER / "payments")
    )

    unmatched_payments = (
        payments.join(
            transactions.select("transaction_id"),
            on="transaction_id",
            how="left_anti"
        )
        .count()
    )

    check(
        unmatched_payments == 0,
        f"Payments without transactions: {unmatched_payments}"
    )

    print("\n4. GOLD FINANCIAL RECONCILIATION")

    gold_daily = spark.read.parquet(
        str(GOLD / "daily_transactions")
    )

    # Compare totals separately for each currency.
    silver_totals = (
        transactions.groupBy("currency")
        .agg(
            count("*").alias("silver_count"),
            spark_sum("amount").alias("silver_amount")
        )
    )

    gold_totals = (
        gold_daily.groupBy("currency")
        .agg(
            spark_sum("transaction_count").alias("gold_count"),
            spark_sum("total_amount").alias("gold_amount")
        )
    )

    comparison = silver_totals.join(
        gold_totals,
        on="currency",
        how="full_outer"
    )

    mismatches = comparison.filter(
        col("silver_count").isNull()
        | col("gold_count").isNull()
        | (col("silver_count") != col("gold_count"))
        | col("silver_amount").isNull()
        | col("gold_amount").isNull()
        | (col("silver_amount") != col("gold_amount"))
    ).count()

    check(
        mismatches == 0,
        f"Gold daily totals reconcile with Silver: "
        f"{mismatches} currency mismatches"
    )

    print("\n5. GOLD DATASET CHECKS")

    for table in [
        "daily_transactions",
        "transaction_summary",
        "payment_summary",
        "fraud_indicators"
    ]:
        df = spark.read.parquet(
            str(GOLD / table)
        )

        rows = df.count()

        check(
            rows > 0,
            f"{table}: {rows:,} rows"
        )

    print("\n" + "=" * 45)

    if failures:
        print(f"DATA QUALITY FAILED: {len(failures)} checks")
        for failure in failures:
            print(f" - {failure}")
        raise ValueError("NovaBank data quality checks failed")

    print("ALL NOVABANK DATA QUALITY CHECKS PASSED!")

finally:
    spark.stop()
