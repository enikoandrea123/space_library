import pytest
from app import create_app
from app.forms import BookForm, UserForm


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_book_form_valid(client):
    form = BookForm(title="Test Book", author="Test Author", isbn="1234567890123", quantity=5, genre="Science Fiction",
                    publication_year=2022)

    assert form.validate()


def test_book_form_invalid_isbn(client):
    form = BookForm(title="Test Book", author="Test Author", isbn="invalidisbn", quantity=5, genre="Sci-Fi",
                    publication_year=2022)

    assert not form.validate()


def test_user_form_valid(client):
    form = UserForm(name="Jane Doe", email="jane@example.com", phone_number="1234567890", birthdate="2000-01-01")
    assert form.validate()
