import functools
import typing
from collections.abc import Callable
from flask import Response, request, Request
from db import db
from models.auth_tokens import auth_token_schema, AuthToken, AuthTokenSchema
from datetime import datetime



def validate_auth_token(arg_zero):
    auth_token = arg_zero.headers["auth_token"]
    if auth_token is None or auth_token == "" or auth_token == 'not required' or auth_token=='undefined':
        return False
    auth_record = db.session.query(
        AuthToken
    ).filter(
        AuthToken.auth_token == auth_token
    ).filter(
        AuthToken.expiration > datetime.utcnow()
    ).first()

    return auth_record

def failure_response():
    return Response("Authentication Required", 401)



def authenticate(func:Callable[[request], Response]):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        # print(args)
        auth_info = validate_auth_token(args[0])
        return (
            func(
                *args, **kwargs
            ) if auth_info else failure_response()
        )

    return wrapper_authenticate

def authenticate_return_auth(func:Callable[[request], Response]):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        # print(args)
        auth_info = validate_auth_token(args[0])
        kwargs["auth_info"] = auth_info
        return (
            func(
                *args, **kwargs
            ) if auth_info else failure_response()
        )

    return wrapper_authenticate
