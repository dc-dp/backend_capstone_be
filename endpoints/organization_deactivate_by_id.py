from flask import jsonify
import flask
from db import db
from models.organizations import Organization, organization_schema
from models.auth_tokens import AuthToken, auth_token_schema
# from models.app_users import AppUser
from lib.authenticate import authenticate_return_auth
from util.validate_uuid4 import validate_uuid4

@authenticate_return_auth
def organization_deactivate_by_id(req:flask.Request, org_id, auth_info) -> flask.Response:
    org_id = org_id.strip()
    if validate_uuid4(org_id) == False:
        return jsonify("Invalid org ID"), 404

    if org_id == auth_info.user.org_id:
        return jsonify("Access Denied: You cannot delete your own organization"), 401

    org_data = db.session.query(Organization).filter(Organization.org_id == org_id).first()
    if org_data:
        org_data.active = False
        db.session.commit()

        # Remove all auth records for anyone from that company
        # auth_record_query = db.session.query(AuthToken)\
        #     .join(AppUser, AuthToken.user_id == AppUser.user_id)\
        #     .filter(AppUser.org_id == org_id)
        
        # auth_records = auth_record_query.all()
        # for auth_record in auth_records:
        #     db.session.delete(auth_record)

        # db.session.commit()

        return jsonify(organization_schema.dump(org_data)), 200

        return jsonify(f'Organization with org_id {org_id} not found'), 404

        return jsonify("ERROR: request must be in JSON format"), 400