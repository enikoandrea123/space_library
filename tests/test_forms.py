import unittest
from datetime import date, datetime, timedelta
from app.forms import BookForm, UserForm, BorrowForm, ReturnForm
from app.models import Book, User, Borrow
from app.utils import calculate_late_fee


class TestBookForm(unittest.TestCase):
    def test_valid_book_form(self):
        form = BookForm(data={
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'quantity': 10,
            'publication_year': 2023,
            'genre': 'Fiction',
            'page_number': 250
        })
        self.assertTrue(form.validate(), "BookForm should validate with valid data.")

    def test_invalid_book_form_missing_title(self):
        form = BookForm(data={
            'author': 'Test Author',
            'isbn': '1234567890123',
            'quantity': 10,
            'publication_year': 2023,
            'genre': 'Fiction',
            'page_number': 250
        })
        self.assertFalse(form.validate(), "BookForm should not validate without a title.")

    def test_invalid_isbn_length(self):
        form = BookForm(data={
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '123',  # Invalid length
            'quantity': 10,
            'publication_year': 2023,
            'genre': 'Fiction',
            'page_number': 250
        })
        self.assertFalse(form.validate(), "BookForm should not validate with an invalid ISBN length.")

    def test_invalid_publication_year(self):
        form = BookForm(data={
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'quantity': 10,
            'publication_year': 999,  # Invalid year
            'genre': 'Fiction',
            'page_number': 250
        })
        self.assertFalse(form.validate(), "BookForm should not validate with an invalid publication year.")


class TestUserForm(unittest.TestCase):
    def test_valid_user_form(self):
        form = UserForm(data={
            'name': 'Test User',
            'birthdate': '1990-01-01',
            'email': 'testuser@example.com',
            'phone_number': '1234567890'
        })
        self.assertTrue(form.validate(), "UserForm should validate with valid data.")

    def test_invalid_email_format(self):
        form = UserForm(data={
            'name': 'Test User',
            'birthdate': '1990-01-01',
            'email': 'invalid-email',  # Invalid email format
            'phone_number': '1234567890'
        })
        self.assertFalse(form.validate(), "UserForm should not validate with an invalid email format.")

    def test_missing_phone_number(self):
        form = UserForm(data={
            'name': 'Test User',
            'birthdate': '1990-01-01',
            'email': 'testuser@example.com',
        })
        self.assertFalse(form.validate(), "UserForm should not validate without a phone number.")

    def test_invalid_birthdate_format(self):
        form = UserForm(data={
            'name': 'Test User',
            'birthdate': '01-01-1990',  # Wrong format
            'email': 'testuser@example.com',
            'phone_number': '1234567890'
        })
        self.assertFalse(form.validate(), "UserForm should not validate with an invalid birthdate format.")


class TestBorrowForm(unittest.TestCase):
    def test_valid_borrow_form(self):
        form = BorrowForm(data={
            'user': 'Test User'
        })
        self.assertTrue(form.validate(), "BorrowForm should validate with valid data.")

    def test_missing_user_name(self):
        form = BorrowForm(data={})
        self.assertFalse(form.validate(), "BorrowForm should not validate without a user name.")


class TestReturnForm(unittest.TestCase):
    def test_valid_return_form(self):
        form = ReturnForm(data={})
        self.assertTrue(form.validate(), "ReturnForm should validate as it has no required fields.")


class TestUtils(unittest.TestCase):
    def test_calculate_late_fee_no_late(self):
        borrow = Borrow(
            borrow_date=datetime(2023, 11, 1),
            due_date=datetime(2023, 11, 15),
            return_date=datetime(2023, 11, 14)
        )
        self.assertEqual(calculate_late_fee(borrow), 0, "Late fee should be 0 for on-time returns.")

    def test_calculate_late_fee_late(self):
        borrow = Borrow(
            borrow_date=datetime(2023, 11, 1),
            due_date=datetime(2023, 11, 15),
            return_date=datetime(2023, 11, 20)
        )
        self.assertEqual(calculate_late_fee(borrow), 5, "Late fee should be calculated correctly for late returns.")

    def test_calculate_late_fee_no_return_date(self):
        borrow = Borrow(
            borrow_date=datetime(2023, 11, 1),
            due_date=datetime(2023, 11, 15),
            return_date=None
        )
        self.assertEqual(calculate_late_fee(borrow), 0, "Late fee should be 0 if no return date is set.")


if __name__ == '__main__':
    unittest.main()
