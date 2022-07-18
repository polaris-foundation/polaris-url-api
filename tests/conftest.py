from typing import Generator

import pytest
from flask import Flask


@pytest.fixture()
def app() -> Flask:
    """Fixture that creates app for testing"""
    import dhos_url_api.app

    return dhos_url_api.app.create_app(testing=True, use_pgsql=False, use_sqlite=True)


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield
