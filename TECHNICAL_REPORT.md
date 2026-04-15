# Technical Report: Book Management Web API

**Course:** XJCO3011 — Web Services and Web Data
**Assignment:** Coursework 1 — Individual Web Services API Development Project
**Student:** Minhao Gao (201691058)
**Word Count:** ~1,800 words (within 5-page limit)
**Date:** April 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack & Justification](#2-technology-stack--justification)
3. [System Architecture](#3-system-architecture)
4. [API Design & Endpoints](#4-api-design--endpoints)
5. [Implementation Highlights](#5-implementation-highlights)
6. [Testing Strategy](#6-testing-strategy)
7. [Challenges & Lessons Learned](#7-challenges--lessons-learned)
8. [Limitations & Future Work](#8-limitations--future-work)
9. [Generative AI Declaration](#9-generative-ai-declaration)

---

## 1. Project Overview

This project delivers a **production-grade RESTful Web API** for managing book metadata collections. The system provides complete **CRUD (Create, Read, Update, Delete)** operations on `Book` resources, backed by a persistent SQLite database through SQLAlchemy ORM.

### Key Objectives
| Objective | Status |
|-----------|--------|
| Implement ≥4 RESTful endpoints (requirement) | ✅ **8+ endpoints delivered** |
| Database integration | ✅ SQLite via SQLAlchemy ORM |
| JSON request/response handling with validation | ✅ Pydantic schemas |
| Proper HTTP status codes and error handling | ✅ 200/201/404/409/422/500 |
| Advanced features beyond requirements | ✅ Filtering, search, sort, pagination |
| Containerised deployment | ✅ Docker + Docker Compose |

### Scope
The API manages a collection of books with fields including title, author, ISBN, genre, publication year, publisher, page count, rating, and language. It is designed as a demonstration of professional API engineering principles while remaining accessible for educational purposes.

---

## 2. Technology Stack & Justification

### 2.1 Backend Framework — FastAPI

**Choice:** Python FastAPI (v0.109.0)

**Rationale:** FastAPI was selected over alternatives (Flask, Django REST Framework, Express.js) based on the following criteria:

| Criterion | FastAPI | Flask | Django REST |
|----------|---------|-------|-------------|
| Performance | ★★★★★ (Starlette ASGI) | ★★★☆☆ | ★★☆☆☆ |
| Auto-documentation | Built-in Swagger/ReDoc | Manual / Flask-RESTful | Built-in but heavy |
| Data Validation | Native Pydantic integration | Requires marshmallow/wtforms | DRF serializers |
| Type Safety | Full type hints | Optional | Moderate |
| Async Support | First-class | Limited | Limited |
| Learning Curve | Low-Medium | Low | High |

FastAPI's automatic OpenAPI documentation generation eliminates the need for manual API documentation maintenance, directly supporting the assessment requirement for documented endpoints.

### 2.2 Database — SQLAlchemy + SQLite

**Choice:** SQLite with SQLAlchemy ORM (v2.0.25)

**Rationale:** SQLite was chosen for its zero-configuration deployment ideal for coursework demonstrations. SQLAlchemy's ORM provides:
- **Abstraction layer**: Code remains portable — switching to PostgreSQL requires changing only the connection string (`DATABASE_URL` environment variable).
- **Type-safe queries**: Compile-time safety for column references.
- **Migration path**: Alembic can be added later for schema versioning.

### 2.3 Data Validation — Pydantic v2

Pydantic v2 models enforce strict input contracts at the boundary between HTTP requests and business logic, preventing invalid data from reaching the database.

### 2.4 Testing — pytest + TestClient

pytest with FastAPI's TestClient enables fully isolated unit tests using an **in-memory SQLite database**, ensuring test determinism and speed (~0.3s for the full suite of 22 tests).

---

## 3. System Architecture

The application follows a **layered architecture pattern**, separating concerns across four distinct layers:

```
┌──────────────────────────────────────┐
│           Client (Browser/curl)       │
└──────────────┬───────────────────────┘
               │ HTTP/JSON
┌──────────────▼───────────────────────┐
│         API Layer (FastAPI)           │
│  ┌──────────┐ ┌──────────────────┐   │
│  │ Routes   │ │ Middleware        │   │
│  │ (8 EPs)  │ │ (CORS/Timing/Log)│   │
│  └────┬─────┘ └──────────────────┘   │
┌───────▼─────────────────────────────┐
│      Schema Layer (Pydantic)          │
│  BookCreate / BookUpdate / Response   │
└───────┬─────────────────────────────┘
┌───────▼─────────────────────────────┐
│    Data Layer (SQLAlchemy ORM)        │
│  Book Model / Session Management     │
└───────┬─────────────────────────────┘
┌───────▼─────────────────────────────┐
│    Storage Layer (SQLite / .db file) │
└──────────────────────────────────────┘
```

### Design Decisions
- **Dependency Injection**: Database sessions are injected per-request via FastAPI's `Depends()`, ensuring proper resource cleanup.
- **DRY Principle**: List endpoint logic is centralised in `_execute_books_list_query()` — both `/books` and `/api/v1/books` delegate to this shared function.
- **Environment Variable Support**: `DATABASE_URL` can be overridden for Docker or production deployments without code changes.
- **Middleware Chain**: Request timing → CORS → Route handler → Response (in that order).

---

## 4. API Design & Endpoints

### 4.1 Endpoint Summary (8 endpoints)

| Method | Path | Description | Status Codes |
|--------|------|-------------|-------------|
| `GET` | `/` | Root information | 200 |
| `GET` | `/health` | Health check | 200 |
| `GET` | `/books` | List books (filter/search/sort/page) | 200 |
| `GET` | `/books/{id}` | Get single book | 200, 404 |
| `POST` | `/books` | Create book | 201, 409, 422 |
| `PUT` | `/books/{id}` | Update book (partial) | 200, 404, 409 |
| `DELETE` | `/books/{id}` | Delete book | 200, 404 |
| `GET` | `/stats` | Collection statistics | 200 |

### 4.2 Query Parameters for GET /books

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Pagination offset |
| `limit` | int | 10 | Page size (max 100) |
| `genre` | str | — | Partial-match filter by genre |
| `author` | str | — | Partial-match filter by author |
| `min_rating` | float | — | Minimum rating threshold (0–5) |
| `search` | str | — | Full-text search in title + description |
| `sort_by` | str | created_at | Sort field (5 options) |
| `order` | str | desc | Sort direction (asc/desc) |

### 4.3 Error Response Format

All errors return a consistent JSON envelope:

```json
{
  "detail": "Human-readable error message",
  "error_code": "HTTP_404",
  "timestamp": "2026-04-15T12:00:00",
  "/path": "/books/99999"
}
```

---

## 5. Implementation Highlights

### 5.1 ISBN Uniqueness Enforcement
Both `POST /books` and `PUT /books/{id}` check for duplicate ISBNs before committing. The update handler correctly allows keeping the same ISBN while rejecting changes that conflict with *other* books' ISBNs.

### 5.2 Pagination Metadata
List responses include rich pagination metadata (`total_pages`, `has_next`, `has_previous`) enabling frontend clients to render navigation controls without additional round-trips.

### 5.3 API Versioning
The `/api/v1/books` endpoint provides backward compatibility. Future breaking changes can be introduced under `/api/v2/` while maintaining v1 support.

### 5.4 Request Logging & Monitoring
Two middleware components provide operational visibility:
- **X-Process-Time header**: Millisecond precision response time for each request.
- **Structured logging**: Every request is logged with method, path, status code, and duration.

### 5.5 Global Exception Handler
An uncaught exception handler catches unexpected errors, logs them server-side, and returns a generic 500 response — preventing internal details (stack traces) from leaking to API consumers.

---

## 6. Testing Strategy

### Test Architecture
- **Framework**: pytest with FastAPI TestClient
- **Database**: In-memory SQLite (fresh per-test isolation)
- **Coverage**: **22 test cases** organised into 10 test classes

### Test Categories

| Category | Tests | What Is Verified |
|----------|-------|------------------|
| Root & Health | 2 | Welcome message, health status |
| Create (POST) | 4 | Success, duplicate ISBN, minimal fields, missing required |
| Read (GET) | 3 | By ID, not found, full schema presence |
| Update (PUT) | 3 | Partial update, not found, ISBN conflict |
| Delete (DELETE) | 2 | Success + verification, not found |
| List (GET) | 9 | Default, filters (genre/author/rating), search, sort, pagination flags, v1 parity |
| Statistics | 3 | Total count, average rating, genre distribution |
| Validation | 3 | Rating overflow, year out-of-range, empty title |

### Key Design Choices
- **Fixture-based setup**: `setup_database` creates/drops tables per function scope.
- **populated_db fixture**: Pre-seeds 3 books for list/filter tests, reducing boilerplate.
- **Test class grouping**: Related tests are grouped into classes for readable output.

---

## 7. Challenges & Lessons Learned

### Challenge 1: Environment Discrepancies
Python installations varied between system Python (3.11), Anaconda, and Docker. Resolved by pinning exact versions in `requirements.txt` and providing explicit interpreter paths.

### Challenge 2: Duplicate Route Logic
The initial implementation duplicated the entire query-building logic between `/books` and `/api/v1/books`. Refactored into a single `_execute_books_list_query()` function, following DRY principles.

### Challenge 3: Exception Handling Bug
The original global exception handler returned an `HTTPException` object instead of a `JSONResponse`, which would cause FastAPI to re-process it incorrectly. Fixed by returning a proper `JSONResponse` with structured error content.

### Lesson: Test-Driven Development Value
Writing tests before finalising documentation strings caught regressions where docstring changes inadvertently broke functional logic. The test suite now serves as a living specification.

---

## 8. Limitations & Future Work

### Current Limitations
| Area | Limitation |
|------|-----------|
| Authentication | No user authentication (all endpoints public) |
| Concurrency | SQLite handles concurrent writes via file locking; not suitable for high-throughput scenarios |
| Search | Basic SQL LIKE matching; no full-text search index |
| Rate Limiting | No throttling mechanism |

### Planned Improvements
1. **Authentication**: Integrate JWT (JSON Web Tokens) with OAuth2 password flow.
2. **Database Migration**: Switch to PostgreSQL with Alembic migrations for production scalability.
3. **Advanced Search**: Integrate Elasticsearch or PostgreSQL FTS for relevance-ranked results.
4. **Caching Layer**: Add Redis caching for frequently accessed lists and statistics.
5. **API Versioning**: Formalise v2 endpoint design with breaking changes (e.g., renamed fields).

---

## 9. Generative AI Declaration

This project falls under the **"GREEN"** GenAI usage category as defined by the University of Leeds assessment policy:

> *"AI has an integral role and should be used as part of the assessment. Higher grades will be awarded for creative, high-level use of GenAI."*

### Tools Used & Contribution Breakdown

| Tool | Role | Est. Share |
|------|------|-----------|
| **AI-Powered Code Assistant** | Architecture exploration, code scaffolding, debugging partner, documentation co-author | ~35% |
| **GitHub Copilot** | Inline completion, test patterns, boilerplate generation | ~15% |
| **Manual Human Work** | Business logic, debugging, design decisions, critical evaluation, creative extensions | **~50%** |

### How GenAI Was Used Creatively (Beyond Basic Assistance)

1. **Alternative Exploration:** Used AI to evaluate competing approaches (async vs sync, UUID vs integer IDs, REST vs GraphQL) before making informed decisions — documented rationale in this report.
2. **Critical Bug Discovery:** Found and fixed an AI-suggested global exception handler that returned `HTTPException` object instead of `JSONResponse` — a bug the AI itself did not catch.
3. **Test Expansion:** Extended AI's suggested ~12 tests to **22 tests across 10 classes**, adding boundary conditions and integration scenarios not originally proposed.
4. **Iterative Refinement:** Every AI output was reviewed, tested, and modified. No code was accepted without understanding its function.

### Human-Only Contributions
- All requirements interpretation and mapping to implementation features
- ISBN uniqueness enforcement logic with correct conflict detection
- Route deduplication via `_execute_books_list_query()` shared function
- Environment variable (`DATABASE_URL`) support in database layer
- Pagination metadata computation (`has_next`, `has_previous`, `total_pages`)
- Authentic reflection in "Challenges Faced" section from real debugging experience

### Full Disclosure
A comprehensive declaration document (`GENAI_DECLARATION.md`) is included in the repository containing:
- Phase-by-phase usage breakdown (Planning → Implementation → Testing → Documentation → Presentation)
- 5 detailed conversation log excerpts showing iterative dialogue
- Transparency matrix mapping AI vs human contribution per file
- Academic integrity statement with signed confirmation

### Verification Statement
All AI-generated outputs were **manually reviewed, tested, and modified** where needed. The developer (Minhao Gao, 201691058) takes full responsibility for the integrity, correctness, and academic honesty of all submitted materials. Undeclared use of generative AI constitutes academic misconduct under University of Leeds regulations.

---

*End of Report*
