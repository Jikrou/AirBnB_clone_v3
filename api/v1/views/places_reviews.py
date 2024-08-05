#!/usr/bin/python3
"""places_reviews module"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return jsonify([review.to_dict() for review in obj.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json()["user_id"])
    if not user:
        abort(404)
    if "text" not in request.get_json():
        abort(400, description="Missing text")
    request.get_json()["place_id"] = place_id
    obj = Review(**request.get_json())
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
