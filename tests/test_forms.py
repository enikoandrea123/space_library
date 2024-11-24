import pytest
from app import app
from app.forms import BorrowForm
from flask import url_for

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_borrow_form(client):
    response = client.get('/borrow/1')
    assert b'Borrow Book' in response.data

    response = client.post('/borrow/1', data={
        'user': 'John Doe'
    }, follow_redirects=True)
    assert b'Library Management System' in response.data
    assert b'John Doe' in response.data

def test_borrow_form_invalid(client):
    response = client.post('/borrow/1', data={
        'user': ''
    })
    assert b'This field is required.' in response.data
