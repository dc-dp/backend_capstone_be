import controllers
from flask import request, Response, Blueprint

snipeit = Blueprint("snipeit", __name__)


@snipeit.route("/snipeit/add", methods=["POST"])
def snipeit_site_add() -> Response:
    return controllers.snipeit_add(request)


@snipeit.route("/user/update", methods=["POST"])
def snipeit_update() -> Response:
    return controllers.snipeit_update(request)


@snipeit.route("/user/get", methods=["GET"])
def snipeit_get_all() -> Response:
    return controllers.snipeit_get_all(request)


@snipeit.route("/user/get/<snipeit_id>", methods=["GET"])
def snipeit_get_by_id(snipeit_id) -> Response:
    return controllers.snipeit_get_by_id(request, snipeit_id)


@snipeit.route("/user/get/me", methods=["GET"])
def snipeit_get_from_auth_token() -> Response:
    return controllers.snipeit_get_from_auth_token(request)


@snipeit.route("/user/get/organization/<org_id>", methods=["GET"])
def snipeit_get_by_org_id(org_id) -> Response:
    return controllers.snipeit_get_by_org_id(request, org_id)


@snipeit.route("/user/delete/<snipeit_id>", methods=["DELETE"])
def snipeit_delete(snipeit_id) -> Response:
    return controllers.snipeit_delete(request, snipeit_id)


@snipeit.route("/user/activate/<snipeit_id>", methods=["PUT"])
def snipeit_activate(snipeit_id) -> Response:
    return controllers.snipeit_controller(request, snipeit_id)


@snipeit.route("/user/deactivate/<snipeit_id>", methods=["PUT"])
def snipeit_deactivate(snipeit_id) -> Response:
    return controllers.snipeit_deactivate(request, snipeit_id)


@snipeit.route("/user/search/<search_term>")
def snipeit_get_by_search(
    search_term, internal_call=False, p_auth_info=None
) -> Response:
    return controllers.snipeit_get_by_search(
        request, search_term, internal_call, p_auth_info
    )
