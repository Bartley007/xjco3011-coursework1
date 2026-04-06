"""
Pydantic Schemas for Request/Response Validation
=================================================

Defines data models for:
- BookCreate   — input validation when creating a book
- BookUpdate   — partial update schema (all fields optional)
- BookResponse — API response serialization (from ORM)
- PaginationMeta / BookListResponse — paginated list responses
- ErrorResponse  — standard error envelope

All models use Field() constraints for automatic validation.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# ---------------------------------------------------------------------------
# Base book fields shared by create/update/response
# ---------------------------------------------------------------------------

class BookBase(BaseModel):
    """Common fields for book creation and updates."""
    title: str = Field(..., min_length=1, max_length=255, description="Book title (required)")
    author: str = Field(..., min_length=1, max_length=255, description="Author name (required)")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN-10 or ISBN-13")
    description: Optional[str] = Field(None, description="Book synopsis or notes")
    genre: Optional[str] = Field(None, max_length=100, description="Genre or category")
    publication_year: Optional[int] = Field(None, ge=1000, le=2100, description="Year published")
    publisher: Optional[str] = Field(None, max_length=255, description="Publishing house")
    pages: Optional[int] = Field(None, gt=0, description="Total page count")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Rating on 0–5 scale")
    language: Optional[str] = Field("English", max_length=50, description="Language of the book")


class BookCreate(BookBase):
    """Schema used when creating a new book via POST."""
    pass


class BookUpdate(BaseModel):
    """
    Schema used when updating an existing book via PUT.
    
    All fields are Optional — only send the ones you want to change.
    Partial updates are supported.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    genre: Optional[str] = Field(None, max_length=100)
    publication_year: Optional[int] = Field(None, ge=1000, le=2100)
    publisher: Optional[str] = Field(None, max_length=255)
    pages: Optional[int] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    language: Optional[str] = Field(None, max_length=50)


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class BookResponse(BookBase):
    """Full book record returned by the API (includes server-managed fields)."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    """Pagination metadata included in list responses."""
    total: int           # Total number of matching records
    skip: int            # Number of records skipped (offset)
    limit: int           # Page size
    has_next: bool       # Whether a next page exists
    has_previous: bool   # Whether a previous page exists
    total_pages: int     # Total number of pages


class BookListResponse(BaseModel):
    """Envelope for paginated book-list responses."""
    meta: PaginationMeta
    books: List[BookResponse]


class ErrorResponse(BaseModel):
    """Standard error response format."""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
