#!/usr/bin/python3
"""Amenities view for API"""

from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """retrieve list of all Amenity object"""
    obj = storage.all(Amenity).values()
    amenities = [ameny.to_dict() for ameny in obj]
    return jsonify(amenities)


@app_views.route(
        "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """retrieve Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
        "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create Amenity object"""
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    obj = Amenity(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Update Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
