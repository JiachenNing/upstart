"""Add userName to submissions

Revision ID: af73dd6ef01b
Revises: 3f27d4fce21a
Create Date: 2026-04-29 15:20:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "af73dd6ef01b"
down_revision: Union[str, None] = "3f27d4fce21a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("submissions", sa.Column("userName", sa.String(), nullable=True))
    op.create_index(op.f("ix_submissions_userName"), "submissions", ["userName"], unique=False)
    op.execute("UPDATE submissions SET \"userName\" = name WHERE \"userName\" IS NULL")
    op.alter_column("submissions", "userName", nullable=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_submissions_userName"), table_name="submissions")
    op.drop_column("submissions", "userName")
