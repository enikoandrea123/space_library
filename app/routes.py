from sqlite3 import OperationalError, IntegrityError

from flask import render_template, request, redirect, url_for, Blueprint, flash
from app import db
from app.models import Book, User, Borrow
from app.forms import BookForm, UserForm, BorrowForm
from datetime import datetime, timedelta
import datetime

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/catalog')
def catalog():
    try:
        search = request.args.get('search', '').strip()
        genre = request.args.get('genre', '').strip()
        year = request.args.get('year', type=int)

        page = request.args.get('page', 1, type=int)
        per_page = 10

        query = Book.query

        if search:
            query = query.filter(
                (Book.title.ilike(f'%{search}%')) | (Book.author.ilike(f'%{search}%'))
            )

        if genre:
            query = query.filter_by(genre=genre)

        if year:
            query = query.filter_by(publication_year=year)

        books = query.paginate(page=page, per_page=per_page, error_out=False)

    except OperationalError:
        books = []
        error_message = "Error: Unable to access the database. Please try again later."
        return render_template('catalog.html', books=books, error_message=error_message)

    return render_template('catalog.html', books=books)


@main.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        quantity = request.form['quantity']
        genre = request.form['genre']
        publication_year = request.form['publication_year']

        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            quantity=quantity,
            genre=genre,
            publication_year=publication_year
        )

        try:
            db.session.add(new_book)
            db.session.commit()
            flash("Book added successfully!", "success")
            return redirect(url_for('main.catalog'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding book: {e}", "error")
            return render_template('add_book.html')

    return render_template('add_book.html')


@main.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.genre = form.genre.data
        book.quantity = form.quantity.data
        book.publication_year = form.publication_year.data

        try:
            db.session.commit()
            flash("Book updated successfully!", "success")
            return redirect(url_for('main.catalog'))  # Redirect to catalog
        except:
            db.session.rollback()
            flash("There was an issue updating the book.", "error")
            return render_template('edit_book.html', form=form)

    return render_template('edit_book.html', form=form)

@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            birthdate=datetime.datetime.strptime(form.birthdate.data, '%Y-%m-%d').date()
        )

        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('main.users'))

    return render_template('add_user.html', form=form)

@main.route('/delete_book/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully!", "success")
    except:
        db.session.rollback()
        flash("There was an issue deleting the book.", "error")
    return redirect(url_for('main.catalog'))


@main.route('/users', methods=['GET', 'POST'])
def users():
    search = request.args.get('search', '')
    user_id = request.args.get('id', '')

    query = User.query
    if search:
        query = query.filter(User.name.ilike(f'%{search}%') | User.email.ilike(f'%{search}%'))
    if user_id:
        query = query.filter(User.id == user_id)

    users = query.paginate(page=request.args.get('page', 1, type=int), per_page=5)

    return render_template('users.html', users=users)

@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    form = UserForm(obj=user)

    if request.method == 'POST' and form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        user.birthdate = form.birthdate.data

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('main.users'))

    return render_template('edit_user.html', form=form, user=user)

@main.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except IntegrityError:
        flash('Error: Unable to delete user due to existing references!', 'danger')

    return redirect(url_for('main.users'))
@main.route('/borrowed_books')
def borrowed_books():
    borrowed_books = Borrow.query.filter_by(return_date=None).all()
    for borrow in borrowed_books:
        borrow.late_fee_amount = borrow.late_fee()
    return render_template('borrowed_books.html', borrowed_books=borrowed_books)

@main.route('/borrow', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int)
        book_id = request.form.get('book_id', type=int)
        errors = {}

        user = User.query.get(user_id)
        if not user:
            errors['user_id'] = "User not found."

        book = Book.query.get(book_id)
        if not book:
            errors['book_id'] = "Book not found."
        elif book.quantity < 1:
            errors['book_id'] = "This book is currently unavailable."

        if errors:
            return render_template('borrowed_books.html', errors=errors)

        borrow = Borrow(
            user_id=user_id,
            book_id=book_id,
            borrow_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=14)
        )
        try:
            book.quantity -= 1
            db.session.add(borrow)
            db.session.commit()
            flash("Book borrowed successfully!", "success")
            return redirect(url_for('main.borrowed_books'))
        except:
            db.session.rollback()
            flash("An error occurred while borrowing the book.", "error")
            return redirect(url_for('main.borrow_book'))

    return render_template('borrowed_books.html')


@main.route('/borrow', methods=['GET', 'POST'])
def borrow_page():
    form = BorrowForm()

    borrowed_books = Borrow.query.join(Book, Borrow.book_id == Book.id) \
        .join(User, Borrow.user_id == User.id) \
        .add_columns(Book.title, Book.author, User.name, User.id, Book.isbn,
                     Borrow.borrow_date, Borrow.return_date, Borrow.due_date) \
        .all()

    return render_template('borrowed_books.html', form=form, borrowed_books=borrowed_books)


@main.route('/registrate_borrowing', methods=['GET', 'POST'])
def registrate_borrowing():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        isbn = request.form.get('isbn')
        borrow_date_str = request.form.get('borrow_date')
        due_date_str = request.form.get('due_date')

        user = User.query.get(user_id)
        book = Book.query.filter_by(isbn=isbn).first()

        if not user:
            error_message = "User not found."
            return render_template('registrate_borrowing.html', error_message=error_message)

        if not book:
            error_message = "Book not found."
            return render_template('registrate_borrowing.html', error_message=error_message)

        if book.quantity <= 0:
            error_message = f"The book '{book.title}' is currently out of stock."
            return render_template('registrate_borrowing.html', error_message=error_message)

        borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else borrow_date + timedelta(days=14)

        borrow = Borrow(
            book_id=book.id,
            user_id=user.id,
            borrow_date=borrow_date,
            due_date=due_date
        )
        db.session.add(borrow)

        book.quantity -= 1

        db.session.commit()

        success_message = f"Borrowing successfully registered for {user.name}. Remaining copies of '{book.title}': {book.quantity}"
        return render_template('registrate_borrowing.html', success_message=success_message)

    return render_template('registrate_borrowing.html')


@main.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrow = Borrow.query.get_or_404(borrow_id)

    if borrow.return_date is None:
        borrow.return_date = datetime.now()

        book = Book.query.get(borrow.book_id)
        if book:
            book.quantity += 1

        try:
            db.session.commit()
            return {"success": True}, 200
        except:
            db.session.rollback()
            return {"success": False}, 400
    return {"success": False}, 400