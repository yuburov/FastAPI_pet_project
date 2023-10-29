"""User Token Todo tables creation

Revision ID: 86ce84775e92
Revises: 
Create Date: 2023-10-27 01:02:32.043424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86ce84775e92'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('username', sa.String(length=20), nullable=False),
                    sa.Column('email', sa.String(length=50), nullable=False),
                    sa.Column('password', sa.String(length=200), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('tokens',
                    sa.Column('user_id', sa.String(length=200), nullable=False),
                    sa.Column('access_token', sa.String(length=450), nullable=False),
                    sa.Column('refresh_token', sa.String(length=450), nullable=False),
                    sa.Column('status', sa.Boolean(), nullable=False),
                    sa.Column('created_date', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('access_token')
                    )
    op.create_table('todos',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('status', sa.Boolean(), nullable=False),
                    sa.Column('priority', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_todos_title'), 'todos', ['title'], unique=False)


def downgrade() -> None:
    pass
