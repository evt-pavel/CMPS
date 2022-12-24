"""users

Revision ID: ee4470a88dd7
Revises: 
Create Date: 2022-12-25 01:34:35.299100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee4470a88dd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100)),
        sa.Column('password_hash', sa.String(128)))


def downgrade() -> None:
    op.drop_table('users')
