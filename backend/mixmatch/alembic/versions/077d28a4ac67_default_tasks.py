"""default_tasks

Revision ID: 077d28a4ac67
Revises: cb65b786c172
Create Date: 2024-07-14 21:00:37.988951

"""
from argon2 import PasswordHasher
from mixmatch.db.models import Task
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '077d28a4ac67'
down_revision: Union[str, None] = 'cb65b786c172'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(Task.__table__, [
        {
            'id': 'mixmatch.tasks.tasks.task_import',
            'name': 'Perform import of music files',
            'schedule': 'Every Hour'
        },
        {
            'id': 'mixmatch.tasks.tasks.task_cleanup',
            'name': 'Cleanup unused cover files',
            'schedule': 'Every Month'
        }
    ])


def downgrade() -> None:
    pass
