from flask import jsonify
import flask
from db import db, populate_object
from models.snipe_it_site import SnipeItSite, snipeit_site_schema, snipeit_sites_schema
import json
from lib.authenticate import authenticate, authenticate_return_auth
import requests
from models.assets import Assets, assets_schema


@authenticate_return_auth
def asset_site_add(req: flask.Request, auth_info) -> flask.Response:
    post_data = req.get_json()
    api_token = post_data.get("api_token")
    url = post_data.get("url")
    name = post_data.get("name")
    org_id = auth_info.user.org_id

    asset_site = SnipeItSite(api_token, url, name, org_id)

    db.session.add(asset_site)
    db.session.commit()

    return jsonify(snipeit_site_schema.dump(asset_site)), 201


@authenticate_return_auth
def asset_site_get_all(req: flask.Request, auth_info) -> flask.Response:
    all_sites = []
    all_sites = (
        db.session.query(SnipeItSite)
        .filter(auth_info.user.org_id == SnipeItSite.org_id)
        .all()
    )

    return jsonify(snipeit_sites_schema.dump(all_sites))


@authenticate_return_auth
def assets_get_all(req: flask.Request, auth_info) -> flask.Response:
    all_assets = []
    all_assets = (
        db.session.query(Assets)
        .join(SnipeItSite)
        .filter(
            (SnipeItSite.site_id == Assets.site_id)
            and (auth_info.user.org_id == SnipeItSite.org_id)
        )
        .order_by(Assets.asset_tag.asc())
    ).all()

    return jsonify(assets_schema.dump(all_assets))


@authenticate_return_auth
def asset_site_get_by_id(req: flask.Request, site_id, auth_info) -> flask.Response:

    site = (
        db.session.query(SnipeItSite)
        .filter(
            (auth_info.user.org_id == SnipeItSite.org_id),
            (SnipeItSite.site_id == site_id),
        )
        .first()
    )

    return jsonify(snipeit_site_schema.dump(site))


@authenticate
def asset_site_delete(req: flask.Request, site_id) -> flask.Response:

    site = (
        db.session.query(SnipeItSite)
        .filter(
            (SnipeItSite.site_id == site_id),
        )
        .first()
    )

    db.session.delete(site)

    return jsonify("Site Removed")


@authenticate_return_auth
def asset_site_sync_by_id(req: flask.Request, site_id, auth_info) -> flask.Response:

    site = (
        db.session.query(SnipeItSite)
        .filter(
            (auth_info.user.org_id == SnipeItSite.org_id),
            (SnipeItSite.site_id == site_id),
        )
        .first()
    )

    site = snipeit_site_schema.dump(site)

    request_url = f"{site['url']}/api/v1/hardware"
    api_token = site["api_token"]

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    assets = requests.get(request_url, headers=headers)
    assets_json = assets.json()["rows"]

    with open("assets.json", "w") as outfile:
        json.dump(assets_json, outfile)
    count = 0
    for asset in assets_json:
        if not asset["manufacturer"]:
            continue

        if asset["manufacturer"]["name"].title() != "Apple":
            continue

        if not asset["assigned_to"]:
            asset["assigned_to"] = {"first_name": "", "last_name": ""}
        new_asset = {
            "asset_tag": asset["asset_tag"],
            "serial_number": asset["serial"].upper(),
            "make": asset["manufacturer"]["name"],
            "model_num": asset["model_number"],
            "model_name": asset["model"]["name"],
            "deployed": asset["status_label"]["status_meta"] == "deployed",
            "assigned_to": (
                f"{asset['assigned_to']['last_name']}, {asset['assigned_to']['first_name']}"
            ),
            "site_id": site_id,
        }
        if not asset["assigned_to"]["first_name"]:
            new_asset["assigned_to"] = ""
        existing = (
            db.session.query(Assets)
            .filter(Assets.serial_number == new_asset["serial_number"])
            .first()
        )

        if existing:
            populate_object(existing, new_asset)

        else:
            db.session.add(
                Assets(
                    new_asset["serial_number"],
                    new_asset["site_id"],
                    new_asset["make"],
                    new_asset["model_num"],
                    new_asset["model_name"],
                    new_asset["deployed"],
                    new_asset["assigned_to"],
                    new_asset["asset_tag"],
                )
            )
        db.session.commit()
        count += 1

    return jsonify(f"Sucessfully synced {count} devices")


@authenticate
def asset_site_update(req: flask.Request) -> flask.Response:
    post_data = req.get_json()
    print(post_data)
    site_id = post_data.get("site_id")
    org_id = post_data.get("org_id")
    if org_id == None:
        return jsonify("ERROR: org_id missing"), 400
    name = post_data.get("name")
    url = post_data.get("url")
    api_token = post_data.get("api_token")

    # if active == None:
    #     active = True

    site_data = (
        db.session.query(SnipeItSite).filter(SnipeItSite.site_id == site_id).first()
    )
    site_data.name = name
    site_data.url = url
    site_data.api_token = api_token

    # site_data.active = active

    db.session.commit()

    return jsonify(snipeit_site_schema.dump(site_data)), 200


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
