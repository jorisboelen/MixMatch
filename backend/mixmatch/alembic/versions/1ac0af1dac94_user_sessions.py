"""user sessions

Revision ID: 1ac0af1dac94
Revises: 56c7ed2bd2fa
Create Date: 2024-12-14 09:25:50.630133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '1ac0af1dac94'
down_revision: Union[str, None] = '56c7ed2bd2fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_sessions',
    sa.Column('token', sqlmodel.sql.sqltypes.AutoString(length=64), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_index(op.f('ix_user_sessions_expires'), 'user_sessions', ['expires'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_sessions_expires'), table_name='user_sessions')
    op.drop_table('user_sessions')
    # ### end Alembic commands ###
