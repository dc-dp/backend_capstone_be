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
def enrolled_devices_sync(req: flask.Request, auth_info) -> flask.Response:
    all_asset_sites = asset_site_get_all(req, auth_info=auth_info)
    asset_site = all_asset_sites.get_json("response")
    for site in asset_site:
        site_id = site["site_id"]
        asset_site_sync_by_id(req, site_id, auth_info=auth_info)

    # sleep(3)
    all_mdm_sites = mdmsite_get_all(req, auth_info=auth_info)
    mdm_site = all_mdm_sites.get_json("response")
    for site in mdm_site:
        site_id = site["mdm_site_id"]
        mdmsite_sync_by_id(req, site_id, auth_info=auth_info)

    # sleep(3)

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


# @authenticate_return_auth
# def organization_activate_by_id(
#     req: flask.Request, org_id, auth_info
# ) -> flask.Response:
#     org_id = org_id.strip()
#     if validate_uuid4(org_id) == False:
#         return jsonify("Invalid org ID"), 404

#     org_data = (
#         db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
#     )
#     if org_data:
#         org_data.active = True
#         db.session.commit()
#         return jsonify(organization_schema.dump(org_data)), 200

#         return jsonify(f"Organizations with org_id {org_id} not found"), 404

#     return jsonify("ERROR: request must be in JSON format"), 400


# @authenticate
# def organization_add(req: flask.Request) -> flask.Response:
#     post_data = req.get_json()
#     name = post_data.get("name")
#     address = post_data.get("address")
#     city = post_data.get("city")
#     state = post_data.get("state")
#     zip_code = post_data.get("zip_code")
#     phone = post_data.get("phone")
#     active = post_data.get("active")
#     created_date = datetime.now()
#     if active == None:
#         active = True

#     stripped_phone = strip_phone(phone)
#     org_data = Organizations(
#         name, address, city, state, zip_code, stripped_phone, created_date, active
#     )

#     db.session.add(org_data)
#     db.session.commit()

#     return jsonify(organization_schema.dump(org_data)), 201


# @authenticate_return_auth
# def organization_deactivate_by_id(
#     req: flask.Request, org_id, auth_info
# ) -> flask.Response:
#     org_id = org_id.strip()
#     if validate_uuid4(org_id) == False:
#         return jsonify("Invalid org ID"), 404

#     if org_id == auth_info.user.org_id:
#         return jsonify("Access Denied: You cannot delete your own Organizations"), 401

#     org_data = (
#         db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
#     )
#     if org_data:
#         org_data.active = False
#         db.session.commit()

#         # Remove all auth records for anyone from that company
#         # auth_record_query = db.session.query(AuthToken)\
#         #     .join(AppUser, AuthToken.user_id == AppUser.user_id)\
#         #     .filter(AppUser.org_id == org_id)

#         # auth_records = auth_record_query.all()
#         # for auth_record in auth_records:
#         #     db.session.delete(auth_record)

#         # db.session.commit()

#         return jsonify(organization_schema.dump(org_data)), 200

#         return jsonify(f"Organizations with org_id {org_id} not found"), 404

#         return jsonify("ERROR: request must be in JSON format"), 400


# @authenticate_return_auth
# def organization_delete_by_id(req: flask.Request, org_id, auth_info) -> flask.Response:
#     org_id = org_id.strip()
#     if validate_uuid4(org_id) == False:
#         return jsonify("Invalid org ID"), 404

#     if org_id == auth_info.user.org_id:
#         return jsonify("Access Denied: You cannot delete your own Organizations"), 401

#     org_data = (
#         db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
#     )

#     if org_data:
#         db.session.delete(org_data)
#         db.session.commit()
#         return jsonify(f"Organizations with org_id {org_id} deleted"), 201

#     return jsonify(f"Organizations with org_id {org_id} not found"), 404

#     return jsonify("ERROR: request must be in JSON format"), 400


# @authenticate_return_auth
# def organization_get_by_id(req: flask.Request, org_id, auth_info) -> flask.Response:
#     org_id = org_id.strip()
#     if validate_uuid4(org_id) == False:
#         return jsonify("Invalid org ID"), 404
#     org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id)

#     if auth_info.user.role != "super-admin":
#         org_query = org_query.filter(Organizations.org_id == auth_info.user.org_id)

#     org_data = org_query.first()

#     if org_data:
#         return jsonify(organization_schema.dump(org_data))

#     return jsonify(f"Organizations with org_id {org_id} not found"), 404


# @authenticate_return_auth
# def organization_get_by_search(
#     req: flask.Request, search_term, internal_call, p_auth_info, auth_info
# ) -> flask.Response:
#     auth_info = {}
#     if internal_call == False:
#         auth_info = validate_auth_token(req.headers.get("auth_token"))
#     elif p_auth_info:
#         auth_info = p_auth_info

#     if not auth_info:
#         return jsonify("Access Denied"), 401

#     search_term = search_term.lower()

#     org_query = db.session.query(Organizations).filter(
#         db.or_(
#             db.func.lower(Organizations.name).contains(search_term),
#             Organizations.phone.contains(search_term),
#             db.func.lower(Organizations.city).contains(search_term),
#             db.func.lower(Organizations.state).contains(search_term),
#         )
#     )

#     if auth_info.user.role == "admin" or auth_info.user.role == "user":
#         org_query.filter(Organizations.org_id == auth_info.user.org_id)
#     org_data = org_query.order_by(Organizations.name.asc()).all()
#     if internal_call:
#         return organizations_schema.dump(org_data)

#     return jsonify(organizations_schema.dump(org_data))


# @authenticate
# def organization_update(req: flask.Request) -> flask.Response:
#     post_data = req.get_json()
#     org_id = post_data.get("org_id")
#     if org_id == None:
#         return jsonify("ERROR: org_id missing"), 400
#     name = post_data.get("name")
#     address = post_data.get("address")
#     city = post_data.get("city")
#     state = post_data.get("state")
#     zip_code = post_data.get("zip_code")
#     phone = post_data.get("phone")
#     active = post_data.get("active")
#     if active == None:
#         active = True

#     org_data = (
#         db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
#     )
#     org_data.name = name
#     org_data.address = address
#     org_data.city = city
#     org_data.state = state
#     org_data.zip_code = zip_code
#     org_data.phone = strip_phone(phone)
#     org_data.active = active

#     db.session.commit()

#     return jsonify(organization_schema.dump(org_data)), 200
