import controllers
from flask import request, Response, Blueprint

mdmsite = Blueprint("mdmsite", __name__)


@mdmsite.route("/mdmsite/add", methods=["POST"])
def mdmsite_add() -> Response:
    return controllers.mdmsite_add(request)


@mdmsite.route("/user/update", methods=["POST"])
def mdmsite_update() -> Response:
    return controllers.mdmsite_update(request)


@mdmsite.route("/user/get", methods=["GET"])
def mdmsite_get_all() -> Response:
    return controllers.mdmsite_get_all(request)


@mdmsite.route("/user/get/<mdmsite_id>", methods=["GET"])
def mdmsite_get_by_id(mdmsite_id) -> Response:
    return controllers.mdmsite_get_by_id(request, mdmsite_id)


@mdmsite.route("/user/get/me", methods=["GET"])
def mdmsite_get_from_auth_token() -> Response:
    return controllers.mdmsite_get_from_auth_token(request)


@mdmsite.route("/user/get/organization/<org_id>", methods=["GET"])
def mdmsite_get_by_org_id(org_id) -> Response:
    return controllers.mdmsite_get_by_org_id(request, org_id)


@mdmsite.route("/user/delete/<mdmsite_id>", methods=["DELETE"])
def mdmsite_delete(mdmsite_id) -> Response:
    return controllers.mdmsite_delete(request, mdmsite_id)


@mdmsite.route("/user/activate/<mdmsite_id>", methods=["PUT"])
def mdmsite_activate(mdmsite_id) -> Response:
    return controllers.mdmsite_controller(request, mdmsite_id)


@mdmsite.route("/user/deactivate/<mdmsite_id>", methods=["PUT"])
def mdmsite_deactivate(mdmsite_id) -> Response:
    return controllers.mdmsite_deactivate(request, mdmsite_id)


@mdmsite.route("/user/search/<search_term>")
def mdmsite_get_by_search(
    search_term, internal_call=False, p_auth_info=None
) -> Response:
    return controllers.mdmsite_get_by_search(
        request, search_term, internal_call, p_auth_info
    )
