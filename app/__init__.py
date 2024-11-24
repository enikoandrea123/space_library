import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Get the absolute path to the 'library.db' file in the instance folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "library.db")}'
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Initialize the database with the app
    db.init_app(app)

    # Ensure that the database file exists
    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))

    # Import the routes here to avoid circular imports
    from app.routes import main
    app.register_blueprint(main)

    # Create the tables only once, after everything is set up
    with app.app_context():
        try:
            # Attempt to create the tables
            db.create_all()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")

    return app
