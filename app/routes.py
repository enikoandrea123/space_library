from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Book, Transaction
from app.forms import BorrowForm, ReturnForm
from datetime import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/catalog')
def catalog():
    books = Book.query.all()
    return render_template('catalog.html', books=books)

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow(book_id):
    form = BorrowForm()
    if form.validate_on_submit():
        transaction = Transaction(
            book_id=book_id, user=form.user.data, borrow_date=datetime.now()
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('borrow.html', form=form)

@app.route('/return/<int:book_id>', methods=['GET', 'POST'])
def return_book(book_id):
    form = ReturnForm()
    if form.validate_on_submit():
        transaction = Transaction.query.filter_by(book_id=book_id).first()
        transaction.return_date = datetime.now()
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('return.html', form=form)

@app.route('/report')
def report():
    overdue_books = Transaction.query.filter(Transaction.return_date == None, Transaction.due_date < datetime.now()).all()
    return render_template('report.html', overdue_books=overdue_books)
