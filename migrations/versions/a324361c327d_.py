"""empty message

Revision ID: a324361c327d
Revises: 
Create Date: 2018-03-26 23:01:40.617516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a324361c327d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('short_url',
                    sa.Column('uuid', sa.String(length=36), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('modified', sa.DateTime(), nullable=False),
                    sa.Column('original_url', sa.String(), nullable=False),
                    sa.Column('short_form', sa.String(), nullable=False),
                    sa.Column('remaining_uses', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('short_form')
                    )


def downgrade():

    op.drop_table('short_url')
