"""Make userName nullable

Revision ID: b1e2d7c0a9f4
Revises: af73dd6ef01b
Create Date: 2026-04-29 15:25:00.000000
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b1e2d7c0a9f4"
down_revision: Union[str, None] = "af73dd6ef01b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("submissions", "userName", nullable=True)


def downgrade() -> None:
    op.execute("UPDATE submissions SET \"userName\" = name WHERE \"userName\" IS NULL")
    op.alter_column("submissions", "userName", nullable=False)
