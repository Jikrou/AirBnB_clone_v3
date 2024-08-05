#!/usr/bin/python3
""" State view dor RESTFul API"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_obj():
    """retrieve a list of all State objects"""
    objs = storage.all(State).values()
    list_obj = [obj.to_dict() for obj in objs]
    return jsonify(list_obj)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_obj_id(state_id):
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify([obj.to_dict()])


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def states_obj_del(state_id):
    """deletes astates object """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_obj_create():
    """ create an obj state """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    new_obj = State(**data)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_obj_update(state_id):
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
