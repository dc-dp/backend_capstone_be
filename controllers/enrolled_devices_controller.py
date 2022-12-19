from datetime import datetime
from flask import jsonify
import json
import flask
from time import sleep
from db import db
from models.enrolled_devices import (
    EnrolledDevices,
    enrolled_device_schema,
    enrolled_devices_schema,
)
from models.organizations import (
    Organizations,
    organization_schema,
    organizations_schema,
)
from lib.authenticate import authenticate, authenticate_return_auth, validate_auth_token
from util.foundation_utils import strip_phone
from util.validate_uuid4 import validate_uuid4
from controllers.mdm_site_controller import mdmsite_get_all, mdmsite_sync_by_id
from controllers.asset_controller import asset_site_get_all, asset_site_sync_by_id
import requests


@authenticate_return_auth
def enrolled_devices_sync(
    req: flask.Request, auth_info, return_counts=False
) -> flask.Response:
    all_asset_sites = asset_site_get_all(req, auth_info=auth_info)
    asset_site = all_asset_sites.get_json("response")
    for site in asset_site:
        site_id = site["site_id"]
        asset_serials = asset_site_sync_by_id(req, site_id, auth_info=auth_info)

    all_mdm_sites = mdmsite_get_all(req, auth_info=auth_info)
    mdm_site = all_mdm_sites.get_json("response")
    for site in mdm_site:
        site_id = site["mdm_site_id"]
        mdm_serials = mdmsite_sync_by_id(req, site_id, auth_info=auth_info)

    if return_counts:
        total_owned = len(asset_serials) - len(mdm_serials)
        enrolled_count = 0
        pester_list = []
        for serial, person in asset_serials.items():
            if serial in mdm_serials:
                enrolled_count += 1
            else:
                if person != ", ":
                    pester_list.append({"serial": serial, "person": person})
                    print(person)
        return jsonify([total_owned, enrolled_count], pester_list)
    return jsonify("Sites Synced Successully")


@authenticate_return_auth
def enrolled_devices_get(req: flask.Request, auth_info) -> flask.Response:
    all_devices = []

    all_devices = (
        db.session.query(EnrolledDevices)
        .order_by(EnrolledDevices.last_seen.desc())
        .all()
    )

    return jsonify(enrolled_devices_schema.dump(all_devices))


@authenticate_return_auth
def sync_apple_dep(req: flask.Request, auth_info) -> flask.Response:
    all_mdm_sites = []
    all_mdm_sites = mdmsite_get_all(req, auth_info=auth_info)
    mdm_sites = all_mdm_sites.get_json("response")

    sync_result = []
    for site in mdm_sites:
        post_url = f"{site['url']}/v1/dep/syncnow"
        auth_info = ("micromdm", site["api_token"])
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        sync_result.append(
            f"Site ID: {site['mdm_site_id']}, Status Code: {requests.post(post_url, headers=header, auth=auth_info).status_code}"
        )

    print(sync_result)

    return jsonify(sync_result)
