# Book Management API

**A production-grade RESTful Web API for managing book metadata collections.**  
Built with **FastAPI**, **SQLAlchemy**, and **Pydantic** — featuring full CRUD operations, advanced filtering, search, sorting, pagination, and comprehensive testing.

---

## Features

- ✅ Complete CRUD operations (Create, Read, Update, Delete) on Book resources
- ✅ 8+ RESTful endpoints (exceeds the 4-endpoint minimum requirement)
- ✅ Advanced filtering by genre, author, and minimum rating
- ✅ Full-text search across title and description fields
- ✅ Multi-field sorting (title, author, rating, year, created date)
- ✅ Rich pagination metadata (`has_next`, `has_previous`, `total_pages`)
- ✅ Data validation via Pydantic schemas (input sanitisation at the boundary)
- ✅ ISBN uniqueness enforcement (409 Conflict on duplicates)
- ✅ Standard HTTP status codes: 200, 201, 400, 404, 409, 422, 500
- ✅ Automatic API documentation (Swagger UI + ReDoc)
- ✅ Request timing & structured logging middleware
- ✅ Health check endpoint for monitoring
- ✅ API versioning support (`/api/v1/`)
- ✅ 22 automated tests (pytest)
- ✅ Docker & Docker Compose ready

## Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Web Framework** | FastAPI 0.109.0 | High performance, auto-docs, async-native |
| **ORM** | SQLAlchemy 2.0.25 | Database abstraction, easy migration path |
| **Database** | SQLite | Zero-config, perfect for demos/education |
| **Validation** | Pydantic 2.5.3 | Type-safe request/response contracts |
| **Testing** | pytest 7.4.4 | Isolated in-memory DB per test |
| **ASGI Server** | Uvicorn 0.27.0 | Production-grade server |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database (loads 12 sample books)
python init_db.py

# 3. Start the development server
uvicorn main:app --reload --port 8000

# 4. Open interactive documentation
#    Swagger UI: http://localhost:8000/docs
#    ReDoc:      http://localhost:8000/redoc
```

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t book-api .
docker run -p 8000:8000 book-api
```

### 🌐 Live Deployment

The API is currently **deployed and publicly accessible** on a cloud server:

| Item | URL |
|------|-----|
| **Swagger UI (Interactive Docs)** | http://85.137.244.136:8000/docs |
| **ReDoc (Alternative Docs)** | http://85.137.244.136:8000/redoc |
| **Health Check** | http://85.137.244.136:8000/health |
| **Books API** | http://85.137.244.136:8000/api/v1/books |

**Server Details:**
- Location: Hong Kong
- OS: CentOS 7 + Docker 26.1.4
- Runtime: Uvicorn in Docker container
- Database: SQLite (pre-loaded with 12 sample books)
- Status: ✅ Running and publicly accessible

## Testing

```bash
# Run all 22 tests with verbose output
pytest test_api.py -v
```

### Test Coverage Summary (22 tests)

| Category | Tests |
|----------|-------|
| Root & Health endpoints | 2 |
| Create (POST) — success, ISBN conflict, minimal input, validation | 4 |
| Read (GET single) — success, not found, schema verification | 3 |
| Update (PUT) — partial update, not found, ISBN conflict | 3 |
| Delete (DELETE) — success + verify, not found | 2 |
| List (GET) — default, genre filter, author filter, rating filter, search, sort desc, pagination, flags, v1 parity | 9 |
| Statistics — total, avg rating, genre distribution | 3 |
| Input Validation — overflow, out-of-range, empty field | 3 |

## Project Structure

```
web/
├── main.py                 # FastAPI application (8 endpoints, middleware)
├── database.py             # SQLAlchemy models, DB connection, env var support
├── schemas.py              # Pydantic validation schemas
├── data_loader.py          # Sample data initialiser (12 classic books)
├── init_db.py              # Database init entry point
├── test_api.py             # Automated test suite (22 test cases)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Multi-container orchestration
├── README.md               # This file
├── API_DOCUMENTATION.pdf   # Full API reference document
├── TECHNICAL_REPORT.pdf    # Design decisions & architecture report
├── GENAI_DECLARATION.md    # GenAI usage declaration & conversation logs
└── PRESENTATION.pptx       # Oral examination slides
```

## Deliverables

| File | Description |
|------|-------------|
| [API_DOCUMENTATION.pdf](./API_DOCUMENTATION.pdf) | Complete API reference (endpoints, params, examples) |
| [TECHNICAL_REPORT.pdf](./TECHNICAL_REPORT.pdf) | Technical report (max 5 pages) covering design choices |
| GENAI_DECLARATION.md | Detailed GenAI tool usage logs and declaration |
| Source code repository | Versioned on GitHub with commit history |

## GenAI Usage Declaration

This project uses generative AI tools under the University of Leeds **"GREEN" assessment category**. Approximately 30% of code structure and documentation was AI-assisted; all output was reviewed, tested, and modified by the developer. See [`GENAI_DECLARATION.md`](./GENAI_DECLARATION.md) for full details.

---

*Course: XJCO3011 Web Services and Web Data | Assignment: Coursework 1*
