from sqlalchemy.orm import Session
import models, schemas

def get_submissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Submission).offset(skip).limit(limit).all()

def create_submission(db: Session, submission: schemas.SubmissionCreate):
    db_submission = models.Submission(
        name=submission.name, 
        userName=submission.userName,
        email=submission.email, 
        phone=submission.phone,
        gender=submission.gender,
        message=submission.message
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def delete_submission(db: Session, submission_id: int):
    db_submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if db_submission is None:
        return False

    db.delete(db_submission)
    db.commit()
    return True
