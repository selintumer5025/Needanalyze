# Needanalyze

Needanalyze is an internal learning & development assistant that analyzes competency gaps, recommends activities, and tracks development journeys for employees. The project ships with a FastAPI backend and a React + TypeScript frontend.

## Architecture overview

```
backend/
  app/
    config.py             # environment settings (database URL, frontend origin)
    database.py           # SQLAlchemy engine/session helpers
    models/               # ORM models for employees, competencies, activities, plans
    schemas/              # Pydantic schemas shared by routers/services
    services/             # Domain services (e.g., matching_service)
    routers/              # FastAPI routers (employees, catalog)
    main.py               # application entrypoint
frontend/
  src/
    api/                  # Axios API clients
    components/           # Reusable UI components
    context/              # Auth context (mock login)
    pages/                # Login, employee dashboard, admin dashboard
    App.tsx / main.tsx    # React root
```

The backend exposes RESTful endpoints that return recommendations (`/employees/{id}/recommendations`), plan data (`/employees/{id}/plan`), and CRUD catalog endpoints under `/catalog`. The matching service compares employee assessments with role competency requirements and recommends activities grouped into journeys.

The frontend consumes these APIs and provides three primary routes: `/login`, `/dashboard` (employee view), and `/admin` (catalog/analytics workspace).

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/needanalyze"  # adjust as needed
uvicorn app.main:app --reload
```

> **Note:** For local experiments you can also point `DATABASE_URL` to a SQLite database (e.g., `sqlite:///./needanalyze.db`). Production deployments should use PostgreSQL with Alembic migrations.

### Key endpoints

- `GET /health` – service heartbeat.
- `GET /employees/{id}/recommendations` – competency gap analysis and journey suggestions.
- `GET /employees/{id}/plan` – list of planned activities (with status & metadata).
- `POST /employees/{id}/plan` – add an activity to an employee plan.
- `PATCH /employees/{id}/plan/{plan_id}` – update plan status/dates.
- `GET|POST|PUT|DELETE /catalog/competencies` – competency catalog management.
- `GET|POST|PUT|DELETE /catalog/activities` – development activity catalog.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server will start on http://localhost:5173. Update `VITE_API_URL` in a `.env` file if your backend runs on a different host or port.

### Mock authentication

Login accepts any employee code. For demo purposes the numeric part of the code is used as the employee ID when calling the backend (e.g., entering `EMP001` targets employee ID `1`).

## Development notes

- The matching logic lives in `backend/app/services/matching_service.py` and is intentionally modular so that scoring/ML approaches can replace the rule-based recommender in the future.
- Database tables are created automatically via `Base.metadata.create_all` for convenience. Replace this with Alembic migrations in production.
- Analytics components in the frontend currently display placeholder text but are wired for future expansion.
