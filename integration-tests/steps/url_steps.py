from typing import Dict

from behave import given, step, use_step_matcher
from behave.runner import Context
from clients.dhos_url_client import get_original_url, post_short_url
from faker import Faker

use_step_matcher("re")


@given("I have a URL")
def get_random_url(context: Context) -> None:
    context.url = Faker().url()


@step("I send the URL to the shortener")
def create_short_url(context: Context) -> None:
    context.response = post_short_url(
        url=context.url,
        maximum_uses=1,
    )


@step("I send the URL with (?P<maximum_uses>\d+) maximum uses? to the shortener")
def create_short_url_with_max_uses(context: Context, maximum_uses: str) -> None:
    context.response = post_short_url(
        url=context.url,
        maximum_uses=int(maximum_uses),
    )


@step("a short code for a static activation")
def use_static_short_form(context: Context) -> None:
    context.url = "https://dev.sensynehealth.com/gdm-bff/gdm/v1/activation/1"
    context.short_form = "dev11"


@step("I retrieve the long URL (?P<use_count>\d+) times?")
def retrieve_long_url_repeatedly(context: Context, use_count: str) -> None:
    for count in range(0, int(use_count)):
        context.response = get_original_url(
            short_form=context.short_form,
        )


@step("I get a short code from the shortener")
def assert_create_url_response(context: Context) -> None:
    assert context.response.status_code == 200

    response_json: Dict = context.response.json()
    assert "short_form" in response_json
    context.short_form = response_json["short_form"]


@step("I get (?P<result>.+)")
def assert_get_url_result(context: Context, result: str) -> None:
    if result == "the original url":
        assert context.response.status_code == 200
        response_json = context.response.json()
        assert "original_url" in response_json
        assert context.url == response_json["original_url"]
    elif result == "an error":
        assert context.response.status_code == 404
        response_json = context.response.json()
        assert "message" in response_json
        assert "URL not found" == response_json["message"]
    else:
        raise ValueError(f"Unable to handle {result}")
