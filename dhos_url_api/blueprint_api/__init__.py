from typing import Optional

from flask import Blueprint, Response, jsonify
from she_logging import logger
from validators import ValidationFailure
from validators.url import url as validate_url

from dhos_url_api.blueprint_api import controller

api_blueprint = Blueprint("api", __name__)


# URL shortener endpoint requires no protection.
@api_blueprint.route("/short_url", methods=["POST"])
def create_short_url(url_details: dict) -> Response:
    """
    ---
    post:
      summary: Create short URL
      description: Create a short URL for the URL provided in the request body.
      tags: [url]
      requestBody:
        description: URL to shorten
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ShortUrlRequest'
              x-body-name: url_details
      responses:
        '200':
          description: Shortened url
          content:
            application/json:
              schema: ShortUrlResponse
        default:
          description: Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    url_to_shorten: str = url_details["url"]
    maximum_uses: Optional[int] = url_details.get("maximum_uses", None)

    if type(validate_url(url_to_shorten)) == ValidationFailure:
        logger.info("Invalid URL provided: %s", url_to_shorten)
        raise ValueError("Invalid URL provided")

    return jsonify(controller.create_short_url(url_to_shorten, maximum_uses))


# URL shortener endpoint requires no protection.
@api_blueprint.route("/original_url/<short_form>", methods=["GET"])
def get_original_url(short_form: str) -> Response:
    """
    ---
    get:
      summary: Get original URL
      description: Get the original URL using the short form provided in the request.
      tags: [url]
      parameters:
        - name: short_form
          in: path
          required: true
          description: Short form of URL
          schema:
            type: string
            example: 7dfh6
      responses:
        '200':
          description: Original url
          content:
            application/json:
              schema: OriginalUrlResponse
        default:
          description: Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(controller.get_original_url(short_form))
