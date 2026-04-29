from pydantic import BaseModel
from typing import Optional

class SubmissionBase(BaseModel):
    name: str
    userName: Optional[str] = None
    email: str
    phone: str
    gender: Optional[str] = None
    message: str

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
