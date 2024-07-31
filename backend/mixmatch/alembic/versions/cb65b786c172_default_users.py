"""default_users

Revision ID: cb65b786c172
Revises: b7db86f55625
Create Date: 2024-07-14 20:57:05.509375

"""
from argon2 import PasswordHasher
from mixmatch.db.models import User
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'cb65b786c172'
down_revision: Union[str, None] = 'b7db86f55625'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(User.__table__, [
        {
            'username': 'mixmatch',
            'password': PasswordHasher().hash('mixmatch'),
            'is_admin': 1
        }
    ])


def downgrade() -> None:
    pass
