"""Convert poll_id to UUID

Revision ID: e6b7a9c1d2f3
Revises: d4a9f2c7e8b1
Create Date: 2026-04-29 16:55:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "e6b7a9c1d2f3"
down_revision: Union[str, None] = "d4a9f2c7e8b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.add_column(
        "poll",
        sa.Column(
            "poll_uuid",
            postgresql.UUID(as_uuid=False),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    op.add_column("option", sa.Column("poll_uuid_ref", postgresql.UUID(as_uuid=False), nullable=True))

    op.execute(
        """
        UPDATE option o
        SET poll_uuid_ref = p.poll_uuid
        FROM poll p
        WHERE o.poll_id = p.poll_id
        """
    )

    op.drop_constraint("option_poll_id_fkey", "option", type_="foreignkey")
    op.drop_constraint("poll_pkey", "poll", type_="primary")
    op.drop_index(op.f("ix_option_poll_id"), table_name="option")
    op.drop_index(op.f("ix_poll_poll_id"), table_name="poll")

    op.drop_column("option", "poll_id")
    op.drop_column("poll", "poll_id")

    op.alter_column("poll", "poll_uuid", new_column_name="poll_id", server_default=sa.text("gen_random_uuid()"))
    op.alter_column("option", "poll_uuid_ref", new_column_name="poll_id", nullable=False)

    op.create_primary_key("poll_pkey", "poll", ["poll_id"])
    op.create_foreign_key(
        "option_poll_id_fkey",
        "option",
        "poll",
        ["poll_id"],
        ["poll_id"],
        ondelete="CASCADE",
    )
    op.create_index(op.f("ix_poll_poll_id"), "poll", ["poll_id"], unique=False)
    op.create_index(op.f("ix_option_poll_id"), "option", ["poll_id"], unique=False)


def downgrade() -> None:
    op.drop_constraint("option_poll_id_fkey", "option", type_="foreignkey")
    op.drop_constraint("poll_pkey", "poll", type_="primary")
    op.drop_index(op.f("ix_option_poll_id"), table_name="option")
    op.drop_index(op.f("ix_poll_poll_id"), table_name="poll")

    op.add_column("poll", sa.Column("poll_id_int", sa.Integer(), nullable=True))
    op.add_column("option", sa.Column("poll_id_int_ref", sa.Integer(), nullable=True))

    op.execute(
        """
        WITH numbered_polls AS (
            SELECT poll_id, ROW_NUMBER() OVER (ORDER BY created_at, question) AS new_id
            FROM poll
        )
        UPDATE poll p
        SET poll_id_int = np.new_id
        FROM numbered_polls np
        WHERE p.poll_id = np.poll_id
        """
    )

    op.execute(
        """
        UPDATE option o
        SET poll_id_int_ref = p.poll_id_int
        FROM poll p
        WHERE o.poll_id = p.poll_id
        """
    )

    op.drop_column("option", "poll_id")
    op.drop_column("poll", "poll_id")

    op.alter_column("poll", "poll_id_int", new_column_name="poll_id", nullable=False)
    op.alter_column("option", "poll_id_int_ref", new_column_name="poll_id", nullable=False)

    op.create_primary_key("poll_pkey", "poll", ["poll_id"])
    op.create_foreign_key(
        "option_poll_id_fkey",
        "option",
        "poll",
        ["poll_id"],
        ["poll_id"],
        ondelete="CASCADE",
    )
    op.create_index(op.f("ix_poll_poll_id"), "poll", ["poll_id"], unique=False)
    op.create_index(op.f("ix_option_poll_id"), "option", ["poll_id"], unique=False)
