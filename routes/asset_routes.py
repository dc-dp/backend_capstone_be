import controllers
from flask import request, Response, Blueprint

asset = Blueprint("asset", __name__)


@asset.route("/asset/add", methods=["POST"])
def asset_site_add() -> Response:
    return controllers.asset_add(request)


@asset.route("/user/update", methods=["POST"])
def asset_update() -> Response:
    return controllers.asset_update(request)


@asset.route("/asset/get", methods=["GET"])
def asset_get_all() -> Response:
    return controllers.asset_get_all(request)


@asset.route("/asset/get/<asset_id>", methods=["GET"])
def asset_get_by_id(asset_id) -> Response:
    return controllers.asset_get_by_id(request, asset_id)


@asset.route("/asset/sync/<asset_id>", methods=["GET"])
def asset_sync_by_id(asset_id) -> Response:
    return controllers.asset_sync_by_id(request, asset_id)


@asset.route("/user/get/me", methods=["GET"])
def asset_get_from_auth_token() -> Response:
    return controllers.asset_get_from_auth_token(request)


@asset.route("/user/get/organization/<org_id>", methods=["GET"])
def asset_get_by_org_id(org_id) -> Response:
    return controllers.asset_get_by_org_id(request, org_id)


@asset.route("/user/delete/<asset_id>", methods=["DELETE"])
def asset_delete(asset_id) -> Response:
    return controllers.asset_delete(request, asset_id)


@asset.route("/user/activate/<asset_id>", methods=["PUT"])
def asset_activate(asset_id) -> Response:
    return controllers.asset_controller(request, asset_id)


@asset.route("/user/deactivate/<asset_id>", methods=["PUT"])
def asset_deactivate(asset_id) -> Response:
    return controllers.asset_deactivate(request, asset_id)


@asset.route("/user/search/<search_term>")
def asset_get_by_search(search_term, internal_call=False, p_auth_info=None) -> Response:
    return controllers.asset_get_by_search(
        request, search_term, internal_call, p_auth_info
    )
