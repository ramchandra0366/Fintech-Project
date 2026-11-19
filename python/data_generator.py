import csv
import random
from datetime import date, timedelta
from pathlib import Path


# =====================================================
# NOVABANK - SYNTHETIC BANKING DATA GENERATOR
# Project: Enterprise Banking Data Engineering Platform
# =====================================================

# STEP 1: CONFIGURATION

random.seed(42)

PROJECT_FOLDER = Path(__file__).resolve().parents[1]

OUTPUT_FOLDER = PROJECT_FOLDER / "data" / "raw"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

NUMBER_OF_CUSTOMERS = 1000
NUMBER_OF_ACCOUNTS = 1500
NUMBER_OF_MERCHANTS = 200
NUMBER_OF_TRANSACTIONS = 100000
NUMBER_OF_PAYMENTS = 30000

START_DATE = date(2026, 8, 1)


# STEP 2: SYNTHETIC CUSTOMER INFORMATION

FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Jamie",
    "Casey", "Riley", "Avery", "Sam", "Charlie",
    "Robin", "Drew", "Cameron", "Blake", "Sky"
]

LAST_NAMES = [
    "Smith", "Jones", "Taylor", "Brown", "Wilson",
    "Davies", "Evans", "Thomas", "Roberts", "Walker",
    "Wright", "Hall", "Green", "Adams", "Clark"
]

COUNTRIES = ["GB", "IE", "FR", "DE", "ES"]

ACCOUNT_TYPES = ["CURRENT", "SAVINGS"]

MERCHANT_CATEGORIES = [
    "GROCERY",
    "RESTAURANT",
    "TRAVEL",
    "RETAIL",
    "ENTERTAINMENT",
    "FUEL",
    "UTILITIES",
    "ONLINE"
]

PAYMENT_METHODS = [
    "DEBIT_CARD",
    "BANK_TRANSFER",
    "DIRECT_DEBIT",
    "ONLINE_PAYMENT",
    "MOBILE_PAYMENT"
]


def random_date(start_date, end_date):
    """Generate a random date between two dates."""

    days = (end_date - start_date).days

    return start_date + timedelta(
        days=random.randint(0, days)
    )


def write_csv(filename, fieldnames, records):
    """Save a collection of records into a CSV file."""

    file_path = OUTPUT_FOLDER / filename

    with file_path.open(
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"Created: {file_path.name}")


# STEP 3: GENERATE CUSTOMERS

print("\nGenerating customers...")

customers = []

for number in range(1, NUMBER_OF_CUSTOMERS + 1):

    customer = {
        "customer_id": f"CUST{number:05d}",

        "first_name": random.choice(FIRST_NAMES),

        "last_name": random.choice(LAST_NAMES),

        "date_of_birth": random_date(
            date(1950, 1, 1),
            date(2005, 12, 31)
        ).isoformat(),

        "customer_since": random_date(
            date(2018, 1, 1),
            date(2026, 7, 31)
        ).isoformat(),

        "country": random.choice(COUNTRIES),

        "risk_segment": random.choices(
            ["LOW", "MEDIUM", "HIGH"],
            weights=[70, 25, 5]
        )[0]
    }

    customers.append(customer)


write_csv(
    "customers.csv",
    list(customers[0].keys()),
    customers
)


# STEP 4: GENERATE BANK ACCOUNTS

print("\nGenerating bank accounts...")

accounts = []

for number in range(1, NUMBER_OF_ACCOUNTS + 1):

    # Ensure every customer receives at least one account.
    if number <= NUMBER_OF_CUSTOMERS:

        customer = customers[number - 1]

    else:

        customer = random.choice(customers)

    account = {
        "account_id": f"ACCT{number:06d}",

        "customer_id": customer["customer_id"],

        "account_type": random.choice(ACCOUNT_TYPES),

        "currency": "GBP",

        "account_open_date": random_date(
            date(2019, 1, 1),
            date(2026, 7, 31)
        ).isoformat(),

        "account_status": random.choices(
            ["ACTIVE", "CLOSED", "FROZEN"],
            weights=[95, 3, 2]
        )[0]
    }

    accounts.append(account)


write_csv(
    "accounts.csv",
    list(accounts[0].keys()),
    accounts
)


# STEP 5: GENERATE MERCHANTS

print("\nGenerating merchants...")

merchants = []

for number in range(1, NUMBER_OF_MERCHANTS + 1):

    merchant = {
        "merchant_id": f"MERCH{number:04d}",

        "merchant_name": (
            f"NovaMerchant_{number:04d}"
        ),

        "merchant_category": random.choice(
            MERCHANT_CATEGORIES
        ),

        "country": random.choice(COUNTRIES),

        "merchant_status": random.choice(
            ["ACTIVE", "ACTIVE", "ACTIVE", "INACTIVE"]
        )
    }

    merchants.append(merchant)


write_csv(
    "merchants.csv",
    list(merchants[0].keys()),
    merchants
)


# STEP 6: GENERATE BANK TRANSACTIONS

print("\nGenerating 100,000 transactions...")

transactions = []

transaction_statuses = [
    "SETTLED",
    "DECLINED",
    "PENDING"
]

for number in range(1, NUMBER_OF_TRANSACTIONS + 1):

    account = random.choice(accounts)

    merchant = random.choice(merchants)

    transaction_type = random.choices(
        ["CREDIT", "DEBIT"],
        weights=[30, 70]
    )[0]

    # Amount is generated in pence to avoid
    # floating-point monetary calculations.

    amount_in_pence = random.randint(
        100,
        500000
    )

    amount = f"{amount_in_pence / 100:.2f}"

    transaction = {
        "transaction_id": f"TXN{number:08d}",

        "account_id": account["account_id"],

        "transaction_date": random_date(
            START_DATE,
            date(2026, 10, 31)
        ).isoformat(),

        "transaction_type": transaction_type,

        "amount": amount,

        "currency": "GBP",

        "merchant_id": merchant["merchant_id"],

        "country": merchant["country"],

        "channel": random.choice(
            ["MOBILE", "WEB", "ATM", "BRANCH"]
        ),

        "transaction_status": random.choices(
            transaction_statuses,
            weights=[96, 3, 1]
        )[0]
    }

    transactions.append(transaction)


write_csv(
    "transactions.csv",
    list(transactions[0].keys()),
    transactions
)


# STEP 7: GENERATE PAYMENT RECORDS

print("\nGenerating payment records...")

selected_transactions = random.sample(
    transactions,
    NUMBER_OF_PAYMENTS
)

payments = []

for number, transaction in enumerate(
    selected_transactions,
    start=1
):

    payment = {
        "payment_id": f"PAY{number:08d}",

        "transaction_id": transaction["transaction_id"],

        "payment_method": random.choice(
            PAYMENT_METHODS
        ),

        "payment_status": transaction[
            "transaction_status"
        ],

        "payment_reference": f"REF{number:010d}"
    }

    payments.append(payment)


write_csv(
    "payments.csv",
    list(payments[0].keys()),
    payments
)


# STEP 8: DISPLAY FINAL REPORT

print("\n" + "=" * 45)
print("NOVABANK DATA GENERATION COMPLETED")
print("=" * 45)

print(f"Customers:     {len(customers):,}")
print(f"Accounts:      {len(accounts):,}")
print(f"Merchants:     {len(merchants):,}")
print(f"Transactions:  {len(transactions):,}")
print(f"Payments:      {len(payments):,}")

print("\nOutput folder:")
print(OUTPUT_FOLDER)

print("\nAll generated data is synthetic.")
print("No real banking information was used.")

print("\nDATA GENERATION SUCCESSFUL!")
