from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import EXCLUDE, Schema, fields

dhos_url_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="DHOS URL API",
    info={
        "description": "The DHOS URL API is responsible for shortening URLs and allowing their retrieval."
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)

initialise_apispec(dhos_url_api_spec)


@openapi_schema(dhos_url_api_spec)
class ShortUrlRequest(Schema):
    class Meta:
        description = "Short URL request"
        unknown = EXCLUDE
        ordered = True

    url = fields.String(
        required=True, description="URL to shorten", example="http://google.com"
    )
    maximum_uses = fields.Integer(
        required=False,
        allow_none=True,
        description="Maximum number of times the original URL can be retrieved",
        example=2,
    )


@openapi_schema(dhos_url_api_spec)
class ShortUrlResponse(Schema):
    class Meta:
        description = "Short URL response"
        unknown = EXCLUDE
        ordered = True

    short_form = fields.String(
        required=True, description="Short form of original URL", example="ja7s9"
    )


@openapi_schema(dhos_url_api_spec)
class OriginalUrlResponse(Schema):
    class Meta:
        description = "Original URL response"
        unknown = EXCLUDE
        ordered = True

    original_url = fields.String(
        required=True,
        description="Original URL that was shortened",
        example="http://google.com",
    )
