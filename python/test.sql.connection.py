
import os
import pyodbc

password = os.environ["NOVABANK_SQL_PASSWORD"]

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost,1434;"
    "DATABASE=NovaBankDB;"
    "UID=sa;"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;",
    timeout=10
)

cursor = connection.cursor()

cursor.execute("""
    SELECT
        DB_NAME() AS database_name,
        @@VERSION AS server_version
""")

row = cursor.fetchone()

print("Connection successful!")
print("Database:", row.database_name)
print("SQL Server:", row.server_version.splitlines()[0])

cursor.close()
connection.close()
