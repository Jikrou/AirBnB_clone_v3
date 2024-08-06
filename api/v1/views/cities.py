#!/usr/bin/python3
"""Cities view for API"""

from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route(
        "/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def det_cities(state_id):
    """Retrieve the list of all City object of a state"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404, "Not found")
    cities = [city.to_dict() for city in obj.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieve a city object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404, "Not found")
    return jsonify(obj.to_dict())


@app_views.route(
        "/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    """delete a city object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404, "Not found")
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """Create a city object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404, "Not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    data["state_id"] = state_id
    new_obj = City(**data)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Update city object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404, "Not found")

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
