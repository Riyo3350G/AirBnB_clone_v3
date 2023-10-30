#!/usr/bin/python3
""" places_amenities document """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("places/<place_id>/amenities",
                 strict_slashes=False,
                 methods=['GET'])
def get_place_amenities(place_id):
    """ get all amenities """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    output = []
    for amenity in place.amenities:
        output.append(amenity.to_dict())
    return jsonify(output)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def del_place_amenity(place_id, amenity_id):
    """ delete an amenity """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity not in place.amenities:
        return jsonify({"error": "Not found"}), 404
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['POST'])
def add_place_amenity(place_id, amenity_id):
    """ add an amenity """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
