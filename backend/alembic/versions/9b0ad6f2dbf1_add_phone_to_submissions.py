"""Add phone to submissions

Revision ID: 9b0ad6f2dbf1
Revises: cdb4ff47bc49
Create Date: 2026-04-25 22:02:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9b0ad6f2dbf1"
down_revision: Union[str, None] = "cdb4ff47bc49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("submissions", sa.Column("phone", sa.String(), nullable=True))
    op.create_index(op.f("ix_submissions_phone"), "submissions", ["phone"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_submissions_phone"), table_name="submissions")
    op.drop_column("submissions", "phone")
