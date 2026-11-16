"""

expand restaurant fields

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-17

"""

from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("restaurant") as batch_op:
        batch_op.add_column(
            sa.Column(
                "area",
                sa.String(length=100),
                nullable=False,
                server_default="Unknown",
            )
        )
        batch_op.add_column(sa.Column("address", sa.String(length=255), nullable=True))
        batch_op.add_column(
            sa.Column("description", sa.String(length=500), nullable=True)
        )
        batch_op.drop_column("rating")


def downgrade() -> None:
    with op.batch_alter_table("restaurant") as batch_op:
        batch_op.add_column(
            sa.Column("rating", sa.Float(), nullable=False, server_default="0")
        )
        batch_op.drop_column("description")
        batch_op.drop_column("address")
        batch_op.drop_column("area")