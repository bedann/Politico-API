from flask import make_response, jsonify, Blueprint


bp = Blueprint('api', __name__, url_prefix='/api/v1')


def validate_object(item, collection, name):
    """This function validates an object and rejects or accepts it"""
    for key, value in item.items():
        if not value:
            return response(
                "Please provide a {} for the {}".format(key, name), 400)
        if key == "name":
            if len(value) < 3:
                return response(
                    "The {} name provided is too short".format(name), 400)
        for i in range(len(collection)):
            if collection[i]['id'] == id:
                return response(
                    "{} already exists".format(name), 400)


def generate_id(list):
    """ Creates a unique ID for a new item to be added to the list"""

    return len(list) + 1


def response(message, code, data=[]):
    """ Creates a basic reposnse """
    response = {
        "status": code,
        "message": message,
        "data": data
    }
    return make_response(jsonify(response), code)


def exists(key, value, collection):
    filtered = filter(lambda item: item[key] == value, collection)
    filtered = list(filtered)
    return len(filtered) > 0


def validate_strings(*args):
    """ validates that inputs are strings only """

    for value in args:
        if not isinstance(value, str):
            return False
    return True


def validate_bool(*args):
    """ validates that inputs are boolean only """

    for value in args:
        if not isinstance(value, bool):
            return False
    return True


def validate_ints(*args):
    """ validates that inputs are ints only """

    for value in args:
        if not isinstance(value, int):
            return False
    return True
