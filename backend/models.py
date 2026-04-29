from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    userName = Column(String, nullable=True, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    gender = Column(String, nullable=True)
    message = Column(Text)


class Poll(Base):
    __tablename__ = "poll"

    poll_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )
    question = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    create_by = Column(String, nullable=True)

    options = relationship(
        "Option",
        back_populates="poll",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Option(Base):
    __tablename__ = "option"

    option_id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(UUID(as_uuid=True), ForeignKey("poll.poll_id", ondelete="CASCADE"), index=True, nullable=False)
    option_text = Column(String, nullable=False)
    vote_count = Column(Integer, nullable=False, default=0, server_default="0")

    poll = relationship("Poll", back_populates="options")
