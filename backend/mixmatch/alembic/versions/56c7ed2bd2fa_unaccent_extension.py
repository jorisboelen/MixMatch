"""unaccent_extension

Revision ID: 56c7ed2bd2fa
Revises: 077d28a4ac67
Create Date: 2024-07-16 11:58:54.438250

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '56c7ed2bd2fa'
down_revision: Union[str, None] = '077d28a4ac67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION unaccent')


def downgrade() -> None:
    pass
