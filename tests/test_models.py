import pytest
from app import app, db
from app.models import Book, Transaction
from datetime import datetime, timedelta

@pytest.fixture
def setup_books():
    book1 = Book(title="Test Book 1", author="Test Author 1", isbn="1234567890123")
    book2 = Book(title="Test Book 2", author="Test Author 2", isbn="1234567890456")
    db.session.add_all([book1, book2])
    db.session.commit()
    return book1, book2

def test_book_model_query(setup_books, querie=None):
    book1, book2 = setup_books
    queried_book1 = Book.query.filter_by(isbn="1234567890123").first()
    queried_book2 = Book.query.filter_by(isbn="1234567890456").first()

    assert queried_book1 is not None
    assert queried_book1.title == "Test Book 1"
    assert querie
