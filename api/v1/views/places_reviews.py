#!/usr/bin/python3
""" places_reviews document """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['GET'])
def get_reviews(place_id):
    """ get all reviews """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    output = []
    for rev in place.reviews:
        output.append(rev.to_dict())
    return jsonify(output)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ get a review by ID """
    rev = storage.get(Review, review_id)
    if rev is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(rev.to_dict())


@app_views.route(
    '/reviews/<review_id>',
    strict_slashes=False,
    methods=['DELETE'])
def del_review(review_id):
    """ delete a review """
    rev = storage.get(Review, review_id)
    if rev is None:
        return jsonify({"error": "Not found"}), 404
    rev.delete()
    storage.save()
    return (jsonify({})), 200


# /places/b39cada5-3ac8-42c4-972a-3d4b412a0c5a/reviews
@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False)
def add_review(place_id):
    """add a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, data['user_id'])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>',
    methods=['PUT'],
    strict_slashes=False)
def update_review(review_id):
    """PUT a review"""
    rev = storage.get(Review, review_id)
    if rev is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    keys = [
        'id',
        'user_id',
        'place_id',
        'created_at',
        'updated_at'
    ]
    for key, val in request.get_json().items():
        if key not in keys:
            setattr(rev, key, val)
    rev.save()
    return jsonify(rev.to_dict()), 200
