"""static codes

Revision ID: 7bfacc9a5761
Revises: d1ca5a608cc7
Create Date: 2021-01-04 11:31:51.308741

"""
import uuid
from datetime import datetime, timezone
from typing import List

import sqlalchemy as sa
from alembic import op
from flask_batteries_included.config import is_production_environment

# revision identifiers, used by Alembic.
revision = "7bfacc9a5761"
down_revision = "d1ca5a608cc7"
branch_labels = None
depends_on = None


def upgrade():
    if is_production_environment():
        # Don't do anything on prod.
        return
    values = [
        (
            str(uuid.uuid4()),
            f"https://dev.sensynehealth.com/gdm-bff/gdm/v1/activation/{i}",
            f"dev{i}{i}",
        )
        for i in range(1, 10)
    ]
    # Remove existing static activation codes.
    short_forms: List[str] = [v[2] for v in values]
    op.get_bind().execute(
        sa.text("DELETE FROM short_url WHERE short_form in :short_forms").bindparams(
            sa.bindparam("short_forms", value=short_forms, expanding=True)
        )
    )
    # Add new ones.
    time_now_iso: str = datetime.now(tz=timezone.utc).isoformat(timespec="milliseconds")
    short_url_table = sa.table(
        "short_url",
        sa.Column("uuid"),
        sa.Column("created"),
        sa.Column("modified"),
        sa.Column("original_url"),
        sa.Column("short_form"),
        sa.Column("created_by_"),
        sa.Column("modified_by_"),
    )
    op.bulk_insert(
        short_url_table,
        [
            {
                "uuid": v[0],
                "created": time_now_iso,
                "modified": time_now_iso,
                "original_url": v[1],
                "short_form": v[2],
                "created_by_": "sys",
                "modified_by_": "sys",
            }
            for v in values
        ],
    )


def downgrade():
    """Nothing to do."""
