from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class SubmissionBase(BaseModel):
    name: str
    userName: Optional[str] = None
    email: str
    phone: str
    gender: Optional[str] = None
    message: str

# Input schema (POST request)
class SubmissionCreate(SubmissionBase):
    pass

# Output schema (response model)
class Submission(SubmissionBase):
    id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str


class PollCreate(BaseModel):
    question: str
    options: list[str]
    create_by: Optional[str] = None


class PollOption(BaseModel):
    option_id: int
    poll_id: UUID
    option_text: str
    vote_count: int

    class Config:
        from_attributes = True


class Poll(BaseModel):
    poll_id: UUID
    question: str
    created_at: datetime
    create_by: Optional[str] = None
    options: list[PollOption]

    class Config:
        from_attributes = True
