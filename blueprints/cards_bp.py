from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from auth import admin_only
from models.card import Card, CardSchema
from init import app, db, bcrypt
import json

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Get all cards
@cards_bp.route("/", methods=["GET"])
def all_cards():
    stmt = db.select(Card)
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)

# Get one card
@cards_bp.route("/<int:id>", methods=["GET"])
def one_card(id):
    card = db.get_or_404(Card, id)
    return CardSchema().dump(card)

# Create a new card
@cards_bp.route("/", methods=["POST"])
@jwt_required()
def create_card():
    admin_only()
    card_info = CardSchema(only=["card_id", "name", "type", "set_id"], unknown="exclude").load(
        request.json
    )
    card = Card(
        card_id=card_info["card_id"],
        name=card_info["name"],
        type=card_info["type"],
        set_id=card_info["set_id"]
    )
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201

# Update an existing card
@cards_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_card(id):
    card = db.get_or_404(Card, id)
    admin_only()
    card_info = CardSchema(only=["card_id", "name", "type", "set_id"], unknown="exclude").load(
        request.json
    )
    card = Card(
        card_id=card_info["card_id"],
        name=card_info["name"],
        type=card_info["type"],
        set_id=card_info["set_id"]
    )
    db.session.commit()
    return CardSchema().dump(card)

# Delete an existing card
@cards_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_card(id):
    card = db.get_or_404(Card, id)
    admin_only()
    db.session.delete(card)
    db.session.commit()
    return {}