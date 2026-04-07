"""
Data Loader — Sample Data Initialization
========================================

Initializes the SQLite database with a curated set of sample books.
The dataset includes 12 classic titles across 7 genres to demonstrate
filtering, search, sorting, and statistics features.

Usage:
    python init_db.py
"""

from database import SessionLocal, Book, engine, Base


def init_database():
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)
    print("[init] Database tables created/verified.")


def load_sample_data():
    """
    Populate the database with 12 sample books across diverse genres.
    
    Skips import if data already exists (idempotent operation).
    """
    db = SessionLocal()
    try:
        # Prevent duplicate imports
        if db.query(Book).count() > 0:
            print(f"[load] Data already exists ({db.query(Book).count()} books). Skipping import.")
            return

        sample_books = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "978-0743273565",
                "description": (
                    "A story of the fabulously wealthy Jay Gatsby and his love "
                    "for Daisy Buchanan, set in the Jazz Age on Long Island."
                ),
                "genre": "Fiction",
                "publication_year": 1925,
                "publisher": "Scribner",
                "pages": 180,
                "rating": 4.2,
                "language": "English"
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "isbn": "978-0061120084",
                "description": (
                    "A novel about the serious issues of rape and racial "
                    "injustice, told through the eyes of Scout Finch."
                ),
                "genre": "Fiction",
                "publication_year": 1960,
                "publisher": "J.B. Lippincott & Co.",
                "pages": 281,
                "rating": 4.5,
                "language": "English"
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "isbn": "978-0451524935",
                "description": (
                    "A dystopian social science fiction novel and cautionary "
                    "tale about totalitarianism, surveillance, and truth."
                ),
                "genre": "Science Fiction",
                "publication_year": 1949,
                "publisher": "Secker & Warburg",
                "pages": 328,
                "rating": 4.4,
                "language": "English"
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "isbn": "978-0141439518",
                "description": (
                    "A romantic novel of manners depicting British Regency "
                    "society and the relationship between Elizabeth Bennet "
                    "and Mr. Darcy."
                ),
                "genre": "Romance",
                "publication_year": 1813,
                "publisher": "T. Egerton",
                "pages": 279,
                "rating": 4.3,
                "language": "English"
            },
            {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "isbn": "978-0316769488",
                "description": (
                    "A controversial novel about teenage alienation and loss "
                    "of innocence, narrated by Holden Caulfield."
                ),
                "genre": "Fiction",
                "publication_year": 1951,
                "publisher": "Little, Brown and Company",
                "pages": 234,
                "rating": 3.9,
                "language": "English"
            },
            {
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "isbn": "978-0747532699",
                "description": (
                    "The first novel in the Harry Potter series, following a "
                    "young wizard who discovers his magical heritage at Hogwarts."
                ),
                "genre": "Fantasy",
                "publication_year": 1997,
                "publisher": "Bloomsbury",
                "pages": 223,
                "rating": 4.7,
                "language": "English"
            },
            {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "isbn": "978-0547928227",
                "description": (
                    "A fantasy novel about the journey of Bilbo Baggins, who "
                    "is drawn into a quest to reclaim the lost Dwarf Kingdom."
                ),
                "genre": "Fantasy",
                "publication_year": 1937,
                "publisher": "George Allen & Unwin",
                "pages": 310,
                "rating": 4.6,
                "language": "English"
            },
            {
                "title": "The Three-Body Problem",
                "author": "Cixin Liu",
                "isbn": "978-7536692930",
                "description": (
                    "A hard science fiction novel about humanity's first contact "
                    "with an alien civilization, winner of the Hugo Award."
                ),
                "genre": "Science Fiction",
                "publication_year": 2008,
                "publisher": "Chongqing Press",
                "pages": 302,
                "rating": 4.8,
                "language": "Chinese"
            },
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "isbn": "978-0441172719",
                "description": (
                    "A landmark science fiction novel set in a distant future "
                    "amidst an interstellar feudal society, exploring politics, "
                    "religion, and ecology."
                ),
                "genre": "Science Fiction",
                "publication_year": 1965,
                "publisher": "Chilton Books",
                "pages": 412,
                "rating": 4.6,
                "language": "English"
            },
            {
                "title": "The Diary of a Young Girl",
                "author": "Anne Frank",
                "isbn": "978-0553296408",
                "description": (
                    "The personal diary written by Anne Frank while hiding during "
                    "the Nazi occupation of the Netherlands in World War II."
                ),
                "genre": "Non-Fiction",
                "publication_year": 1947,
                "publisher": "Contact Publishing",
                "pages": 283,
                "rating": 4.7,
                "language": "English"
            },
            {
                "title": "The Little Prince",
                "author": "Antoine de Saint-Exupéry",
                "isbn": "978-0156012195",
                "description": (
                    "A poetic tale about a young prince who visits various planets "
                    "in space, including Earth, addressing themes of loneliness, "
                    "friendship, love, and loss."
                ),
                "genre": "Fiction",
                "publication_year": 1943,
                "publisher": "Reynal & Hitchcock",
                "pages": 96,
                "rating": 4.8,
                "language": "French"
            },
            {
                "title": "Neuromancer",
                "author": "William Gibson",
                "isbn": "978-0441569595",
                "description": (
                    "The seminal cyberpunk novel that coined the term 'cyberspace', "
                    "following a washed-up computer hacker hired for one last job."
                ),
                "genre": "Science Fiction",
                "publication_year": 1984,
                "publisher": "Ace Books",
                "pages": 271,
                "rating": 4.1,
                "language": "English"
            }
        ]

        for book_data in sample_books:
            db_book = Book(**book_data)
            db.add(db_book)

        db.commit()
        print(f"[load] Successfully imported {len(sample_books)} sample books.")

    except Exception as e:
        print(f"[error] Import failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    load_sample_data()
    print("[done] Database initialization completed.")
