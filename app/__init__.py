from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/library.db'
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Initialize the database with the app
    db.init_app(app)

    # Create the database file if it doesn't exist
    if not os.path.exists('instance'):
        os.makedirs('instance')
    if not os.path.exists('instance/library.db'):
        with app.app_context():
            db.create_all()

    # Import the routes here to avoid circular imports
    from app.routes import main
    app.register_blueprint(main)

    return app
