
import csv
import os
from pathlib import Path

import pyodbc

PROJECT = Path(__file__).resolve().parents[1]
RAW_FOLDER = PROJECT / "data" / "raw"

password = os.environ.get("NOVABANK_SQL_PASSWORD")

if not password:
    raise RuntimeError(
        "NOVABANK_SQL_PASSWORD is not set."
    )

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost,1434;"
    "DATABASE=NovaBankDB;"
    "UID=sa;"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;",
    timeout=15
)

TABLES = [
    "customers",
    "accounts",
    "merchants",
    "transactions",
    "payments"
]

try:
    cursor = connection.cursor()

    for table in TABLES:
        file_path = RAW_FOLDER / f"{table}.csv"

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        with file_path.open(
            newline="",
            encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)
            columns = reader.fieldnames

            if not columns:
                raise ValueError(
                    f"No columns in {file_path}"
                )

            placeholders = ", ".join(
                "?" for _ in columns
            )

            column_names = ", ".join(
                f"[{column}]" for column in columns
            )

            sql = (
                f"INSERT INTO dbo.[{table}] "
                f"({column_names}) "
                f"VALUES ({placeholders})"
            )

            count = 0

            for record in reader:
                values = [
                    record[column]
                    for column in columns
                ]

                cursor.execute(sql, *values)
                count += 1

        connection.commit()

        print(f"{table}: {count:,} rows imported")

    print("NovaBank import completed!")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()
