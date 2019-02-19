from flask import Blueprint
from flask import request, jsonify
from flask import make_response
from app.v2.utils.validator import response, response_error, not_admin
from app.v2.models.user_model import User
from app.blueprints import v2
from werkzeug.security import check_password_hash
from app.v2.utils.jwt_utils import admin_optional
from flask_jwt_extended import get_jwt_identity


@v2.route('/auth/signup', methods=['POST', 'PUT'])
@admin_optional
def register_user():
    """ Register user end point """

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    if request.method == 'POST':
        try:
            first_name = data['firstname']
            last_name = data['lastname']
            other_name = data['othername']
            email = data['email']
            phone_number = data['phoneNumber']
            passport_url = data['passportUrl']
            is_admin = data['isAdmin']
            password = data['password']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400)

        user = User(
            first_name, last_name, other_name, email, phone_number,
            passport_url,
            is_admin, password)

        if not user.validate_object():
                return response_error(user.error_message, user.error_code)

        if not get_jwt_identity() or not_admin():
            user.is_admin = False

        # append new user to list
        user.save()

        response_data = {
            'token': user.access_token,
            'user': user.as_json()
        }

        # return registered user
        return response("Success", 201, [response_data])
    else:

        try:
            email = data['email']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400)

        if not get_jwt_identity():
            return response_error("Missing Authorization Header", 400)

        model = User()

        user = model.find_by('email', email)

        if user:
            restricted = not_admin()
            if restricted:
                return restricted
            admin = user['admin']
            admin = not admin

            model.edit('admin', admin, user['id'])

            msg = "User demoted to normal user"
            if admin:
                msg = "User promoted to Admin"
            return response(msg, 200)
        else:
            return response_error("No user under that email", 404)


@v2.route('/auth/login', methods=['POST'])
def login():
    """ login user end point """

    message = ""
    status = 200
    response_data = None

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    try:
        email = data['email']
        password = data['password']
    except KeyError as e:
        return response_error("{} field is required".format(e.args[0]), 400)

    user = User().find_by('email', email)

    if not user:
        message = "User not registered"
        status = 404

    elif not check_password_hash(user['password'], password):
        message = "Incorrect password"
        status = 401

    else:
        model = User(id=user['id'])
        model.create_tokens()

        status = 200
        message = 'Success'

        del user['password']

        response_data = {
            'token': model.access_token,
            'user': user
        }

    # return registered user
    if response_data:
        return response(message, status, [response_data])

    return response_error(message, status)


@v2.route('/auth/reset', methods=['POST'])
def reset_password():
    """ Reset user password end point """

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    try:
        email = data['email']
    except KeyError as e:
        return response_error("{} field is required".format(e.args[0]), 400)

    model = User()

    if not model.find_by('email', email):
            return response_error('User not found', 404)

    response_data = {
        'status': 200,
        'data': [
            {
                "message": "Check your email for password reset link",
                "email": email
            }
        ]
    }

    return make_response(jsonify(response_data), 200)
