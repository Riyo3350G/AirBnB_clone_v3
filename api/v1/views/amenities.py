#!/usr/bin/python3
""" document """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ get all amenities """
    amenities = storage.all(Amenity).values()
    output = []
    for amenity in amenities:
        output.append(amenity.to_dict())
    return jsonify(output)


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['GET'])
def get_amenity(amenity_id):
    """ get <amenity_id> """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """delete a amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    amenity.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def post_amenity():
    """Create a amenities """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(name=request.json["name"])
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Update a amenity Object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
