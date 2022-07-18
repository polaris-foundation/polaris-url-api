import time

from flask import Blueprint, Response, current_app, jsonify

from .controller import drop_data, reset_database

development_blueprint = Blueprint("development", __name__)


@development_blueprint.route("/reset_test_data")
def reset_data_route() -> Response:
    start = time.time()
    reset_database()
    total_time = time.time() - start
    return jsonify({"complete": True, "time_taken": str(total_time) + "s"})


@development_blueprint.route("/drop_data", methods=["POST"])
def drop_data_route() -> Response:

    if current_app.config["ALLOW_DROP_DATA"] is not True:
        raise PermissionError("Cannot drop data in this environment")

    start = time.time()
    drop_data()
    total_time = time.time() - start
    return jsonify({"complete": True, "time_taken": str(total_time) + "s"})
