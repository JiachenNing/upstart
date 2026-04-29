# Full-Stack Application (FastAPI + React + PostgreSQL)

React (TypeScript) frontend, FastAPI backend, PostgreSQL with SQLAlchemy and Alembic.

## Prerequisites

- Docker and Docker Compose
- Node.js and npm
- Python 3.10+
---------------------------------


---------------------------------
## Afrer migration:
```bash
cd backend
source venv/bin/activate
alembic upgrade head
uvicorn main:app --reload
```
```bash
cd frontend
npm run dev
```

## Initial setup
```bash
docker-compose up -d
```

Backend: virtual environment and dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Apply database migrations
```bash
alembic upgrade head
```
This repo already includes migration files under `backend/alembic/versions/`. You only need `alembic revision --autogenerate -m "..."` when you **change models** and want to generate a new migration; then run `alembic upgrade head` again.

Frontend:
```bash
cd frontend
npm install
```

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Frontend dev server: [http://localhost:5173](http://localhost:5173) (Vite default)

## Stopping services
- **Stop PostgreSQL (keep data):** from the project root, `docker-compose down`.
- **Remove the database volume (wipes local DB data):** `docker-compose down -v`. Only use this if you intend to delete all data in the Docker volume.
