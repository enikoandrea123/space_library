from sqlite3 import OperationalError

from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models import Book, User, Borrow
from app.forms import BookForm, UserForm, BorrowForm
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

# Homepage with navigation options
@main.route('/')
def home():
    return render_template('home.html')

# Book Catalog Page
@main.route('/catalog')
def catalog():
    try:
        # Attempt to query the database
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Number of books per page
        books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    except OperationalError:
        # If there's an OperationalError, the database might be missing or corrupt
        books = []  # Fallback to an empty book list
        error_message = "Error: Unable to access the database. Please try again later."
        return render_template('catalog.html', books=books, error_message=error_message)

    # If the database is available, return the paginated books
    return render_template('catalog.html', books=books)
# Add Book Page
@main.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            quantity=form.quantity.data,
            genre=form.genre.data,
            page_number=form.page_number.data,
            publication_year=form.publication_year.data
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('main.catalog'))
    return render_template('add_book.html', form=form)

# Edit Book Page
@main.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.quantity = form.quantity.data
        book.genre = form.genre.data
        book.page_number = form.page_number.data
        book.publication_year = form.publication_year.data
        db.session.commit()
        return redirect(url_for('main.catalog'))
    return render_template('edit_book.html', form=form, book=book)

# Delete Book Page
@main.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('main.catalog'))
    return render_template('confirm_delete_book.html', book=book)


# User Catalog Page
@main.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Add User Page
@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            birthdate=form.birthdate.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            member_since=datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.users'))
    return render_template('add_user.html', form=form)

# Edit User Page
@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.birthdate = form.birthdate.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        db.session.commit()
        return redirect(url_for('main.users'))
    return render_template('edit_user.html', form=form, user=user)

# Delete User Page
@main.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.users'))

# Borrowed Books Catalog Page
@main.route('/borrowed_books')
def borrowed_books():
    borrowed_books = Borrow.query.filter_by(return_date=None).all()
    return render_template('borrowed_books.html', borrowed_books=borrowed_books)

# Borrow Book Page
@main.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow(book_id):
    form = BorrowForm()
    book = Book.query.get(book_id)
    if not book:
        return redirect(url_for('main.catalog'))  # Redirect if book doesn't exist

    if form.validate_on_submit():
        # Check if the book is already borrowed
        existing_borrow = Borrow.query.filter_by(book_id=book_id, return_date=None).first()
        if existing_borrow:
            form.user.errors.append('This book has already been borrowed.')
            return render_template('borrow.html', form=form)

        new_borrow = Borrow(
            book_id=book_id,
            user=form.user.data,
            borrow_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=14)
        )
        db.session.add(new_borrow)
        db.session.commit()
        return redirect(url_for('main.borrowed_books'))
    return render_template('borrow.html', form=form)


# Return Book Page
@main.route('/return/<int:book_id>', methods=['GET', 'POST'])
def return_book(book_id):
    borrow = Borrow.query.filter_by(book_id=book_id, return_date=None).first()
    if borrow:
        borrow.return_date = datetime.now()
        db.session.commit()
        return redirect(url_for('main.borrowed_books'))
    return redirect(url_for('main.borrowed_books'))
