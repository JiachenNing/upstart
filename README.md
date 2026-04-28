# Full-Stack Application (FastAPI + React + PostgreSQL)

React (TypeScript) frontend, FastAPI backend, PostgreSQL with SQLAlchemy and Alembic.

## Prerequisites

- Docker and Docker Compose
- Node.js and npm
- Python 3.10+

All commands below assume your shell’s current directory is the **project root** (the folder that contains `docker-compose.yml`).

---

## Initial setup (first time on this machine)

Do these steps once after cloning or copying the repo.

### 1. Start PostgreSQL (Docker)

```bash
docker-compose up -d
```

PostgreSQL listens on `localhost:5432` with user `postgres`, password `12345`, and database `postgres` (see `docker-compose.yml` and `backend/database.py`).

### 2. Backend: virtual environment and dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the venv with `venv\Scripts\activate` instead of `source venv/bin/activate`.

### 3. Apply database migrations

With the database container running and the venv **activated** in `backend`:

```bash
alembic upgrade head
```

This repo already includes migration files under `backend/alembic/versions/`. You only need `alembic revision --autogenerate -m "..."` when you **change models** and want to generate a **new** migration; then run `alembic upgrade head` again.

### 4. Frontend: install dependencies

From the project root:

```bash
cd frontend
npm install
```

### 5. Confirm URLs (optional)

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000) — docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Frontend dev server: [http://localhost:5173](http://localhost:5173) (Vite default)

---

## After every computer restart

Docker does not restart this project’s containers by default. Each time you come back from a reboot (or if PostgreSQL is not running), do the following.

### 1. Start the database again

From the project root:

```bash
docker-compose up -d
```

### 2. Run the backend (one terminal)

```bash
cd backend
source venv/bin/activate
alembic upgrade head
uvicorn main:app --reload
```

`alembic upgrade head` is quick and safe if you are already up to date; skip it if you prefer, but it ensures any new migrations from a `git pull` are applied.

### 3. Run the frontend (second terminal)

```bash
cd frontend
npm run dev
```

Open the app in the browser at the URL printed by Vite (usually `http://localhost:5173`).

---

## Stopping services

- **Stop app processes:** press `Ctrl+C` in each terminal running `uvicorn` or `npm run dev`.
- **Stop PostgreSQL (keep data):** from the project root, `docker-compose down`.
- **Remove the database volume (wipes local DB data):** `docker-compose down -v`. Only use this if you intend to delete all data in the Docker volume.
