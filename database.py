"""
Database Configuration & ORM Models
====================================

SQLAlchemy setup for the Book Management API.
Uses SQLite for development with easy migration path to PostgreSQL/MySQL.

Environment variable support:
    DATABASE_URL — override default SQLite connection string
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Support environment variable override (useful for Docker / production)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./books.db"
)

# SQLite-specific: allow cross-thread connections
connect_args = {"check_same_thread": False}
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
else:
    # PostgreSQL/MySQL don't need check_same_thread
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Book(Base):
    """
    Book data model — represents a single book record in the library.
    
    Fields:
        id              — Primary key (auto-increment)
        title           — Book title (required, indexed)
        author          — Author name (required, indexed)
        isbn            — ISBN-13/ISBN-10 (unique, indexed)
        description     — Free-text description / synopsis
        genre           — Category or genre tag (indexed)
        publication_year— Year of publication
        publisher       — Publishing house name
        pages           — Page count
        rating          — User/critic rating 0–5 scale
        language        — ISO language code or name
        created_at      — Record creation timestamp
        updated_at      — Last modification timestamp
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), unique=True, index=True, nullable=True)
    description = Column(Text, nullable=True)
    genre = Column(String(100), index=True, nullable=True)
    publication_year = Column(Integer, nullable=True)
    publisher = Column(String(255), nullable=True)
    pages = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    language = Column(String(50), default="English", nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db():
    """
    Dependency-injected database session generator.
    
    Yields a SQLAlchemy session and ensures it is closed after use,
    preventing connection leaks in FastAPI's async context.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables on module import (safe — won't recreate existing tables)
Base.metadata.create_all(bind=engine)
