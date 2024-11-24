from datetime import datetime, timedelta
from app import db


# Book model with additional details (genre, page number, publication year, and quantity)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Quantity of books available
    publication_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)

    # Relationship to Borrow model (One-to-many relationship)
    borrows = db.relationship('Borrow', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'


# User model with personal details
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    member_since = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship to Borrow model (One-to-many relationship)
    borrows = db.relationship('Borrow', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'


# Borrow model for tracking borrowed books by users
class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=14))

    def __repr__(self):
        return f'<Borrow {self.book.title} by {self.user.name}>'

    # Method to calculate late fee if applicable
    def late_fee(self):
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late * 1  # Late fee $1 per day
        return 0
