import controllers
from flask import request, Response, Blueprint

device = Blueprint("device", __name__)


@device.route("/devices/get", methods=["GET"])
def enrolled_devices_get() -> Response:
    return controllers.enrolled_devices_get(request)


# @device.route("/device/get/<device_id>", methods=["GET"])
# def device_get_by_id(device_id) -> Response:
#     return controllers.enrolled_device_get_by_id(request, device_id)


@device.route("/devices/sync_all", methods=["GET"])
def device_sync_all() -> Response:
    return controllers.enrolled_devices_sync(request)
