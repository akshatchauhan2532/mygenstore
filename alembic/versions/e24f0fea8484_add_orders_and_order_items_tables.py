"""add orders and order_items tables

Revision ID: e24f0fea8484
Revises: 3107d2a83dc5
Create Date: 2025-12-22 15:06:00.898764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e24f0fea8484'
down_revision: Union[str, Sequence[str], None] = '3107d2a83dc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
