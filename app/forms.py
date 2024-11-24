from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class BorrowForm(FlaskForm):
    user = StringField('User Name', validators=[DataRequired()])
    submit = SubmitField('Borrow Book')

class ReturnForm(FlaskForm):
    submit = SubmitField('Return Book')
