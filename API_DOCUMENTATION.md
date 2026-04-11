# Book Management API Documentation
**Version 1.0.0** | **Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Quick Start](#2-quick-start)
3. [Authentication](#3-authentication)
4. [Error Handling](#4-error-handling)
5. [Endpoints](#5-endpoints)
   - 5.1 [Root & Health](#51-root--health)
   - 5.2 [List Books](#52-list-books-get-books)
   - 5.3 [Create Book](#53-create-book-post-books)
   - 5.4 [Get Single Book](#54-get-single-book-get-booksid)
   - 5.5 [Update Book](#55-update-book-put-booksid)
   - 5.6 [Delete Book](#56-delete-book-delete-booksid)
   - 5.7 [Statistics](#57-statistics-get-stats)

---

## 1. Introduction

The **Book Management API** is a RESTful web service for managing book metadata collections. It provides complete CRUD operations with advanced features including filtering, full-text search, multi-field sorting, and pagination.

**Technology:** Python FastAPI + SQLAlchemy ORM + SQLite

---

## 2. Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Initialise database with sample data (12 books)
python init_db.py

# Start server
uvicorn main:app --reload --port 8000

# Open interactive documentation
open http://localhost:8000/docs    # Swagger UI
open http://localhost:8000/redoc   # ReDoc
```

---

## 3. Authentication

> **Status:** Not required for this version.
>
> All endpoints are publicly accessible. This design decision was made to keep the demonstration focused on core RESTful principles. Authentication (JWT/OAuth2) is listed as a future enhancement.

---

## 4. Error Handling

All errors return a consistent JSON structure:

| Field | Type | Description |
|-------|------|-------------|
| `detail` | string | Human-readable error description |
| `error_code` | string | Machine-readable code (e.g., `HTTP_404`) |
| `timestamp` | string | ISO 8601 UTC timestamp |
| `path` | string | The request path that triggered the error |

### HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| **200 OK** | Success | GET list, GET single, PUT update, DELETE success |
| **201 Created** | Resource created | POST new book |
| **400 Bad Request** | Invalid parameters | Malformed query params |
| **404 Not Found** | Resource missing | Non-existent book ID |
| **409 Conflict** | Data conflict | Duplicate ISBN detected |
| **422 Unprocessable Entity** | Validation failed | Missing/invalid request body fields |
| **500 Internal Server Error** | Unexpected failure | Unhandled server exception |

---

## 5. Endpoints

### 5.1 Root & Health

#### `GET /`
Welcome endpoint with API information.

**Response (200):**
```json
{
  "message": "Welcome to Book Management API",
  "version": "1.0.0",
  "docs_url": "/docs",
  "redoc_url": "/redoc"
}
```

#### `GET /health`
Health check for monitoring and load balancers.

**Response (200):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-04-15T12:00:00"
}
```

---

### 5.2 List Books — `GET /books`

Retrieve a paginated, filterable, searchable, sortable list of books.

**URL:** `/books` or `/api/v1/books`

#### Query Parameters

| Parameter | Type | Default | Constraints | Description |
|-----------|------|---------|-------------|-------------|
| `skip` | int | 0 | ≥ 0 | Pagination offset (records to skip) |
| `limit` | int | 10 | 1–100 | Maximum records per page |
| `genre` | string | — | — | Filter by genre (partial match, e.g., `?genre=Fiction`) |
| `author` | string | — | — | Filter by author name (partial match) |
| `min_rating` | float | — | 0–5 | Minimum rating threshold |
| `search` | string | — | — | Full-text search in **title** AND **description** |
| `sort_by` | string | `created_at` | See below | Sort field |
| `order` | string | `desc` | `asc` / `desc` | Sort direction |

**Valid `sort_by` values:** `title`, `author`, `rating`, `publication_year`, `created_at`

#### Example Requests

```bash
# Get first 10 books (default)
curl http://localhost:8000/books

# Get Fiction books with rating >= 4.0, sorted by rating descending
curl "http://localhost:8000/books?genre=Fiction&min_rating=4&sort_by=rating&order=desc"

# Search for books containing 'Potter' in title or description
curl "http://localhost:8000/books?search=Potter"

# Page 2 (skip 10, limit 10)
curl "http://localhost:8000/books?skip=10&limit=10"
```

#### Response (200 OK)

```json
{
  "meta": {
    "total": 12,
    "skip": 0,
    "limit": 10,
    "has_next": true,
    "has_previous": false,
    "total_pages": 2
  },
  "books": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0743273565",
      "description": "A story of the fabulously wealthy Jay Gatsby...",
      "genre": "Fiction",
      "publication_year": 1925,
      "publisher": "Scribner",
      "pages": 180,
      "rating": 4.2,
      "language": "English",
      "created_at": "2026-04-15T10:00:00",
      "updated_at": "2026-04-15T10:00:00"
    }
  ]
}
```

---

### 5.3 Create Book — `POST /books`

Add a new book to the collection.

#### Request Body (JSON)

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | ✅ Yes | 1–255 chars | Book title |
| `author` | string | ✅ Yes | 1–255 chars | Author name |
| `isbn` | string | No | ≤ 20 chars, unique | ISBN-10 or ISBN-13 |
| `description` | string | No | — | Book synopsis |
| `genre` | string | No | ≤ 100 chars | Genre/category |
| `publication_year` | int | No | 1000–2100 | Year published |
| `publisher` | string | No | ≤ 255 chars | Publishing house |
| `pages` | int | No | > 0 | Total pages |
| `rating` | float | No | 0–5 | Rating score |
| `language` | string | No | ≤ 50 chars, default `"English"` | Language |

#### Example Request

```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "description": "A handbook of agile software craftsmanship.",
    "genre": "Non-Fiction",
    "publication_year": 2008,
    "publisher": "Prentice Hall",
    "pages": 464,
    "rating": 4.7,
    "language": "English"
  }'
```

#### Responses

**201 Created** (success):
Returns the created book object with auto-generated `id`, `created_at`, `updated_at`.

**409 Conflict** (duplicate ISBN):
```json
{ "detail": "ISBN '978-0132350884' is already registered (Book ID: 5)", "error_code": "HTTP_409", ... }
```

**422 Unprocessable Entity** (validation failure):
Returned when required fields are missing or values violate constraints (e.g., `rating: 6.0`).

---

### 5.4 Get Single Book — `GET /books/{id}`

Fetch detailed metadata for one specific book.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | The unique book identifier |

#### Example

```bash
curl http://localhost:8000/books/1
```

**Response (200):** Full book object (same schema as create response).

**Response (404 Not Found):**
```json
{ "detail": "Book ID 99999 not found", "error_code": "HTTP_404", ... }
```

---

### 5.5 Update Book — `PUT /books/{id}`

Update an existing book. Supports **partial updates** — only include the fields you want to change.

#### Example Request

```bash
curl -X PUT http://localhost:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{ "rating": 5.0, "publisher": "Updated Publisher" }'
```

**Response (200):** Updated book object with all current field values.

**Error responses:** Same as Create (404 if not found, 409 if new ISBN conflicts).

---

### 5.6 Delete Book — `DELETE /books/{id}`

Remove a book from the collection permanently.

#### Example

```bash
curl -X DELETE http://localhost:8000/books/1
```

**Response (200 OK):**
```json
{ "message": "Book 'The Great Gatsby' deleted successfully", "deleted_id": 1 }
```

**Response (404):** If the book ID does not exist.

---

### 5.7 Statistics — `GET /stats`

Get aggregate statistics about the entire book collection.

#### Example

```bash
curl http://localhost:8000/stats
```

**Response (200):**
```json
{
  "total_books": 12,
  "average_rating": 4.45,
  "books_with_rating": 11,
  "genres_count": 7,
  "genre_distribution": {
    "Science Fiction": 4,
    "Fiction": 3,
    "Fantasy": 2,
    "Non-Fiction": 1,
    "Romance": 1,
    ...
  }
}
```

---

## Appendix A: Response Time Header

Every response includes an `X-Process-Time` header indicating server-side processing time in seconds:

```
X-Process-Time: 0.0023
```

This header is useful for performance monitoring and debugging.

## Appendix B: Interactive Documentation

When the server is running, access:
- **Swagger UI:** `http://localhost:8000/docs` — interactive testing interface
- **ReDoc:** `http://localhost:8000/redoc` — clean reference documentation

These are automatically generated from the source code docstrings and Pydantic schemas, ensuring they stay synchronised with the implementation.

---

*Document version 1.0.0 — Generated for XJCO3011 Coursework 1 submission*
