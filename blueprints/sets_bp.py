from flask import Blueprint, request
from auth import admin_only
from models.set import Set, SetSchema
from init import db

sets_bp = Blueprint("sets", __name__, url_prefix="/sets")

# Get all sets
@sets_bp.route("/", methods=["GET"], endpoint="all_sets")
def all_sets():
    stmt = db.select(Set)
    sets = db.session.scalars(stmt).all()
    return SetSchema(many=True).dump(sets)

# Get one set
@sets_bp.route("/<int:id>", methods=["GET"], endpoint="one_set")
def one_set(id):
    set = db.get_or_404(Set, id)
    return SetSchema().dump(set)

# Create a new set
@sets_bp.route("/", methods=["POST"], endpoint="create_set")
@admin_only
def create_set():
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
@sets_bp.route("/<int:id>", methods=["PUT", "PATCH"], endpoint="update_set")
@admin_only
def update_set(id):
    set = db.get_or_404(Set, id)
    set_info = SetSchema(only=["name", "series"], unknown="exclude").load(
        request.json
    )
    # Update the attributes of the existing set object
    set.name = set_info["name"]
    set.series = set_info["series"]

    db.session.commit()
    return SetSchema().dump(set)

# Delete an existing set
@sets_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_set")
@admin_only
def delete_set(id):
    set = db.get_or_404(Set, id)
    db.session.delete(set)
    db.session.commit()
    return {}