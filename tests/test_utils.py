import pytest
from app.utils import calculate_late_fee
from app.models import Transaction
from datetime import datetime, timedelta

def test_calculate_late_fee_no_late_return():
    transaction = Transaction(
        book_id=1,
        user="John Doe",
        borrow_date=datetime.now(),
        return_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=14)
    )
    fee = calculate_late_fee(transaction)
    assert fee == 0

def test_calculate_late_fee_with_late_return():
    transaction = Transaction(
        book_id=1,
        user="John Doe",
        borrow_date=datetime.now(),
        return_date=datetime.now() + timedelta(days=16),  # 2 days late
        due_date=datetime.now() + timedelta(days=14)
    )
    fee = calculate_late_fee(transaction)
    assert fee == 2  # $1 per day late
