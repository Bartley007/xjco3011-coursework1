"""
Automated Test Suite — Book Management API
============================================

Uses pytest + FastAPI TestClient with an in-memory SQLite database.
Covers: CRUD operations, error handling, validation, filtering,
pagination, sorting, search, statistics, and edge cases.

Run:
    pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

# ---------------------------------------------------------------------------
# In-memory SQLite for testing (isolated from development database)
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the DB dependency to use the in-memory test database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def setup_database():
    """Create and tear down tables around each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def populated_db(setup_database):
    """Fixture that creates 3 sample books in the database."""
    books = [
        {"title": "Book A", "author": "Author A", "genre": "Fiction", "rating": 4.0},
        {"title": "Book B", "author": "Author B", "genre": "Science Fiction", "rating": 4.5},
        {"title": "Book C", "author": "Author A", "genre": "Fantasy", "rating": 3.5},
    ]
    created_ids = []
    for b in books:
        resp = client.post("/books", json=b)
        created_ids.append(resp.json()["id"])
    return created_ids


# ===========================================================================
# Root & Health Tests
# ===========================================================================

class TestRootEndpoints:

    def test_root_returns_welcome(self, setup_database):
        """GET / returns welcome message and metadata."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "Welcome to Book Management API"

    def test_health_check(self, setup_database):
        """GET /health returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


# ===========================================================================
# CRUD Operation Tests
# ===========================================================================

class TestCreateBook:

    def test_create_book_success(self, setup_database):
        """POST /books creates a book and returns 201."""
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "123-4567890123",
            "genre": "Fiction",
            "publication_year": 2024,
            "pages": 200,
            "rating": 4.5
        }
        response = client.post("/books", json=book_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Book"
        assert data["author"] == "Test Author"
        assert data["id"] >= 1
        assert "created_at" in data

    def test_create_book_duplicate_isbn(self, setup_database):
        """POST /books with duplicate ISBN returns 409 Conflict."""
        book_data = {"title": "Book 1", "author": "Author 1", "isbn": "123-4567890123"}
        client.post("/books", json=book_data)

        book_data2 = {"title": "Book 2", "author": "Author 2", "isbn": "123-4567890123"}
        response = client.post("/books", json=book_data2)
        assert response.status_code == 409
        assert "already" in response.json()["detail"].lower()

    def test_create_book_minimal_fields(self, setup_database):
        """POST /books with only required fields succeeds."""
        response = client.post("/books", json={"title": "Minimal", "author": "Auth"})
        assert response.status_code == 201

    def test_create_book_missing_title(self, setup_database):
        """POST /books without required title returns 422."""
        response = client.post("/books", json={"author": "No Title"})
        assert response.status_code == 422


class TestGetBook:

    def test_get_book_by_id(self, populated_db):
        """GET /books/{id} returns correct book."""
        book_id = populated_db[0]
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Book A"

    def test_get_book_not_found(self, setup_database):
        """GET /books/{nonexistent_id} returns 404."""
        response = client.get("/books/99999")
        assert response.status_code == 404

    def test_get_book_returns_full_schema(self, populated_db):
        """Response includes all expected fields."""
        book_id = populated_db[0]
        resp = client.get(f"/books/{book_id}")
        data = resp.json()
        for field in ("id", "title", "author", "created_at", "updated_at"):
            assert field in data, f"Missing field: {field}"


class TestUpdateBook:

    def test_update_book_partial(self, populated_db):
        """PUT /books/{id} with partial data updates only those fields."""
        book_id = populated_db[0]
        response = client.put(f"/books/{book_id}", json={"rating": 5.0, "title": "Updated"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["rating"] == 5.0

    def test_update_book_not_found(self, setup_database):
        """PUT /books/{nonexistent_id} returns 404."""
        response = client.put("/books/9999", json={"title": "Ghost"})
        assert response.status_code == 404

    def test_update_book_isbn_conflict(self, populated_db):
        """PUT /books/{id} changing ISBN to existing one returns 409."""
        # Create two books with different ISBNs
        r1 = client.post("/books", json={"title": "Alpha", "author": "X", "isbn": "111"})
        r2 = client.post("/books", json={"title": "Beta", "author": "Y", "isbn": "222"})
        id_beta = r2.json()["id"]

        # Try to change Beta's isbn to Alpha's -> conflict
        resp = client.put(f"/books/{id_beta}", json={"isbn": "111"})
        assert resp.status_code == 409


class TestDeleteBook:

    def test_delete_book_success(self, populated_db):
        """DELETE /books/{id} removes the book and returns confirmation."""
        book_id = populated_db[0]
        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()

        # Verify it's gone
        assert client.get(f"/books/{book_id}").status_code == 404

    def test_delete_book_not_found(self, setup_database):
        """DELETE /books/{nonexistent_id} returns 404."""
        response = client.delete("/books/9999")
        assert response.status_code == 404


# ===========================================================================
# List Endpoint Tests (Filtering, Search, Sort, Pagination)
# ===========================================================================

class TestListBooks:

    def test_list_books_default(self, populated_db):
        """GET /books returns paginated list."""
        response = client.get("/books")
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["total"] == 3
        assert len(data["books"]) == 3
        assert "has_next" in data["meta"]

    def test_filter_by_genre(self, populated_db):
        """?genre=Fiction filters correctly."""
        response = client.get("/books?genre=Fiction")
        data = response.json()
        assert all(b["genre"] == "Fiction" or "Fiction" in b["genre"]
                   for b in data["books"])

    def test_filter_by_author(self, populated_db):
        """?author=Author A filters by author."""
        response = client.get("/books?author=Author A")
        data = response.json()
        assert data["meta"]["total"] == 2

    def test_filter_by_min_rating(self, populated_db):
        """?min_rating=4.0 filters by rating threshold."""
        response = client.get("/books?min_rating=4.0")
        data = response.json()
        assert all(b["rating"] >= 4.0 for b in data["books"])

    def test_search_in_title_and_description(self, populated_db):
        """?search=text matches title or description."""
        response = client.get("/books?search=Book A")
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["total"] >= 1

    def test_sort_by_rating_desc(self, populated_db):
        """?sort_by=rating&order=desc sorts descending by rating."""
        response = client.get("/books?sort_by=rating&order=desc")
        books = response.json()["books"]
        ratings = [b["rating"] for b in books if b["rating"]]
        assert ratings == sorted(ratings, reverse=True)

    def test_pagination_skip_limit(self, populated_db):
        """?skip=1&limit=1 returns one item starting at offset 1."""
        response = client.get("/books?skip=1&limit=1")
        data = response.json()
        assert len(data["books"]) == 1
        assert data["meta"]["skip"] == 1
        assert data["meta"]["limit"] == 1

    def test_pagination_has_next_previous(self, populated_db):
        """Pagination meta flags are set correctly."""
        response = client.get("/books?limit=2")
        meta = response.json()["meta"]
        assert meta["has_next"] is True   # 3 total, limit=2 => has next
        assert meta["has_previous"] is False  # skip=0 => no previous

        response2 = client.get("/books?skip=2&limit=2")
        meta2 = response2.json()["meta"]
        assert meta2["has_next"] is False
        assert meta2["has_previous"] is True

    def test_v1_endpoint_works_too(self, populated_db):
        """GET /api/v1/books mirrors GET /books behaviour."""
        r1 = client.get("/books").json()
        r2 = client.get("/api/v1/books").json()
        assert r1["meta"]["total"] == r2["meta"]["total"]


# ===========================================================================
# Statistics Tests
# ===========================================================================

class TestStatistics:

    def test_stats_total_count(self, populated_db):
        """GET /stats reports correct total count."""
        response = client.get("/stats")
        data = response.json()
        assert data["total_books"] == 3

    def test_stats_average_rating(self, populated_db):
        """Average rating is computed correctly."""
        response = client.get("/stats")
        data = response.json()
        expected_avg = sum([4.0, 4.5, 3.5]) / 3
        assert abs(data["average_rating"] - round(expected_avg, 2)) < 0.01

    def test_stats_genre_distribution(self, populated_db):
        """Genre distribution reflects actual data."""
        response = client.get("/stats")
        dist = response.json()["genre_distribution"]
        assert "Fiction" in dist
        assert dist["Fiction"] == 1


# ===========================================================================
# Validation & Edge Case Tests
# ===========================================================================

class TestValidation:

    def test_invalid_rating_above_max(self, setup_database):
        """Rating > 5 is rejected with 422."""
        resp = client.post("/books", json={
            "title": "Bad", "author": "A", "rating": 6.0
        })
        assert resp.status_code == 422

    def test_invalid_year_out_of_range(self, setup_database):
        """Year outside [1000, 2100] rejected with 422."""
        resp = client.post("/books", json={
            "title": "Bad", "author": "A", "publication_year": 3000
        })
        assert resp.status_code == 422

    def test_empty_title_rejected(self, setup_database):
        """Empty string title is rejected."""
        resp = client.post("/books", json={"title": "", "author": "A"})
        assert resp.status_code == 422
