import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Book, User, Borrow


class TestModels(unittest.TestCase):
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

    def test_create_book(self):
        """Test the creation of a Book instance."""
        book = Book(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            quantity=5,
            publication_year=2023,
            genre='Fiction',
            page_number=250
        )
        with self.app.app_context():
            db.session.add(book)
            db.session.commit()

        added_book = Book.query.filter_by(isbn='1234567890123').first()
        self.assertIsNotNone(added_book)
        self.assertEqual(added_book.title, 'Test Book')
        self.assertEqual(added_book.author, 'Test Author')

    def test_create_user(self):
        """Test the creation of a User instance."""
        user = User(
            name='John Doe',
            birthdate=datetime(1990, 1, 1).date(),
            email='john.doe@example.com',
            phone_number='1234567890'
        )
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        added_user = User.query.filter_by(email='john.doe@example.com').first()
        self.assertIsNotNone(added_user)
        self.assertEqual(added_user.name, 'John Doe')
        self.assertEqual(added_user.phone_number, '1234567890')

    def test_create_borrow_and_relationship(self):
        """Test the creation of a Borrow instance and the relationship with Book and User."""
        book = Book(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            quantity=5,
            publication_year=2023,
            genre='Fiction',
            page_number=250
        )
        user = User(
            name='Jane Smith',
            birthdate=datetime(1992, 5, 15).date(),
            email='jane.smith@example.com',
            phone_number='0987654321'
        )
        borrow = Borrow(
            book_id=book.id,
            user_id=user.id,
            borrow_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=14)
        )

        with self.app.app_context():
            db.session.add(book)
            db.session.add(user)
            db.session.add(borrow)
            db.session.commit()

        added_borrow = Borrow.query.filter_by(book_id=book.id, user_id=user.id).first()
        self.assertIsNotNone(added_borrow)
        self.assertEqual(added_borrow.book.title, 'Test Book')
        self.assertEqual(added_borrow.user.name, 'Jane Smith')

    def test_late_fee(self):
        """Test the late fee calculation in the Borrow model."""
        book = Book(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            quantity=5,
            publication_year=2023,
            genre='Fiction',
            page_number=250
        )
        user = User(
            name='Alice Johnson',
            birthdate=datetime(1991, 4, 10).date(),
            email='alice.johnson@example.com',
            phone_number='1122334455'
        )
        borrow = Borrow(
            book_id=book.id,
            user_id=user.id,
            borrow_date=datetime.now(),
            return_date=datetime.now() + timedelta(days=16),  # 2 days late
            due_date=datetime.now() + timedelta(days=14)
        )

        with self.app.app_context():
            db.session.add(book)
            db.session.add(user)
            db.session.add(borrow)
            db.session.commit()

        late_fee = borrow.late_fee()
        self.assertEqual(late_fee, 2)  # 2 days late * $1 per day = $2

    def test_book_quantity_reduction_on_borrow(self):
        """Test that the book quantity reduces when a borrow is registered."""
        book = Book(
            title='Test Book for Quantity Check',
            author='Test Author',
            isbn='9876543210987',
            quantity=10,
            publication_year=2023,
            genre='Fiction',
            page_number=300
        )
        user = User(
            name='Bob White',
            birthdate=datetime(1989, 12, 25).date(),
            email='bob.white@example.com',
            phone_number='2233445566'
        )

        with self.app.app_context():
            db.session.add(book)
            db.session.add(user)
            db.session.commit()

            borrow = Borrow(
                book_id=book.id,
                user_id=user.id,
                borrow_date=datetime.now(),
                due_date=datetime.now() + timedelta(days=14)
            )
            db.session.add(borrow)
            db.session.commit()

            book.quantity -= 1
            db.session.commit()

        updated_book = Book.query.filter_by(isbn='9876543210987').first()
        self.assertEqual(updated_book.quantity, 9)

if __name__ == '__main__':
    unittest.main()
