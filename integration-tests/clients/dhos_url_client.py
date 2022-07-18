import requests
from environs import Env
from requests import Response


def _get_base_url() -> str:
    return Env().str("DHOS_URL_BASE_URL", "http://dhos-url-api:5000")


def post_short_url(maximum_uses: int, url: str) -> Response:
    return requests.post(
        url=f"{_get_base_url()}/dhos/v1/short_url",
        timeout=15,
        json={"maximum_uses": maximum_uses, "url": url},
    )


def get_original_url(short_form: str) -> Response:
    return requests.get(
        url=f"{_get_base_url()}/dhos/v1/original_url/{short_form}",
        timeout=15,
    )
