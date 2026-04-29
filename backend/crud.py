from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from uuid import UUID
import models, schemas

# using SQLAlchemy ORM
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


def get_polls(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Poll)
        .options(joinedload(models.Poll.options))
        .order_by(models.Poll.poll_id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_poll(db: Session, poll_id: UUID):
    return (
        db.query(models.Poll)
        .options(joinedload(models.Poll.options))
        .filter(models.Poll.poll_id == poll_id)
        .first()
    )


def create_poll(db: Session, poll: schemas.PollCreate):
    db_poll = models.Poll(question=poll.question, create_by=poll.create_by)
    db.add(db_poll)
    db.flush()

    for option_text in poll.options:
        db_option = models.Option(
            poll_id=db_poll.poll_id,
            option_text=option_text,
            vote_count=0,
        )
        db.add(db_option)

    db.commit()
    db.refresh(db_poll)
    return get_poll(db=db, poll_id=db_poll.poll_id)
