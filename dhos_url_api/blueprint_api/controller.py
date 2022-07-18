from typing import Dict, Optional

from flask_batteries_included.helpers.error_handler import EntityNotFoundException
from flask_batteries_included.sqldb import db, generate_uuid
from she_logging import logger

from dhos_url_api.helpers.generation import generate_secure_random_string
from dhos_url_api.models.short_url import ShortUrl


def create_short_url(url_to_shorten: str, maximum_uses: Optional[int] = None) -> Dict:
    logger.debug("Looking for existing short URL")
    existing_short_url: ShortUrl = ShortUrl.query.filter_by(
        original_url=url_to_shorten
    ).first()

    # Return the existing shortened version if it exists
    if existing_short_url:
        logger.debug("Existing short URL found")
        return existing_short_url.to_dict()

    logger.debug("Existing short URL not found - creating a new one")

    short_form: str = _generate_short_form()

    # Make a new short URL
    new_short_url: ShortUrl = ShortUrl(
        uuid=generate_uuid(),
        original_url=url_to_shorten,
        short_form=short_form,
        remaining_uses=maximum_uses,
        created_by_="sys",
        modified_by_="sys",
    )

    db.session.add(new_short_url)
    db.session.commit()

    logger.debug("Saved a new short URL")

    return new_short_url.to_dict()


def get_original_url(short_form: str) -> Dict:
    short_url: ShortUrl = ShortUrl.query.filter_by(short_form=short_form).first()

    if not short_url:
        logger.info("Nonexistent short form attempted: %s", short_form)
        raise EntityNotFoundException("URL not found")

    if short_url.remaining_uses == 0:
        logger.info("No uses remaining short form attempted: %s", short_form)
        raise EntityNotFoundException("URL not found")

    # Decrement remaining_uses
    if short_url.remaining_uses is not None:
        short_url.remaining_uses = short_url.remaining_uses - 1
        db.session.add(short_url)
        db.session.commit()

    return {"original_url": short_url.original_url}


def _generate_short_form() -> str:
    short_form: str = generate_secure_random_string(5)
    # JUST in case we generate a collision, loop til we find a new one
    find_a_short_form: bool = True
    while find_a_short_form:
        short_form = generate_secure_random_string(5)
        existing_short_form: ShortUrl = ShortUrl.query.filter_by(
            short_form=short_form
        ).first()
        if not existing_short_form:
            logger.debug("Found a new short form")
            find_a_short_form = False
        else:
            logger.debug("Found a short URL collision, trying again")
    return short_form
