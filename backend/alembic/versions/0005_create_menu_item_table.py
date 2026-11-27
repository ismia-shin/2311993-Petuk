"""create menu item table

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-27 12:20:57.841136

"""

from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "menu_item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurant.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_menu_item_restaurant_id", "menu_item", ["restaurant_id"])

def downgrade() -> None:
    op.drop_index("ix_menu_item_restaurant_id", table_name="menu_item")
    op.drop_table("menu_item")