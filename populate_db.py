from app import create_app, db
from app.models import Book, User
from datetime import datetime

app = create_app()


def populate_db():
    with app.app_context():
        books = [
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="9780743273565", quantity=5,
                 genre="Fiction", page_number=218, publication_year=1925),
            Book(title="1984", author="George Orwell", isbn="9780451524935", quantity=3, genre="Dystopian",
                 page_number=328, publication_year=1949),
            Book(title="To Kill a Mockingbird", author="Harper Lee", isbn="9780061120084", quantity=4, genre="Fiction",
                 page_number=281, publication_year=1960),
            Book(title="Pride and Prejudice", author="Jane Austen", isbn="9780141040349", quantity=6, genre="Romance",
                 page_number=279, publication_year=1813),
            Book(title="The Catcher in the Rye", author="J.D. Salinger", isbn="9780316769488", quantity=5,
                 genre="Fiction", page_number=277, publication_year=1951),
            Book(title="Moby-Dick", author="Herman Melville", isbn="9781503280786", quantity=2, genre="Adventure",
                 page_number=585, publication_year=1851),
            Book(title="The Hobbit", author="J.R.R. Tolkien", isbn="9780345339683", quantity=7, genre="Fantasy",
                 page_number=310, publication_year=1937),
            Book(title="War and Peace", author="Leo Tolstoy", isbn="9781853260629", quantity=3,
                 genre="Historical Fiction", page_number=1225, publication_year=1869),
            Book(title="Brave New World", author="Aldous Huxley", isbn="9780060850524", quantity=4, genre="Dystopian",
                 page_number=268, publication_year=1932),
            Book(title="The Odyssey", author="Homer", isbn="9780140268867", quantity=6, genre="Classic",
                 page_number=541, publication_year=-800),
            Book(title="Crime and Punishment", author="Fyodor Dostoevsky", isbn="9780140449136", quantity=3,
                 genre="Philosophical Fiction", page_number=430, publication_year=1866),
            Book(title="The Picture of Dorian Gray", author="Oscar Wilde", isbn="9780141439570", quantity=5,
                 genre="Gothic Fiction", page_number=254, publication_year=1890),
            Book(title="Frankenstein", author="Mary Shelley", isbn="9780486282114", quantity=4, genre="Gothic Fiction",
                 page_number=280, publication_year=1818),
            Book(title="Fahrenheit 451", author="Ray Bradbury", isbn="9781451673319", quantity=3, genre="Dystopian",
                 page_number=158, publication_year=1953),
            Book(title="The Shining", author="Stephen King", isbn="9780307743657", quantity=4, genre="Horror",
                 page_number=447, publication_year=1977)
        ]

        db.session.bulk_save_objects(books)

        users = [
            User(name="Alice Smith", birthdate=datetime(1990, 5, 14), email="alice@example.com",
                 phone_number="555-1234", member_since=datetime(2020, 1, 15)),
            User(name="Bob Johnson", birthdate=datetime(1985, 9, 22), email="bob@example.com", phone_number="555-5678",
                 member_since=datetime(2019, 11, 23)),
            User(name="Charlie Brown", birthdate=datetime(1992, 3, 10), email="charlie@example.com",
                 phone_number="555-9876", member_since=datetime(2021, 7, 9)),
            User(name="David Williams", birthdate=datetime(1995, 7, 30), email="david@example.com",
                 phone_number="555-4321", member_since=datetime(2022, 4, 2)),
            User(name="Eva White", birthdate=datetime(1991, 2, 18), email="eva@example.com", phone_number="555-8765",
                 member_since=datetime(2021, 5, 30))
        ]

        db.session.bulk_save_objects(users)

        db.session.commit()
        print("Database populated with books and users!")


if __name__ == '__main__':
    populate_db()
