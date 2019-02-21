from flask import make_response, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app.v2.models.user_model import User


error_value = None


def not_admin():
    current_user = User().find_by('id', get_jwt_identity())

    if not current_user['admin']:
        return response_error(
            "This action is reserved to Admins only", 401)
    return None


def response(message, code, data=[]):
    """ Creates a basic reposnse """

    response = {
        "status": code,
        "message": message,
        "data": data
    }
    return make_response(jsonify(response), code)


def response_error(message, code):
    """ Creates a basic error reposnse """

    response = {
        "status": code,
        "error": message
    }
    return make_response(jsonify(response), code)


def validate_ints(*args):
    """ validates that inputs are ints only """

    for value in args:
        if not isinstance(value, int):
            return False
    return True


def validate_strings(*args):
    """ validates that inputs are strings only """

    for value in args:
        if not isinstance(value, str) or not value or not value.split():
            return False
    return True


def validate_bool(*args):
    """ validates that inputs are boolean only """

    for value in args:
        if not isinstance(value, bool):
            return False
    return True
