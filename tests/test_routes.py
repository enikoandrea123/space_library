import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Book, User, Borrow
from flask import url_for


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the app and the database for all tests."""
        cls.app = create_app()
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up by dropping all tables after tests."""
        with cls.app.app_context():
            db.drop_all()

    def test_home_route(self):
        """Test the home page route."""
        with self.app.app_context():
            response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Library", response.data)

    def test_catalog_route(self):
        """Test the catalog route (book listing)."""
        with self.app.app_context():
            book = Book(
                title='Test Book',
                author='Test Author',
                isbn='1234567890123',
                quantity=5,
                publication_year=2023,
                genre='Fiction',
                page_number=300
            )
            db.session.add(book)
            db.session.commit()

            response = self.client.get(url_for('main.catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Book", response.data)

    def test_add_book_route(self):
        """Test the add book route."""
        with self.app.app_context():
            response = self.client.get(url_for('main.add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Book", response.data)

        with self.app.app_context():
            response = self.client.post(url_for('main.add_book'), data={
                'title': 'New Book',
                'author': 'New Author',
                'isbn': '9876543210123',
                'quantity': 3,
                'publication_year': 2023,
                'genre': 'Non-Fiction',
                'page_number': 250
            })
        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('main.catalog'), response.headers['Location'])

    def test_edit_book_route(self):
        """Test the edit book route."""
        with self.app.app_context():
            book = Book(
                title='Old Book',
                author='Old Author',
                isbn='1234567890123',
                quantity=5,
                publication_year=2020,
                genre='Fiction',
                page_number=200
            )
            db.session.add(book)
            db.session.commit()

            response = self.client.post(url_for('main.edit_book', book_id=book.id), data={
                'title': 'Updated Book',
                'author': 'Updated Author',
                'isbn': book.isbn,
                'quantity': book.quantity,
                'publication_year': book.publication_year,
                'genre': book.genre,
                'page_number': book.page_number
            })
        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('main.catalog'), response.headers['Location'])

        with self.app.app_context():
            updated_book = Book.query.get(book.id)
            self.assertEqual(updated_book.title, 'Updated Book')
            self.assertEqual(updated_book.author, 'Updated Author')

    def test_borrow_book_route(self):
        """Test the borrow book route."""
        with self.app.app_context():
            user = User(
                name='Test User',
                birthdate=datetime(1995, 6, 10).date(),
                email='test.user@example.com',
                phone_number='1234567890'
            )
            book = Book(
                title='Test Book to Borrow',
                author='Test Author',
                isbn='1234567890123',
                quantity=3,
                publication_year=2023,
                genre='Fiction',
                page_number=250
            )
            db.session.add(user)
            db.session.add(book)
            db.session.commit()

            response = self.client.post(url_for('main.borrow_book'), data={
                'user_id': user.id,
                'book_id': book.id
            })
        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('main.borrowed_books'), response.headers['Location'])

        with self.app.app_context():
            updated_book = Book.query.get(book.id)
            self.assertEqual(updated_book.quantity, 2)

    def test_delete_book_route(self):
        """Test the delete book route."""
        with self.app.app_context():
            book = Book(
                title='Book to Delete',
                author='Delete Author',
                isbn='1112223334445',
                quantity=5,
                publication_year=2023,
                genre='Fiction',
                page_number=150
            )
            db.session.add(book)
            db.session.commit()

            response = self.client.get(url_for('main.delete_book', book_id=book.id))
        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('main.catalog'), response.headers['Location'])

        with self.app.app_context():
            deleted_book = Book.query.get(book.id)
            self.assertIsNone(deleted_book)


if __name__ == '__main__':
    unittest.main()
