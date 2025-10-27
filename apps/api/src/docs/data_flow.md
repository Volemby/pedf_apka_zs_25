                          🧠 FASTAPI CLEAN ARCHITECTURE OVERVIEW
                          =====================================

                             ┌────────────────────────────────┐
                             │            CLIENTS              │
                             │  (Next.js Frontend, Mobile, etc.) │
                             └────────────────────────────────┘
                                             │
                                             ▼
                          ┌────────────────────────────────┐
                          │     PRESENTATION LAYER (API)   │
                          │────────────────────────────────│
                          │ 📂 api/presentation/            │
                          │                                │
                          │ • routers/  → FastAPI endpoints │
                          │ • schemas/  → Pydantic models   │
                          │                                │
                          │ Role:                          │
                          │ - Validates HTTP input (request)│
                          │ - Maps JSON ↔ Domain DTOs       │
                          │ - Adapts responses per UI view  │
                          │                                │
                          │ Example:                        │
                          │   POST /artworks → ArtworkIn    │
                          │   GET /artist-dashboard →       │
                          │         ArtworkForArtistDashboard│
                          └────────────────────────────────┘
                                             │
                                             ▼
                          ┌────────────────────────────────┐
                          │        DOMAIN LAYER (Core)     │
                          │────────────────────────────────│
                          │ 📂 api/domain/                  │
                          │                                │
                          │ • models/  → DTOs, enums        │
                          │ • repositories/ → Interfaces    │
                          │ • services/ → Business logic    │
                          │                                │
                          │ Role:                          │
                          │ - Encapsulates business rules   │
                          │ - Pure Python (no FastAPI, ORM) │
                          │ - Defines system behavior       │
                          │                                │
                          │ Example:                        │
                          │   ArtworkService.create_artwork │
                          │   ArtistService.list_artists    │
                          └────────────────────────────────┘
                                             │
                                             ▼
                          ┌────────────────────────────────┐
                          │   INFRASTRUCTURE LAYER (DB)    │
                          │────────────────────────────────│
                          │ 📂 api/infrastructure/orm/     │
                          │                                │
                          │ • SQLAlchemy ORM models         │
                          │ • Repository implementations    │
                          │ • DB adapters / sessions        │
                          │                                │
                          │ Role:                          │
                          │ - Interacts with PostgreSQL     │
                          │ - Maps ORM ↔ Domain DTOs        │
                          │ - Hides persistence details     │
                          │                                │
                          │ Example:                        │
                          │   SqlAlchemyArtworkRepository   │
                          │     (implements ArtworkRepo)    │
                          └────────────────────────────────┘
                                             │
                                             ▼
                          ┌────────────────────────────────┐
                          │   DATABASE / EXTERNAL SYSTEMS   │
                          │────────────────────────────────│
                          │ PostgreSQL / Alembic / Stripe / │
                          │ S3 / etc.                        │
                          └────────────────────────────────┘


               ┌──────────────────────────────────────────────────────────────┐
               │  DEPENDENCY DIRECTION (Flow of knowledge)                    │
               │──────────────────────────────────────────────────────────────│
               │  Presentation  →  Domain  →  Infrastructure  →  Database      │
               │  (API Layer)      (Logic)     (Implementation)   (Storage)    │
               └──────────────────────────────────────────────────────────────┘


              ┌────────────────────────────────────────────────────────────────┐
              │            DATA FLOW EXAMPLES                                   │
              │────────────────────────────────────────────────────────────────│
              │ READ (GET /artworks)                                            │
              │ ─────────────────────────────────────────────────────────────── │
              │ 1️⃣ HTTP Request → Router (presentation)                        │
              │ 2️⃣ Calls Service (domain)                                      │
              │ 3️⃣ Service uses Repository (domain→infrastructure)             │
              │ 4️⃣ Repository queries DB (ORM)                                 │
              │ 5️⃣ ORM → Domain DTO                                            │
              │ 6️⃣ Domain DTO → Presentation Schema                            │
              │ 7️⃣ Response → JSON to Frontend                                 │
              │                                                                │
              │ WRITE (POST /artworks)                                          │
              │ ─────────────────────────────────────────────────────────────── │
              │ 1️⃣ HTTP JSON → Input Schema (presentation)                     │
              │ 2️⃣ Schema → Domain DTO                                         │
              │ 3️⃣ DTO → Service (business logic)                              │
              │ 4️⃣ Service → Repository → ORM → DB commit                      │
              │ 5️⃣ ORM → DTO → Output Schema                                   │
              │ 6️⃣ Schema → JSON → Frontend                                    │
              └────────────────────────────────────────────────────────────────┘


                    ⚙️ SUPPORT LAYERS
                    -----------------
                    📂 api/core/di.py      → Dependency Injection wiring
                    📂 api/api.py          → FastAPI app composition
                    📂 api/alembic/        → DB migrations
                    📂 api/scripts/db_admin.py → Admin utilities


   Summary:
   - Presentation: shapes and validates data for HTTP (still backend)
   - Domain: pure logic, DB-agnostic, the heart of the app
   - Infrastructure: handles persistence and I/O details
   - Composition (DI): wires everything together

