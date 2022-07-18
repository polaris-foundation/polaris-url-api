from typing import Any

from flask_batteries_included.sqldb import db, generate_uuid

from dhos_url_api.models.short_url import ShortUrl


def reset_database() -> None:
    session = db.session
    __drop_data(session)
    __add_data(session)
    session.close()


def drop_data() -> None:
    __drop_data()


def __add_data(session: Any) -> None:
    environments = {
        "dev": "https://dev.sensynehealth.com/dhos-activation-auth/dhos/v1/activation/",
        "sta": "https://staging.sensynehealth.com/dhos-activation-auth/dhos/v1/activation/",
        "dem": "https://demo.sensynehealth.com/dhos-activation-auth/dhos/v1/activation/",
    }

    # For each environment, add patient IDs 1-9
    for env_name, env_url in environments.items():
        for i in range(1, 10):
            session.add(
                ShortUrl(
                    uuid=generate_uuid(),
                    original_url=env_url + str(i),
                    short_form=env_name + str(i) + str(i),
                    remaining_uses=None,
                    created_by_="sys",
                    modified_by_="sys",
                )
            )

    session.commit()


def __drop_data(session: Any = None) -> None:

    if not session:
        local_session = True
        session = db.session
    else:
        local_session = False

    session.execute("TRUNCATE TABLE short_url cascade")
    session.commit()

    if local_session:
        session.close()
