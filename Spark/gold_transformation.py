
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg,
    to_date, when, lit
)

ROOT = Path(__file__).resolve().parent.parent
SILVER = ROOT / "data" / "silver"
GOLD = ROOT / "data" / "gold"

spark = (
    SparkSession.builder
    .appName("NovaBank-Gold-Transformation")
    .master("local[2]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

try:
    # Read cleaned Silver data
    transactions = spark.read.parquet(
        str(SILVER / "transactions")
    )

    payments = spark.read.parquet(
        str(SILVER / "payments")
    )

    # 1. Daily transaction reporting
    daily_transactions = (
        transactions
        .groupBy(
            to_date("transaction_date").alias("date"),
            "currency"
        )
        .agg(
            count("*").alias("transaction_count"),
            spark_sum("amount").alias("total_amount"),
            avg("amount").alias("average_amount")
        )
        .orderBy("date", "currency")
    )

    daily_transactions.write.mode("overwrite").parquet(
        str(GOLD / "daily_transactions")
    )

    print("\nDaily transaction summary:")
    daily_transactions.show(5, truncate=False)

    # 2. Overall transaction KPIs
    transaction_summary = (
        transactions
        .groupBy(
            "currency",
            "transaction_type",
            "transaction_status"
        )
        .agg(
            count("*").alias("transaction_count"),
            spark_sum("amount").alias("total_amount"),
            avg("amount").alias("average_amount")
        )
    )

    transaction_summary.write.mode("overwrite").parquet(
        str(GOLD / "transaction_summary")
    )

    print("\nTransaction KPI summary:")
    transaction_summary.show(5, truncate=False)

    # 3. Payment method reporting
    # Payments contain no amount column, so join
    # to transactions using transaction_id.
    payment_summary = (
        payments
        .join(
            transactions.select(
                "transaction_id",
                "amount",
                "currency"
            ),
            on="transaction_id",
            how="left"
        )
        .groupBy(
            "payment_method",
            "payment_status",
            "currency"
        )
        .agg(
            count("*").alias("payment_count"),
            count("amount").alias("matched_payment_count"),
            spark_sum("amount").alias("total_amount")
        )
    )

    payment_summary.write.mode("overwrite").parquet(
        str(GOLD / "payment_summary")
    )

    print("\nPayment summary:")
    payment_summary.show(5, truncate=False)

    # 4. Fraud review indicators
    # These are review flags, not confirmed fraud.
    fraud_indicators = (
        transactions
        .withColumn(
            "high_value_flag",
            when(col("amount") >= lit(5000), 1).otherwise(0)
        )
        .groupBy("currency", "country", "channel")
        .agg(
            count("*").alias("transaction_count"),
            spark_sum("high_value_flag").alias(
                "high_value_transaction_count"
            ),
            spark_sum("amount").alias("total_amount")
        )
    )

    fraud_indicators.write.mode("overwrite").parquet(
        str(GOLD / "fraud_indicators")
    )

    print("\nFraud review indicators:")
    fraud_indicators.show(5, truncate=False)

    print("\nNovaBank Gold transformation completed!")

finally:
    spark.stop()
