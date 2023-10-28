#!/usr/bin/python3
""" document """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """ get all cities """
    state = storage.get('State', state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    output = []
    for city in state.cities:
        output.append(city.to_dict())
    return jsonify(output)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """get a city by id"""
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """delete a city """
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    city.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a new city"""
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    keys = request.get_json()
    keys['state_id'] = state_id
    city = City(**keys)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ Update a city Object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
