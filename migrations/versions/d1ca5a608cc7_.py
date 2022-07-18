"""empty message

Revision ID: d1ca5a608cc7
Revises: 9e2d8b7d5b29
Create Date: 2018-07-23 16:38:45.252310

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer


# revision identifiers, used by Alembic.
revision = 'd1ca5a608cc7'
down_revision = '9e2d8b7d5b29'
branch_labels = None
depends_on = None


environments = {
    "dev": "https://dev.sensynehealth.com/dhos-activation-auth/dhos/v1/activation/",
    "sta": "https://staging.sensynehealth.com/dhos-activation-auth/dhos/v1/activation/",
    "dem": "https://demo.sensynehealth.com/dhos-activation-auth/dhos/v1/activation/"
}

user_ids = list(map(str, range(1, 10)))

short_url_table = table('short_url',
                        column('original_url', String)
                        )


def upgrade():
    for _, url_prefix in environments.items():
        op.execute(
            short_url_table.delete().
            where(short_url_table.c.original_url.like(url_prefix + '%'))
            )



def downgrade():
    pass
