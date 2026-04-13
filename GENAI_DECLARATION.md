# GenAI Usage Declaration and Conversation Logs

## Project Information
- **Project Name:** Book Management Web API
- **Course:** XJCO3011 — Web Services and Web Data
- **Assignment:** Coursework 1 — Individual Web Services API Development Project
- **Date:** April 2026

---

## 1. Assessment Category

**GREEN** — AI has an integral role and should be used as part of the assessment.  
This project strategically leverages generative AI tools for code scaffolding, architecture suggestions, documentation, and test design, with full human review and modification of all outputs.

---

## 2. Tools Used Summary

| Tool | Purpose | Estimated Contribution |
|------|---------|----------------------|
| **Microsoft Copilot / GitHub Copilot** | Code structure templates, FastAPI routing patterns, SQLAlchemy model definitions, Pydantic schema design | ~25% |
| **AI Chat Assistant (GPT-based)** | Technology stack comparison, architectural decisions, test case design, English language refinement, documentation structuring | ~20% |
| **Manual Human Work (~55%)** | Requirements interpretation, business logic implementation, debugging, iterative testing, final review and quality assurance | ~55% |

### What AI Assisted With:
1. Initial project scaffolding (FastAPI app boilerplate)
2. Database model field recommendations
3. RESTful endpoint design patterns (CRUD conventions)
4. Error handling strategy and HTTP status code selection
5. Test case structure and coverage planning
6. Documentation formatting and English grammar
7. Docker configuration best practices

### What Was Done Entirely by Hand:
1. Mapping coursework requirements to implementation features
2. Writing all business logic and route handlers
3. Debugging edge cases (ISBN conflict handling, pagination metadata)
4. Refactoring duplicate code into shared functions
5. Fixing bugs (exception handler, environment variable support)
6. Running tests and iterating on failures
7. Final review of all code and documents for correctness
8. Designing presentation content and slide structure

---

## 3. Conversation Log Examples

### Log 1: Technology Stack Selection

**User:** I need to build a Web API for a university assignment requiring CRUD operations, database integration, and at least 4 endpoints. What technology stack do you recommend?

**AI Assistant:** For a Python-based web API assignment, I recommend:

1. **FastAPI** — High performance (Starlette), auto-generated Swagger/ReDoc docs, native Pydantic validation, async support. Better than Flask (more setup) or Django DRF (heavier) for API-only projects.

2. **SQLAlchemy + SQLite** — ORM gives you clean abstraction. SQLite is zero-config, perfect for demos. Easy switch to PostgreSQL later.

3. **pytest + TestClient** — Industry-standard testing with isolated in-memory databases.

4. **Docker** — Containerise for easy deployment demonstration.

**Decision Made:** Adopted FastAPI + SQLAlchemy + SQLite + pytest + Docker as the core stack.

---

### Log 2: Book Data Model Design

**User:** I'm building a book management system. What fields should my Book data model include?

**AI Assistant:** A well-designed book model should include:

| Field | Type | Notes |
|-------|------|-------|
| id | Integer PK | Auto-increment |
| title | String (required) | Indexed for search |
| author | String (required) | Indexed |
| isbn | String (unique) | ISBN-10/13 |
| description | Text | Synopsis |
| genre | String | For filtering |
| publication_year | Integer | Validation range 1000-2100 |
| publisher | String | Publishing house |
| pages | Integer | Page count |
| rating | Float | Scale 0-5 |
| language | String | Default "English" |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

**Implementation:** Used this as a starting point, added `created_at`/`updated_at` timestamps for audit trail purposes.

---

### Log 3: RESTful Endpoint Design

**User:** I need at least 4 endpoints for CRUD on books. How should I design them?

**AI Assistant:** Standard RESTful pattern:

```
GET    /books         → List (with filtering, search, sort, pagination)
GET    /books/{id}    → Get single
POST   /books         → Create
PUT    /books/{id}    → Update (partial)
DELETE /books/{id}    → Remove
GET    /stats         → Aggregate statistics (bonus endpoint)
GET    /health        → Health check (bonus)
```

Status codes:
- 200 OK (GET success, PUT success)
- 201 Created (POST success)
- 404 Not Found (resource missing)
- 409 Conflict (duplicate ISBN)
- 422 Unprocessable Entity (Pydantic validation failure)
- 500 Internal Server Error (unexpected)

**Implementation:** Adopted this design exactly. Added `/api/v1/books` versioned alias for backward compatibility.

---

### Log 4: Error Handling & Middleware

**User:** How should I handle errors professionally in FastAPI?

**AI Assistant:** Best practices:
1. Use `HTTPException` for known errors (404, 409)
2. Create custom exception handlers that return JSON responses
3. Add a global fallback handler for unexpected exceptions (never expose stack traces)
4. Include structured error format: `{detail, error_code, timestamp, path}`
5. Add request timing middleware (`X-Process-Time` header)

**Implementation:** Implemented all five points. Discovered and fixed a bug where the original global handler returned `HTTPException` object instead of `JSONResponse`.

---

### Log 5: Testing Strategy

**User:** What test cases should I cover for my Book API?

**AI Assistant:** Organise your tests into categories:

**Happy Path:**
- POST creates a book → 201
- GET by ID returns correct book → 200
- PUT updates only provided fields
- DELETE removes and verifies gone

**Edge Cases:**
- GET non-existent ID → 404
- POST with duplicate ISBN → 409
- POST missing required field → 422
- PUT/DELETE non-existent ID → 404

**Feature Tests:**
- Filter by genre, author, min_rating
- Search in title/description
- Sort by multiple fields
- Pagination metadata (has_next, has_previous)
- Statistics endpoint accuracy
- Input boundary validation (rating > 5, year out of range)

**Implementation:** Expanded from original 13 tests to 22 tests across 10 test classes using pytest fixtures.

---

### Log 6: Documentation & Report Writing

**User:** Help me write a technical report for my coursework. It needs to justify my tech choices, describe architecture, discuss challenges, and declare GenAI usage. Max 5 pages.

**AI Assistant:** Structure it like this:

1. **Overview** — what you built, key objectives table
2. **Technology Stack** — comparison table (FastAPI vs alternatives), why each choice
3. **Architecture diagram** — layered approach (API → Schema → Data → Storage)
4. **API Design** — endpoint table, query params, error format
5. **Implementation Highlights** — ISBN enforcement, pagination, middleware
6. **Testing Strategy** — test categories, count, tools
7. **Challenges** — honest reflection on problems faced
8. **Limitations & Future Work** — show self-awareness
9. **GenAI Declaration** — transparent disclosure

Keep tables compact. Use diagrams where possible. Aim for ~1,800 words.

**Implementation:** Followed this structure precisely. Added inline ASCII architecture diagram for clarity.

---

## 4. Verification Statement

> **I confirm that all generative AI outputs used in this project have been:**
> 
> 1. **Reviewed** — Every piece of AI-suggested code was read and understood before inclusion.
> 2. **Tested** — All functionality was verified through the automated test suite (22 passing tests).
> 3. **Modified** — AI outputs were adapted to fit specific requirements and coding standards.
> 4. **Documented** — This declaration provides transparency about the extent and nature of AI usage.
>
> The developer takes full responsibility for the integrity, correctness, and academic honesty of all submitted materials.
>
> *Signed: Student Developer*
> *Date: April 2026*

---

## 5. Files Generated/Augmented by AI Assistance

| File | Nature of AI Contribution |
|------|--------------------------|
| `main.py` | Route structure patterns, error handling template, middleware concept |
| `database.py` | Model field recommendations, connection string pattern |
| `schemas.py` | Pydantic field constraints, validator syntax |
| `test_api.py` | Test category organisation, fixture patterns |
| `README.md` | Section structure, feature list wording |
| `TECHNICAL_REPORT.md` | Document structure, comparison table format |
| `API_DOCUMENTATION.md` | Endpoint documentation template, example JSON |
| `GENAI_DECLARATION.md` | This document itself |

*All files were significantly modified by human hands after initial AI assistance.*
