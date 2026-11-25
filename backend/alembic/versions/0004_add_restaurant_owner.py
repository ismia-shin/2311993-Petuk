"""add restaurant owner

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-25 16:53:25.923320

"""

from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    with op.batch_alter_table("restaurant") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_restaurant_owner_id_app_user",
            "app_user",
            ["owner_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_index("ix_restaurant_owner_id", ["owner_id"])

def downgrade() -> None:
    with op.batch_alter_table("restaurant") as batch_op:
        batch_op.drop_index("ix_restaurant_owner_id")
        batch_op.drop_constraint("fk_restaurant_owner_id_app_user", type_="foreignkey")
        batch_op.drop_column("owner_id")