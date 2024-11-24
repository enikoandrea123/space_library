import pytest
from app import app, db
from app.models import Book, Transaction
from datetime import datetime, timedelta


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert b'Library Management System' in response.data


def test_catalog(client):
    response = client.get('/catalog')
    assert b'Book Catalog' in response.data


def test_borrow(client):
    book = Book(title="Test Book", author="Test Author", isbn="1234567890123")
    db.session.add(book)
    db.session.commit()

    response = client.get(f'/borrow/{book.id}')
    assert b'Borrow Book' in response.data
