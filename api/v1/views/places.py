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

    state_ids = req.get("states")
    city_ids = req.get("cities")
    amenity_ids = req.get("amenities")
    searched_places = []

    if not req and not state_ids and not city_ids:
        searched_places = storage.all(Place)

    if state_ids:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        searched_places.append(place)

    if city_ids:
        for city_id in city_ids:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in searched_places:
                        searched_places.append(place)

    if amenity_ids:
        for place in searched_places:
            if place.amenities:
                place_amenity_ids = [amenity.id for amenity in place.amenities]
                for amenity_id in amenity_ids:
                    if amenity_id not in place_amenity_ids:
                        searched_places.remove(place)
                        break

    # serialize to json
    searched_places = [storage.get(Place, place.id).
                       to_dict() for place in searched_places]
    keys_to_remove = ["amenities", "reviews", "amenity_ids"]
    searched_places = [
        {k: v for k, v in place_dict.items() if k not in keys_to_remove}
        for place_dict in searched_places
    ]

    return jsonify(searched_places)
