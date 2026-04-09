"""
Book Management Web API
========================

A RESTful API for managing book collections with complete CRUD operations,
advanced filtering, full-text search, sorting, and pagination.

Course: XJCO3011 Web Services and Web Data
Author: XJCO3011 Student
"""

from fastapi import FastAPI, HTTPException, Depends, Query, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Literal
from datetime import datetime
from database import SessionLocal, Book, get_db
from schemas import (
    BookCreate, BookUpdate, BookResponse,
    BookListResponse, ErrorResponse, PaginationMeta
)
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Book Management API",
    description=(
        "A production-ready RESTful API for book metadata management. "
        "Features include CRUD operations, advanced filtering, "
        "full-text search, sorting, pagination, and statistics."
    ),
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)


# ============================================================================
# Middleware
# ============================================================================

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add response time header for performance monitoring."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log incoming requests for debugging and monitoring."""
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration:.2f}ms)")
    return response


# CORS middleware — allows cross-origin requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Shared Query Logic (eliminates code duplication between versioned routes)
# ============================================================================

def _build_books_query(db: Session, genre: Optional[str], author: Optional[str],
                       min_rating: Optional[float], search: Optional[str]):
    """Build a filtered Book query with common filters applied."""
    query = db.query(Book)

    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if min_rating is not None:
        query = query.filter(Book.rating >= min_rating)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Book.title.ilike(search_pattern)) |
            (Book.description.ilike(search_pattern))
        )
    return query


def _apply_sorting(query, sort_by: str, order: str):
    """Apply ordering to the query based on sort parameters."""
    sort_column = getattr(Book, sort_by, Book.created_at)
    if order == "desc":
        return query.order_by(sort_column.desc())
    return query.order_by(sort_column.asc())


def _execute_books_list_query(db: Session, skip: int, limit: int,
                               genre: Optional[str], author: Optional[str],
                               min_rating: Optional[float], search: Optional[str],
                               sort_by: str, order: str) -> dict:
    """
    Execute the paginated books list query.
    
    Returns a dict matching BookListResponse schema with 'meta' and 'books' keys.
    This is the single source of truth for all list endpoints.
    """
    query = _build_books_query(db, genre, author, min_rating, search)
    total = query.count()
    query = _apply_sorting(query, sort_by, order)
    books = query.offset(skip).limit(limit).all()
    
    total_pages = (total + limit - 1) // limit if limit > 0 else 0

    return {
        "meta": PaginationMeta(
            total=total,
            skip=skip,
            limit=limit,
            has_next=skip + limit < total,
            has_previous=skip > 0,
            total_pages=total_pages
        ),
        "books": books
    }


# ============================================================================
# Root & Health Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
def root():
    """API root path — returns basic information and documentation links."""
    return {
        "message": "Welcome to Book Management API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "books": "/books",
            "health": "/health",
            "stats": "/stats"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring and load balancer probes."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# Book CRUD Endpoints
# ============================================================================

@app.get("/api/v1/books", response_model=BookListResponse, tags=["Books"])
def get_books_v1(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    author: Optional[str] = Query(None, description="Filter by author"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort_by: Literal["title", "author", "rating", "publication_year", "created_at"] = Query(
        "created_at", description="Sort field"),
    order: Literal["asc", "desc"] = Query("desc", description="Sort order"),
    db: Session = Depends(get_db),
):
    """
    Get list of books (v1 endpoint).
    
    Supports filtering by genre, author, minimum rating, full-text search,
    multi-field sorting, and pagination.
    """
    return _execute_books_list_query(
        db, skip, limit, genre, author, min_rating, search, sort_by, order
    )


@app.get("/books", response_model=BookListResponse, tags=["Books"])
def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    author: Optional[str] = Query(None, description="Filter by author"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort_by: Literal["title", "author", "rating", "publication_year", "created_at"] = Query(
        "created_at", description="Sort field"),
    order: Literal["asc", "desc"] = Query("desc", description="Sort order"),
    db: Session = Depends(get_db),
):
    """
    Get list of books (current version).
    
    Supports filtering by genre, author, minimum rating, full-text search,
    multi-field sorting, and pagination with rich metadata.
    """
    return _execute_books_list_query(
        db, skip, limit, genre, author, min_rating, search, sort_by, order
    )


@app.get("/books/{book_id}", response_model=BookResponse, tags=["Books"])
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve detailed information about a specific book by its ID.
    
    Returns 404 if the book does not exist.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book ID {book_id} not found"
        )
    return book


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"]
)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book entry in the database.
    
    Validates ISBN uniqueness before creation. Returns 201 on success
    or 409 Conflict if the ISBN already exists.
    """
    # Check ISBN uniqueness
    if book_data.isbn:
        existing = db.query(Book).filter(Book.isbn == book_data.isbn).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"ISBN '{book_data.isbn}' is already registered (Book ID: {existing.id})"
            )

    db_book = Book(**book_data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    logger.info(f"Created book: {db_book.title} (ID: {db_book.id})")
    return db_book


@app.put("/books/{book_id}", response_model=BookResponse, tags=["Books"])
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    """
    Update an existing book's information.
    
    Supports partial updates — only include fields you want to change.
    Returns 404 if book doesn't exist, 409 if new ISBN conflicts.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book ID {book_id} not found"
        )

    # Check ISBN conflict (if changing ISBN)
    if book_data.isbn and book_data.isbn != book.isbn:
        existing = db.query(Book).filter(Book.isbn == book_data.isbn).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"ISBN '{book_data.isbn}' is already used by another book (ID: {existing.id})"
            )

    # Apply partial updates only for provided fields
    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    logger.info(f"Updated book ID {book_id}: {book.title}")
    return book


@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book from the database by its ID.
    
    Returns 200 with confirmation message on success, 404 if not found.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book ID {book_id} not found"
        )

    title = book.title
    db.delete(book)
    db.commit()
    logger.info(f"Deleted book ID {book_id}: {title}")
    return {"message": f"Book '{title}' deleted successfully", "deleted_id": book_id}


# ============================================================================
# Statistics Endpoint
# ============================================================================

@app.get("/stats", tags=["Statistics"])
def get_statistics(db: Session = Depends(get_db)):
    """
    Get aggregate statistics about the book collection.
    
    Returns total count, average rating, books-with-rating count,
    and distribution of books across genres.
    """
    total_books = db.query(Book).count()

    rated_books = db.query(Book).filter(Book.rating != None).all()
    avg_rating_value = (
        sum(b.rating for b in rated_books) / len(rated_books)
        if rated_books else 0.0
    )

    # Genre distribution using SQLAlchemy group_by
    genre_stats = db.query(
        Book.genre,
        func.count(Book.id).label("count")
    ).group_by(Book.genre).all()

    return {
        "total_books": total_books,
        "average_rating": round(avg_rating_value, 2),
        "books_with_rating": len(rated_books),
        "genres_count": len([g for g, _ in genre_stats if g]),
        "genre_distribution": {genre: count for genre, count in genre_stats if genre}
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for HTTPExceptions — returns structured JSON error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global fallback handler for uncaught exceptions.
    
    Logs the error details and returns a generic 500 response
    to avoid leaking internal implementation details.
    """
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred. Please try again later.",
            "error_code": "INTERNAL_ERROR",
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Book Management API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
