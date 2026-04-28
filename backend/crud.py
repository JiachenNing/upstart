from sqlalchemy.orm import Session
import models, schemas

def get_submissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Submission).offset(skip).limit(limit).all()

def create_submission(db: Session, submission: schemas.SubmissionCreate):
    db_submission = models.Submission(
        name=submission.name, 
        email=submission.email, 
        phone=submission.phone,
        gender=submission.gender,
        message=submission.message
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission
