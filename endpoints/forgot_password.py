import flask
from db import db
from models.app_users import user_schema, AppUsers, AppUsersSchema
from models.pw_reset_token import PWResetTokens
from util.validate_uuid4 import validate_uuid4
from flask import jsonify
from util.send_email import send_email
from datetime import datetime, timedelta
import base64
import uuid

def forgot_password_change(req:flask.Request, bcrypt) -> flask.Response:

    req = req.get_json()
    token = req["token"]
    pw_reset_token = db.session.query(PWResetTokens).filter(PWResetTokens.user_id == req["user_id"]).filter(PWResetTokens.token == token).filter(PWResetTokens.expiration > datetime.utcnow()).first()
    
    if not pw_reset_token:
        return jsonify("Expired password reset link."), 401

    user_db = db.session.query(AppUsers).filter(AppUsers.user_id == req["user_id"]).first()
    if not req["new_password"] or len(req["new_password"]) < 1:
        return jsonify("Cannot set to blank password."), 400

    user_db.password = bcrypt.generate_password_hash(req["new_password"]).decode("utf8")
    db.session.commit()
    try:
        send_email(user_db.email, "Geotagger Password Change", "We've successfully updated your password for GeoTagger. If this wasn't you, please contact us.")
    except Exception as e:
        print(e)
    return flask.make_response(flask.jsonify({"message": "password changed"}), 200)


def pw_change_request(req:flask.Request) -> flask.Response:
    post_data = req.get_json()
    email = post_data.get('email')
    print(email)
    try:

        user = db.session.query(AppUsers).filter(AppUsers.email == email).filter(AppUsers.active == True).first()
        if user: 
            reset_pw_link, token, expiration = get_reset_link(req, user.user_id)
            token_record = PWResetTokens(user.user_id, expiration, token)
            print(token_record)
            db.session.add(token_record)
            db.session.commit()
            send_email(email, "Password Update Request", '''<div style="background-color:white;color:#3e5c76;"><h1>Hello '''+user.first_name.capitalize()+ ''',</h1><p>You requested a password reset for your GeoTagger.io account.
            </p><p>Click the link below or copy it into your browser to reset your password</p></div>'''"<p>"+reset_pw_link+"</p>")
        else:
            return jsonify("user not found"), 404
        return jsonify("email sent"), 201

    except Exception as inst:
        return jsonify(inst.args[0],inst), 400

def get_reset_link(req:flask.Request, user_id) -> flask.Response:
    expiration_datetime = datetime.utcnow() + timedelta(minutes=30)
    expiration_string = expiration_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    token = str(uuid.uuid4())
    link_string = f"user_id={user_id}|expires={expiration_string}|token={token}"
    encoded_string = base64.b64encode(link_string.encode('ascii')).decode('ascii')
    link = f"http://127.0.0.1:3000/login/password/change/{encoded_string}/"
    return link, token, expiration_string