import controllers
from flask import request, Response, Blueprint

assetsite = Blueprint("assetsite", __name__)


@assetsite.route("/asset_site/add", methods=["POST"])
def asset_site_add() -> Response:
    return controllers.asset_site_add(request)


@assetsite.route("/asset_site/update", methods=["POST"])
def asset_site_update() -> Response:
    return controllers.asset_site_update(request)


@assetsite.route("/asset_sites/get", methods=["GET"])
def asset_site_get_all() -> Response:
    return controllers.asset_site_get_all(request)


@assetsite.route("/asset_site/get/<asset_id>", methods=["GET"])
def asset_site_get_by_id(asset_id) -> Response:
    return controllers.asset_site_get_by_id(request, asset_id)


@assetsite.route("/asset_site/sync/<asset_id>", methods=["GET"])
def asset_site_sync_by_id(asset_id) -> Response:
    return controllers.asset_site_sync_by_id(request, asset_id)


@assetsite.route("/asset_site/del/<asset_id>", methods=["DELETE"])
def asset_site_delete(asset_id) -> Response:
    return controllers.asset_site_delete(request, asset_id)


# @assetsite.route("/asset_site/activate/<asset_id>", methods=["PUT"])
# def asset_activate(asset_id) -> Response:
#     return controllers.asset_controller(request, asset_id)


# @assetsite.route("/asset_site/deactivate/<asset_id>", methods=["PUT"])
# def asset_deactivate(asset_id) -> Response:
#     return controllers.asset_site_deactivate(request, asset_id)
