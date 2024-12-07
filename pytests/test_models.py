import pytest
from app import create_app, db
from app.models import Book, User, Borrow
from datetime import datetime, timedelta


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


from datetime import datetime


@pytest.fixture
def sample_user(app):
    birthdate = datetime.strptime("1990-01-01", "%Y-%m-%d").date()
    user = User(name="John Doe", email="john@example.com", phone_number="1234567890", birthdate=birthdate)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_book(app):
    book = Book(title="Sample Book", author="Author A", isbn="1234567890123", quantity=10, publication_year=2020,
                genre="Fiction")
    db.session.add(book)
    db.session.commit()
    return book


@pytest.fixture
def sample_borrow(app, sample_user, sample_book):
    borrow = Borrow(user_id=sample_user.id, book_id=sample_book.id, borrow_date=datetime.now(),
                    due_date=datetime.now() + timedelta(days=14))
    db.session.add(borrow)
    db.session.commit()
    return borrow


def test_late_fee(sample_borrow):
    borrow = sample_borrow
    borrow.return_date = borrow.due_date + timedelta(days=3)
    db.session.commit()
    assert borrow.late_fee() == 3
