#!/usr/bin/python3
""" document """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.state import State


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """places search"""
    req = request.get_json()
    if req is None:
        return jsonify({"error": "Not a JSON"}), 400

    state_list = req.get("states")
    city_list = req.get("cities")
    amenity_list = req.get("amenities")
    searched_places = []

    if state_list:
        for state_id in state_list:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        searched_places.append(place)

    if city_list:
        for city_id in city_list:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in searched_places:
                        searched_places.append(place)

    if amenity_list:
        for place in searched_places:
            if place.amenities:
                place_amenity_ids = [amenity.id for amenity in place.amenities]
                for amenity_id in amenity_list:
                    if amenity_id not in place_amenity_ids:
                        searched_places.remove(place)
                        break

    # serialize to json and remove unnecessary keys
    searched_places = [storage.get(Place, place.id).
                       to_dict() for place in searched_places]
    to_be_removed = ["amenities", "reviews", "amenity_ids"]
    searched_places = [
        {key: v for key, v in place_dict.items() if key not in to_be_removed}
        for place_dict in searched_places
    ]

    return jsonify(searched_places)
