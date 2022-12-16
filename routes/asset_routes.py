import controllers
from flask import request, Response, Blueprint

assets = Blueprint("assets", __name__)


@assets.route("/assets/get", methods=["GET"])
def assets_get_all() -> Response:
    return controllers.assets_get_all(request)
