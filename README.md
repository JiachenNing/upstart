# Full-Stack Application (FastAPI + React + PostgreSQL)

React (TypeScript) frontend, FastAPI backend, PostgreSQL with SQLAlchemy and Alembic.

## Prerequisites

- Docker and Docker Compose
- Node.js and npm
- Python 3.10+
---------------------------------
Poll API

A Poll is a single question with multiple options. An example Poll:

What is your favorite place to go on vacation?
Bahamas
Europe
South America
Staycation

Desired features:
Features are listed in priority order. You do not need to implement all of the features.

An endpoint for a user to create a new poll with a title and a list of options
An endpoint for a user to edit their poll
An endpoint for a user to vote on a poll
Modify the create and edit endpoints to allow for a poll to be marked as public or private
An endpoint to get all polls along with their options and vote counts
Create a UI that uses the endpoints to do CRUD on polls


MVP V1
- create a poll & view all polls
user should see the list of existing polls (GET /polls)
at the top of the page, create a "Add" button which allow user to create a new poll, user should have text boxes to enter the question + options, then click on "Submit" will call (POST /polls)

- vote on a poll option
user can click on each of the poll, and direct to the dedicated poll page. (GET /polls/{id})
on the poll page, user should see all the options, and allow user to choose one option. 


API schema:
GET /polls

POST /polls
{
    question: "What is your favorite place to go on vacation?",
    options: []
}

GET /polls/{id}


DB schema:

poll table:
poll_id (UUID PK)
question
created_at
create_by

option table: 
option_id (PK)
poll_id (FK)
option_text
vote_count


seed data:

poll
- (1) What is your favorite place to go on vacation?
- (2) What is your favorite season?

option
- poll_id=1: Bahamas, Europe, South America, Staycation
- poll_id=2: Spring, Summer, Autumn, Winter


Out of scope:
authentication


MVP V2:

Modify the create and edit endpoints to allow for a poll to be marked as public or private
add 



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
