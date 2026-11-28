"""create review table

Revision ID: 0006
Revises: 0005
Create Date: 2026-11-27 23:12:23.508696

"""

from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

RATING_COLUMNS = ["taste", "atmosphere", "cleanliness", "price", "service"]

def upgrade() -> None:
    op.create_table(
        "review",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        *[sa.Column(name, sa.Integer(), nullable=False) for name in RATING_COLUMNS],
        sa.Column("comment", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        *[
            sa.CheckConstraint(f"{name} BETWEEN 1 AND 5", name=f"ck_review_{name}")
            for name in RATING_COLUMNS
        ],
        sa.ForeignKeyConstraint(
            ["restaurant_id"], ["restaurant.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["app_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "restaurant_id", "user_id", name="uq_review_restaurant_user"
        ),
    )
    op.create_index("ix_review_restaurant_id", "review", ["restaurant_id"])
    op.create_index("ix_review_user_id", "review", ["user_id"])

def downgrade() -> None:
    op.drop_index("ix_review_user_id", table_name="review")
    op.drop_index("ix_review_restaurant_id", table_name="review")
    op.drop_table("review")