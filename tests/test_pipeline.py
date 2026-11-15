
import unittest
from decimal import Decimal


def is_valid_transaction(transaction):
    """Validate a banking transaction."""
    if not transaction.get("transaction_id"):
        return False

    try:
        amount = Decimal(str(transaction.get("amount")))
    except (ValueError, TypeError):
        return False

    return amount.is_finite() and amount > 0


def has_duplicate_ids(transactions):
    """Check for duplicate transaction IDs."""
    ids = [t["transaction_id"] for t in transactions]
    return len(ids) != len(set(ids))


class TestNovaBankPipeline(unittest.TestCase):

    def test_valid_transaction(self):
        transaction = {
            "transaction_id": "TXN00000001",
            "amount": "250.00"
        }
        self.assertTrue(is_valid_transaction(transaction))

    def test_missing_transaction_id(self):
        transaction = {
            "transaction_id": None,
            "amount": "250.00"
        }
        self.assertFalse(is_valid_transaction(transaction))

    def test_negative_amount(self):
        transaction = {
            "transaction_id": "TXN00000002",
            "amount": "-100.00"
        }
        self.assertFalse(is_valid_transaction(transaction))

    def test_zero_amount(self):
        transaction = {
            "transaction_id": "TXN00000003",
            "amount": "0"
        }
        self.assertFalse(is_valid_transaction(transaction))

    def test_duplicate_transaction_ids(self):
        transactions = [
            {"transaction_id": "TXN001"},
            {"transaction_id": "TXN001"}
        ]
        self.assertTrue(has_duplicate_ids(transactions))

    def test_unique_transaction_ids(self):
        transactions = [
            {"transaction_id": "TXN001"},
            {"transaction_id": "TXN002"}
        ]
        self.assertFalse(has_duplicate_ids(transactions))


if __name__ == "__main__":
    unittest.main()
