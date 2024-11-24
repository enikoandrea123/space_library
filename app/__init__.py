import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "library.db")}'
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)

    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        try:
            db.create_all()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")

    return app
