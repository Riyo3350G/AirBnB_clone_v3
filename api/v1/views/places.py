#!/usr/bin/python3
""" document """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['GET'])
def get_places(city_id):
    """ get all places """
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    output = []
    for place in city.places:
        output.append(place.to_dict())
    return jsonify(output)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """ get place by id """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """delete a place """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    place.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create a new place"""
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get('User', data['user_id'])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ put place """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
