from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Create the database tables if they do not exist
# Note: Migrations are handled by alembic, but to be safe for dev without migrations we can leave this or rely strictly on alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Full-Stack Web App API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change to frontend url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Full-Stack Web App API",
        "docs": "/docs",
        "submissions": "/submissions/",
    }


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submissions/", response_model=schemas.Submission)
def create_submission(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    return crud.create_submission(db=db, submission=submission)

@app.get("/submissions/", response_model=list[schemas.Submission])
def read_submissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    submissions = crud.get_submissions(db, skip=skip, limit=limit)
    return submissions


@app.delete("/submissions/{submission_id}", response_model=schemas.MessageResponse)
def remove_submission(submission_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_submission(db=db, submission_id=submission_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Submission not found.")
    return {"message": "Submission deleted successfully."}
