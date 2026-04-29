"""Create poll and option tables with seed data

Revision ID: d4a9f2c7e8b1
Revises: b1e2d7c0a9f4
Create Date: 2026-04-29 16:40:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d4a9f2c7e8b1"
down_revision: Union[str, None] = "b1e2d7c0a9f4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "poll",
        sa.Column("poll_id", sa.Integer(), nullable=False),
        sa.Column("question", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("create_by", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("poll_id"),
    )
    op.create_index(op.f("ix_poll_poll_id"), "poll", ["poll_id"], unique=False)

    op.create_table(
        "option",
        sa.Column("option_id", sa.Integer(), nullable=False),
        sa.Column("poll_id", sa.Integer(), nullable=False),
        sa.Column("option_text", sa.String(), nullable=False),
        sa.Column("vote_count", sa.Integer(), server_default="0", nullable=False),
        sa.ForeignKeyConstraint(["poll_id"], ["poll.poll_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("option_id"),
    )
    op.create_index(op.f("ix_option_option_id"), "option", ["option_id"], unique=False)
    op.create_index(op.f("ix_option_poll_id"), "option", ["poll_id"], unique=False)

    op.execute(
        """
        INSERT INTO poll (poll_id, question, create_by)
        VALUES
            (1, 'What is your favorite place to go on vacation?', 'system'),
            (2, 'What is your favorite season?', 'system');
        """
    )

    op.execute(
        """
        INSERT INTO option (poll_id, option_text, vote_count)
        VALUES
            (1, 'Bahamas', 0),
            (1, 'Europe', 0),
            (1, 'South America', 0),
            (1, 'Staycation', 0),
            (2, 'Spring', 0),
            (2, 'Summer', 0),
            (2, 'Autumn', 0),
            (2, 'Winter', 0);
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_option_poll_id"), table_name="option")
    op.drop_index(op.f("ix_option_option_id"), table_name="option")
    op.drop_table("option")

    op.drop_index(op.f("ix_poll_poll_id"), table_name="poll")
    op.drop_table("poll")
