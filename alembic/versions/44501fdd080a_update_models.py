"""update models

Revision ID: 44501fdd080a
Revises: 3dfeb24d718f
Create Date: 2024-05-29 13:06:18.620601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44501fdd080a'
down_revision: Union[str, None] = '3dfeb24d718f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
