#!/usr/bin/python3
""" document """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ get all users """
    users = storage.all(User).values()
    output = []
    for user in users:
        output.append(user.to_dict())
    return jsonify(output)


@app_views.route(
    '/users/<user_id>',
    strict_slashes=False,
    methods=['GET'])
def get_user(user_id):
    """ get <user_id> """
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """delete a user """
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    user.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_user():
    """Create a user """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if "password" not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    user = User(email=request.json["email"], password=request.json["password"])
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Update a user Object"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
