from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/library.db'
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Initialize the database with the app
    db.init_app(app)

    # Import the routes here to avoid circular imports
    from app.routes import main
    app.register_blueprint(main)

    return app
