from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from datetime import date


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)])
    author = StringField('Author', validators=[DataRequired(), Length(min=1, max=150)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=13, max=13)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    publication_year = IntegerField('Publication Year',
                                    validators=[DataRequired(), NumberRange(min=1000, max=date.today().year)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Save Book')


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=150)])
    birthdate = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=150)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Save User')


class BorrowForm(FlaskForm):
    user = StringField('Your Name', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Borrow Book')


class ReturnForm(FlaskForm):
    submit = SubmitField('Return Book')
