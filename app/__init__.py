from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/library.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

from app import routes
