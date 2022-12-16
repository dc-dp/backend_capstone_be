import controllers
from flask import request, Response, Blueprint

mdmsite = Blueprint("mdmsite", __name__)


@mdmsite.route("/mdmsite/add", methods=["POST"])
def mdmsite_add() -> Response:
    return controllers.mdmsite_add(request)


@mdmsite.route("/mdmsites/get", methods=["GET"])
def mdmsite_get_all() -> Response:
    return controllers.mdmsite_get_all(request)


@mdmsite.route("/mdmsite/get/<mdmsite_id>", methods=["GET"])
def mdmsite_get_by_id(mdmsite_id) -> Response:
    return controllers.mdmsite_get_by_id(request, mdmsite_id)


@mdmsite.route("/mdmsite/sync/<mdmsite_id>", methods=["GET"])
def mdmsite_sync_by_id(mdmsite_id) -> Response:
    return controllers.mdmsite_sync_by_id(request, mdmsite_id)


@mdmsite.route("/mdmsite/update", methods=["POST"])
def mdmsite_update() -> Response:
    return controllers.mdm_site_update(request)


@mdmsite.route("/mdmsite/delete/<mdmsite_id>", methods=["DELETE"])
def mdmsite_delete(mdmsite_id) -> Response:
    return controllers.mdmsite_delete(request, mdmsite_id)


# @mdmsite.route("/mdmsite/activate/<mdmsite_id>", methods=["PUT"])
# def mdmsite_activate(mdmsite_id) -> Response:
#     return controllers.mdmsite_controller(request, mdmsite_id)


# @mdmsite.route("/mdmsite/deactivate/<mdmsite_id>", methods=["PUT"])
# def mdmsite_deactivate(mdmsite_id) -> Response:
#     return controllers.mdmsite_deactivate(request, mdmsite_id)
