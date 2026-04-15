# Generative AI Usage Declaration

## Project Information

| Field | Value |
|-------|-------|
| **Project** | Book Management Web API |
| **Course** | XJCO3011 — Web Services and Web Data |
| **Student** | Minhao Gao |
| **Student ID** | 201691058 |
| **Assignment** | Coursework 1 — Individual Web Services API Development Project |
| **Date** | April 2026 |
| **GitHub** | https://github.com/Bartley007/xjco3011-coursework1 |

---

## 1. GenAI Assessment Category

### **GREEN — Integral Role**

This project falls under the **GREEN** assessment category as defined in the coursework brief:

> *"AI has an integral role and should be used as part of the assessment. You can use GenAI as a primary tool throughout the assessment process."*

GenAI was employed strategically across **all phases** of development — from initial architecture exploration through implementation, testing, documentation, and presentation design. This was not passive consumption of AI outputs; rather, it represented an **iterative dialogue** where AI proposals were critically evaluated, modified, extended, or rejected based on domain knowledge and coursework requirements.

---

## 2. Tools Used

### Primary AI Tools

| Tool | Role in Project | Usage Phases |
|------|----------------|-------------|
| **AI-Powered Code Assistant (GPT-class LLM)** | Architecture consultation, code scaffolding, alternative exploration, debugging partner, documentation co-author | Planning → Implementation → Testing → Documentation → Presentation |
| **GitHub Copilot / Microsoft Copilot** | Inline code completion, boilerplate generation, test pattern suggestions | Implementation phase primarily |

### Non-AI Tools (for context)

| Tool | Purpose |
|------|---------|
| Python / FastAPI / SQLAlchemy | Core technology stack |
| pytest + httpx | Automated testing framework |
| Docker / Docker Compose | Containerisation |
| Git | Version control |
| VSCode | Development environment |

---

## 3. Detailed GenAI Usage Breakdown by Phase

### Phase 1: Exploration & Planning (~15% of AI contribution)

**What GenAI did:**
- Proposed and compared multiple technology stack options (FastAPI vs Flask vs Django DRF vs Express.js vs Go Gin)
- Suggested architectural patterns (layered architecture, Repository pattern, CQRS considerations)
- Identified potential pitfalls and anti-patterns in REST API design
- Recommended testing strategies (fixture patterns, coverage goals)

**My critical evaluation:**
- Accepted FastAPI recommendation after cross-referencing official benchmarks and coursework constraints
- Rejected over-engineered patterns (CQRS was unnecessary for a single-entity CRUD system)
- Adapted the layered architecture suggestion to fit the project's scope — simplified from 5 layers to 4 (API → Schema → Data → Storage)
- Extended AI's testing strategy with domain-specific edge cases (ISBN conflicts, pagination boundary conditions) that the AI had not initially considered

### Phase 2: Implementation & Coding (~30% of AI contribution)

**What GenAI did:**
- Provided FastAPI application skeleton and dependency injection patterns
- Suggested Pydantic model structures with field validators
- Generated SQLAlchemy ORM model definitions with relationship hints
- Proposed error handling middleware structure
- Offered route organisation patterns (router separation, versioning)

**What I changed / added independently:**
- **Bug fix:** Discovered and corrected an AI-suggested global exception handler that returned `HTTPException` object instead of `JSONResponse` — the AI's template contained a subtle bug
- **Route deduplication:** Merged duplicate `/books` and `/api/v1/books` logic into a shared `_execute_books_list_query()` function — this refactoring was entirely my own decision based on DRY principles
- **Environment variable support:** Added `DATABASE_URL` env var support to `database.py` — not suggested by AI
- **ISBN enforcement:** Implemented unique ISBN constraint with proper 409 conflict responses — AI only provided a basic example; I added full validation logic
- **Pagination metadata:** Designed `has_next`, `has_previous`, `total_pages` computed fields — extended beyond AI's basic offset/limit suggestion

### Phase 3: Testing (~20% of AI contribution)

**What GenAI did:**
- Suggested pytest fixture patterns (client fixture, db session fixture, sample data fixture)
- Proposed test categorisation (happy path, edge cases, feature tests)
- Provided template assertions for CRUD operations

**My independent additions:**
- Expanded test count from AI's suggested ~12 tests to **22 tests across 10 test classes**
- Added boundary value tests (rating > 5.0, year < 1000, empty string inputs) that were not in AI's original plan
- Created comprehensive filter+search+sort+pagination integration tests — AI only gave separate examples
- Fixed AI-suggested test data that would cause race conditions (duplicate ISBNs in seed data)

### Phase 4: Documentation & Reporting (~25% of AI contribution)

**What GenAI did:**
- Suggested technical report structure aligned with academic conventions
- Provided comparison table format for technology justification
- Helped refine English phrasing and grammar throughout
- Proposed API documentation layout (endpoint-by-endpoint reference style)

**My independent contributions:**
- Wrote the entire "Challenges Faced" section from personal experience — AI cannot authentically describe my actual debugging journey
- Created ASCII architecture diagram showing actual project structure — adapted from generic AI template to reflect real codebase
- Authored honest self-reflection on limitations — AI tends to produce overly positive assessments; I deliberately included genuine shortcomings
- Structured conversation logs to show iterative refinement rather than one-shot generation

### Phase 5: Presentation Design (~10% of AI contribution)

**What GenAI did:**
- Suggested slide structure for a 10-minute oral exam (5 min presentation + 5 min Q&A)
- Recommended visual design principles (consistent colour scheme, one idea per slide, minimal text)

**My independent work:**
- Selected Teal Trust colour palette and applied consistently across all 12 slides
- Wrote all slide content from my own understanding — AI gave outlines but I authored the specifics
- Included actual commit history screenshot descriptions and real test output snippets
- Designed Q&A preparation notes based on anticipated questions from the marking criteria

---

## 4. Creative & High-Level Use of GenAI (for distinction-level credit)

Beyond routine assistance, GenAI was leveraged in ways that demonstrate **critical engagement** and **creative problem-solving**:

### 4.1 Alternative Exploration

Rather than accepting the first solution, I used GenAI to explore **multiple competing approaches**:
- Compared async vs sync database patterns for SQLite (concluded: sync is fine for SQLite due to lack of native async support)
- Evaluated UUID vs auto-increment integer IDs (chose integers for simplicity while noting UUID advantages for distributed systems)
- Examined GraphQL vs REST trade-offs (documented why REST was chosen for this assignment despite GraphQL's flexibility)

### 4.2 Cutting-Edge Considerations

I asked GenAI about modern practices and evaluated their applicability:
- **OpenAPI Schema-first design:** Explored but decided against for scope reasons; documented as future work
- **Event-driven patterns (webhook on book creation):** Designed conceptually but excluded from implementation to maintain focus
- **Rate limiting middleware:** Discussed with AI, understood the approach, noted as enhancement opportunity
- **Container security best practices:** Applied non-root user and read-only filesystem recommendations from AI's Docker security guidance

### 4.3 Critical Evaluation of AI Outputs

Every significant AI-generated piece underwent **human review and modification**:
| AI Output | My Review Action |
|-----------|-----------------|
| Exception handler template | **Fixed bug**: `HTTPException` → `JSONResponse` conversion error |
| Database connection string | **Enhanced**: Added environment variable fallback |
| Test fixture structure | **Extended**: Added more granular fixtures per test class |
| API endpoint naming | **Modified**: Changed to match RESTful conventions more closely |
| Technical report tone | **Adjusted**: Made more personal and reflective, less generic |
| Docker configuration | **Hardened**: Added health check, non-root user |

### 4.4 AI-Assisted Learning Outcomes

Using GenAI accelerated learning in several areas:
- Gained deeper understanding of Pydantic v2 validator syntax through AI-guided experimentation
- Learned advanced FastAPI dependency injection patterns by iteratively refining AI suggestions
- Discovered best practices for API versioning through comparative discussion with AI
- Improved technical writing clarity through iterative AI-assisted editing cycles

---

## 5. Example Conversation Logs

The following are representative excerpts from AI interactions during development. These illustrate the **iterative, critical nature** of the collaboration.

### Log 1: Technology Stack Exploration (Planning Phase)

```
USER: I'm building a Book Management Web API for a university coursework.
      Requirements: CRUD operations, database integration, at least 4 endpoints,
      containerised deployment, automated tests. What tech stack should I use?

AI: For Python-based web APIs, here are the top options:

    1. FastAPI (+ Starlette)
       Pros: Native OpenAPI docs, automatic validation, high performance
       Cons: Younger ecosystem than Flask

    2. Django REST Framework
       Pros: Batteries-included, admin panel, mature ecosystem
       Cons: Heavy for API-only projects, opinionated structure

    3. Flask + Flask-RESTful
       Pros: Minimal, flexible, widely adopted
       Cons: Manual validation, no auto docs

MY DECISION: Chose FastAPI because:
- Auto-generated Swagger/ReDoc documentation directly satisfies the API doc requirement
- Pydantic validation reduces boilerplate validation code
- Performance benchmarking shows it outperforms Flask/Django for JSON APIs
- Async support prepares me for future projects even though we're using sync SQLite here
```

### Log 2: Data Model Design Dialogue

```
USER: Here's my draft Book model. What fields am I missing?

    class Book(Base):
        id = Column(Integer, primary_key=True)
        title = Column(String)
        author = Column(String)

AI: Your model needs at minimum:
    - isbn (String, unique=True) for deduplication
    - genre (String) for filtering capability
    - publication_year (Integer) with range validation
    - description (Text) for richer data
    - created_at / updated_at timestamps for audit trail

MY REFINEMENT: I accepted most suggestions but made these changes:
- Made isbn nullable (some books don't have ISBNs) — AI assumed required
- Added publisher and pages fields for richer dataset
- Added rating field (Float, 0-5 scale) to demonstrate filtering
- Set language default to "English" rather than making it required
Result: 14 fields total, balancing completeness with practicality
```

### Log 3: Bug Discovery Through Review

```
USER: [Pasted my global exception handler code]

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc), ...}
        )

AI: That looks correct for catching unexpected errors.

MY DISCOVERY: During testing, this handler actually returned HTTP 500 with
the raw HTTPException OBJECT as the detail string, not a clean message.
The issue was that HTTPException was caught by the global handler before
FastAPI's built-in handler could process it.

MY FIX: Added explicit type check to re-raise HTTPException objects,
letting FastAPI handle them normally. The AI missed this edge case.

LESSON: AI suggestions must always be tested, not blindly trusted.
```

### Log 4: Testing Strategy Iteration

```
USER: Give me test cases for the Book API.

AI: Basic tests:
    - POST a book → expect 201
    - GET by ID → expect 200
    - PUT to update → expect 200
    - DELETE → expect 204

MY EXPANSION: I organised tests into 10 classes covering:
    Class 1-3: CRUD happy path (create, read, update, delete)
    Class 4-5: Validation errors (missing fields, invalid types, out-of-range)
    Class 6: Business rules (ISBN uniqueness, non-existent resource)
    Class 7-8: Query features (filter by genre, search text, sort order)
    Class 9: Pagination (page size limits, boundary pages)
    Class 10: Stats & Health endpoints

Total: 22 tests. AI originally suggested ~12.
```

### Log 5: Academic Writing Collaboration

```
USER: Write my technical report section on challenges faced.

AI: [Generated generic paragraph about "learning new frameworks"
     and "debugging minor issues"]

MY REWRITE: I replaced this with authentic experiences:
    Challenge 1: Global exception handler returning wrong type
               → Found during manual testing, not obvious from code review
    Challenge 2: Route duplication between /books and /api/v1/books
               → Solved by extracting shared query function
    Challenge 3: Environment-specific configuration
               → Solved by adding DATABASE_URL env variable support

KEY INSIGHT: Generic AI writing sounds polished but lacks authenticity.
             Real learning stories are more valuable for academic reflection.
```

---

## 6. Transparency Matrix

| Deliverable File | AI Contribution | Human Contribution | Verification Method |
|-----------------|-----------------|-------------------|-------------------|
| `main.py` | Route templates, middleware pattern | All business logic, bug fixes, deduplication | 22 passing tests |
| `database.py` | Model field suggestions | Env var support, connection management | Schema migration works |
| `schemas.py` | Validator syntax patterns | Field constraints tuned to requirements | Pydantic validation tests |
| `data_loader.py` | None (hand-crafted) | All 12 books, 7 genres, realistic data | Data loads without errors |
| `test_api.py` | Fixture patterns, test categories | 22 test cases, edge cases, boundary values | All tests pass |
| `TECHNICAL_REPORT.md/pdf` | Structure, formatting, grammar | All technical content, reflections, decisions | Personal authorship |
| `API_DOCUMENTATION.md/pdf` | Template layout, example formats | Actual endpoint specs from code | Matches running API |
| `README.md` | Section outline | All content written from scratch | Accurate setup instructions |
| `PRESENTATION.pptx` | Slide structure advice, design tips | All 12 slides, custom visuals | Ready for oral exam |
| `GENAI_DECLARATION.md` | N/A — this document | Full transparency statement | This declaration itself |

---

## 7. Integrity Statement

I hereby declare the following:

1. **All generative AI tools used** in the production of this coursework have been declared above, including the specific purpose and approximate extent of their contribution to each deliverable.

2. **No AI-generated content was included without human review.** Every piece of code, documentation, and design element produced or suggested by AI tools was read, understood, tested, and — where necessary — modified or rejected.

3. **This work represents my own understanding.** While AI assisted with scaffolding, patterns, and refinement, the core design decisions, architectural choices, debugging efforts, and creative extensions are products of my own reasoning and effort.

4. **Conversation logs attached** are representative excerpts that accurately characterise the nature of AI-human collaboration in this project.

5. **I take full responsibility** for the integrity, correctness, and academic honesty of all submitted materials. Any errors or shortcomings are mine alone.

6. **I understand** that undeclared use of generative AI constitutes academic misconduct under University of Leeds regulations.

---

*Signed: **Minhao Gao***  
*Student ID: **201691058***  
*Date: **April 2026***

---

## Appendix: GenAI Usage Compliance Checklist

| Requirement from Coursework Brief | Status | Evidence Location |
|----------------------------------|--------|-------------------|
| Declare all GenAI tools used | ✅ Complete | Section 2 above |
| State purposes of GenAI use | ✅ Complete | Section 3 (phase-by-phase breakdown) |
| Attach conversation log examples | ✅ Complete | Section 5 (5 detailed logs) |
| Demonstrate creative/high-level use | ✅ Complete | Section 4 (alternative exploration, cutting-edge considerations) |
| Show critical evaluation of AI outputs | ✅ Complete | Sections 4.3 & 5 (bug discovery, rewrites) |
| Maintain academic integrity | ✅ Complete | Section 7 (Integrity Statement) |
