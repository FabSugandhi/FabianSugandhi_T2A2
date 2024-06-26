from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from auth import admin_only
from models.set import Set, SetSchema
from init import app, db, bcrypt
import json

sets_bp = Blueprint("sets", __name__, url_prefix="/sets")

# Get all sets
@sets_bp.route("/", methods=["GET"])
def all_sets():
    stmt = db.select(Set)
    sets = db.session.scalars(stmt).all()
    return SetSchema(many=True).dump(sets)

# Get one set
@sets_bp.route("/<int:id>", methods=["GET"])
def one_set(id):
    set = db.get_or_404(Set, id)
    return SetSchema().dump(set)

# Create a new set
@sets_bp.route("/", methods=["POST"])
@jwt_required()
def create_set():
    admin_only()
    set_info = SetSchema(only=["name", "series"], unknown="exclude").load(
        request.json
    )
    set = Set(
        name=set_info["name"],
        series=set_info["series"],
    )
    db.session.add(set)
    db.session.commit()
    return SetSchema().dump(set), 201

# Update an existing set
@sets_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_set(id):
    set = db.get_or_404(Set, id)
    admin_only()
    set_info = SetSchema(only=["name", "series"], unknown="exclude").load(
        request.json
    )
    set = Set(
        name=set_info["name"],
        series=set_info["series"],
    )
    db.session.commit()
    return SetSchema().dump(set)

# Delete an existing set
@sets_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_set(id):
    set = db.get_or_404(Set, id)
    admin_only()
    db.session.delete(set)
    db.session.commit()
    return {}