"""Add gender to submissions

Revision ID: 3f27d4fce21a
Revises: 9b0ad6f2dbf1
Create Date: 2026-04-25 22:30:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f27d4fce21a"
down_revision: Union[str, None] = "9b0ad6f2dbf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("submissions", sa.Column("gender", sa.String(), nullable=True))
    op.create_index(op.f("ix_submissions_gender"), "submissions", ["gender"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_submissions_gender"), table_name="submissions")
    op.drop_column("submissions", "gender")
